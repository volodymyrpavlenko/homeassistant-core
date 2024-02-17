"""Support for Denon Network Receivers."""
from __future__ import annotations

import logging

import serial_asyncio
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN
from .m2tech_data_update_coordinator import M2TechDataUpdateCoordinator
from .m2tech_serial_protocol import INPUTS, InputChunkProtocol, UnitState

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "M2Tech Young MkIII"

SUPPORT_M2TECH = (
    MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.SELECT_SOURCE
)

USB_SUPPORTED_FEATURES = (
    MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.NEXT_TRACK
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICE): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up an APCUPSd Online Status binary sensor."""
    m2tech_update_coordinator = M2TechDataUpdateCoordinator(hass, config_entry.title)
    transport, protocol = await serial_asyncio.create_serial_connection(
        hass.loop,
        lambda: InputChunkProtocol(m2tech_update_coordinator),
        config_entry.data["device"],
        baudrate=115200,
    )
    m2tech = M2TechYoungMkIIIDevice(
        config_entry.entry_id, config_entry.title, protocol, m2tech_update_coordinator
    )
    async_add_entities([m2tech])


class M2TechYoungMkIIIDevice(CoordinatorEntity, MediaPlayerEntity):
    """Representation of a Denon device."""

    def __init__(
        self,
        entry_id,
        name,
        m2tech_protocol: InputChunkProtocol,
        coordinator: M2TechDataUpdateCoordinator,
    ):
        """Initialize the Denon device."""
        super().__init__(coordinator)
        self._m2tech_protocol = m2tech_protocol
        self._name = name
        self._attr_unique_id = entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self._name,
        )
        self._attr_source_list = list(INPUTS.keys())
        self._attr_audio_type = None
        self._attr_frequency = None

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    def turn_off(self) -> None:
        """Turn off media player."""
        _LOGGER.debug("Turning off")
        self._m2tech_protocol.toggle_power()

    def set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        self._m2tech_protocol.set_volume(volume)
        _LOGGER.debug("Setting volume level to: %f", volume)

    def mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        self._m2tech_protocol.toggle_mute()
        _LOGGER.debug("Toggling mute to: %s", mute)

    def turn_on(self) -> None:
        """Turn the media player on."""
        self._m2tech_protocol.toggle_power()
        _LOGGER.debug("Turning on")

    @property
    def app_name(self) -> str | None:
        return f"{self._attr_audio_type} ({self._attr_frequency})"

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data
        if "state" in data:
            self.update_data_state(data["state"])
        if "volume" in data:
            self._attr_volume_level = data["volume"]
        if "input" in data:
            self._attr_source = data["input"]
        if "mute" in data:
            self._attr_is_volume_muted = data["mute"]
        if "audio_type" in data:
            self._attr_audio_type = data["audio_type"]
        if "frequency" in data:
            self._attr_frequency = data["frequency"]
        self.async_write_ha_state()

    def update_data_state(self, state):
        if state == UnitState.ON:
            self._attr_state = MediaPlayerState.ON
        elif state == UnitState.STANDBY:
            self._attr_state = MediaPlayerState.OFF
        else:
            _LOGGER.warning("Unknown state: %s", state)

    @property
    def assumed_state(self) -> bool:
        return self._attr_source == "USB"

    def select_source(self, source: str) -> None:
        """Select input source."""
        self._m2tech_protocol.set_input(source)
        _LOGGER.debug("Select source %s", source)

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        if self.source == "USB":
            return SUPPORT_M2TECH | USB_SUPPORTED_FEATURES
        return SUPPORT_M2TECH

    def media_play(self) -> None:
        self._m2tech_protocol.toggle_playpause()

    def media_pause(self) -> None:
        self._m2tech_protocol.toggle_playpause()

    def media_previous_track(self) -> None:
        self._m2tech_protocol.previous_track()

    def media_stop(self) -> None:
        self._m2tech_protocol.stop()

    def media_next_track(self) -> None:
        self._m2tech_protocol.next_track()
