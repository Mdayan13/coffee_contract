from src import buy_me_a_coffee
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network
from script.deploy_mocks import deploy_feed

def deploy_coffee(price_feed: VyperContract)-> VyperContract:
    coffee: VyperContract =buy_me_a_coffee.deploy(price_feed)
    active_network = get_active_network()
    if active_network.has_explorer():
        result_verify = active_network.moccasin_verify(coffee)
        result_verify.wait_for_verification()
    return coffee
    
    
    
def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed : VyperContract= active_network.manifest_named("price_feed")
    print(f"on network {active_network.name} using pricefeed at {price_feed.address}")
    return deploy_coffee(price_feed)