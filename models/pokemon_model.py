from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Color(BaseModel):
    name: str
    url: str


class EggGroup(BaseModel):
    name: str
    url: str


class EvolutionChain(BaseModel):
    url: str


class EvolvesFromSpecies(BaseModel):
    name: str
    url: str


class Language(BaseModel):
    name: str
    url: str


class Version(BaseModel):
    name: str
    url: str


class FlavorTextEntry(BaseModel):
    flavor_text: str
    language: Language
    version: Version


class Language1(BaseModel):
    name: str
    url: str


class Genus(BaseModel):
    genus: str
    language: Language1


class Generation(BaseModel):
    name: str
    url: str


class GrowthRate(BaseModel):
    name: str
    url: str


class Habitat(BaseModel):
    name: str
    url: str


class Language2(BaseModel):
    name: str
    url: str


class Name(BaseModel):
    language: Language2
    name: str


class Area(BaseModel):
    name: str
    url: str


class PalParkEncounter(BaseModel):
    area: Area
    base_score: int
    rate: int


class Pokedex(BaseModel):
    name: str
    url: str


class PokedexNumber(BaseModel):
    entry_number: int
    pokedex: Pokedex


class Shape(BaseModel):
    name: str
    url: str


class Pokemon(BaseModel):
    name: str
    url: str


class Variety(BaseModel):
    is_default: bool
    pokemon: Pokemon


class PokemonModel(BaseModel):
    base_happiness: int
    capture_rate: int
    color: Color
    egg_groups: List[EggGroup]
    evolution_chain: EvolutionChain
    evolves_from_species: EvolvesFromSpecies
    flavor_text_entries: List[FlavorTextEntry]
    form_descriptions: List
    forms_switchable: bool
    gender_rate: int
    genera: List[Genus]
    generation: Generation
    growth_rate: GrowthRate
    habitat: Habitat
    has_gender_differences: bool
    hatch_counter: int
    id: int
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    name: str
    names: List[Name]
    order: int
    pal_park_encounters: List[PalParkEncounter]
    pokedex_numbers: List[PokedexNumber]
    shape: Shape
    varieties: List[Variety]
