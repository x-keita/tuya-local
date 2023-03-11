"""Tests for Parkside PLGS 2012 A1 Smart Charger"""
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    PERCENTAGE,
    UnitOfTime,
    UnitOfTemperature,
)
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.components.sensor import (
    SensorDeviceClass,
    STATE_CLASS_MEASUREMENT,
)
from ..const import PARKSIDE_PLGS2012A1_PAYLOAD
from ..mixins.binary_sensor import MultiBinarySensorTests
from ..mixins.number import MultiNumberTests
from ..mixins.select import BasicSelectTests
from ..mixins.sensor import MultiSensorTests
from ..mixins.switch import MultiSwitchTests
from .base_device_tests import TuyaDeviceTestCase

SWITCH_DPS = "1"
NAME_DPS = "2"
CURRENT_DPS = "3"
VOLTAGE_DPS = "4"
BATTERY_DPS = "5"
TEMPERATURE_DPS = "6"
MODE_DPS = "7"
STORAGE_DPS = "8"
LIMITER_DPS = "9"
MAXTEMPCOUNT_DPS = "10"
UNKNOWN11_DPS = "11"
MAXCURRENT_DPS = "101"
REMAIN_DPS = "102"
ALMOSTCHARGED_DPS = "103"
FULLYCHARGED_DPS = "104"


class TestParksidePLGS2012A1Charger(
    MultiBinarySensorTests,
    MultiNumberTests,
    BasicSelectTests,
    MultiSensorTests,
    MultiSwitchTests,
    TuyaDeviceTestCase,
):
    __test__ = True

    def setUp(self):
        self.setUpForConfig(
            "parkside_plgs2012a1_smart_charger.yaml", PARKSIDE_PLGS2012A1_PAYLOAD
        )
        self.setUpMultiBinarySensors(
            [
                {
                    "name": "binary_sensor_almost_charged",
                    "dps": ALMOSTCHARGED_DPS,
                },
                {
                    "name": "binary_sensor_fully_charged",
                    "dps": FULLYCHARGED_DPS,
                },
            ],
        )
        self.setUpMultiNumber(
            [
                {
                    "name": "number_charge_current",
                    "dps": CURRENT_DPS,
                    "device_class": NumberDeviceClass.CURRENT,
                    "max": 30000,
                    "step": 100,
                    "unit": UnitOfElectricCurrent.MILLIAMPERE,
                },
                {
                    "name": "number_charge_voltage",
                    "dps": VOLTAGE_DPS,
                    "device_class": NumberDeviceClass.VOLTAGE,
                    "max": 25.0,
                    "scale": 1000,
                    "step": 0.1,
                    "unit": UnitOfElectricPotential.VOLT,
                },
            ],
        )
        self.setUpBasicSelect(
            MODE_DPS,
            self.entities.get("select_charge_type"),
            {
                "ECO": "Eco",
                "quick": "Performance",
                "standard": "Balanced",
                "individual": "Expert",
            },
        )
        self.setUpMultiSensors(
            [
                {
                    "name": "sensor_battery",
                    "dps": BATTERY_DPS,
                    "unit": PERCENTAGE,
                    "device_class": SensorDeviceClass.BATTERY,
                },
                {
                    "name": "sensor_time_remaining",
                    "dps": REMAIN_DPS,
                    "unit": UnitOfTime.MINUTES,
                    "device_class": SensorDeviceClass.DURATION,
                },
                {
                    "name": "sensor_current_temperature",
                    "dps": TEMPERATURE_DPS,
                    "unit": UnitOfTemperature.CELSIUS,
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "state_class": STATE_CLASS_MEASUREMENT,
                },
                {
                    "name": "sensor_max_current",
                    "dps": MAXCURRENT_DPS,
                    "unit": UnitOfElectricCurrent.MILLIAMPERE,
                    "device_class": SensorDeviceClass.CURRENT,
                },
                {
                    "name": "sensor_max_temperature_count",
                    "dps": MAXTEMPCOUNT_DPS,
                },
                {
                    "name": "sensor_name",
                    "dps": NAME_DPS,
                    "testdata": ("test", "test"),
                },
            ],
        )
        self.setUpMultiSwitch(
            [
                {
                    "name": "switch",
                    "dps": SWITCH_DPS,
                },
                {
                    "name": "switch_storage",
                    "dps": STORAGE_DPS,
                },
                {
                    "name": "switch_temperature_limiter",
                    "dps": LIMITER_DPS,
                },
            ],
        )

        self.mark_secondary(
            [
                "number_charge_current",
                "number_charge_voltage",
                "switch_storage",
                "switch_temperature_limiter",
                "sensor_current_temperature",
                "sensor_max_temperature_count",
                "sensor_name",
                "select_charge_type",
                "sensor_max_current",
                "binary_sensor_almost_charged",
                "binary_sensor_fully_charged",
            ]
        )

    def test_multi_switch_state_attributes(self):
        switch = self.multiSwitch.get("switch")
        storage = self.multiSwitch.get("switch_storage")
        temp = self.multiSwitch.get("switch_temperature_limiter")
        self.assertEqual(storage.extra_state_attributes, {})
        self.assertEqual(temp.extra_state_attributes, {})
        self.dps[UNKNOWN11_DPS] = "unknown_11"
        self.assertDictEqual(
            switch.extra_state_attributes, {"unknown_11": "unknown_11"}
        )
