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

    def __init__(self, identifier: str | None = None) -> None:
        """Initialize the handler for Clever lookup."""
        self._last_location_refresh = None
        self._last_availability_refresh = None
        self._identifier = identifier
        self._location = None
        self._cp_weights = {}
        self.chargepoints = None

        self.update()

    @property
    def all_locations(self) -> str:
        """Returns all locations if data is available."""
        return self._location.all_locations

    @property
    def uuid(self) -> str:
        """Get location UUID."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.uuid

    @property
    def chargepoint_total(self) -> int:
        """Get total number of chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.total_sockets

    @property
    def chargepoint_total_per_socket_type(self) -> int:
        """Get total number of chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.total_sockets_per_socket_type

    @property
    def chargepoint_available(self) -> int:
        """Get total number of available chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self.chargepoints.available(self._cp_weights)

    @property
    def chargepoint_available_per_socket_type(self) -> int:
        """Get total number of available chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self.chargepoints.available(self._cp_weights, True)

    @property
    def chargepoint_occupied(self) -> int:
        """Get total number of occupied chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self.chargepoints.occupied(self._cp_weights)

    @property
    def chargepoint_occupied_per_socket_type(self) -> int:
        """Get total number of occupied chargepoints."""
        if isinstance(self._identifier, type(None)):
            return None
        return self.chargepoints.occupied(self._cp_weights, True)

    @property
    def location(self) -> str:
        """Get master data for the location."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.location

    @property
    def name(self) -> str:
        """Get the public name."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.location["name"]

    @property
    def plug_types(self) -> list:
        """Get a list of connectors at this location."""
        if isinstance(self._identifier, type(None)):
            return None

        all_sockets = []
        for cp in self._cp_weights.items():
            for socket in cp[1]["socket_types"]:
                if not socket in all_sockets:
                    all_sockets.append(socket)

        return all_sockets

    @property
    def directions(self) -> str | None:
        """Return directions for the location."""
        if isinstance(self._identifier, type(None)):
            return None
        return (
            self._location.location["directions"]["da"]
            if "directions" in self._location.location
            else None
        )

    @property
    def address(self) -> dict:
        """Return the address."""
        if isinstance(self._identifier, type(None)):
            return None
        return self._location.location["address"]

    @property
    def coordinates(self) -> str:
        """Return location coordiantes."""
        if isinstance(self._identifier, type(None)):
            return None
        coords = self._location.location["coordinates"]
        coords.pop("quality")
        return coords

    def update(self) -> None:
        """Update the states."""
        self._location = CleverLocations(self._identifier)
        if not isinstance(self._identifier, type(None)):
            self.chargepoints = CleverAvailability(
                self._location.chargepoint_identifiers
            )

            self._cp_weights = {}

            for cp in self._location.chargepoint_identifiers:
                self._cp_weights.update({cp: self._location.get_sockets(cp)})
