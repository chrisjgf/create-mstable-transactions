from brownie import Contract, accounts, network
import json

mta_abi = json.load(open('contracts/erc20.json',))
mta_address = "0x273bc479E5C21CAA15aA8538DecBF310981d14C0"
mta: Contract

stk_mta_abi = json.load(open('contracts/stkmta.json',))
stk_mta_address = "0xc3DCB920C30D4a4222220250DD2E8bA0c5A40d51"
stk_mta: Contract

emissions_abi = json.load(open('contracts/emissions.json',))
emissions_address = "0x02fAE3f4B7A749Ac92a13C5C27B53C1cB7fFC018"
emissions: Contract

account = ""


def setup(priv_key):
    global account, mta, stk_mta, emissions

    account = accounts.add(priv_key)

    print(account)

    mta = Contract.from_abi("MetaToken", mta_address, mta_abi, owner=None)

    stk_mta = Contract.from_abi(
        "StakedTokenMTA", stk_mta_address, stk_mta_abi, owner=None)

    emissions = Contract.from_abi(
        "EmissionsController", emissions_address, emissions_abi, owner=None)


def stake():
    mta_balance = mta.balanceOf(account)

    print(f"Approve {mta_balance / 1e18} MTA")

    mta.approve(stk_mta_address, mta_balance, {'from': account, 'value': 0})

    print(mta_balance)

    print(f"Staking {mta_balance / 1e18} MTA")

    stk_mta.stake(mta_balance, {'from': account, 'value': 0})

    print(f"Staked {mta_balance / 1e18} MTA")

    staked_balance = stk_mta.getVotes(account) / 1e18

    print(staked_balance)


def set_dials():
    print("Emissions", emissions_address)

    # dialId, weight - scaled to 200
    dials = [(0, 30), (1, 50)]

    emissions.setVoterDialWeights(dials, {'from': account, 'value': 0})

    print("setVoterDialWeights", dials)


def poke_weight():
    print("Emissions", emissions_address)

    emissions.pokeSources(account, {'from': account, 'value': 0})

    print("pokeSources")


def main():

    addresses = [
        "privKeyHere"]

    for address in addresses:
        setup(address)
        stake()
        set_dials()
        poke_weight()
