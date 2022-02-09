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
