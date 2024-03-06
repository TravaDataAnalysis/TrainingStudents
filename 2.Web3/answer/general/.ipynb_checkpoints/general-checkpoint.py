import json

from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware


class General:
    def __init__(self, provider_url="https://bsc-dataseed4.binance.org/",
                 token_address='0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402'):
        self.web3 = Web3(HTTPProvider(provider_url))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        token_address = self.web3.to_checksum_address(token_address)
        with open('../../abi/erc_20.json', 'r') as f:
            abi = json.loads(f.read())

        self.contract = self.web3.eth.contract(abi=abi, address=token_address)

    def ex1(self, start_block, end_block):
        total = 0
        count = 0
        for block_number in range(start_block, end_block + 1):
            print(f'Current block: {block_number}')
            total += self.web3.eth.get_block_transaction_count(block_number)
            count += 1

        with open('chung1.json', 'w') as f:
            result = json.dumps({
                'fromBlock': start_block,
                'toBlock': end_block,
                'averageTransactions': total / count
            }, indent=2)
            f.write(result)

        return total / count

    def ex2a(self, start_block, end_block):
        events = self.contract.events.Transfer.create_filter(fromBlock=start_block, toBlock=end_block).get_all_entries()
        event_list = []
        for event in events:
            event_list.append(json.loads(self.web3.to_json(event)))

        with open('chung2a.json', 'w') as f:
            result = json.dumps({
                'blocksInfo': {
                    'startBlock': start_block,
                    'endBlock': end_block
                },
                'transferEvents': event_list
            }, indent=2)
            f.write(result)
        return len(event_list)

    def ex2b(self):
        decimals = self.contract.functions.decimals().call()

        with open('chung2b.json', 'w') as f:
            result = json.dumps({
                'decimal': decimals
            }, indent=2)
            f.write(result)

        return decimals

    def ex2c(self):
        block_number = -1
        supply = self.contract.functions.totalSupply().call(block_identifier=block_number)
        supply /= 10 ** 18

        with open('chung2c.json', 'w') as f:
            result = json.dumps({
                'totalSupply': supply
            }, indent=2)
            f.write(result)

        return supply

    def ex2d(self, start_block, end_block):
        events = self.contract.events.Transfer.create_filter(fromBlock=start_block, toBlock=end_block).get_all_entries()
        wallet_frequency = {}
        for event in events:
            wallet_address = event['args']['from']
            if wallet_address not in wallet_frequency:
                wallet_frequency[wallet_address] = 1
            else:
                wallet_frequency[wallet_address] += 1

        max_frequency = max(wallet_frequency.values())
        addresses = [address for address, frequency in wallet_frequency.items() if frequency == max_frequency]

        wallets = {}
        for address in addresses:
            balance = self.contract.functions.balanceOf(address).call()
            wallets[address] = balance / 10 ** 18

        with open('chung2d.json', 'w') as f:
            result = json.dumps({
                'blocksInfo': {
                    'startBlock': start_block,
                    'endBlock': end_block
                },
                'maxFrequency': max_frequency,
                'wallets': wallets
            }, indent=2)
            f.write(result)
        return wallets

    def ex2e(self, start_block, end_block):
        events = self.contract.events.Transfer.create_filter(fromBlock=start_block, toBlock=end_block).get_all_entries()
        wallet_frequency = {}
        for event in events:
            wallet_address = event['args']['to']
            if wallet_address not in wallet_frequency:
                wallet_frequency[wallet_address] = 1
            else:
                wallet_frequency[wallet_address] += 1

        max_frequency = max(wallet_frequency.values())
        addresses = [address for address, frequency in wallet_frequency.items() if frequency == max_frequency]

        wallets = {}
        for address in addresses:
            balance = self.contract.functions.balanceOf(address).call()
            wallets[address] = balance / 10 ** 18

        with open('chung2e.json', 'w') as f:
            result = json.dumps({
                'blocksInfo': {
                    'startBlock': start_block,
                    'endBlock': end_block
                },
                'maxFrequency': max_frequency,
                'wallets': wallets
            }, indent=2)
            f.write(result)
        return wallets

    def ex2f(self):
        symbol = self.contract.functions.symbol().call()
        name = self.contract.functions.name().call()

        with open('chung2f.json', 'w') as f:
            result = json.dumps({
                'name': name,
                'symbol': symbol
            }, indent=2)
            f.write(result)


if __name__ == '__main__':
    runner = General()
