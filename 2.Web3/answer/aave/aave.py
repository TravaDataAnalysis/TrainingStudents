import json

from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.receipt_log_handler import EthReceiptLogHandler


class Aave:
    def __init__(self, provider_url="https://rpc3.fantom.network",
                 pool_address='0x9FAD24f572045c7869117160A571B2e50b10d068'):
        self.web3 = Web3(HTTPProvider(provider_url))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        pool_address = self.web3.toChecksumAddress(pool_address)
        with open('../../abi/lending_pool_aave_v2.json', 'r') as f:
            self.abi = json.loads(f.read())

        self.contract_address = pool_address
        self.handler = EthReceiptLogHandler()

    """
    Crawl dữ liệu event theo 5 loại: Deposit, Borrow, Withdraw, Repay và Liquidate trong 100.000 blocks gần nhất.
    """

    def ex1(self, start_block=None, end_block=None, batch_size=20000):
        if not start_block or not end_block:
            # Get data from 100000 latest block
            end_block = self.web3.eth.block_number
            start_block = end_block - 99999

        event_types = {'Deposit', 'Borrow', 'Withdraw', 'Repay', 'LiquidationCall'}
        event_abi = []
        for _abi in self.abi:
            if (_abi['type'] == 'event') and (_abi['name'] in event_types):
                event_abi.append(_abi)

        event_abi_info = self.handler.build_list_info_event(event_abi)

        event_hashes = []
        event_subscriber = {}
        for event_info in event_abi_info:
            event_hashes.append(event_info[1])
            event_subscriber[event_info[1]] = event_info[0]

        event_list = []
        from_block = start_block
        while from_block < end_block:
            to_block = from_block + batch_size - 1
            if to_block > end_block:
                to_block = end_block

            filter_params = {
                "fromBlock": from_block,
                "toBlock": to_block,
                "topics": [event_hashes],
                "address": [self.contract_address]
            }

            event_filter = self.web3.eth.filter(filter_params)
            events = event_filter.get_all_entries()

            for event in events:
                log = self.handler.web3_dict_to_receipt_log(event)
                eth_event = self.handler.extract_event_from_log(log, event_subscriber[log.topics[0]])
                if eth_event is not None:
                    eth_event_dict = self.handler.eth_event_to_dict(eth_event)
                    event_list.append(eth_event_dict)

            print(f'Crawled events from block {from_block} to block {to_block}')
            self.web3.eth.uninstallFilter(event_filter.filter_id)
            from_block = to_block + 1

        result = {
            'blocksInfo': {
                'startBlock': start_block,
                'endBlock': end_block
            },
            'event': event_list
        }

        with open('aave1.json', 'w') as f:
            result = json.dumps(result, indent=2)
            f.write(result)

        return event_list

    """
    Crawl dữ liệu transaction của những event đã crawl.
    """

    def ex2(self, start_block=None, end_block=None, batch_size=20000):
        if not start_block or not end_block:
            # Get data from 100000 latest block
            end_block = self.web3.eth.block_number
            start_block = end_block - 999

        event_list = self.ex1(start_block, end_block, batch_size)
        transaction_hashes = set([event.get('transaction_hash') for event in event_list])

        transactions = []
        for tx_hash in transaction_hashes:
            tx = self.web3.eth.get_transaction(tx_hash)
            tx = json.loads(self.web3.toJSON(tx))
            transactions.append(tx)
        print(f'Got {len(transactions)} transactions')

        with open('aave2.json', 'w') as f:
            result = json.dumps({
                'blocksInfo': {
                    'startBlock': start_block,
                    'endBlock': end_block
                },
                'transactions': transactions
            }, indent=2)
            f.write(result)

        return transactions

    """
    Lấy thông tin địa chỉ token được thực hiện giao dịch Deposit và Borrow nhiều nhất 
    (gợi ý: địa chỉ token nằm trong trường reserve trong event, nếu số event của các token bằng nhau thì lấy token bất kỳ)
    """

    def ex3(self, start_block=None, end_block=None, batch_size=20000):
        if not start_block or not end_block:
            # Get data from 100000 latest block
            end_block = self.web3.eth.block_number
            start_block = end_block - 99999

        event_list = self.ex1(start_block, end_block, batch_size)

        reserves_freq = {}
        for event in event_list:
            if event.get('event_type') not in {'BORROW', 'DEPOSIT'}:
                continue

            reserve = event.get('reserve')
            if reserve not in reserves_freq:
                reserves_freq[reserve] = 1
            else:
                reserves_freq[reserve] += 1

        max_freq = max(reserves_freq.values())
        most_reserved_tokens = [token for token, frequency in reserves_freq.items() if frequency == max_freq]

        result = {
            'blocksInfo': {
                'startBlock': start_block,
                'endBlock': end_block
            },
            'maxFrequency': max_freq,
            'tokens': most_reserved_tokens
        }

        print(f'max frequency: {max_freq}')
        print(f'tokens: {most_reserved_tokens}')

        with open('aave3.json', 'w') as f:
            result = json.dumps(result, indent=2)
            f.write(result)

        return result

    """
    Lấy thông tin địa chỉ thực hiện transaction nhiều nhất trong lending pool 
    (gợi ý: địa chỉ ví nằm trong trường from của dữ liệu transaction, nếu số transaction 
    của các địa chỉ bằng nhau thì lấy địa chỉ bất kỳ).
    """

    def ex4(self, start_block=None, end_block=None, batch_size=20000):
        if not start_block or not end_block:
            # Get data from 100000 latest block
            end_block = self.web3.eth.block_number
            start_block = end_block - 999

        transactions = self.ex2(start_block, end_block, batch_size)
        wallet_addresses = [tx.get('from') for tx in transactions]

        wallet_address_freq = {}
        for address in wallet_addresses:
            if address not in wallet_address_freq:
                wallet_address_freq[address] = 1
            else:
                wallet_address_freq[address] += 1

        max_frequency = max(wallet_address_freq.values())
        most_active_wallet = [wallet for wallet, frequency in wallet_address_freq.items() if frequency == max_frequency]

        result = {
            'blocksInfo': {
                'startBlock': start_block,
                'endBlock': end_block
            },
            'maxFrequency': max_frequency,
            'wallets': most_active_wallet
        }

        print(f'max frequency: {max_frequency}')
        print(f'wallets: {most_active_wallet}')

        with open('aave4.json', 'w') as f:
            result = json.dumps(result, indent=2)
            f.write(result)

        return result

    """
    Dựa vào địa chỉ Oracle (Aave oracle) và abi/oracle_abi.json tìm giá (asset price) của token ở câu 3.
    """

    def ex5(self, token, abi_url='../../../abi/oracle_abi.json', contract_address='0xC466e3FeE82C6bdc2E17f2eaF2c6F1E91AD10FD3'):
        token = self.web3.toChecksumAddress(token)
        if not self.web3.isAddress(contract_address):
            contract_address = self.web3.toChecksumAddress(contract_address)

        with open(abi_url, 'r') as f:
            oracle_abi = json.loads(f.read())

        oracle_contract = self.web3.eth.contract(abi=oracle_abi, address=contract_address)
        token_price = oracle_contract.functions.getAssetPrice(token).call() / 10 ** 18

        print(f'token: {token}')
        print(f'token price: {token_price}')

        with open('aave5.json', 'w') as f:
            result = json.dumps({
                'token': token,
                'price': token_price
            }, indent=2)
            f.write(result)

        return token_price


if __name__ == '__main__':
    runner = Aave()
    runner.ex2()
