# Thermostat ECO Logo Control During Peak Periods (Hydro-Québec)

This repository contains two Home Assistant blueprints to manage the ECO logo on Sinopé thermostats during Hydro-Québec peak periods. These automations allow you to:

- **Start** blinking the ECO logo at the beginning of a peak period.
- **Stop** the ECO logo blinking at the end of the peak period.

## Requirements

- A `binary_sensor` from the [Hydro-Québec integration](https://github.com/claudegel/hydroqc) that indicates when a peak period is active.
- One or more `number` entities on your Sinopé thermostats, typically named `number.your_thermostat_eco_delta_setpoint`.

## Blueprints

### `show_dr_logo.yaml` — Start ECO Logo

- **Triggers**: Every day at `05:00` and `15:00`
- **Condition**: The Hydro-Québec peak period binary_sensor is `on`
- **Action**: Sends `0` to each `eco_delta_setpoint` number entity to activate the ECO logo blinking

### `stop_dr_logo.yaml` — Stop ECO Logo

- **Triggers**: Every day at `09:10` and `20:10`
- **Action**: Sends `-128` to each `eco_delta_setpoint` number entity to stop the ECO logo blinking

## ⚙️ Inputs

| Input             | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `condition_target` | Entity ID of the Hydro-Québec binary sensor indicating peak period status   |
| `number_target`    | One or more thermostat `number` entities to control the ECO logo            |

## Example Automations

### Start ECO Logo

```yaml
use_blueprint:
  path: show_dr_logo.yaml
  input:
    condition_target: binary_sensor.hydroqc_peak_active
    number_target:
      entity_id:
        - number.thermostat_living_room_eco_delta_setpoint
        - number.thermostat_bedroom_eco_delta_setpoint
```
