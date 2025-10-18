# Thermostat Icon Update via Openweathermap (Day/Night)

This blueprint updates the icon of your Sinopé thermostat on ZHA based on Openweathermap weather condition codes and time of day.

## Requirements

- Openweathermap integration with a sensor that exposes the weather condition code.
- Sun integration (`sun.sun`) to determine day/night.
- One or more `select` entities linked to your thermostats for icon control.

## Inputs

- `weather_entity`: Sensor entity that provides the weather condition code.
- `select_target`: One or more `select` entities to update.
- `daytime`: Boolean to choose day (`true`) or night (`false`) mode.

## Usage

Create two automations from this blueprint:
- One with `daytime: true` for daytime icons.
- One with `daytime: false` for nighttime icons.

## Example

```yaml
use_blueprint:
  path: update_icon_openweathermap/update_icon_openweathermap.yaml
  input:
    weather_entity: sensor.openweathermap_condition_code
    select_target:
      entity_id:
        - select.thermostat_living_room
        - select.thermostat_bedroom
    daytime: true
