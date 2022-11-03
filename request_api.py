import pprint

from requests import get
from json import load
from models.pokemon_model import Pokemon

def get_pokemon(name: str):
    response = get(f"https://pokeapi.co/api/v2/pokemon-species/{name}/")
    pprint.pprint(response.json())
    print(Pokemon(**response.json()).pokedex_numbers)

get_pokemon("squirtle")