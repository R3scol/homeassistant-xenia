from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .api import XeniaApi

_LOGGER = logging.getLogger(__name__)


class XeniaDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Koordiniert Abruf von /overview für alle Entitäten."""

    def __init__(self, hass: HomeAssistant, api: XeniaApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Xenia Espresso",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self.api.get_overview)
        except Exception as err:
            raise UpdateFailed(f"Fehler beim Abrufen der Xenia-Daten: {err}") from err
