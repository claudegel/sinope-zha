# - send_outdoor_temperature

This Home Assistant blueprint send celsius outdoor temperature to the second display of your Sinopé thermostat.

## Requirements

- A temperature sensor that reports in **Celsius** (e.g., OpenWeatherMap, Environment Canada, or any local source).
- One or more `number` entities linked to your ZHA Sinopé thermostats for external temperature display.

## Inputs

| Input           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `weather_entity` | Entity ID of the outdoor temperature sensor (in Celsius)                |
| `number_target`  | One or more `number` entities to update with the converted temperature     |

## Trigger

- The automation runs each time the temperature sensor updates.

## Example Automation YAML

```yaml
use_blueprint:
  path: send_outdoor_temperature.yaml
  input:
    weather_entity: sensor.outdoor_temperature
    number_target:
      entity_id:
        - number.living_room_outdor_temperature
        - number.bedroom_outdor_temperature
```


# - send_outdoor_farenheight_temperature

This Home Assistant blueprint converts outdoor temperature from Fahrenheit to Celsius and sends it to the second display of your Sinopé thermostat. The thermostat will internally reconvert and round the value to Fahrenheit if configured that way.

## Requirements

- A temperature sensor that reports in **Fahrenheit** (e.g., OpenWeatherMap, Environment Canada, or any local source).
- One or more `number` entities linked to your Sinopé thermostats for external temperature display.

## Inputs

| Input           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `weather_entity` | Entity ID of the outdoor temperature sensor (in Fahrenheit)                |
| `number_target`  | One or more `number` entities to update with the converted temperature     |

## Trigger

- The automation runs each time the temperature sensor updates.

## Conversion Logic

- Converts Fahrenheit to Celsius using:  
  `C = (F - 32) / 1.8`
- Multiplies the result by 100 to match thermostat format.
- Rounds to the nearest integer before sending.

## Example Automation YAML

```yaml
use_blueprint:
  path: send_outdoor_temperature_f_to_c.yaml
  input:
    weather_entity: sensor.outdoor_temperature_f
    number_target:
      entity_id:
        - number.living_room_outdor_temperature
        - number.bedroom_outdor_temperature
```
