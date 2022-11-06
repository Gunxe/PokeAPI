from pprint import pprint
from typing import List, Optional

import strawberry

from fastapi import FastAPI
from requests import get
from strawberry.fastapi import GraphQLRouter

from models.evolution_chain_model import EvolvesToItem, Chain, EvolutionChain, NamedAPIResource
from models.pokemon_location_model import LocationItem
from models.pokemon_model import PokedexNumber, PokemonModel


@strawberry.type
class Location:
    location_name: str
    versions: List[str]


@strawberry.type
class Evolution:
    name: str
    held_item: Optional[str] = None
    item: Optional[str] = None
    location: Optional[str] = None
    min_affection: Optional[str] = None
    min_happiness: Optional[str] = None
    min_level: Optional[int] = None
    time_of_day: Optional[str] = None
    trade_species: Optional[str] = None
    trigger: Optional[str] = None


@strawberry.type
class Pokedex:
    entry_number: int
    pokedex: str


@strawberry.type
class Pokemon:
    name: str
    pokedex: List[Pokedex]
    evolution: List[Evolution]
    encounter_location: List[Location]

3
def get_pokedex_list(pokedex_numbers: List[PokedexNumber]) -> List[Pokedex]:
    pokedexs: List[Pokedex] = []
    for pokedex in pokedex_numbers:
        pokedexs.append(Pokedex(
            entry_number=pokedex.entry_number,
            pokedex=pokedex.pokedex.name,
        ))
    return pokedexs


def get_name(obj: NamedAPIResource):
    return obj.name if obj else None


def create_evolution(
        evolutions: List[Evolution],
        evol_data: Chain
):
    for evol_details in evol_data.evolution_details:
        evolutions.append(Evolution(
            name=evol_data.species.name,
            held_item=get_name(evol_details.held_item),
            item=get_name(evol_details.item),
            location=get_name(evol_details.location),
            min_affection=evol_details.min_happiness,
            min_happiness=evol_details.min_affection,
            min_level=evol_details.min_level,
            time_of_day=evol_details.time_of_day,
            trade_species=get_name(evol_details.location),
            trigger=evol_details.trigger.name,
        ))


def create_evolution_list(evolutions: List[Evolution], evolves_to: List[EvolvesToItem]):
    for evol_data in evolves_to:
        create_evolution(
            evolutions=evolutions,
            evol_data=evol_data
        )
        if evol_data.evolves_to:
            create_evolution_list(
                evolutions=evolutions,
                evolves_to=evol_data.evolves_to
            )


def get_evolutions(url: str) -> List[Evolution]:
    evolution_chain: Chain = EvolutionChain(**get(url).json()).chain
    evolutions: List[Evolution] = []

    if evolution_chain.evolution_details:
        create_evolution(
            evolutions=evolutions,
            evol_data=evolution_chain
        )
    else:
        evolutions.append(Evolution(
            name=evolution_chain.species.name,
        ))
    if evolution_chain.evolves_to:
        create_evolution_list(
            evolutions=evolutions,
            evolves_to=evolution_chain.evolves_to
        )
    return evolutions


def get_locations(name: str) -> List[Location]:
    response = get(f"https://pokeapi.co/api/v2/pokemon/{name}/encounters")
    LocationItems: List[LocationItem] = [LocationItem(**location_item) for location_item in response.json()]
    locations: List[Location] = []
    for location in LocationItems:
        versions: List[str] = [version_details.version.name for version_details in location.version_details]
        locations.append(Location(
            location_name=location.location_area.name,
            versions=versions
        ))
    return locations



def get_pokemon(name: str):
    response = get(f"https://pokeapi.co/api/v2/pokemon-species/{name}/")
    pokemon: PokemonModel = PokemonModel(**response.json())
    return Pokemon(
        name=name,
        pokedex=get_pokedex_list(
            pokedex_numbers=pokemon.pokedex_numbers
        ),
        evolution=get_evolutions(pokemon.evolution_chain.url),
        encounter_location=get_locations(name=name)
    )


@strawberry.type
class Query:
    pokemon: Pokemon = strawberry.field(resolver=get_pokemon)


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
