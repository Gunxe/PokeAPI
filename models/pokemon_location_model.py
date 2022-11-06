from typing import List

from pydantic import Field, BaseModel


class NamedAPIResource(BaseModel):
    name: str = Field(..., alias="name")
    url: str = Field(..., alias="url")


class LocationArea(NamedAPIResource):
    """
    Location Area
    """


class Version(NamedAPIResource):
    """
    Version
    """


class VersionDetails(BaseModel):
    max_chance: int = Field(..., alias="max_chance")
    version: Version = Field(..., alias="version")


class LocationItem(BaseModel):
    location_area: LocationArea = Field(..., alias="location_area")
    version_details: List[VersionDetails] = Field(..., alias="version_details")
