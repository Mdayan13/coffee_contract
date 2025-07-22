from eth_utils import to_wei
import boa
from tests.conftest import AMOUNT_VALUE
RANDOM_USER = boa.env.generate_address("non_user")

def test_priceFeed_is_correct(eth_usd, deploy):
    assert deploy.price_feed() == eth_usd.address
    

def test_minimum_amount(deploy, account):
    assert deploy.MINIMUM_USD() == to_wei(5, "ether")
    assert deploy.OWNER() == account.address
    
def test_fund_fails_due_to_unsufficient_amiount(deploy):
    with boa.reverts("You need to spend more ETH!"):
        deploy.fund()
        
def test_fund_with_money(account, deploy):
    #arrange 
    boa.env.set_balance(account.address,AMOUNT_VALUE )
    #act vlaue
    deploy.fund(value=AMOUNT_VALUE)
    #assert
    funder  = deploy.funders(0)
    assert funder == account.address
    assert deploy.address_to_amount_funded(funder) == AMOUNT_VALUE
    
def test_non_owner_caanot_withdraw(contract_deployed):

    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner"):
            contract_deployed.withdraw()
            
def test_owner_can_withdraw(contract_deployed):
    boa.env.set_balance(contract_deployed.OWNER(), AMOUNT_VALUE)
    with boa.env.prank(contract_deployed.OWNER()):
        contract_deployed.withdraw()
    assert boa.env.get_balance(contract_deployed.address) == 0
    
def test_funding_from_ten_user(deploy, account):
    totalamout = 0
    for i in range (10):
        funder = boa.env.generate_address(f"non_user{i}")
        boa.env.set_balance(funder, AMOUNT_VALUE)
        with boa.env.prank(funder):
            deploy.fund(value=AMOUNT_VALUE)
        totalamout += AMOUNT_VALUE
    deploy.withdraw()
    assert boa.env.get_balance(deploy.address) == 0
    print(f"owner balance is: {boa.env.get_balance(account.address)}")
    assert boa.env.get_balance(account.address) == 1010000000000000000000
    
def test_get_eth_usd_value(deploy):
    assert deploy.return_eth_usd_value(AMOUNT_VALUE) > 0
    
    
    
