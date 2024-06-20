import pandas as pd
import web3
from config import ABI, contract
from web3 import AsyncHTTPProvider, AsyncWeb3
import random
from tqdm import tqdm
from loguru import logger
import asyncio

async def LXP_checker(path: str):
    w3 = AsyncWeb3(AsyncHTTPProvider("https://linea.decubate.com"), request_kwargs=None)
    lxp_contract = w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract),
            abi=ABI
        )
    with open(path, 'r') as file:
        addresses = file.read().splitlines()

    res = {}
    for address in tqdm(addresses):
        add_cheksum = w3.to_checksum_address(address)
        amount_in_wei = await lxp_contract.functions.balanceOf(add_cheksum).call()
        decimals = await lxp_contract.functions.decimals().call()
        final_amount =  amount_in_wei / 10 ** decimals
        res[address] = final_amount

    results = pd.DataFrame([res]).T.reset_index().rename(columns={"index":"address",0:"LXP_amount"})
    results.to_csv("results.csv")
    logger.info(f"Final amount of LXP points {int(results.LXP_amount.sum())}")


path = "addresses.txt"
if __name__ == "__main__":
    asyncio.run(LXP_checker(path))