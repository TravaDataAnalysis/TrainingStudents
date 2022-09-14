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

    # Get poolInfo values
    pool_info_array = contract.functions.poolInfo(pid).call()
    pool_info = {
        'accCakePerShare': pool_info_array[0],
        'lastRewardBlock': pool_info_array[1],
        'allocPoint': pool_info_array[2],
        'totalBoostedShare': pool_info_array[3],
        'isRegular': pool_info_array[4]
    }

    # PoolInfo explanation. Reference: comments in the source code of the smart contract
    pool_info_explanation = {
        'accCakePerShare': "Accumulated CAKEs per share, times 1e12",
        'lastRewardBlock': "Last block number that pool update action is executed",
        'allocPoint':  "The amount of allocation points assigned to the pool",
        'totalBoostedShare': "The total amount of user shares in each pool, after considering the share boosts",
        'isRegular': "The flag to set pool is regular or special"
    }

    # Save result to JSON
    result = {
        'poolInfo': pool_info,
        'poolExplanation': pool_info_explanation,
    }
    json_obj = json.dumps(result, indent=2)
    with open('uniswap1.json', 'w') as f:
        f.write(json_obj)


if __name__ == '__main__':
    main()