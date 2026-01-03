from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN


# --------------------------------------------------
# SETUP
# --------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
):
    entities = [
        EnergyCostDaySensor(hass, entry),
        EnergyCostNightSensor(hass, entry),
        EnergyCostPeakSensor(hass, entry),
    ]

    async_add_entities(entities)

    for entity in entities:
        await entity.async_start_listening()


# --------------------------------------------------
# BASE COST SENSOR
# --------------------------------------------------
class BaseEnergyCostSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR"
    _attr_device_class = "monetary"
    _attr_state_class = "total_increasing"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._attr_native_value = 0.0
        self._last_energy = None

        self.energy_sensor = entry.data["grid_import_sensor"]
        self.rate_sensor = "sensor.ireland_energy_import_rate"

    async def async_added_to_hass(self):
        self._restore_state()

    def _restore_state(self):
        state = self.hass.states.get(self.entity_id)
        if state and state.state not in ("unknown", "unavailable"):
            self._attr_native_value = float(state.state)

    async def async_start_listening(self):
        async_track_state_change_event(
            self.hass,
            self.energy_sensor,
            self._handle_energy_change,
        )

    @callback
    def _handle_energy_change(self, event):
        new_state = event.data.get("new_state")
        if not new_state or new_state.state in ("unknown", "unavailable"):
            return

        try:
            energy = float(new_state.state)
        except ValueError:
            return

        if self._last_energy is None:
            self._last_energy = energy
            return

        delta_kwh = energy - self._last_energy
        self._last_energy = energy

        if delta_kwh <= 0:
            return

        # Check if this sensor should accumulate now
        if not self._is_active_period():
            return

        rate_state = self.hass.states.get(self.rate_sensor)
        if not rate_state or rate_state.state in ("unknown", "unavailable"):
            return

        try:
            rate = float(rate_state.state)
        except ValueError:
            return

        self._attr_native_value += delta_kwh * rate
        self.async_write_ha_state()

    def _is_active_period(self) -> bool:
        rate_state = self.hass.states.get(self.rate_sensor)
        if not rate_state:
            return False

        return rate_state.attributes.get("current_period") == self.period


# --------------------------------------------------
# DAY COST SENSOR
# --------------------------------------------------
class EnergyCostDaySensor(BaseEnergyCostSensor):
    _attr_name = "Electricity Cost Day"
    _attr_unique_id = "electricity_cost_day"
    period = "day"


# --------------------------------------------------
# NIGHT COST SENSOR
# --------------------------------------------------
class EnergyCostNightSensor(BaseEnergyCostSensor):
    _attr_name = "Electricity Cost Night"
    _attr_unique_id = "electricity_cost_night"
    period = "night"


# --------------------------------------------------
# PEAK COST SENSOR
# --------------------------------------------------
class EnergyCostPeakSensor(BaseEnergyCostSensor):
    _attr_name = "Electricity Cost Peak"
    _attr_unique_id = "electricity_cost_peak"
    period = "peak"
