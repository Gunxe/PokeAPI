from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

class NamedAPIResource(BaseModel):
    name: str
    url: str


class Item(NamedAPIResource):
    """
    Item
    """


class Trigger(NamedAPIResource):
    """
    Trigger
    """


class Location(NamedAPIResource):
    """
    Location
    """


class Species(NamedAPIResource):
    """
    Species
    """


class EvolutionDetail(BaseModel):
    held_item: Optional[Item] = Field(..., alias="held_item")
    item: Optional[Item] = Field(..., alias="item")
    location: Optional[Any] = Field(..., alias="location")
    min_affection: Optional[int] = Field(..., alias="min_affection")
    min_beauty: Optional[int] = Field(..., alias="min_beauty")
    min_happiness: Optional[int] = Field(..., alias="min_happiness")
    min_level: Optional[int] = Field(..., alias="min_level")
    time_of_day: str = Field(..., alias="time_of_day")
    trade_species: Optional[Species] = Field(..., alias="trade_species")
    trigger: Trigger = Field(..., alias="trigger")


class EvolvesToItem(BaseModel):
    evolution_details: List[EvolutionDetail] = Field(..., alias="evolution_details")
    evolves_to: List[EvolvesToItem] = Field(..., alias="evolves_to")
    is_baby: bool = Field(..., alias="is_baby")
    species: Species = Field(..., alias="species")


class Chain(BaseModel):
    evolution_details: List = Field(..., alias="evolution_details")
    evolves_to: List[EvolvesToItem] = Field(..., alias="evolves_to")
    is_baby: bool = Field(..., alias="is_baby")
    species: Species = Field(..., alias="species")


class  EvolutionChain(BaseModel):
    baby_trigger_item: Optional[Any] = Field(..., alias="baby_trigger_item")
    chain: Chain = Field(..., alias="chain")
    id: int = Field(..., alias="id")
