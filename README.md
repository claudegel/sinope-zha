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

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- |---|
|0xff01|0x0002|t.enum8|keypadLockout|0 = unlocked, 1 = locked|read/write
|0xff01|0x0004|t.CharacterString|firmware_version| |read
|0xff01|0x0010|t.int16s|outdoor_temp|temp*100|read/write
|0xff01|0x0011|t.uint16_t|outdoor_temp_timeout| Delay in seconds before reverting to setpoint display if no more outdoor temp is received|read/write
|0xff01|0x0012|t.enum8|config2ndDisplay| 0 = auto, 1 = setpoint, 2 = outside temperature.|read/write
|0xff01|0x0020|t.uint32_t|secs_since_2k| second since year 2000|read/write
|0xff01|0x0070|t.bitmap8|currentLoad| watt/hr|
|0xff01|0x0071|t.int8s|ecoMode| default:-128, -100-0-100%|
|0xff01|0x0072|t.uint8_t|ecoMode1| default:255, 0-99|
|0xff01|0x0073|t.uint8_t|ecoMode2| default 255, 0-100|
|0xff01|0x0075|t.bitmap32|unknown testing| |read/write
|0xff01|0x0100|t.uint8_t|unknown testing| |read
|0xff01|0x0105|t.enum8|airFloorMode|Air: 1, floor: 2|read/write
|0xff01|0x0106|t.enum8|auxOutputMode|0=off, 1=expantion module|read/write
|0xff01|0x0107|t.int16s|FloorTemperature|temp: celcius*100|read
|0xff01|0x0108|t.int16s|airMaxLimit|temp: celcius*100, valid only if floor mode is selected|read/write
|0xff01|0x0109|t.int16s|floorMinSetpoint| off: -32768, temp: temp*100|read/write
|0xff01|0x010A|t.int16s|floorMaxSetpoint| off: -32768, temp: temp*100|read/write
|0xff01|0x010B|t.enum8|tempSensorType| 0=10k, 1=12k|read/write
|0xff01|0x010C|t.uint8_t|floorLimitStatus|0=ok, 1=floorLimitLowReached, 2=floorLimitMaxReached, 3=floorAirLimitMaxReached|report/read
|0xff01|0x010D|t.int16s|RoomTemperature|temp: celcius*100|read
|0xff01|0x0114|t.enum8|timeFormat|0=24h, 1=12h|read/write
|0xff01|0x0115|t.enum8|gfciStatus|0=ok, 1=error|report/read
|0xff01|0x0118|t.uint16_t|auxConnectedLoad| watt/hr, 0xffff=off|read/write
|0xff01|0x0119|t.uint16_t|connectedLoad|None: 0xffff|
|0xff01|0x0128|t.uint8_t|pumpProtection| Off: 0xff, On: 0x1|read/write
|0xff01|0x012A|t.uint8_t|unknown|default:60||5,10,15,20,30,60|read/write
|0xff01|0x012B|t.int16s|currentSetpoint| |read/write
|0xff01|0x012D|t.int16s|reportLocalTemperature| Celcius * 100|read
|0xff01|0x0200|t.bitmap32|Unknown| 0x00000000|
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
| --- | --- | --- | --- | --- |---|
|0x0201|0x0400|t.enum8|SetOccupancy| Home: 0, away:1|read/write
|0x0201|0x0401|t.uint16_t|MainCycleOutput| Number of second|read/write
|0x0201|0x0402|t.enum8|BacklightAutoDimParam| OnDemand: 0, Always: 1|read/write
|0x0201|0x0404|t.uint16_t|AuxCycleOutput| Number of second|read/write
| --- | --- | --- | --- | --- |---|
|0x0b04|0x050f|t.uint16_t|Apparent_Power|watt/hr|report/read	
|0x0b04|0x050b|t.uint16_t|Active_Power|watt/hr|report/read/write
| --- | --- | --- | --- | --- | --- |
|0x0204|0x0000|t.enum8|TemperatureDisplayMode|0=celcius, 1=farenheight|read/write
|0x0204|0x0001|t.enum8|keypadLockout|0=no lock, 1=lock|read/write
| --- | --- | --- | --- | --- | --- |
|0x0702|0x0000|t.uint48_t|CurrentSummationDelivered|watt/hr	|report/read

- lights and dimmer:

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- | --- |
|0xff01|0x0002|t.enum8|KeypadLock| Locked: 1, Unlocked: 0|read/write
|0xff01|0x0004|t.CharacterString|firmware_version| |read
|0xff01|0x0050|t.uint24_t|onLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01|0x0051|t.uint24_t|offLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue
|0xff01|0x0052|t.uint8_t|onLedIntensity| Percent
|0xff01|0x0053|t.uint8_t|offLedIntensity| Percent
|0xff01|0x0054|t.enum8|actionReport| singleTapUp: 2, doubleTapUp: 4, singleTapDown: 18, doubleTapDown: 20|read/repport
|0xff01|0x0055|t.uint16_t|minIntensity| 0 to 3000
|0xff01|0x00A0|t.uint32_t|Timer| Number of seconds
|0xff01|0x0119|t.uint16_t|ConnectedLoad| None: 0, watt
|0xff01|0x0200|t.bitmap32|Unknown| ?
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
| --- | --- | --- | --- | --- | --- |
|0x0702|0x0000|t.uint48_t|CurrentSummationDelivered| Sum of delivered watt/hr
|0x0006|0x0000|t.Bool|OnOff| 1=on, 0=off
|0x0008|0x0000|t.uint8_t|CurrentLevel| 0=0%, 254=100%

