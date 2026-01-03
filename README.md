# 🇮🇪 Ireland Time-Based Energy Tariffs

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
![Version](https://img.shields.io/github/v/release/d4diaz/ireland_time_tariff_energy)
![Maintenance](https://img.shields.io/maintenance/yes/2026)

A **Home Assistant custom integration** that provides **day / night / peak electricity pricing**
for **import and export**, fully compatible with the **Energy Dashboard**.

Designed primarily for **Irish electricity tariffs**, but configurable for any country or supplier.

---

✨ New features:
- Built-in electricity cost sensors (Day / Night / Peak)
- No YAML required
- Automatic statistics support
- Cost breakdown ready for dashboards

🔧 Improvements:
- Refactored rate sensors (rates only)
- New internal cost engine
- Clean separation of concerns

## ✨ Features

- ✅ Day / Night / Peak pricing
- ✅ Separate **import** and **export** rates
- ✅ Fully compatible with **Home Assistant Energy Dashboard**
- ✅ UI-based configuration (no YAML)
- ✅ HACS installable
- ✅ Works with smart meters, solar, and batteries

---

### Configuration screen

After installing via HACS:

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Ireland Time-Based Energy Tariffs**
4. Enter your tariff details:
   - Import: Night / Day / Peak rates
   - Export: Night / Day / Peak rates
   - Time windows

---

## 🔌 Energy Dashboard Setup

Use the generated sensors:

- **Import cost sensor**
  - `sensor.ireland_energy_import_rate`
- **Export value sensor**
  - `sensor.ireland_energy_export_rate`

Go to:
Settings → Energy → Electricity Grid


Select the sensors above.

Home Assistant will automatically apply the **correct rate at the correct time**.

---

## 🇮🇪 Default Tariff Structure (editable)

| Period | Typical Time |
|------|-------------|
| Night | 23:00 – 08:00 |
| Day | 08:00 – 17:00 |
| Peak | 17:00 – 19:00 |

All times and prices are fully configurable in the UI.

---

## ❓ FAQ

### ❓ Why is there only one sensor for import/export?
Home Assistant Energy expects **one rate sensor** whose value changes over time.
This integration handles the switching internally (night/day/peak).

---

### ❓ Can I use this outside Ireland?
Yes. The name is Ireland-focused, but **all prices and times are configurable**.

---

### ❓ Does this work with solar and batteries?
Yes. It works with:
- Grid import
- Grid export
- Solar PV
- Battery systems (e.g. Sigenergy, Tesla, etc.)

---

### ❓ Can I add weekend or seasonal tariffs?
Not yet — but planned. See Roadmap below.

---

## 🛠️ Troubleshooting

### ❌ Integration does not appear when adding
- Restart Home Assistant
- Make sure it is installed via **HACS → Integrations**

---

### ❌ “Failed to set up – Check logs”
Check logs at:
Settings → System → Logs
Search for:
ireland_time_tariff_energy

Most issues are caused by:
- Old cached versions (restart HA)
- Incomplete HACS install (reinstall)

---

### ❌ README not visible in HACS
- Ensure `README.md` is at **repo root**
- Ensure `hacs.json` has `"render_readme": true`
- In HACS → **⋮ → Reload**

---

## 🛣️ Roadmap

- ⏭️ Weekday vs weekend tariffs
- ⏭️ Multiple peak windows
- ⏭️ Seasonal pricing
- ⏭️ Irish supplier presets (Electric Ireland, Energia, Bord Gáis)
- ⏭️ Attributes showing active tariff period

---

## 🧑‍💻 Author
Created by **Diaz Xavier, based in Sligo, Ireland who owns a small digital marketing company called Sevenoways Innovations**  
Community-driven, open-source 🇮🇪
