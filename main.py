from pprint import pprint
from typing import List, Optional

import strawberry

from fastapi import FastAPI
from requests import get
from strawberry.fastapi import GraphQLRouter

from models.evolution_chain_model import EvolvesToItem, Chain, EvolutionChain, NamedAPIResource
from models.pokemon_model import PokedexNumber, PokemonModel


@strawberry.type
class Evolution:
    name: str
    held_item: Optional[str]
    item: Optional[str]
    location: Optional[str]
    min_affection: Optional[str]
    min_happiness: Optional[str]
    min_level: Optional[int]
    time_of_day: Optional[str]
    trade_species: Optional[str]
    trigger: Optional[str]


@strawberry.type
class Pokedex:
    entry_number: int
    pokedex: str


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


def get_evolution(evolutions: List[Evolution], evolves_to: List[EvolvesToItem]):
    for evol_data in evolves_to:
        for evol_details in evol_data.evolution_details:
            evolutions.append(Evolution(
                name=evol_data.species.name,
                held_item=get_name(evol_details.held_item),
                item=get_name(evol_details.item),
                location=get_name(evol_details.location),
                min_affection=evol_details.min_affection,
                min_happiness=evol_details.min_happiness,
                min_level=evol_details.min_level,
                time_of_day=evol_details.time_of_day,
                trade_species=get_name(evol_details.location),
                trigger=evol_details.trigger.name,
            ))
        if evol_data.evolves_to:
            get_evolution(
                evolutions=evolutions,
                evolves_to=evol_data.evolves_to
            )


def get_evolutions(url: str) -> List[Evolution]:
    evolution_chain: Chain = EvolutionChain(**get(url).json()).chain
    evolutions: List[Evolution] = []

    if evolution_chain.evolution_details:
        for evol_details in evolution_chain.evolution_details:
            evolutions.append(Evolution(
                name=evolution_chain.species.name,
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
    else:
        evolutions.append(Evolution(
            name=evolution_chain.species.name,
            held_item=None,
            item=None,
            location=None,
            min_affection=None,
            min_happiness=None,
            min_level=None,
            time_of_day=None,
            trade_species=None,
            trigger=None,
        ))
    if evolution_chain.evolves_to:
        get_evolution(
            evolutions=evolutions,
            evolves_to=evolution_chain.evolves_to
        )
    return evolutions


def get_pokemon(name: str):
    response = get(f"https://pokeapi.co/api/v2/pokemon-species/{name}/").json()
    pokemon: PokemonModel = PokemonModel(**response)
    return Pokemon(
        name=name,
        pokedex=get_pokedex_list(
            pokedex_numbers=pokemon.pokedex_numbers
        ),
        evolution=get_evolutions(pokemon.evolution_chain.url)
    )


@strawberry.type
class Pokemon:
    name: str
    pokedex: List[Pokedex]
    evolution: List[Evolution]


@strawberry.type
class Query:
    pokemon: Pokemon = strawberry.field(resolver=get_pokemon)


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
