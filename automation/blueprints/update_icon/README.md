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
  path: update_icon/update_icon_openweathermap.yaml
  input:
    weather_entity: sensor.openweathermap_weather_code
    select_target:
      entity_id:
        - select.thermostat_living_room
        - select.thermostat_bedroom
    daytime: true

```

# Thermostat Icon Update via Environment Canada

This blueprint updates the icon of your Sinopé thermostat on ZHA based on Environment Canada weather condition codes.

## Requirements

- Environment Canada integration with a sensor that exposes the weather condition code.
- One or more `select` entities linked to your thermostats for icon control.

## Inputs

- `weather_entity`: Sensor entity that provides the weather condition code.
- `select_target`: One or more `select` entities to update.

## Usage

Create one automations from this blueprint:
- It works day and night as icon number are different

## Example

```yaml
use_blueprint:
  path: update_icon/update_icon_env_canada.yaml
  input:
    weather_entity: sensor.your_city_icon_code
    select_target:
      entity_id:
        - select.living_room_weather_icons
        - select.bedroom_weather_icons

```
