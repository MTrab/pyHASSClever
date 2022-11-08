"""Module for interfacing with Clevers Firebase information."""
from __future__ import annotations

from .locations import CleverLocations


class Clever:
    """
    "Reverse engineered" lookup for charging points from Clever and their availability.
    As this is "reverse engineered" and a fully undocumentet and unsupported feature, DO NOT EXPECT THIS TO WORK FOR EVER.
    Whenever Clever changes something, this module WILL break!
    """

    def __init__(self) -> None:
        """Initialize the handler for Clever lookup."""
        self._last_location_refresh = None
        self._last_availability_refresh = None
        self._locations = CleverLocations()

    @property
    def all_locations(self) -> str:
        """Returns all locations if data is available."""
        return self._locations.all_locations

    def get_location_by_id(self, location_id: str) -> str:
        """Get location by location ID."""
        return self._locations.get_location_by_id(location_id)
