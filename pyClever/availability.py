"""Clever availability lookup."""
from __future__ import annotations

import requests

from .const import BASE_URL


class CleverAvailability:
    """Clever availability lookup."""

    def __init__(self, chargepoints: list) -> None:
        """Initialize the availability lookup."""
        self.chargepoints = chargepoints
