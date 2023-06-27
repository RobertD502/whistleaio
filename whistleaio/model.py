""" Data classes for Whistle API """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any



@dataclass
class WhistleData:
    """ Dataclass for Whistle data. """

    pets: dict[str, Pet]



@dataclass
class Pet:
    """ Dataclass for Whistle Pet. """

    id: str
    data: dict[str, Any]
    device: dict[str, Any]
    dailies: dict[str, Any]
    events: dict[str, Any] | None
    places: list[dict]
    stats: dict[str, Any]
    health: dict[str, Any]

