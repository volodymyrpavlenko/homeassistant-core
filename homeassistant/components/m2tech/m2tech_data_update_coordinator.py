import logging

from homeassistant.components.m2tech.m2tech_serial_protocol import UpdateListener
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class M2TechDataUpdateCoordinator(DataUpdateCoordinator, UpdateListener):
    def __init__(self, hass: HomeAssistant, name: str) -> None:
        """Init the M2Tech Data Update Coordinator."""
        self._data = {}

        super().__init__(
            hass,
            _LOGGER,
            name=f"{name} Update Coordinator",
        )

    def unit_state(self, unit_state):
        self._data["state"] = unit_state
        self.async_set_updated_data(self._data)

    def volume(self, volume: float):
        self._data["volume"] = volume
        self.async_set_updated_data(self._data)

    def mute(self, mute: bool):
        self._data["mute"] = mute
        self.async_set_updated_data(self._data)

    def input(self, input):
        self._data["input"] = input
        self.async_set_updated_data(self._data)

    def audio_type(self, value):
        self._data["audio_type"] = value
        self.async_set_updated_data(self._data)

    def frequency(self, value):
        self._data["frequency"] = value
        self.async_set_updated_data(self._data)
