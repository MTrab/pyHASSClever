"""Clever availability lookup."""
from __future__ import annotations

import requests

from .const import BASE_URL


class CleverAvailability:
    """Clever availability lookup."""

    def __init__(self, chargepoints: list) -> None:
        """Initialize the availability lookup."""
        self._cp_list = chargepoints
        self._chargepoints = self._get_all(True)

    def _get_all(self, filtered: bool = False) -> str:
        """Get all chargepoints."""
        req = requests.get(BASE_URL.format("availability"))

        if req.status_code == 200:
            json = req.json()

            return self._filter_list(json) if filtered else req.json()
        else:
            return None

    def _filter_list(self, chargepoints: str) -> str:
        """Only save those we need."""
        filtered_points = []
        for dataset in chargepoints:
            for chargepoint in chargepoints[dataset]:
                if chargepoint in self._cp_list:
                    filtered_points.append(chargepoints[dataset][chargepoint])

        return filtered_points

    @property
    def total(self) -> int:
        """Get total number of chargers."""
        return len(self._chargepoints)

    @property
    def available(self) -> int:
        """Get number of available chargers."""
        cnt = 0
        for cp in self._chargepoints:
            if cp["status"] == "Available":
                cnt += 1

        return cnt

    @property
    def occupied(self) -> int:
        """Get number of occupied chargers."""
        cnt = 0
        for cp in self._chargepoints:
            if cp["status"] == "Occupied":
                cnt += 1

        return cnt

    def get_chargepoint_detail(self, chargepoint_id: str) -> str:
        """Get the detailed info for a specific chargepoint."""
        for cp in self._chargepoints:
            if cp["evseId"] == chargepoint_id:
                return cp