- Switch SP2600ZB, SP2610ZB, Outlet

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- | --- |
|0xff01|0x0004|t.CharacterString|firmware_version| |read
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
|0x0702|0x0000|t.uint48_t|CurrentSummationDelivered|watt/hr
|0x0b04|0x050B|t.uint16_t|Active_Power|watt/hr
|0x0b04|0x0605|t.uint16_t|ACPowerDivisor| 10
|0x0b04|0x0604|t.uint16_t|ACPowerMultiplier|	1
|0x0006|0x0000|t.Bool|OnOff| 0=off, 1=on

- Switch RM3250ZB, Load Controller

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- | --- |
|0xff01|0x0002|t.enum8|keypadLockout|0 = unlocked, 1 = locked|read/write
|0xff01|0x0004|t.CharacterString|firmware_version| |read
|0xff01|0x0060|t.uint16_t|ConnectedLoad|	watt/hr
|0xff01|0x00A0|t.uint32_t|Timer| Seconds
|0xff01|0x0002|t.enum8|KeyboardLock| on=1, off=0
|0xff01|0x0070|t.bitmap8|CurrentLoad|	watt/hr
|0xff01|0x0200|t.bitmap32|Unknown| ?
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
|0x0006|0x0000|t.Bool|OnOff|	1=on, 0=off
|0x0b04|0x050B|t.uint16_t|Active_Power|	watt/hr
|0x0b04|0x0605|t.uint16_t|AC_Power_Divisor| 1
|0x0b04|0x0604|t.uint16_t|AC_Power_Multiplier|	1
|0x0702|0x0000|t.uint48_t|CurrentSummationDelivered|	watt/hr

- Switch RM3500ZB, Calypso water tank controller

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- |---|
|0xff01|0x0002|t.enum8|keypadLockout|0 = unlocked, 1 = locked|read/write
|0xff01|0x0004|t.CharacterString|firmware_version|1|read
|0xff01|0x0010|t.int16s|unknown|400|
|0xff01|0x0013|t.enum8|tankSize|1,2,3,4|
|0xff01|0x0060|t.uint16_t|ConnectedLoad|	watt/hr
|0xff01|0x0070|t.bitmap8|CurrentLoad|	watt/hr
|0xff01|0x0076|t.uint8_t|drConfigWaterTempMin|	45 or 0
|0xff01|0x0077|t.uint8_t|drConfigWaterTempTime|	2
|0xff01|0x0078|t.uint16_t|drWTTimeOn|	240
|0xff01|0x0079|t.bitmap8|unknown| 0| report/read
|0xff01|0x0200|t.bitmap32|unknown| 0| report/read
|0xff01|0x0283|t.uint8_t|ColdLoadPickupStatus| 1, 2|read
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
|0x0500|0x0030|t.uint16_t|ZoneStatus| 0=no leak, 1=leak
|0x0006|0x0000|t.Bool|OnOff|	1=on, 0=off
|0x0b04|0x050B|t.uint16_t|Active_Power|	watt/hr
|0x0b04|0x0605|t.uint16_t|AC_Power_Divisor| 1
|0x0b04|0x0604|t.uint16_t|AC_Power_Multiplier|	1
|0x0b05|0x011d|t.int8s|Rssi| value -45
|0x0402|0x0000|t.int16s|WaterTemperature| temp oC

- Switch MC3100ZB, multi controller

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- |---|
|0xff01|0x00A0|t.uint32_t|Timer|	second, on endpoint 1 and 2
|0xff01|0xFFFD|t.uint16_t|cluster_revision| |read
|0x0001|0x003E|t.bitmap32|BatteryAlarmState| 0=no alarm, 1=alarn
|0x0006|0x0000|t.Bool|OnOff| 1=on, 0=off, on endpoint 1 and 2

- Switch valve VA4200ZB VA4201ZB, VA4220ZB, VA4221ZB

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- |---|
|0x0001|0x0020|t.uint8_t|Battery_Voltage| Volt
|0x0001|0x003e|t.bitmap32|BatteryAlarmState| 0=no alarm, 1=alarm
|0x0006|0x0000|t.Bool|OnOff|	1=on, 0=off

- Sensors WL4200 and WL4200S

|Cluster|Attributes|Data type|Fonction |Value|Access
| --- | --- | --- | --- | --- |---|
|0x0402|0x0000|t.uint16_t|MeasuredValueTemperature|	celcius*100	
|0x0500|0x0030|t.uint16_t|ZoneStatus| 0=no leak, 1=leak

# Devices reporting

