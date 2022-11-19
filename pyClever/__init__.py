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

    def __init__(self, identifier: str) -> None:
        """Initialize the handler for Clever lookup."""
        self._last_location_refresh = None
        self._last_availability_refresh = None

        self._location = CleverLocations(identifier)
        self.chargepoints = CleverAvailability(self._location.chargepoint_identifiers)

        self._cp_weights = {}

        for cp in self._location.chargepoint_identifiers:
            self._cp_weights.update({cp: self._location.get_sockets(cp)})

    @property
    def all_locations(self) -> str:
        """Returns all locations if data is available."""
        return self._location.all_locations

    @property
    def uuid(self) -> str:
        """Get location UUID."""
        return self._location.uuid

    @property
    def chargepoint_total(self) -> int:
        """Get total number of chargepoints."""
        return self._location.total_sockets

    @property
    def chargepoint_available(self) -> int:
        """Get total number of available chargepoints."""
        return self.chargepoints.available(self._cp_weights)

    @property
    def chargepoint_occupied(self) -> int:
        """Get total number of occupied chargepoints."""
        return self.chargepoints.occupied(self._cp_weights)

    @property
    def location(self) -> str:
        """Get master data for the location."""
        return self._location.location

    @property
    def name(self) -> str:
        """Get the public name."""
        return self._location.location["name"]

    @property
    def plug_types(self) -> list:
        """Get a list of connectors at this location."""
        all_sockets = []
        for cp in self._cp_weights.items():
            for socket in cp[1]["socket_types"]:
                if not socket in all_sockets:
                    all_sockets.append(socket)

        return all_sockets

    @property
    def directions(self) -> str:
        """Return directions for the location."""
        return self._location.location["directions"]["da"]

    @property
    def address(self) -> dict:
        """Return the address."""
        return self._location.location["address"]

    @property
    def coordinates(self) -> str:
        """Return location coordiantes."""
        coords = self._location.location["coordinates"]
        coords.pop("quality")
        return coords
