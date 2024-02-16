"""The denon component."""
import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "m2tech"


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Use config values to set up a function enabling status retrieval."""
    # Store the data service object.
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "config": config_entry,
        "created_in_async_setup_entry": True,
    }

    # Forward the config entries to the supported platforms.
    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.MEDIA_PLAYER]
    )
    return True
