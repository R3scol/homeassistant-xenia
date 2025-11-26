from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import XeniaDataUpdateCoordinator


@dataclass
class XeniaSensorDescription:
    key: str
    name: str
    unit: Optional[str]


SENSORS: list[XeniaSensorDescription] = [
    XeniaSensorDescription("MA_STATUS", "Xenia Status", None),
    XeniaSensorDescription("BG_SENS_TEMP_A", "Brühgruppe Temperatur", "°C"),
    XeniaSensorDescription("BB_SENS_TEMP_A", "Boiler Temperatur", "°C"),
    XeniaSensorDescription("SB_SENS_PRESS", "Dampfkessel Druck", "bar"),
    XeniaSensorDescription("PU_SENS_PRESS", "Pumpendruck", "bar"),
    XeniaSensorDescription("MA_EXTRACTIONS", "Bezüge gesamt", None),
    XeniaSensorDescription("MA_OPERATING_HOURS", "Betriebsstunden", "h"),
    XeniaSensorDescription("MA_ENERGY_TOTAL_KWH", "Energie gesamt", "kWh"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: XeniaDataUpdateCoordinator = data["coordinator"]

    entities: list[XeniaSensor] = [
        XeniaSensor(coordinator, desc) for desc in SENSORS
    ]

    async_add_entities(entities)


class XeniaSensor(CoordinatorEntity, SensorEntity):
    """Ein generischer Sensor, der auf /overview basiert."""

    def __init__(
        self,
        coordinator: XeniaDataUpdateCoordinator,
        description: XeniaSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = description.name
        self._key = description.key
        self._unit = description.unit

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        return self._unit

    @property
    def native_value(self) -> Any:
        data: Dict[str, Any] = self.coordinator.data or {}
        value = data.get(self._key)

        # Status als lesbaren Text
        if self._key == "MA_STATUS":
            if value == 0 or value == "0":
                return "Aus"
            if value == 1 or value == "1":
                return "An"
            return value

        return value
