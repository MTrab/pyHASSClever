"""Clever locations lookup."""
from __future__ import annotations

import requests

from .const import BASE_URL


class CleverLocations:
    """Clever location lookup."""

    def __init__(self, identifier: str) -> None:
        """Initialize the location lookup."""
        self._locations: str | None = None
        self._last_refresh: str = None
        self._identifier = identifier
        self._uuid = None
        self._locations = self._get_all_locations()
        self._location = self._get_location()
        self._cp_ident = self._get_location_identifier()
        self._total_sockets = self._get_total_sockets()

    def _get_all_locations(self) -> str:
        """Fetch all locations - BE AWARE LARGE RESULT SET."""
        req = requests.get(BASE_URL.format("locations"))

        if req.status_code == 200:
            return req.json()
        else:
            return None

    @property
    def total_sockets(self) -> int:
        """Get the total number of sockets at this location."""
        return self._total_sockets

    @property
    def location(self) -> str:
        """Get the location data."""
        return self._location

    @property
    def all_locations(self) -> str:
        """Return all locations."""
        return self._locations

    @property
    def uuid(self) -> str:
        """Return UUID of the location."""
        return self._uuid

    @property
    def chargepoint_identifiers(self) -> list:
        """Return the identifier(s) for the chargepoint(s)"""
        return self._cp_ident

    def _get_location(self) -> str:
        """Get location."""
        self._uuid = self._get_location_uid_by_address(self._identifier)
        if isinstance(self._uuid, type(None)):
            self._uuid = self._get_location_uid_from_id(self._identifier)

        return (
            self._get_location_by_uid(self._uuid)
            if not isinstance(self._uuid, type(None))
            else self._get_location_by_uid(self._identifier)
        )

    def _get_location_identifier(self) -> list:
        """Get the location identifier(s) for this location."""
        location = self._get_location_by_uid(self._uuid)
        identifiers = []
        for identifier in location["evses"]:
            identifiers.append(identifier)

        return identifiers

    def _get_location_by_uid(self, location_uid: str) -> str:
        """Get location by location UID."""
        if location_uid in self._locations["clever"]:
            return self._locations["clever"][location_uid]
        elif location_uid in self._locations["hubject"]:
            return self._locations["hubject"][location_uid]
        else:
            return None

    def _get_location_uid_from_id(self, chargepoint_id: str) -> str:
        """Find location UID for charge point ID."""
        for dataset in self._locations.items():
            for location in dataset[1].items():
                cp = location[1]["evses"][list(location[1]["evses"].keys())[0]]
                if "chargePointId" in cp:
                    if cp["chargePointId"] == chargepoint_id:
                        return location[0]

        return None

    def _get_location_uid_by_address(self, address: str) -> str:
        """
        Find location UID by address.
        Address need to be in the format "Street number, zipcode"
        Example: "Gasværksvej 5, 8660"
        """
        try:
            addr = address.strip().split(",")
            zc = addr[1].strip().split(" ")

            street = addr[0].lower()
            zipcode = zc[0]

            for dataset in self._locations.items():
                for location in dataset[1].items():
                    if (
                        location[1]["address"]["address"].lower() == street
                        and location[1]["address"]["postalCode"].lower() == zipcode
                    ):
                        return location[0]
        except:
            return None

        return None

    def _get_total_sockets(self) -> int:
        """Get total number of sockets for this location."""
        total_connections = 0
        for evse in self._location["evses"]:
            for _ in self._location["evses"][evse]["connectors"]:
                total_connections += 1

        return total_connections

    def get_sockets(self, evseId: str) -> int:
        """Get the number of sockets by ID."""
        sockets = {"connections": 0, "socket_types": []}
        for connector in self._location["evses"][evseId]["connectors"]:
            sockets.update({"connections": sockets["connections"] + 1})
            if (
                not self._location["evses"][evseId]["connectors"][connector][
                    "plugType"
                ]
                in sockets["socket_types"]
            ):
                sockets["socket_types"].append(
                    self._location["evses"][evseId]["connectors"][connector][
                        "plugType"
                    ]
                )

        return sockets
