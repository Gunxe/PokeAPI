import pprint

from requests import get
from models.pokemon_model import PokemonModel
from models.evolution_chain_model import EvolutionChain

def get_pokemon(name: str):
    response = get(f"https://pokeapi.co/api/v2/evolution-chain/{name}/")
    pprint.pprint(response.json())
    print(EvolutionChain(**response.json()))

get_pokemon("27")