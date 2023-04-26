"""Tests for the switch entity."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfTime,
    UnitOfPower,
)

from ..const import TOMPD63LW_SOCKET_PAYLOAD
from ..mixins.sensor import MultiSensorTests
from .base_device_tests import TuyaDeviceTestCase

ENERGY_DP = "1"
PHASEA_DP = "6"
FAULT_DP = "9"
PREPAY_DP = "11"
RESET_DP = "12"
BALANCE_DP = "13"
CHARGE_DP = "14"
LEAKAGE_DP = "15"
SWITCH_DP = "16"
ALARM1_DP = "17"
ALARM2_DP = "18"
IDNUM_DP = "19"
TEST_DP = "21"


class TestTOMPD63lw(MultiSensorTests, TuyaDeviceTestCase):
    __test__ = True

    def setUp(self):
        self.setUpForConfig("tompd_63lw_breaker.yaml", TOMPD63LW_SOCKET_PAYLOAD)
        self.subject = self.entities.get("switch")
        self.setUpMultiSensors(
            [
                {
                    "name": "sensor_voltage_a",
                    "dps": PHASEA_DP,
                    "unit": UnitOfElectricPotential.VOLT,
                    "device_class": SensorDeviceClass.VOLTAGE,
                    "testdata": ("CHoAQgQADlwAAA==", 217.0),
                },
                {
                    "name": "sensor_current_a",
                    "dps": PHASEA_DP,
                    "unit": UnitOfElectricCurrent.MILLIAMPERE,
                    "device_class": SensorDeviceClass.CURRENT,
                    "testdata": ("CHoAQgQADlwAAA==", 16900),
                },
                {
                    "name": "sensor_power_a",
                    "dps": PHASEA_DP,
                    "unit": UnitOfPower.WATT,
                    "device_class": SensorDeviceClass.POWER,
                    "testdata": ("CHoAQgQADlwAAA==", 3676),
                },
            ]
        )
        self.mark_secondary(
            [
                "button_earth_leak_test",
                "button_energy_reset",
                "number_charge_energy",
                "sensor_balance_energy",
                "sensor_current_a",
                "sensor_leakage_current",
                "sensor_power_a",
                "sensor_voltage_a",
                "switch_prepayment",
            ]
        )

    def test_phasea_encoding(self):
        self.dps[PHASEA_DP] = "CMAAD6AAAzUAAA=="
        self.assertEqual(self.multiSensor["sensor_voltage_a"].native_value, 224.0)
        self.assertEqual(self.multiSensor["sensor_current_a"].native_value, 4000)
        self.assertEqual(self.multiSensor["sensor_power_a"].native_value, 821.0)

    def test_phasea_missing(self):
        self.dps[PHASEA_DP] = None
        self.assertIsNone(self.multiSensor["sensor_voltage_a"].native_value)
        self.assertIsNone(self.multiSensor["sensor_current_a"].native_value)
        self.assertIsNone(self.multiSensor["sensor_power_a"].native_value)
