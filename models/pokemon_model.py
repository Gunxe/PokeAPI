from typing import List

from pydantic import BaseModel, Field


class Pokedex(BaseModel):
    name: str


class PokedexNumbers(BaseModel):
    entry_number: int = Field(..., alias="entry_number")
    pokedex: Pokedex = Field(..., alias="pokedex")


class Pokemon(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    pokedex_numbers: List[PokedexNumbers] = Field(..., alias="pokedex_numbers")
