from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import asyncio
from datetime import timedelta
from .api import XeniaAPI

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data['xenia']['api']
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER:=hass.logger,
        name="xenia",
        update_interval=timedelta(seconds=10),
        update_method=lambda: hass.async_add_executor_job(api.overview)
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([
        XeniaPowerSwitch(api, coordinator),
        XeniaEcoSwitch(api, coordinator),
        XeniaSteamSwitch(api, coordinator)
    ], True)

class BaseXeniaSwitch(SwitchEntity):
    def __init__(self, api, coordinator):
        self._api = api
        self._coordinator = coordinator

    async def async_update(self):
        await self._coordinator.async_request_refresh()
        data = self._coordinator.data

class XeniaPowerSwitch(BaseXeniaSwitch):
    def __init__(self, api, coordinator):
        super().__init__(api, coordinator)
        self._is_on = False

    @property
    def name(self):
        return "Xenia Power"

    @property
    def is_on(self):
        try:
            return self._coordinator.data.get('MA_STATUS') == '1'
        except Exception:
            return self._is_on

    async def async_turn_on(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 0)
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 1)
        self._is_on = False

class XeniaEcoSwitch(BaseXeniaSwitch):
    @property
    def name(self):
        return "Xenia Eco Mode"

    @property
    def is_on(self):
        return self._coordinator.data.get('MA_MODE') == 'eco'

    async def async_turn_on(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 3)  # action 3 assumed for eco
    async def async_turn_off(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 4)  # action 4 assumed to leave eco

class XeniaSteamSwitch(BaseXeniaSwitch):
    @property
    def name(self):
        return "Xenia Steam Mode"

    @property
    def is_on(self):
        return self._coordinator.data.get('STEAM') == '1'

    async def async_turn_on(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 5)  # assumed steam action
    async def async_turn_off(self, **kwargs):
        await hass.async_add_executor_job(self._api.power, 6)
