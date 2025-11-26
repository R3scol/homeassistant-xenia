from __future__ import annotations

import logging
from typing import Any, Dict

import requests

_LOGGER = logging.getLogger(__name__)


class XeniaApi:
    """Schnittstelle zur Xenia API v2."""

    def __init__(self, host: str) -> None:
        # host z.B. "192.168.50.3"
        self._base = f"http://{host}/api/v2"

    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{self._base}{path}"
        _LOGGER.debug("Xenia GET %s", url)
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()

    def _post_action(self, action: int) -> None:
        """POST /machine/control mit action-Code.

        Mapping laut Xenia-Doku:
        0 = Maschine AUS
        1 = Maschine AN
        2 = ECO-Modus
        3 = Dampfboiler AUS
        4 = Dampfboiler AN
        5 = Maschine AN + Dampfboiler AUS
        :contentReference[oaicite:0]{index=0}
        """
        url = f"{self._base}/machine/control/"
        data = {"action": str(action)}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        _LOGGER.debug("Xenia POST %s data=%s", url, data)
        resp = requests.post(url, data=data, headers=headers, timeout=5)
        resp.raise_for_status()

    # --- öffentliche Methoden ---

    def get_overview(self) -> Dict[str, Any]:
        """Live-Zustand der Maschine (Temperaturen, Drücke, Status)."""
        return self._get("/overview")

    def get_status(self) -> Dict[str, Any]:
        """Allgemeine Status-/Konfig-Daten."""
        return self._get("/machine/status")

    def get_config(self) -> Dict[str, Any]:
        """Konfiguration (Timer, Max Ampere etc.)."""
        return self._get("/machine/config")

    def list_scripts(self) -> Dict[str, Any]:
        """Liste der Xenia-Skripte (index_list, title_list)."""
        return self._get("/scripts/list")

    def power_on(self) -> None:
        self._post_action(1)

    def power_off(self) -> None:
        self._post_action(0)

    def eco_mode(self) -> None:
        """ECO-Modus aktivieren (einmaliger Aufruf; kein richtiger Toggle)."""
        self._post_action(2)

    def steam_boiler_off(self) -> None:
        self._post_action(3)

    def steam_boiler_on(self) -> None:
        self._post_action(4)

    def power_on_steam_off(self) -> None:
        """Maschine an + Dampfboiler aus (Spezialfall, Action 5)."""
        self._post_action(5)

