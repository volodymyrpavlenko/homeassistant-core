import asyncio
from enum import IntEnum
import logging

import serial_asyncio

MIN_VOLUME = 70
MAX_VOLUME = 210
VOLUME_SPREAD = MAX_VOLUME - MIN_VOLUME

_LOGGER = logging.getLogger(__name__)

INPUTS = {
    "USB": 0,
    "Optical": 1,
    "Coaxial": 2,
    "XLR": 3,
    "Bluetooth": 4,
    "Analog": 5,
}

INPUTS_REVERSE = {v: k for k, v in INPUTS.items()}

AUDIO_TYPES = ["PCM", "DSD", "MQA", "MQA."]

AUDIO_FREQUENCIES = [
    "UNLOCK",
    "44.1 KHz",
    "48.0 KHz",
    "88.2 KHz",
    "96.0 KHz",
    "176.4 KHz",
    "192.0 KHz",
    "352.8 KHz",
    "384.0 KHz",
    "64x",
    "128x",
    "256x",
    "512x",
    "1024x",
    "UNLOCK",
]


class UnitState(IntEnum):
    STANDBY = (0,)
    ON = (1,)
    WAKE_UP = (2,)
    SHUT_DOWN = 3


class UpdateListener:
    def __init__(self, protocol) -> None:
        self.protocol = protocol

    def ready(self):
        _LOGGER.debug("M2Tech ready")

    def unit_state(self, unit_state):
        _LOGGER.debug("Unit state: %s", unit_state)

    def rssi(self, rssi: int):
        _LOGGER.debug("RSSI: %d", rssi)

    def volume(self, volume: float):
        _LOGGER.debug("Volume: %d", volume)

    def mute(self, mute: bool):
        _LOGGER.debug("Mute: %d", mute)

    def input(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "input", value)

    def frequency(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "frequency", value)

    def audio_type(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "audio_type", value)

    def mqa_auth(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "mqa_auth", value)

    def firmware_major(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "firmware_major", value)

    def firmware_minor(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "firmware_minor", value)

    def master_gain(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "master_gain", value)

    def volume_step(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "volume_step", value)

    def volume_mode(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "volume_mode", value)

    def power_on_volume(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "power_on_volume", value)

    def auto_power_off(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "auto_power_off", value)

    def standby_led(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "standby_led", value)

    def auto_power_on(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "auto_power_on", value)

    def remote_power(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "remote_power", value)

    def display_backlight(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "display_backlight", value)

    def pcm_filter(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "pcm_filter", value)

    def dsd_filter(self, value):
        _LOGGER.debug("Received new value: %s=%d", "dsd_filter", value)
        _LOGGER.debug("M2Tech update: %s=%d", "dsd_filter", value)

    def balance_level(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "balance_level", value)

    def paired(self, value):
        _LOGGER.debug("M2Tech update: %s=%d", "paired", value)


class InputChunkProtocol(asyncio.Protocol):
    def __init__(self, update_listener: UpdateListener):
        super().__init__()
        self._update_listener = update_listener

    def connection_made(self, transport: serial_asyncio.SerialTransport):
        self.transport = transport
        self._buf = b""
        self._msgs_recvd = 0
        # self._update_listener = UpdateListener(self)
        # self.query_status()

    def data_received(self, data):
        """Store characters until a newline is received."""
        self._buf += data
        if b"\n" in self._buf:
            lines = self._buf.split(b"\n")
            self._buf = lines[-1]  # whatever was left over
            for line in lines[:-1]:
                self.process_line(line.decode())

    def query_status(self):
        self.send_cmd("qSQ")
        self.send_cmd("qST")

    def toggle_power(self):
        self.send_cmd("STB")

    def set_volume(self, volume: float):
        volume_num = round(volume * VOLUME_SPREAD + MIN_VOLUME)
        if volume_num >= 70 and volume_num <= 210:
            self.send_cmd(f"VL={volume_num:02X}")
        else:
            _LOGGER.warning("Invalid volume: %f (%d)" % (volume, volume_num))

    def connection_lost(self, exc):
        _LOGGER.warning("Serial connection closed: %s", exc)

    def process_line(self, line):
        split = line.split(":", maxsplit=2)
        match split[0]:
            case "RDY":
                self.query_status()
                self._update_listener.ready()
            case "US":
                self._update_listener.unit_state(UnitState(int(split[1])))
            case "SI":
                self._update_listener.rssi(int(split[1], 16))
            case "VL":
                self._update_listener.volume(
                    (int(split[1], 16) - MIN_VOLUME) / VOLUME_SPREAD
                )
            case "MT":
                self._update_listener.mute(split[1] == "01")
            case "IN":
                self._update_listener.input(INPUTS_REVERSE.get(int(split[1], 16)))
            case "FR":
                self._update_listener.frequency(
                    self.map_audio_frequency(int(split[1], 16))
                )
            case "AT":
                self._update_listener.audio_type(self.map_audio_type(int(split[1], 16)))
            case "MQ":
                self._update_listener.mqa_auth(int(split[1], 16))
            case "F1":
                self._update_listener.firmware_major(int(split[1], 16))
            case "F2":
                self._update_listener.firmware_minor(int(split[1], 16))
            case "MG":
                self._update_listener.master_gain(int(split[1], 16))
            case "VS":
                self._update_listener.volume_step(int(split[1], 16))
            case "VM":
                self._update_listener.volume_mode(int(split[1], 16))
            case "PV":
                self._update_listener.power_on_volume(int(split[1], 16))
            case "AP":
                self._update_listener.auto_power_off(int(split[1], 16))
            case "SL":
                self._update_listener.standby_led(int(split[1], 16))
            case "AN":
                self._update_listener.auto_power_on(int(split[1], 16))
            case "RP":
                self._update_listener.remote_power(int(split[1], 16))
            case "BK":
                self._update_listener.display_backlight(int(split[1], 16))
            case "PF":
                self._update_listener.pcm_filter(int(split[1], 16))
            case "DF":
                self._update_listener.dsd_filter(int(split[1], 16))
            case "BL":
                self._update_listener.balance_level(int(split[1], 16))
            case "PS":
                self._update_listener.paired(int(split[1], 16))
            case _:
                _LOGGER.warning("unknown line: %s" % line)

    def send_cmd(self, cmd):
        _cmd = bytes(cmd, "utf-8")
        self.transport.serial.write(_cmd)
        _LOGGER.debug("Sent command: %s" % _cmd)

    def set_input(self, input):
        input_id = INPUTS.get(input)
        if input_id >= 0 and input_id <= 5:
            self.send_cmd("IN=0%d" % input_id)
        else:
            _LOGGER.error("Invalid input: %s" % input)

    def toggle_mute(self):
        self.send_cmd("MUT")

    def toggle_playpause(self):
        self.send_cmd("UPP")

    def previous_track(self):
        self.send_cmd("UPR")

    def stop(self):
        self.send_cmd("UST")

    def next_track(self):
        self.send_cmd("UNX")

    def map_audio_frequency(self, frequency):
        return (
            AUDIO_FREQUENCIES[frequency]
            if frequency < len(AUDIO_FREQUENCIES)
            else AUDIO_FREQUENCIES[0]
        )

    def map_audio_type(self, audio_type):
        return (
            AUDIO_TYPES[audio_type]
            if audio_type < len(AUDIO_FREQUENCIES)
            else "Unknown"
        )
