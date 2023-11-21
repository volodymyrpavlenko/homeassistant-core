"""Support for Modbus Register sensors."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import CONF_DEVICE_INFO, CONF_MODBUS_COORDINATOR, DOMAIN, HoldingRegisters
from .modbus_coordinator import (
    FlaktgroupModbusDataUpdateCoordinator,
    ModbusDatapointContext,
    ModbusDatapointDescriptionMixin,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1


@dataclass
class ModbusDatapointSensorDescription(
    ModbusDatapointDescriptionMixin, SensorEntityDescription
):
    """Modbus Datapoint Sensor Description."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Fläktgroup sensors from a config entry."""
    hass_config = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "supply_air_temperature", HoldingRegisters.SUPPLY_AIR_TEMPERATURE
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "outdoor_air_temperature", HoldingRegisters.OUTDOOR_AIR_TEMPERATURE
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "extract_air_temperature", HoldingRegisters.EXTRACT_AIR_TEMPERATURE
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "freezing_protection_post_heater",
                HoldingRegisters.FREEZING_PROTECTION_POST_HEATER,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
                icon="mdi:heating-coil",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "defrost_air",
                HoldingRegisters.DEFROST_AIR,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "CO2",
                HoldingRegisters.CO2,
                SensorDeviceClass.CO2,
                "ppm",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "humidity_1",
                HoldingRegisters.HUMIDITY_1,
                SensorDeviceClass.HUMIDITY,
                "%",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "humidity_2",
                HoldingRegisters.HUMIDITY_2,
                SensorDeviceClass.HUMIDITY,
                "%",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "pressure_supply_air",
                HoldingRegisters.PRESSURE_SUPPLY_AIR,
                SensorDeviceClass.ATMOSPHERIC_PRESSURE,
                "%",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "pressure_extract_air",
                HoldingRegisters.PRESSURE_EXTRACT_AIR,
                SensorDeviceClass.ATMOSPHERIC_PRESSURE,
                "%",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "airflow_supply_air",
                HoldingRegisters.AIRFLOW_SUPPLY_AIR,
                SensorDeviceClass.WIND_SPEED,
                "l/s",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "airflow_extract_air",
                HoldingRegisters.AIRFLOW_EXTRACT_AIR,
                SensorDeviceClass.WIND_SPEED,
                "l/s",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "fan_speed_supply_air",
                HoldingRegisters.FAN_SPEED_SUPPLY_AIR,
                SensorDeviceClass.SPEED,
                "%",
                icon="mdi:fan",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "fan_speed_extract_air",
                HoldingRegisters.FAN_SPEED_EXTRACT_AIR,
                SensorDeviceClass.SPEED,
                "%",
                icon="mdi:fan",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "post_heating",
                HoldingRegisters.POST_HEATING,
                SensorDeviceClass.SPEED,
                "%",
                entity_registry_enabled_default=False,
                icon="mdi:heating-coil",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "pre_heating",
                HoldingRegisters.PRE_HEATING,
                SensorDeviceClass.SPEED,
                "%",
                entity_registry_enabled_default=False,
                icon="mdi:heating-coil",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "cooling",
                HoldingRegisters.COOLING,
                SensorDeviceClass.SPEED,
                "%",
                entity_registry_enabled_default=False,
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _sensor_description(
                "rotary_heat_exchanger",
                HoldingRegisters.ROTARY_HEAT_EXCHANGER,
                SensorDeviceClass.SPEED,
                "%",
            ),
        ),
        FlaktgroupSensor(
            hass_config[CONF_MODBUS_COORDINATOR],
            hass_config[CONF_DEVICE_INFO],
            _temperature_sensor_description(
                "active_temperature_setpoint",
                HoldingRegisters.ACTIVE_TEMPERATURE_SETPOINT,
            ),
        ),
    ]
    async_add_entities(entities)


def _temperature_sensor_description(
    kk,
    holding_register_address: HoldingRegisters,
    entity_category=None,
    entity_registry_enabled_default=True,
    icon=None,
):
    return _sensor_description(
        kk,
        holding_register_address,
        SensorDeviceClass.TEMPERATURE,
        "°C",
        entity_category,
        entity_registry_enabled_default,
        icon,
        0.1,
    )


def _sensor_description(
    kk,
    holding_register: HoldingRegisters,
    device_class,
    native_unit_of_measurement,
    entity_category=None,
    entity_registry_enabled_default=True,
    icon=None,
    scale: float = 1,
):
    opt = {}
    if entity_category:
        opt["entity_category"] = entity_category
    if icon:
        opt["icon"] = icon
    key = slugify(holding_register.name)
    return ModbusDatapointSensorDescription(
        key=key,
        translation_key=key,
        has_entity_name=True,
        native_unit_of_measurement=native_unit_of_measurement,
        device_class=device_class,
        modbus_datapoint=holding_register.value,
        scale=scale,
        entity_registry_enabled_default=entity_registry_enabled_default,
        **opt,
    )


class FlaktgroupSensor(CoordinatorEntity, RestoreSensor, SensorEntity):
    """Fläktgroup Sensor."""

    def __init__(
        self,
        coordinator: FlaktgroupModbusDataUpdateCoordinator,
        device_info: DeviceInfo,
        description: ModbusDatapointSensorDescription,
    ) -> None:
        """Initialize the Fläktgroup Sensor."""
        assert description.modbus_datapoint is not None
        self._attr_unique_id = f"{description.modbus_datapoint.slave}-{description.modbus_datapoint.address}"
        self._attr_device_info = device_info
        self.entity_description: ModbusDatapointSensorDescription = description

        super().__init__(
            coordinator,
            ModbusDatapointContext(description.modbus_datapoint, lambda: self.enabled),
        )

    async def async_added_to_hass(self) -> None:
        """Restore ATTR_CHANGED_BY on startup since it is likely no longer in the activity log."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        last_sensor_state = await self.async_get_last_sensor_data()
        if (
            not last_state
            or not last_sensor_state
            or last_state.state == STATE_UNAVAILABLE
        ):
            return

        self._attr_native_value = last_sensor_state.native_value

    def _handle_coordinator_update(self) -> None:
        value = self.coordinator.data.get(self.entity_description.modbus_datapoint)
        if value is not None:
            self._attr_native_value = self.entity_description.from_modbus_value(value)
            self._attr_available = True
        else:
            self._attr_available = False
        self.async_write_ha_state()
