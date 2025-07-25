# pragma version 0.4.3
# pragma enable-decimals
"""
@license MIT
@title A sample buy-me-a-coffee contract
@author You!
@notice This contract is for creating a sample funding contract
"""
from interfaces import AggregatorV3Interface
import get_price_module

# minimum_usd_decimals: public(constant(decimal)) = 50.0 
MINIMUM_USD: public(constant(uint256)) = 5 * (10**18)
OWNER: public(immutable(address))

funders: public(DynArray[address, 100])
address_to_amount_funded: public(HashMap[address, uint256])
price_feed: public(AggregatorV3Interface)

@deploy
def __init__(price_feed: address):
    self.price_feed = AggregatorV3Interface(price_feed)
    OWNER = msg.sender


@internal
def _only_owner():
    assert msg.sender == OWNER, "Not the contract owner"


@external
@payable
def fund():
    usd_value_of_eth: uint256 = get_price_module._get_eth_to_usd_rate(self.price_feed, msg.value)
    assert usd_value_of_eth >= MINIMUM_USD, "You need to spend more ETH!"
    self.address_to_amount_funded[msg.sender] += msg.value
    self.funders.append(msg.sender)


@external
def withdraw():
    self._only_owner()
    for funder: address in self.funders:
        self.address_to_amount_funded[funder] = 0
    self.funders = []
    # send(OWNER, self.balance)
    raw_call(OWNER, b"", value = self.balance)


@external
@view
def get_version() -> uint256:
    return staticcall self.price_feed.version()


@external
@view
def get_funder(index: uint256) -> address:
    return self.funders[index]


@external
@view
def get_owner() -> address:
    return OWNER

@external
@payable
def __default__():
    pass

@external 
@view 
def return_eth_usd_value(eth_amount: uint256)->uint256:
    return get_price_module._get_eth_to_usd_rate(self.price_feed,eth_amount)