from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ireland_time_tariff_energy"


# --------------------------------------------------
# SETUP
# --------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
):
    async_add_entities(
        [
            IrelandImportRateSensor(entry),
            IrelandExportRateSensor(entry),
        ]
    )


# --------------------------------------------------
# BASE RATE SENSOR
# --------------------------------------------------
class IrelandBaseRateSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR/kWh"
    _attr_device_class = "monetary"
    _attr_state_class = "measurement"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry):
        self.entry = entry

    # ----------------------------
    # TIME HELPERS
    # ----------------------------
    def _now(self):
        return datetime.now().time()

    def _parse(self, value):
        return datetime.strptime(value, "%H:%M").time()

    def _is_weekend(self):
        return datetime.now().weekday() >= 5

    def _current_period(self):
        now = self._now()

        night_start = self._parse(self.entry.data["night_start"])
        day_start = self._parse(self.entry.data["day_start"])

        if self.entry.data.get("has_peak_rates"):
            peak_start = self._parse(self.entry.data["peak_start"])
            peak_end = self._parse(self.entry.data["peak_end"])
            if peak_start <= now < peak_end:
                return "peak"

        if day_start <= now < night_start:
            return "day"

        return "night"

    def _night_boost_active(self):
        if not self.entry.data.get("night_boost_enabled"):
            return False

        now = self._now()
        start = self._parse(self.entry.data["night_boost_start"])
        end = self._parse(self.entry.data["night_boost_end"])

        return start <= now < end

    # ----------------------------
    # ATTRIBUTES
    # ----------------------------
    @property
    def extra_state_attributes(self):
        return {
            "current_period": self._current_period(),
            "is_weekend": self._is_weekend(),
            "night_boost_active": self._night_boost_active(),
        }


# --------------------------------------------------
# IMPORT RATE SENSOR
# --------------------------------------------------
class IrelandImportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Import Rate"
    _attr_unique_id = "ireland_energy_import_rate"

    @property
    def native_value(self):
        # Night boost overrides all
        if self._night_boost_active():
            return self.entry.data["night_boost_import_rate"]

        period = self._current_period()

        if self.entry.data.get("has_weekend_rates"):
            day_type = "weekend" if self._is_weekend() else "weekday"
            return self.entry.data[f"import_{day_type}_{period}_rate"]

        return self.entry.data[f"import_{period}_rate"]


# --------------------------------------------------
# EXPORT RATE SENSOR
# --------------------------------------------------
class IrelandExportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Export Rate"
    _attr_unique_id = "ireland_energy_export_rate"

    @property
    def native_value(self):
        # Night boost overrides all
        if self._night_boost_active():
            return self.entry.data["night_boost_export_rate"]

        period = self._current_period()

        if self.entry.data.get("has_weekend_rates"):
            day_type = "weekend" if self._is_weekend() else "weekday"
            return self.entry.data[f"export_{day_type}_{period}_rate"]

        return self.entry.data[f"export_{period}_rate"]
