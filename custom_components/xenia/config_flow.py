from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .api import XeniaApi

_LOGGER = logging.getLogger(__name__)


async def _test_connection(hass: HomeAssistant, host: str) -> None:
    """Testet, ob /api/v2/overview erreichbar ist."""
    api = XeniaApi(host)
    await hass.async_add_executor_job(api.get_overview)


class XeniaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config-Flow für Xenia."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        errors: Dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            # Doppeltes Setup verhindern
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            try:
                await _test_connection(self.hass, host)
            except Exception as err:
                _LOGGER.warning("Verbindung zur Xenia fehlgeschlagen: %s", err)
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Xenia ({host})",
                    data={CONF_HOST: host},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=config_entries.FLOW_MANAGER_SCHEMA(
                {CONF_HOST: str}  # HA baut ein einfaches Textfeld
            ),
            errors=errors,
        )
