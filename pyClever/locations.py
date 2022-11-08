"""Clever locations lookup."""
from __future__ import annotations

import requests

from .const import BASE_URL

class CleverLocations:
    """Clever location lookup."""

    def __init__(self) -> None:
        """Initialize the location lookup."""
        self._locations:str|None= None
        self._last_refresh:str = None

    def _get_all_locations(self) -> str:
        """Fetch all locations - BE AWARE LARGE RESULT SET."""
        req = requests.get(BASE_URL.format("locations"))

        if req.status_code == 200:
            return req.json()
        else:
            return None

    @property
    def all_locations(self) -> str:
        """Return all locations."""
        if isinstance(self._locations,type(None)): self._locations = self._get_all_locations()

        return self._locations

    def get_location_by_id(self, location_id:str) ->str:
        """Get location by location ID."""
        if isinstance(self._locations,type(None)): self._locations = self._get_all_locations()

        if location_id in self._locations["clever"]:
            return self._locations["clever"][location_id]
        elif location_id in self._locations["hubject"]:
            return self._locations["hubject"][location_id]
        else:
            return None
