import pprint

from requests import get
from models.pokemon_model import PokemonModel
from models.evolution_chain_model import EvolutionChain
from models.pokemon_location_model import LocationModel, LocationItem


def get_pokemon(name: str):
    response = get(f"https://pokeapi.co/api/v2/pokemon/{name}/encounters")
    pprint.pprint(response.json())
    for location in response.json():
        print(location)
        print(LocationItem(**location))


get_pokemon("pikachu")
