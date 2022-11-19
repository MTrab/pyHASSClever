"""Module for interfacing with Clevers Firebase information."""
from __future__ import annotations

from .availability import CleverAvailability
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

        self.chargepoints = None

    @property
    def all_locations(self) -> str:
        """Returns all locations if data is available."""
        return self._locations.all_locations

    def get_location(self, identifier: str) -> str:
        """Get location."""
        return self._locations.get_location(identifier, False)

    def get_uid(self, identifier: str) -> str:
        """Get location UID."""
        return self._locations.get_location(identifier, True)

    def get_identification(self, uid: str) -> list:
        """Get the identification(s) for this location."""
        return self._locations.get_location_identifier(uid)

    def load_chargepoints(self, identifications: list) -> None:
        """Load chargepoints."""
        self.chargepoints = CleverAvailability(identifications)

    @property
    def chargepoint_total(self) -> int:
        """Get total number of chargepoints."""
        return self.chargepoints.total

    @property
    def chargepoint_available(self) -> int:
        """Get total number of available chargepoints."""
        return self.chargepoints.available

    @property
    def chargepoint_occupied(self) -> int:
        """Get total number of occupied chargepoints."""
        return self.chargepoints.occupied
