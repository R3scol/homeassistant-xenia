from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

SENSOR_MAP = {
    'BG_SENS_TEMP_A': ('xenia_brew_group_temp', 'Brühgruppe Temperatur', '°C'),
    'BG_SET_TEMP': ('xenia_brewgroup_set_temp', 'Brühgruppe Solltemp', '°C'),
    'BB_SENS_TEMP_A': ('xenia_boiler_temp', 'Boiler Temperatur', '°C'),
    'PU_SENS_PRESS': ('xenia_pump_pressure', 'Pumpendruck', 'bar'),
    'DB_SENS_PRESS': ('xenia_steam_pressure', 'Dampfkessel Druck', 'bar'),
    'MA_STATUS': ('xenia_status', 'Xenia Status', None)
}

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data['xenia']['api']
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER:=hass.logger,
        name='xenia-coordinator',
        update_interval=timedelta(seconds=5),
        update_method=lambda: hass.async_add_executor_job(api.overview)
    )
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for key, (entity_id, name, unit) in SENSOR_MAP.items():
        entities.append(GenericXeniaSensor(coordinator, key, name, unit))
    async_add_entities(entities, True)

class GenericXeniaSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        self._coordinator = coordinator
        self._key = key
        self._name = name
        self._unit = unit
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        await self._coordinator.async_request_refresh()
        data = self._coordinator.data or {}
        # try common keys with fallbacks
        self._state = data.get(self._key) or data.get(self._key.replace('DB_', 'BB_')) or data.get(self._key.replace('PU_', 'PU_'))
