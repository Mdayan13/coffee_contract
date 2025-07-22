import pytest
from script.deploy import deploy_coffee
from script.deploy_mocks import deploy_feed
from moccasin.config import get_active_network
import boa
from eth_utils import to_wei
AMOUNT_VALUE = to_wei(1, "ether")

@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account()

@pytest.fixture(scope="function")
def eth_usd():
    return deploy_feed()


@pytest.fixture(scope="function")
def deploy(eth_usd):
    return deploy_coffee(eth_usd)

@pytest.fixture(scope="function")
def contract_deployed(deploy,account ):
    boa.env.set_balance(account.address,AMOUNT_VALUE * 3)
    with boa.env.prank(account.address):
        deploy.fund(value= AMOUNT_VALUE)
    return deploy