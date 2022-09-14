from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json


def main():
    # Initiate the contract object
    pid = 3
    provider_url = "https://bsc-dataseed4.binance.org/"
    web3 = Web3(HTTPProvider(provider_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if web3.isConnected():
        print("Connection success")
    else:
        print("Connection fail")
        return 0

    masterchefv2_addr = "0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652"
    with open('../../../../abi/masterchef_abi.json') as f:
        abi = json.load(f)

    contract = web3.eth.contract(abi=abi, address=masterchefv2_addr)

    # Get Lp token address
    lp_address = contract.functions.lpToken(pid).call()

    # Save result
    result = {
        'lpTokenAddress': lp_address,
    }
    json_obj = json.dumps(result, indent=2)
    with open('uniswap2.json', 'w') as f:
        f.write(json_obj)


if __name__ == '__main__':
    main()