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

    def available(self, cp_weights: dict) -> int:
        """Get number of available chargers."""
        if len(self._chargepoints) == 0:
            # Couldn't get detailed info, perhaps this chargepoint is private?
            return -1

        cnt = 0
        for cp in self._chargepoints:
            if cp["status"] == "Available":
                cnt += cp_weights[cp["evseId"]]["connections"]

        return cnt

    def occupied(self, cp_weights: dict) -> int:
        """Get number of occupied chargers."""
        if len(self._chargepoints) == 0:
            # Couldn't get detailed info, perhaps this chargepoint is private?
            return -1

        cnt = 0
        for cp in self._chargepoints:
            if cp["status"] == "Occupied":
                cnt += cp_weights[cp["evseId"]]["connections"]

        return cnt

    def get_chargepoint_detail(self, chargepoint_id: str) -> str:
        """Get the detailed info for a specific chargepoint."""
        for cp in self._chargepoints:
            if cp["evseId"] == chargepoint_id:
                return cp
