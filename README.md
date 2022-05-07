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
In /config/zhaquirks copy the fourth files, light.py, switch.py, thermostat.py and sensor.py then restart Home Assistant

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
...[zhaquirks] Loading custom quirks module sensor
```

# Editing the quirks:
You can edit the files as you like and restart HA to test your changes. Don't forget to delete the ```__pycache__``` folder in /config/zhaquirks before restarting HA so your changes will be added.

# Custom cluster attributes details:

I'll list here all the custom cluster attribute with explanation about how to use them in your automation.
- Thermostats:

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0xff01|0x0010|outdoor_temp|celcius*100
|0xff01|0x0011|outdoor_temp_timeout| Delay in seconds before reverting to setpoint display if no more outdoor temp is received
|0xff01|0x0020|secs_since_2k| second since year 2000
|0xff01|0x0070|currentLoad| watt/hr
|0xff01|0x0071|Unknown| ?
|0xff01|0x0105|airFloorMode|Air: 1, floor: 2
|0xff01|0x0106|auxOutputMode|0=off, 1=expantion module
|0xff01|0x0108|airMaxLimit|temp: celcius*100, valid only if floor mode is selected
|0xff01|0x0109|floorMinSetpoint| off: -32768, temp: temp*100
|0xff01|0x010A|floorMaxSetpoint| off: -32768, temp: temp*100
|0xff01|0x010B|tempSensorType| 0=10k, 1=12k
|0xff01|0x010C|floorLimitStatus|0=ok, 1=floorLimitLowReached, 2=floorLimitMaxReached, 3=floorAirLimitMaxReached
|0xff01|0x0114|timeFormat|0=24h, 1=12h
|0xff01|0x0115|gfciStatus|0=ok, 1=error
|0xff01|0x0118|auxConnectedLoad| watt/hr, 0xffff=off
|0xff01|0x0119|connectedLoad|None: 0xffff
|0xff01|0x0128|pumpProtection| Off: 0xff, On: 0x1
|0xff01|0x012D|reportLocalTemperature| Celcius * 100
| --- | --- | --- | ---
|0x0201|0x0400 |SetOccupancy| Home: 0, away:1
|0x0201|0x0401 |MainCycleOutput| Number of second
|0x0201|0x0402 |BacklightAutoDimParam| OnDemand: 0, Always: 1
|0x0201|0x0404|AuxCycleOutput| Number of second
| --- | --- | --- | ---
|0x0b04|0x050f|Apparent_Power|watt/hr			
|0x0b04|0x050b|Active_Power|watt/hr
| --- | --- | --- | ---
|0x0204|0x0000|TemperatureDisplayMode|0=celcius, 1=farenheight
|0x0204|0x0001|keypadLockout|0=no lock, 1=lock
| --- | --- | --- | ---
|0x0702|0x0000|CurrentSummationDelivered|watt/hr	

- lights and dimmer:

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0xff01|0x0002|KeypadLock| Locked: 1, Unlocked: 0
|0xff01|0x0050|onLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01|0x0051|offLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01|0x0052|onLedIntensity| Percent
|0xff01|0x0053|offLedIntensity| Percent
|0xff01|0x0055|minIntensity| 0 to 3000
|0xff01|0x00A0|Timer| Number of seconds
|0xff01|0x0119|ConnectedLoad| None: 0, watt
| --- | --- | --- | ---
|0x0702|0x0000|CurrentSummationDelivered| Sum of delivered watt/hr
|0x0006|0x0000|OnOff| 1=on, 0=off
|0x0008|0x0000|CurrentLevel| 0=0%, 254=100%

- Switch SP2600ZB, SP2610ZB, Outlet

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0x0702|0x0000|CurrentSummationDelivered|watt/hr
|0x0b04|0x050B|Active_Power|watt/hr
|0x0b04|0x0605|ACPowerDivisor| 10
|0x0b04|0x0604|ACPowerMultiplier|	1
|0x0006|0x0000|OnOff| 0=off, 1=on

- Switch RM3250ZB, RM3500ZB, Load Controller

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0xff01|0x0060|ConnectedLoad|	watt/hr
|0xff01|0x00A0|Timer| Seconds
|0xff01|0x0002|KeyboardLock| on=1, off=0
|0xff01|0x0070|CurrentLoad|	watt/hr
|0x0006|0x0000|OnOff|	1=on, 0=off
|0x0b04|0x050B|Active_Power|	watt/hr
|0x0b04|0x0605|AC_Power_Divisor| 1
|0x0b04|0x0604|AC_Power_Multiplier|	1
|0x0702|0x0000|CurrentSummationDelivered|	watt/hr

- Switch MC3100ZB, multi controller

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0xff01|0x00A0|Timer|	second, on endpoint 1 and 2
|0x0001|0x003E|BatteryAlarmState| 0=no alarm, 1=alarn
|0x0006|0x0000|OnOff| 1=on, 0=off, on endpoint 1 and 2

- Switch valve VA4200ZB VA4201ZB, VA4220ZB, VA4221ZB

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0x0001|0x0020|Battery_Voltage| Volt
|0x0001|0x003e|BatteryAlarmState| 0=no alarm, 1=alarm
|0x0006|0x0000|OnOff|	1=on, 0=off

- Sensors WL4200 and WL4200S

|Cluster|Attributes|Fonction |Value
| --- | --- | --- | ---
|0x0402|0x0000|MeasuredValueTemperature|	celcius*100	
|0x0500|0x0030|ZoneStatus| 0=no leak, 1=leak

# Automation examples:
- Sending outside temperature to thermostats:
  - Celcius:
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
            mode: single
```
   - Farenheight:
```
alias: Update outside Temperature
description: ''
trigger:
  - platform: time_pattern
    minutes: '45'
action:
  - service: zha.set_zigbee_cluster_attribute
    data:
      ieee: 50:0b:91:32:01:03:6b:2f
      endpoint_id: 1
      cluster_id: 65281
      cluster_type: in
      attribute: 16
      value: >-
        {{ (((state_attr('weather.home', 'temperature' ) - 32) * 5/9)|float*100)|int }}
    mode: single
```
You can use either 0xff01 or 65281 in automation. You can send temperature on regular timely basis or when the outside temperature change. Do not pass over 60 minte or thermostat display will go back to setpoint display.

- setting the outside temperature sensor:

You can use any temperature source, local or remote.
```
  - platform: template
    sensors:
      local_temp:
        friendly_name: "Outside_temperature"
        value_template: "{{ state_attr('weather.dark_sky', 'temperature') }}"
```