Device reporting allow device to report any changes that occur on some cluster attributes. If your device was connected to Neviweb before you don't need to activate reporting, except for light and dimmer double tap and long press reporting. If your device is bran new then it should be necessary to implement device reporting. To proceed you can do it by installing ZHA Toolkit (https://github.com/mdeweerd/zha-toolkit) **v0.8.31** or higher, and following example below:

Following are the cluster/attributes set for reproting in Neviweb:

- Thermostat:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- |---|
|Occupancy|0x0003|0x0400|0x10|1|65000|1| 
|local temperature|0x0201|0x0000|0x29|19|300|25| 
|heating demand|0x0201|0x0008|0x0020|11|301|10| 
|occupied heating setpoint|0x0201|0x0012|0x0029|8|302|40| 
|report gfci status|0xFF01|0x0115|0x30|10|3600|1|
|floor limit status|0xFF01|0x010C|0x30|10|3600|1| 

- Light and dimmer

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|onOff|0x0006|0x0000|0x10|0|599|null|
|CurrentLevel|0x0008|0x0000|0x20|3|602|0x01|
|double click|0xff01|0x0054|0x10|0|0|1|

- load control

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|onOff|0x0006|0x0000|0x10|0|600|null|
|ActivePower|0x0B04|0x050B|0x29|60|599|0x64|

- Valve

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|Battery %|(0x0001|0x0020|0x20|60|60*60|1|

- Leak sensors

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|battery percentage|0x0001|0x0021|0x20|30|43200|1| 
|temperature min|0x0402|0x0000|0x29|30|3600|300|  
|battery Alarm State|0x0001|0x003E|0x1b|30|3600|1|

## Light switch and dimmer double tap, long press reporting : 
Sinopé light switches (SW2500ZB), dimmer (DM2500ZB and DM2550ZB) supports single, double and long click, but requires to enable device reporting on attribute 0x0054, cluster 0xff01 to get the action fired in ZHA. To proceed use zha_toolkit services and follow the example bellow : 

The action done on the light switch and dimmer is defined in the cluster: 0xff01 attribut: 0x0054.
|Description|Attribute|Value received|
| --- | --- | --- |
|Single Tap UP|0x0054|2|
|Single Tap DOWN|0x0054|18|
|Double Tap UP|0x0054|4|
|Double Tap DOWN|0x0054|20|
|Long press UP|0x0054|3|
|Long press DOWN|0x0054|19|

### a) create the reporting :
Here is an exemple of how to proceed.
In this exemple : 
- 50:0b:91:40:00:03:db:c2 is your light switch 
- 00:12:4b:00:24:c0:c1:e0 is your Zigbee Coordinator

```
service: zha_toolkit.conf_report
data:
  ieee: 50:0b:91:40:00:03:db:c2
  cluster: 0xff01
  attribute: 0x0054
  manf: 4508
  min_interval: 0
  max_interval: 0
  reportable_change: 1
  tries: 3
  event_success: zha_report_success_trigger_event
  event_fail: zha_report_fail_trigger_event
  event_done: zha_done
```

### b) Specify the bind to your coordinator :
```
service: zha_toolkit.bind_ieee
data:
  ieee: 50:0b:91:40:00:03:db:c2
  command_data: 00:12:4b:00:24:c0:c1:e0
  cluster: 65281
  event_done: zha_done
```

### c) Automation example : 
```
alias: Enable desk light when double tap on light switch
description: ""
trigger:
  - platform: event
    event_type: zha_event
    event_data:
      device_ieee: 50:0b:91:40:00:03:db:c2
      cluster_id: 65281
      args:
        attribute_id: 84
        attribute_name: actionReport
        value: 4
condition: []
action:
  - type: toggle
    device_id: 8b11765575b04f899d9867165fa16069
    entity_id: light.interrupteur_lumiere_bureau_light_2
    domain: light
mode: single
```
For automations you will have acces to those events in the UI for device triggers:
- "Turn on" pressed
- "Turn off" pressed
- "Turn on" double clicked
- "Turn off" double clicked
- "Turn on" continuously pressed
- "Turn off" continuously pressed


# Automation examples:
- Sending outside temperature to thermostats:
- Celcius:
```
- alias: Send-OutdoorTemp
  trigger:
    - platform: state  # send temperature when there are changes
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
- alias: Update outside Temperature
  description: ''
  trigger:
    - platform: time_pattern # send temperature evey 45 minutes
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
You can use either 0xff01 or 65281 in automation. You can send temperature on regular timely basis or when the outside temperature change. Do not pass over 60 minutes or thermostat display will go back to setpoint display. You can change that delay with the outdoor_temp_timeout attribute 0x0011.

- setting the outside temperature sensor:

You can use any temperature source, local or remote.
```
  - platform: template
    sensors:
      local_temp:
        friendly_name: "Outside_temperature"
        value_template: "{{ state_attr('weather.dark_sky', 'temperature') }}"
```

## Buy me a coffee
If you want to make donation as appreciation of my work, you can do so via PayPal. Thank you!
[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/phytoressources/)
