import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

DOMAIN = "ireland_time_tariff_energy"


class IrelandTimeTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    # ---------------------------
    # STEP 1 – STRUCTURE
    # ---------------------------
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_energy()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("has_weekend_rates", default=True): bool,
                vol.Required("has_peak_rates", default=True): bool,
                vol.Required("night_boost_enabled", default=False): bool,
            }),
        )

    # ---------------------------
    # STEP 2 – ENERGY SENSORS
    # ---------------------------
    async def async_step_energy(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title="Ireland Time-Based Energy Tariffs",
                data=self._data,
            )

        return self.async_show_form(
            step_id="energy",
            data_schema=vol.Schema({
                vol.Required("grid_import_sensor"):
                    selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="energy"
                        )
                    ),
                vol.Optional("battery_discharge_sensor"):
                    selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="energy"
                        )
                    ),
            }),
        )
