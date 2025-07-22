import pytest
from moccasin.config import get_active_network
from script.deploy import deploy_coffee
from conftest import AMOUNT_VALUE
import boa

@pytest.mark.staging
@pytest.mark.local
@pytest.mark.ignore_isolation
def test_can_fund_and_withdraw():
     active_network = get_active_network()
     price_feed = active_network.manifest_named("price_feed")
     coffee_contract = deploy_coffee(price_feed)
     coffee_contract.fund(value=AMOUNT_VALUE)
     funded = coffee_contract.address_to_amount_funded(boa.env.eoa)
     print(f"amount funded by user {boa.env.eoa} is only :- {funded}")
     assert funded == AMOUNT_VALUE
     coffee_contract.withdraw()
     print(f"now the balance of contract is {boa.env.get_balance(coffee_contract.address)}")
     assert boa.env.get_balance(coffee_contract.address) == 0