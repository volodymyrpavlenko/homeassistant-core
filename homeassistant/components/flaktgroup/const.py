"""Constants for flaktgroup component."""
from __future__ import annotations

from enum import Enum, IntEnum

from .modbus_coordinator import ModbusDatapoint, ModbusDatapointType

DOMAIN = "flaktgroup"
MODBUS_HUB = "modbus_hub"
CONF_MODBUS_COORDINATOR = "modbus_coordinator"
CONF_DEVICE_INFO = "device_info"
FLAKTGROUP_MODBUS_SLAVE = 2


class FanModes(IntEnum):
    """Fläktgroup Fan Modes."""

    LOW = 0
    NORMAL = 1
    HIGH = 2


class Presets(IntEnum):
    """Fläktgroup Presets."""

    STOP = 0
    AUTO = 1
    MANUAL = 2
    FIREPLACE = 3


def _flaktgroup_holding_register(address) -> ModbusDatapoint:
    return ModbusDatapoint(
        FLAKTGROUP_MODBUS_SLAVE, ModbusDatapointType.HOLDING_REGISTER, address
    )


def _flaktgroup_coil(address) -> ModbusDatapoint:
    return ModbusDatapoint(FLAKTGROUP_MODBUS_SLAVE, ModbusDatapointType.COIL, address)


class HoldingRegisters(Enum):
    """Fläktgroup Holding Registers."""

    SUPPLY_AIR_TEMPERATURE = _flaktgroup_holding_register(25)
    OUTDOOR_AIR_TEMPERATURE = _flaktgroup_holding_register(26)
    EXTRACT_AIR_TEMPERATURE = _flaktgroup_holding_register(27)
    FREEZING_PROTECTION_POST_HEATER = _flaktgroup_holding_register(28)
    DEFROST_AIR = _flaktgroup_holding_register(30)
    CO2 = _flaktgroup_holding_register(32)
    HUMIDITY_1 = _flaktgroup_holding_register(35)
    HUMIDITY_2 = _flaktgroup_holding_register(36)
    PRESSURE_SUPPLY_AIR = _flaktgroup_holding_register(37)
    PRESSURE_EXTRACT_AIR = _flaktgroup_holding_register(38)
    AIRFLOW_SUPPLY_AIR = _flaktgroup_holding_register(39)
    AIRFLOW_EXTRACT_AIR = _flaktgroup_holding_register(40)
    FAN_SPEED_SUPPLY_AIR = _flaktgroup_holding_register(41)
    FAN_SPEED_EXTRACT_AIR = _flaktgroup_holding_register(42)
    POST_HEATING = _flaktgroup_holding_register(43)
    PRE_HEATING = _flaktgroup_holding_register(44)
    COOLING = _flaktgroup_holding_register(45)
    ROTARY_HEAT_EXCHANGER = _flaktgroup_holding_register(46)
    TEMPERATURE_SET_POINT = _flaktgroup_holding_register(49)
    MIN_SUPPLY_TEMPERATURE = _flaktgroup_holding_register(54)
    MAX_SUPPLY_TEMPERATURE = _flaktgroup_holding_register(55)

    SET_POINT_CO2 = _flaktgroup_holding_register(73)

    SUPPLY_FAN_CONFIG_LOW = _flaktgroup_holding_register(78)
    SUPPLY_FAN_CONFIG_NORMAL = _flaktgroup_holding_register(79)
    SUPPLY_FAN_CONFIG_HIGH = _flaktgroup_holding_register(80)
    SUPPLY_FAN_CONFIG_COOKER_HOOD = _flaktgroup_holding_register(81)
    SUPPLY_FAN_CONFIG_FIREPLACE = _flaktgroup_holding_register(82)

    EXTRACT_FAN_CONFIG_LOW = _flaktgroup_holding_register(83)
    EXTRACT_FAN_CONFIG_NORMAL = _flaktgroup_holding_register(84)
    EXTRACT_FAN_CONFIG_HIGH = _flaktgroup_holding_register(85)
    EXTRACT_FAN_CONFIG_COOKER_HOOD = _flaktgroup_holding_register(86)
    EXTRACT_FAN_CONFIG_FIREPLACE = _flaktgroup_holding_register(87)

    FAN_MODE = _flaktgroup_holding_register(202)
    PRESET_MODE = _flaktgroup_holding_register(213)
    ACTIVE_TEMPERATURE_SETPOINT = _flaktgroup_holding_register(275)
    DIRTY_FILTER_ALARM_TIME = _flaktgroup_holding_register(277)


class Coils(Enum):
    """Fläktgroup Coils."""

    EXTERNAL_TIMER_1 = _flaktgroup_coil(13)
    EXTERNAL_TIMER_2 = _flaktgroup_coil(14)
    COOKER_HOOD_SWITCH = _flaktgroup_coil(25)
    SUMMER_WINTER_MODE = _flaktgroup_coil(85)
    FIRE_ALARM = _flaktgroup_coil(94)
    SENSOR_ERROR_SUPPLY_TEMPERATURE = _flaktgroup_coil(95)
    SENSOR_ERROR_OUTDOOR_TEMPERATURE = _flaktgroup_coil(96)
    SENSOR_ERROR_EXTRACT_TEMPERATURE = _flaktgroup_coil(97)
    SENSOR_ERROR_FROST_PROTECTION = _flaktgroup_coil(98)
    SENSOR_ERROR_DEFROST_TEMPERATURE = _flaktgroup_coil(99)
    DIRTY_FILTER = _flaktgroup_coil(105)
    SUPPLY_FAN_ERROR = _flaktgroup_coil(106)
    EXTRACT_FAN_ERROR = _flaktgroup_coil(107)
    FROST_ALARM = _flaktgroup_coil(110)
    ROTARY_HEAT_EXCHANGER_FAILURE = _flaktgroup_coil(111)
    FILTER_ALARM_SUPPLY_AIR = _flaktgroup_coil(112)
    FILTER_ALARM_EXTRACT_AIR = _flaktgroup_coil(113)
    OVERHEATING_ELECTRICAL_HEATER = _flaktgroup_coil(114)
    PUMP_HEATER_MALFUNCTION = _flaktgroup_coil(115)
    FREEZING_HOT_WATER_BATTERY = _flaktgroup_coil(116)
    SUMMARY_ALARM = _flaktgroup_coil(117)
    PUMP_COOLING_MALFUNCTION = _flaktgroup_coil(118)
    TEMPERATURE_ALARM = _flaktgroup_coil(184)
    HUMIDITY_CONTROL_RUNNING = _flaktgroup_coil(214)


CONF_UPDATE_INTERVAL = "update_interval"
