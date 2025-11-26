from __future__ import annotations

from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import XeniaDataUpdateCoordinator
from .api import XeniaApi


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: XeniaDataUpdateCoordinator = data["coordinator"]
    api: XeniaApi = data["api"]

    entities: list[XeniaSwitch] = [
        XeniaPowerSwitch(coordinator, api),
        # Wenn du später Eco/Steam als Button/Switch willst, kann man hier mehr ergänzen
    ]

    async_add_entities(entities)


class XeniaSwitch(CoordinatorEntity, SwitchEntity):
    """Basis-Klasse für Xenia-Switches."""

    def __init__(self, coordinator: XeniaDataUpdateCoordinator, api: XeniaApi) -> None:
        super().__init__(coordinator)
        self._api = api

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success


class XeniaPowerSwitch(XeniaSwitch):
    """Ein/Aus-Schalter der Maschine."""

    @property
    def name(self) -> str:
        return "Xenia Power"

    @property
    def is_on(self) -> bool:
        data: Dict[str, Any] = self.coordinator.data or {}
        status = data.get("MA_STATUS")
        return bool(int(status)) if status is not None else False

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(self._api.power_on)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(self._api.power_off)
        await self.coordinator.async_request_refresh()
