from homeassistant.components.button import ButtonDeviceClass
from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import (
    SensorDeviceClass,
    STATE_CLASS_MEASUREMENT,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
)

from ..const import HIMOX_H05_PURIFIER_PAYLOAD
from ..helpers import assert_device_properties_set
from ..mixins.button import BasicButtonTests
from ..mixins.lock import BasicLockTests
from ..mixins.select import BasicSelectTests
from ..mixins.sensor import MultiSensorTests
from ..mixins.switch import SwitchableTests
from .base_device_tests import TuyaDeviceTestCase

SWITCH_DPS = "1"
TEMP_DPS = "2"
PRESET_DPS = "4"
FILTER_DPS = "5"
LOCK_DPS = "7"
RESET_DPS = "11"
TIMER_DPS = "18"
AQI_DPS = "21"


class TestHimoxH05Purifier(
    BasicButtonTests,
    BasicLockTests,
    BasicSelectTests,
    MultiSensorTests,
    SwitchableTests,
    TuyaDeviceTestCase,
):
    __test__ = True

    def setUp(self):
        self.setUpForConfig("himox_h05_purifier.yaml", HIMOX_H05_PURIFIER_PAYLOAD)
        self.subject = self.entities["fan"]
        self.setUpSwitchable(SWITCH_DPS, self.subject)
        self.setUpBasicButton(
            RESET_DPS,
            self.entities.get("button_filter_reset"),
            ButtonDeviceClass.RESTART,
        )
        self.setUpBasicLock(LOCK_DPS, self.entities.get("lock_child_lock"))
        self.setUpBasicSelect(
            TIMER_DPS,
            self.entities.get("select_timer"),
            {
                "cancel": "Off",
                "1h": "1 hour",
                "2h": "2 hours",
                "4h": "4 hours",
                "8h": "8 hours",
            },
        )
        self.setUpMultiSensors(
            [
                {
                    "dps": TEMP_DPS,
                    "name": "sensor_current_temperature",
                    "unit": UnitOfTemperature.CELSIUS,
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "state_class": STATE_CLASS_MEASUREMENT,
                },
                {
                    "dps": FILTER_DPS,
                    "name": "sensor_active_filter_life",
                    "unit": PERCENTAGE,
                },
                {
                    "dps": AQI_DPS,
                    "name": "sensor_air_quality",
                },
            ]
        )
        self.mark_secondary(
            [
                "button_filter_reset",
                "lock_child_lock",
                "sensor_active_filter_life",
                "select_timer",
                "sensor_current_temperature",
            ]
        )

    def test_supported_features(self):
        self.assertEqual(
            self.subject.supported_features,
            FanEntityFeature.PRESET_MODE,
        )

    def test_preset_modes(self):
        self.assertCountEqual(
            self.subject.preset_modes,
            ["auto", "low", "mid", "high"],
        )

    def test_preset_mode(self):
        self.dps[PRESET_DPS] = "low"
        self.assertEqual(self.subject.preset_mode, "low")

    async def test_set_preset_mode(self):
        async with assert_device_properties_set(
            self.subject._device, {PRESET_DPS: "mid"}
        ):
            await self.subject.async_set_preset_mode("mid")
