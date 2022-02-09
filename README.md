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
|0xff01| 0x105|Sensor mode|Air: 1, floor: 2
|0xff01|0x119|Connected load|None: 0xffff
|0xff01| 0x118|Aux. connected load| None: 0xffff
|0xff01|0x010a|Floor max temperature| off: -32768, temp: temp*100
|0xff01|0x109|Floor min temperature| off: -32768, temp: temp*100
|0xff01|0x108|Air max temperature|temp: temp*100, valid only if floor mode is selected
|0xff01|0x10b|Sensor type|0: 10k, 1: 12k
|0xff01|0x128|Pump protection| Off: 0xff, On: 0x1
|0xff01|0x114|Time format|12h: 0x1, 24h: 0x0
| --- | --- | --- | ---
|0x0201| 0x401 |Main ouput cycle|Number of second
|0x0201|0x402 |Backlight mode|OnDemand: 0, Always: 1
|0x0201| 0x404|Aux ouput cycle|Number of second
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
|0xff01|0x119|Load connected|None: 0, watt
| --- | --- | --- | ---




