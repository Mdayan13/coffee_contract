from src import buy_me_a_coffee
from moccasin.config import get_active_network

def deploy_anvil():
     active_network = get_active_network()
     coffee_contract = active_network.manifest_named("buy_me_a_coffee")
     print(f"on network {active_network.name} with drawing from << {coffee_contract.address} >>")
     coffee_contract.withdraw()


def moccasin_main():
     deploy_anvil()