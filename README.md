# sinope-zha
This is a custom quirks for sinope zigbee devices for testing before it is added to zha-device-handlers. It also explain how to setup those quirks in Home Assistant to use and test them before they are merged in zha-device-handlers.

# Home assistant configuration:
- in /config directory create a new directory zhaquirks -> /config/zhaquirks
- in configuration.yaml add the following:
```
zha:
  database_path: zigbee.db
  custom_quirks_path: /config/zhaquirks/
```
# Copy the quirks
In /config/zhaquirks copy the three file, light.py, switch.py and thermostat.py and restart Home Assistant

# Logging
In configuration.yaml you can add this to get logging info for the quirks:
```
logger:
  default: warning
  logs:
    zhaquirks: debug
```
You should see the following:
```
...[zhaquirks] Loading quirks module zhaquirks.aduro
...
...[zhaquirks] Loading custom quirks from /config/zhaquirks
...[zhaquirks] Loading custom quirks module light
...[zhaquirks] Loading custom quirks module switch
...[zhaquirks] Loading custom quirks module thermostat
```

# Editing the quirks:
You can edit the files as you like and restart HA to test your changes. Don't forget to delete the ```__pycache__``` folder before restarting HA

# Custom cluster attributes details:

I'll list here all the custom cluster attribute with explanation about how to use them in your automation.
- Thermostats:

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0xff01|0x0010|Outdoor Temperature|celcius*100
|0xff01|0x0011|Outdoor temperature timeout| Delay in seconds before reverting to setpoint display if no more outdoor temp is received
|0xff01|0x0020|hour| second since year 2000
|0xff01|0x0105|Sensor mode|Air: 1, floor: 2
|0xff01|0x0119|Connected load|None: 0xffff
|0xff01| 0x0118|Aux. connected load| None: 0xffff
|0xff01|0x010a|Floor max temperature| off: -32768, temp: temp*100
|0xff01|0x0109|Floor min temperature| off: -32768, temp: temp*100
|0xff01|0x0108|Air max temperature|temp: celcius*100, valid only if floor mode is selected
|0xff01|0x010b|Sensor type|0: 10k, 1: 12k
|0xff01|0x0128|Pump protection| Off: 0xff, On: 0x1
|0xff01|0x0114|Time format|12h: 0x1, 24h: 0x0
| --- | --- | --- | ---
|0x0201| 0x0400 |Occupancy|Home: 0, away:1
|0x0201| 0x0401 |Main ouput cycle|Number of second
|0x0201|0x0402 |Backlight mode|OnDemand: 0, Always: 1
|0x0201| 0x0404|Aux ouput cycle|Number of second
| --- | --- | --- | ---

- lights:

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
0xff01|0x00a0|Timer|Number of seconds
|0xff01| 0x0002|Keyboard lock| Locked: 1, Unlocked: 0
|0xff01|0x0050|On - Led color|0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01|0x0051|Off - Led color|0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01| 0x0052|On - Led color intensity|Percent
|0xff01|0x0053|Off - Led color intensity| Percent
|0xff01|0x0119|Load connected|None: 0, watt
| --- | --- | --- | ---

# Automation examples:
- Sending outside temperature to thermostats:
```
- alias: Send-OutdoorTemp
  trigger:
    - platform: state
      entity_id: sensor.local_temp # sensor to get local temperature
  variables:
    thermostats:
      - 50:0b:91:40:00:02:2d:6d  #ieee of your thermostat dvices, one per line
      - 50:0b:91:40:00:02:2a:65
  action:
    - repeat:  #service will be call for each ieee
        count: "{{thermostats|length}}"
        sequence:
          - service: zha.set_zigbee_cluster_attribute
            data:
              ieee: "{{ thermostats[repeat.index-1] }}"
              endpoint_id: 1
              cluster_id: 0xff01 # 65281
              cluster_type: in
              attribute: 0x0010 # 16
              value: "{{ ( trigger.to_state.state|float * 100 ) |int }}" # sending temperature in hundredth of a degree
```
You can use either 0xff01 or 65281 in automation

- setting the outside temperature sensor:

You can use any temperature source, local or remote.
```
  - platform: template
    sensors:
      local_temp:
        friendly_name: "Outside_temperature"
        value_template: "{{ state_attr('weather.dark_sky', 'temperature') }}"
```

