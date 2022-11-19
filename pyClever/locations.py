"""Clever locations lookup."""
from __future__ import annotations

import requests

from .const import BASE_URL


class CleverLocations:
    """Clever location lookup."""

    def __init__(self) -> None:
        """Initialize the location lookup."""
        self._locations: str | None = None
        self._last_refresh: str = None

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
        if isinstance(self._locations, type(None)):
            self._locations = self._get_all_locations()

        return self._locations

    def get_location(self, identifier: str, only_uid: bool = False) -> str:
        """Get location."""
        if isinstance(self._locations, type(None)):
            self._locations = self._get_all_locations()

        uid = self._get_location_uid_by_address(identifier)
        if isinstance(uid, type(None)):
            uid = self._get_location_uid_from_id(identifier)

        if only_uid:
            return uid if not isinstance(uid, type(None)) else identifier
        else:
            return (
                self._get_location_by_uid(uid)
                if not isinstance(uid, type(None))
                else self._get_location_by_uid(identifier)
            )

    def get_location_identifier(self, uid: str) -> list:
        """Get the location identifier(s) for this location."""
        location = self._get_location_by_uid(uid)
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