"""Config flow for APCUPSd integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_DEVICE, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from . import DOMAIN

_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE, default="/dev/rfcomm0"): cv.string,
        vol.Required(CONF_NAME, default="M2Tech Young MkIII"): cv.string,
    }
)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """M2Tech Young integration config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=_SCHEMA)

        # Abort if an entry with same host and port is present.
        self._async_abort_entries_match({CONF_DEVICE: user_input[CONF_DEVICE]})

        await self.async_set_unique_id(user_input[CONF_DEVICE])
        self._abort_if_unique_id_configured()

        title = user_input[CONF_NAME]

        return self.async_create_entry(
            title=title,
            data=user_input,
        )
