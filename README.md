# sinope-zha
This is a custom quirks for sinope zigbee devices for testing before it is added to zha-device-handlers. It also explain how to setup those quirks in Home Assistant to use and test them before they are merged in zha-device-handlers.
You can use it as a regular custom_component along with ZHA. On HA start, ZHA will load his quirks and after load the sinope-zha quirks.

# Home assistant configuration:
- in /config directory create a new directory zhaquirks -> /config/zhaquirks
- in configuration.yaml add the following:
```
zha:
  database_path: zigbee.db
  custom_quirks_path: /config/zhaquirks/
```
# Copy the quirks
In /config/zhaquirks copy the four files, light.py, switch.py, thermostat.py and sensor.py then restart Home Assistant

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
- **Thermostats:** (TH1123ZB, TH1123ZB-G2, TH1124ZB,TH1124ZB-G2, TH1300ZB, TH1400ZB, TH1500ZB, TH1134ZB-HC, HP6000ZB-MA, HP6000ZB-HS, HP6000ZB-GE, OTH3600-GA-ZB)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0001|1|t.Bool|unknown|0, 1|read/write/report|
|0xff01|0x0002|2|t.enum8|keypad_lockout|0 = unlocked, 1 = locked, 2 = prevent disconnect|read/write/report|
|0xff01|0x0003|3|t.uint16_t|firmware_number| |read/report|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read/report|
|0xff01|0x0005|5|t.enum8|display_language|0=en, 1=fr|read/write/report|
|0xff01|0x0010|16|t.int16s|outdoor_temp|celsius * 100, -32768=off|read/write/report|
|0xff01|0x0011|17|t.uint16_t|outdoor_temp_timeout| Delay in seconds before reverting to setpoint display if no more outdoor temp is received|read/write/report|
|0xff01|0x0012|18|t.enum8|config_2nd_display| 0 = auto, 1 = setpoint, 2 = outside temperature., 4=room temp|read/write/report|
|0xff01|0x0013|19|t.enum8|weather_icons|0=no weather icon, 1 to 33=weather icon|read/write/report|
|0xff01|0x0020|32|t.uint32_t|secs_since_2k| second since year 2000|read/write/report|
|0xff01|0x0070|112|t.bitmap8|current_load| watt/hr|read/report|
|0xff01|0x0071|113|t.int8s|eco_delta_setpoint| off:-128, celsius*+-10, amount of setpoint reduction/increase for peak and pre-heating|read/write/report|
|0xff01|0x0072|114|t.uint8_t|eco_max_pi_heating_demand| 255:off, range: 0-99 Set pi_heating_demand percentage limit 0% to 99% (225 = 100%)|read/write/report|
|0xff01|0x0073|115|t.uint8_t|eco_safety_temperature_delta| off:255, range: 0-100, set heating restart if room temperature goes x% below setpoint |read/write/report|
|0xff01|0x0075|117|t.bitmap32|unknown testing|0,1,2,3|read/write/report|
|0xff01|0x0080|128|t.uint32_t|unknown|0, 17563653, 17563654, 17563656|read/report|
|0xff01|0x0100|256|t.uint8_t|unknown testing|0, 3|read/report
|0xff01|0x0101|257|Array|unknown|Array(type=AnonymousLVList, value=[6, 0, 1, 5])|read|
|0xff01|0x0102|258|t.uint8_t|unknown|0|read|
|0xff01|0x0103|259|Array|unknown|Array(type=AnonymousLVList, value=[1, 0, 0, 0])|read|
|0xff01|0x0104|260|t.int16s|setpoint|celsius * 100|read/write|
|0xff01|0x0105|261|t.enum8|air_floor_mode|Air: 1, floor: 2|read/write|
|0xff01|0x0106|262|t.enum8|aux_output_mode|0=off,1=15 minutes, 2=15 seconds 3=expantion module|read/write|
|0xff01|0x0107|263|t.int16s|floor_temperature|celsius*100|read|
|0xff01|0x0108|264|t.int16s|air_max_limit|temp: celsius*100, valid only if floor mode is selected|read/write|
|0xff01|0x0109|265|t.int16s|floor_min_setpoint| off: -32768, temp: celsius*100|read/write|
|0xff01|0x010A|266|t.int16s|floor_max_setpoint| off: -32768, temp: celsius*100|read/write|
|0xff01|0x010B|267|t.enum8|floor_sensor_type_param| 0=10k, 1=12k|read/write|
|0xff01|0x010C|268|t.uint8_t|floor_limit_status|0=ok, 1=floorLimitLowReached, 2=floorLimitMaxReached, 3=floorAirLimitMaxReached|read/report|
|0xff01|0x010D|269|t.int16s|room_temperature|celsius*100|read|
|0xff01|0x0114|276|t.enum8|time_format|0=24h, 1=12h|read/write/report|
|0xff01|0x0115|277|t.enum8|gfci_status|0=ok, 1=error|read/report|
|0xff01|0x0116|278|t.enum8|hvac_mode|0=off, 1=auto, 3=cool, 4=heat|read|
|0xff01|0x0117|279|Array|unknown|Array(type=AnonymousLVList, value=[165, 82, 20, 0, 0, 0, 22, 0, 2, 15, 11, 23])|read|
|0xff01|0x0118|280|t.uint16_t|aux_connected_load|watt/hr, 0xffff=off (65535)|read/write|
|0xff01|0x0119|281|t.uint16_t|connected_load|watt/hr|read/write|
|0xff01|0x0128|296|t.uint8_t|pump_protection_status| Off: 0x00, On: 0x01|read/write|
|0xff01|0x012A|298|t.enum8|pump_protection_duration|default:60, 5,10,15,20,30,60|read/write/report|
|0xff01|0x012B|299|t.int16s|current_setpoint|Celsius*100|read/write/report|
|0xff01|0x012C|300|Array|unknown|Array(type=AnonymousLVList, value=[16, 0, 0, 0, 0, 0, 176, 240, 230, 44]) |read|
|0xff01|0x012D|301|t.int16s|report_local_temperature|Celsius*100|read/report|
|0xff01|0x0130|304|t.bitmap8|unknown|2|read/write/report|
|0xff01|0x0134|308|t.int16s|balance_point|-32768=off, default=-1000 (celsius*100)|report/read/write|
|0xff01|0x0135|309|t.int16s|unknown|300|read/write/report|
|0xff01|0x0136|310|t.uint16_t|weather_icons_timeout|10800 sec (3hrs)|read/write/report|
|0xff01|0x0137|311|t.int16s|abs_min_heat_setpoint_limit|500, celsius*100|read/write/report|
|0xff01|0x0138|312|t.bitmap16|unknown|235, 195|read/write/report|
|0xff01|0x0139|313|t.int16s|heat_lockout_temperature|-32768=off, celsius*100|report/read/write|
|0xff01|0x013A|314|t.int16s|cool_lockout_temperature|-32768=off, celsius*100|read/write/report|
|0xff01|0x013B|315|t.bitmab8|unknown|0,4|read/report|
|0xff01|0x0200|512|t.bitmap32|dev_status| 0x00000000|read/report|
|0xff01|0x0202|514|t.enum8|unknown|0,1,2,6|read|
|0xff01|0x0260|608|t.bitmap16|unknown|0, 7967|read/write/report|
|0xff01|0x0261|609|t.bitmap16|unknown|0|read/write/report|
|0xff01|0x0262|610|t.enum8|unknown|0,1|read/write/report|
|0xff01|0x0263|611|t.enum8|unknown|0|read/write/report|
|0xff01|0x0264|612|t.enum8|unknown|0,1|read/write/report|
|0xff01|0x0265|613|t.enum8|unknown|0,1|read/write/report|
|0xff01|0x0266|614|t.enum8|unknown|0|read/write/report|
|0xff01|0x0267|615|t.EUI64|hc_model_mac_addr|None = [255,255,255,255,255,255,255,255], heat/cool model Mac adress|read/write/report|
|0xff01|0x0268|616|t.bitmap8|unknown|0, 2|read/write/report|
|0xff01|0x0269|617|t.bitmap8|unknown|0, 3|read/write/report|
|0xff01|0x026A|618|t.bitmap8|unknown|0, 15|read/write/report|
|0xff01|0x026B|619|t.int16s|min_heat_setpoint_limit|1600|read/write/report|
|0xff01|0x026C|620|t.int16s|max_heat_setpoint_limit|3000|read/write/report|
|0xff01|0x026D|621|t.int16s|min_cool_setpoint_limit|1600|read/write/report|
|0xff01|0x026E|622|t.int16s|max_cool_setpoint_limit|3000|read/write/report|
|0xff01|0x0280|640|t.int16s|unknown|10000|read/write/report|
|0xff01|0x0281|641|t.uint16_t|cycle_length|15 sec or 15 min (900 sec)|read/write/report|
|0xff01|0x0282|642|t.uint16_t|cool_cycle_length|15 sec or 15 min (900 sec)|report/read/write|
|0xff01|0x0283|643|t.enum8|unknown|1|read/report|
|0xff01|0x0284|644|t.uint16_t|unknown|0, 65535=off|read/write/report|
|0xff01|0x0285|645|t.uint8_t|unknown|65|read/write/report|
|0xff01|0x0286|646|t.uint8_t|unknown|100|read/write/report|
|0xff01|0xFF04|65284|t.LVBytes|unknown|"\u0017"|read/report|
|0xff01|0xFF05|65285|t.LVBytes|unknown|"\u0018"|read/report|
|0xff01|0xFF06|65286|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF07|65287|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF08|65288|t.LVBytes|unknown|"3"|read/report|
|0xff01|0xFF09|65289|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF0A|65290|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF0B|65291|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF0C|65292|t.LVBytes|unknown|""|read/report|
|0xff01|0xFF0D|65293|t.LVBytes|unknown|""|report/read|
|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision|0|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0201|0x0000|0|t.int16s|LocalTemperature|celsius*100|read/report|
|0x0201|0x0001|1|t.int16s|outdoor_temperature|celsius*100|read/report|
|0x0201|0x0002|2|t.bitmap8|occupancy|1=occupied, 0=unoccupied|read|
|0x0201|0x0003|3|t.int16s|abs_min_heat_setpoint_limit|celsius*100|read/report|
|0x0201|0x0004|4|t.int16s|abs_max_heat_setpoint_limit|celsius*100|read/report|
|0x0201|0x0008|8|t.uint8_t|PIHeatingDemand|0 -- 100%|read/report|
|0x0201|0x0010|16|t.int8s|local_temperature_calibration|-25 to +25 (+- 2.5oC)|read/write/report|
|0x0201|0x0011|17|t.int16s|occupied_cooling_setpoint|celsius*100|read/write/report|
|0x0201|0x0012|18|t.int16s|occupied_heating_setpoint|celsius*100|read/write/report|
|0x0201|0x0013|19|t.int16s|unoccupied_cooling_setpoint|celsius*100|read/write|
|0x0201|0x0014|20|t.int16s|unoccupied_heating_setpoint|celsius*100|read/write|
|0x0201|0x0015|21|t.int16s|MinHeating Setpoint|celsius*100|read/write|
|0x0201|0x0016|22|t.int16s|MaxHeating Setpoint|celsius*100|read/write|
|0x0201|0x0017|23|t.int16s|min_cool_setpoint_limit|celsius*100|read/write/report|
|0x0201|0x0018|24|t.int16s|max_cool_setpoint_limit|celsius*100|read/write/report|
|0x0201|0x001B|27|t.enum8|ctrl_sequence_of_oper|2, 4|read/write/report|
|0x0201|0x001C|28|t.enum8|SystemMode|0=off, 1=auto, 3=cool, 4=heat, 7=fan only, 8=dry|read/write|
|0x0201|0x001E|30|t.enum8|running_mode|0=off, 3=cool, 4=heat|read/report|
|0x0201|0x0400|1024|t.enum8|SetOccupancy| Home: 0, away:1|read/write|
|0x0201|0x0401|1025|t.uint16_t|main_cycle_output| Number of second, 15: '15_sec', 300: '5_min', 600: '10_min', 900: '15_min', 1200: '20_min', 1800: '30_min', 65535: 'off'|read/write|
|0x0201|0x0402|1026|t.enum8|backlight_auto_dim_param| On_demand: 0, Always_on: 1, Bedroom: 2|read/write|
|0x0201|0x0404|1028|t.uint16_t|aux_cycle_output| Number of second, 15: '15_sec', 300: '5_min', 600: '10_min', 900: '15_min', 1200: '20_min', 1800: '30_min', 65535: 'off'|read/write|
|0x0201|0x0437|1079|t.uint16_t|unknown|100|read/write/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0202|0x0000|0|t.enum8|fan_mode|0=off,1=low,2=medium,3=high,4=on,5=auto,6=smart (auto),6|read/write/report|
|0x0202|0x0001|1|t.enum8|fan_mode_sequence|0=(Low_Med_High),1=Low_High),2 (Low_Med_High_Auto),3=(Low_High_Auto),4=(On_Auto)|read/write/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0b04|0x050b|1291|t.uint16_t|Active_Power|watt/hr|read/write/report|
|0x0b04|0x050d|1293|t.uint16_t|active_power_max|watt/hr|read|
|0x0b04|0x050f|1295|t.uint16_t|Apparent_Power|watt/hr|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0204|0x0000|0|t.enum8|TemperatureDisplayMode|0=celsius, 1=farenheight|read/write|
|0x0204|0x0001|1|t.enum8|keypadLockout|0=no lock, 1=lock|read/write|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.int16s|measured_value|celsius*100|read/write/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered|watt/hr	|read/report|
|0x0702|0x0200|512|t.bitmap8|status|0=ok|read/report|

- **lights and dimmer**: (SW2500ZB, SW2500ZB-G2, DM2500ZB, DM2500ZB-G2, DM2550ZB, DM2550ZB-G2)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0001|1|t.bool|Unknown|0, 1|read/write|
|0xff01|0x0002|2|t.enum8|KeypadLock| Locked: 1, Unlocked: 0|read/write|
|0xff01|0x0003|3|t.uint16_t|firmware_number| |read|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read|
|0xff01|0x0010|16|t.int16s|on_intensity|minIntensity - 3000|read/write|
|0xff01|0x0012|18|t.enum8|Unknown|0, 1|read/write|
|0xff01|0x0013|19|t.enum8|unknown|0, 1, 2|read/write|
|0xff01|0x0050|80|t.uint24_t|onLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue|read/write|
|0xff01|0x0051|81|t.uint24_t|offLedColor| 0x0affdc - Lim, 0x000a4b - Amber, 0x0100a5 - Fushia, 0x64ffff - Perle, 0xffff00 - Blue|read/write|
|0xff01|0x0052|82|t.uint8_t|onLedIntensity| Percent|read/write|
|0xff01|0x0053|83|t.uint8_t|offLedIntensity| Percent|read/write|
|0xff01|0x0054|84|t.enum8|actionReport| singleTapUp: 2, doubleTapUp: 4, singleTapDown: 18, doubleTapDown: 20|read/repport|
|0xff01|0x0055|85|t.uint16_t|minIntensity| 0 to 3000|read/write|
|0xff01|0x0056|86|t.enum8|phase_control|0=forward, 1=reverse|read/write|
|0xff01|0x0058|88|t.enum8|double_up_full|0=off, 1=on|read/write|
|0xff01|0x0080|128|t.uint32_t|Unknown|16908288|read|
|0xff01|0x0090|144|t.uint32_t|currentSummationDelivered|watt/hr|read/report|
|0xff01|0x00A0|160|t.uint32_t|Timer|Time, 1 to 10800 seconds|read/write|
|0xff01|0x00A1|161|t.uint32_t|Timer_countdown|Seconds remaining on timer|read|
|0xff01|0x0119|281|t.uint16_t|ConnectedLoad| None: 0, watt|read/write|
|0xff01|0x0200|512|t.bitmap32|dev_status| 0x00000000| report/read|
|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision|1|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered| Sum of delivered watt/hr|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff| 1=on, 0=off|report/read/write|
| --- | --- | --- | --- | --- | --- | ---|
|0x0008|0x0000|0|t.uint8_t|CurrentLevel| 0=0%, 254=100%|read/report|
|0x0008|0x0011|17|t.uint8_t|OnLevel| 0=0%, 254=100%|read/write|

- **Switch**: (SP2600ZB, SP2610ZB)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read|
|0xff01|0x0220|544|t.bitmap16|Unknown|0|report/read/write|
|0xff01|0x0221|545|t.bitmap16|Unknown|1|report/read|
|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision| |read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered|watt/hr|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0b04|0x050B|1291|t.uint16_t|Active_Power|watt/hr|read/report|
|0x0b04|0x0604|1540|t.uint16_t|ACPowerMultiplier|1|read|
|0x0b04|0x0605|1541|t.uint16_t|ACPowerDivisor|10|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff| 0=off, 1=on|report/read|

- **Load Controller**: (RM3250ZB)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0001|1|t.bool|unknown|0, 1|read/write|
|0xff01|0x0002|2|t.enum8|keypadLockout|0 = unlocked, 1 = locked|read/write|
|0xff01|0x0003|3|t.uint16_t|firmware_number|378|read|
|0xff01|0x0004|4|t.CharacterString|firmware_version|378|read|
|0xff01|0x0060|96|t.uint16_t|ConnectedLoad|	watt/hr|read|
|0xff01|0x0070|112|t.bitmap8|CurrentLoad|watt/hr|read/report|
|0xff01|0x0074|116|t.enum8|Unknown|0, 1,255=undefined|read/write|
|0xff01|0x0080|128|t.uint32_t|Unknown| |read|
|0xff01|0x0090|144|t.uint32_t|currentSummationDelivered|watt/hr|read/report|
|0xff01|0x00A0|160|t.uint32_t|Timer| Time, 1 to 86400 seconds|read/write|
|0xff01|0x00A1|161|t.uint32_t|Timer_countDown| Seconds remaining on timer|read|
|0xff01|0x0200|512|t.bitmap32|dev_status| 0x00000000 |read/report|
|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision| |read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff|	1=on, 0=off|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0b04|0x050B|1291|t.uint16_t|Active_Power|watt/hr|read/report|
|0x0b04|0x0505|1285|t.uint16_t|rms_voltage|volt|read/report|
|0x0b04|0x0605|1541|t.uint16_t|AC_Power_Divisor|1|read|
|0x0b04|0x0604|1540|t.uint16_t|AC_Power_Multiplier|1|read|
|0x0b04|0x0605|1541|t.uint16_t|AC_Power_Divisor|1|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered|watt/hr|read/report|

- **Calypso**: (RM3500ZB)  water tank controller

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0001|1|t.Bool|Unknown|0, 1|read/write/report|
|0xff01|0x0002|2|t.enum8|keypadLockout|0 = unlocked, 1 = locked|read/write/report|
|0xff01|0x0003|3|t.uint16_t|firmware_number|378|read/report|
|0xff01|0x0004|4|t.CharacterString|firmware_version|378|read/report|
|0xff01|0x0010|16|t.int16s|unknown|400| |
|0xff01|0x0013|19|t.enum8|unknown|1,2,3,4,16,21|read/write|
|0xff01|0x0035|53|t.uint16_t|unknown|0,22|read/report|
|0xff01|0x0037|55|t.uint16_t|unknown|744, 1000|read/write/report|
|0xff01|0x0038|56|t.enum8|unknown|0, 2|read/report|
|0xff01|0x0060|96|t.uint16_t|ConnectedLoad|watt/hr|read|
|0xff01|0x0070|112|t.bitmap8|CurrentLoad|watt/hr|read/report|
|0xff01|0x0074|116|t.enum8|unknown|0,1,255|read/write/report|
|0xff01|0x0076|118|t.uint8_t|drConfigWaterTempMin|0=off, 45 to 55 celsius|read/write/report|
|0xff01|0x0077|119|t.uint8_t|drConfigWaterTempTime|2|read/write/report|
|0xff01|0x0078|120|t.uint16_t|drWTTimeOn|240|read/write/report|
|0xff01|0x0079|121|t.bitmap8|unknown| 0|report/read|
|0xff01|0x007A|122|t.uint16_t|unknown|0|read/write/report|
|0xff01|0x007B|123|t.uint16_t|unknown|288|read/write/report|
|0xff01|0x007C|124|t.int16s|min_measured_temp|water temp celsius*100|read/report|
|0xff01|0x007D|125|t.int16s|max_measured_temp|water temp celsius*100|read/report|
|0xff01|0x007E|126|t.enum8|water_temp_protection_type|0,1|read/write/report|
|0xff01|0c0080|128|t.uint32_t|unknown|0|read/report|
|0xff01|0x0090|144|t.uint32_t|CurrentSummationDelivered|kwh|read/report|
|0xff01|0x00A0|160|t.uint32_t|Timer| Time, 1 to 86400 seconds|read/write/report|
|0xff01|0x00A1|161|t.uint32_t|Timer_countDown| Seconds remaining on timer|read/report|
|0xff01|0x00B0|176|t.Bool|unknown|0,1|read/report|
|0xff01|0x0101|257|t.LVList| |read/report|
|0xff01|0x012A|298|t.enum8|unknown|60|read/write/report|
|0xff01|0x012C|300|t.LVList|unknown|  |read/report|
|0xff01|0x0200|512|t.bitmap32|dev_status| ok=0x00000000, leak cable disconnected=0x00000040, temperature sensor disconnected=0x00000020|read/report|
|0xff01|0x0202|514|t.enum8|unknown|1|read/report|
|0xff01|0x0203|515|t.enum8|unknown|12|read/report|
|0xff01|0x0280|640|t.int16s|max_measured_value|5300, 10000|read/write/report|
|0xff01|0x0281|641|t.uint16_t|unknown|0|read/write/report|
|0xff01|0x0282|642|t.uint16_t|unknown|0|read/write/report|
|0xff01|0x0283|643|t.uint8_t|ColdLoadPickupStatus| 1, 2|read/report|
|0xff01|0x0284|644|t.uint16_t|coldLoadPickupRemainingTime|65535=off countdown| |
|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision| |read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0500|0x0002|2|t.uint16_t|ZoneStatus|48=no leak, 49=temp sensor disconnected, 50=leak sensor disconnected|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff|1=on, 0=off|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0b04|0x050B|1291|t.uint16_t|Active_Power|watt/hr|read/report|
|0x0b04|0x0505|1285|t.uint16_t|rms_voltage|volt|read/report|
|0x0b04|0x0605|1541|t.uint16_t|AC_Power_Divisor|1|read|
|0x0b04|0x0604|1540|t.uint16_t|AC_Power_Multiplier|1|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0b05|0x011d|285|t.int8s|Rssi| value -45||read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.int16s|WaterTemperature| temp oC||read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered|Watt/hr|read/report|

- **multi controller**: (MC3100ZB) 

|Endpoint|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x0001|0x0020|32|t.uint8_t|Battery_Voltage| Volt*10|read/report|
|1|0x0001|0x003e|62|t.bitmap32|BatteryAlarmState| 0=no alarm, 1=alarm|read/report|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0xff01|0x0070|112|t.bitmap8|current_load|0-24 Wh|read/report|
|1|0xff01|0x0074|116|t.enum8|Unknown|0,1,255=undefined|read/write/report|
|1|0xff01|0x00A0|160|t.uint32_t|Timer|Time, 1 to 10800 seconds|read/write|
|2|0xff01|0x00A0|160|t.uint32_t|Timer2|Time, 1 to 10800 seconds|read/write|
|1|0xff01|0x0200|512|t.bitmap32|dev_status|0|read/report|
|1|0xff01|0x02A0|672|t.uint32_t|input_on_delay|seconds, 0=off, 0 to 10800|read/write|
|1|0xff01|0x02A1|673|t.uint32_t|input_off_delay|seconds, 0=off, 0 to 10800|read/write|
|2|0xff01|0x02A0|672|t.uint32_t|input_on_delay|seconds, 0=off, 0 to 10800|read/write|
|2|0xff01|0x02A1|673|t.uint32_t|input_off_delay|seconds, 0=off, 0 to 10800|read/write|
|1|0xff01|0x00B0|175|t,Bool|Unknown|0,1|read/report|
|1|0xff01|0xFFFD|65533|t.uint16_t|cluster_revision| |report/read|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x0006|0x0000|0|t.Bool|OnOff|1=on, 0=off|read/report|
|2|0x0006|0x0000|0|t.Bool|OnOff2|1=on, 0=off|read/report|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x0402|0x0000|0|t.int16s|Measured value, indoor temperature|celsius*100|read/report|
|2|0x0402|0x0000|0|t.int16s|Measured value, outside temperature|celsius*100|read/report|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x0405|0x0000|0|t.uint16_t|measured value, relative humidity|%|read/report|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x0B05|0x011D|285|t.int8s|rssi|-45|read/report|
| --- | --- | --- | --- | --- | --- | --- | ---|
|1|0x000F|0x0055|85|t.Bool|present_value|true=1, false=0|read/write/report|
|2|0x000F|0x0055|85|t.Bool|present_value|true=1, false=0|read/write/report|
|1|0x000F|0x006F|111|t.bitmap8|status-flag|0x00=false, 0x01=true|read/report|
|2|0x000F|0x006F|111|t.bitmap8|status-flag|0x00=false, 0x01=true|read/report|

- **Valve**: VA4200WZ, VA4201WZ, VA4200ZB VA4201ZB, VA4220ZB, VA4221ZB

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0x0001|0x0020|32|t.uint8_t|Battery_Voltage|Volt*10|read/report|
|0x0001|0x0021|33|t.uint8_t|Battery_percentage_remaining|%|read/report|
|0x0001|0x003e|62|t.bitmap32|BatteryAlarmState| 0=no alarm, 1=alarm, 15=no battery|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0200|512|t.bitmap32|dev_status/alarm| 0x00000000|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff|1=on, 0=off|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.uint16_t|MeasuredValue, Temperature|celsius*100|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|CurrentSummationDelivered|	L/h (see below)|read/report|
|0x0702|0x0200|512|t.bitmap8|status|0=off, 1=off/armed, 2=on|read|
|0x0702|0x0300|768|t.enum8|unit_of_measure| 7=L/h|read|
|0x0702|0x0306|774|t.bitmap8|metering_device_type|2  = Water Metering|read|

- **Valve G2**: (VA4220ZB G2, VA4221ZB G2) with flow meter

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0x0000|0x0007|7|t.enum8|power_source|129,130=mains, 3=battery, 4=dc|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0001|0x0020|32|t.uint8_t|Battery_Voltage|Volt*10|read/report|
|0x0001|0x0021|33|t.uint8_t|Battery_percentage_remaining|%|read/report|
|0x0001|0x003e|62|t.bitmap32|BatteryAlarmState| 0=no alarm, 1=alarm, 15=no battery|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0008|0x0000|0|t.uint8_t|Current_level|From 0 to 254|read/report|
|0x0008|0x0011|17|t.uint8_t|On_level|0=off, 1 to 255 valve openning value limit|read/write|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0101|257|Array|unknown|Array(type=AnonymousLVList, value=[0, 3, 3, 2])|read|
|0xff01|0x0200|512|t.bitmap32|dev_status| 0x00000000|read/report|
|0xff01|0x0230|560|t.enum8|alarm_flow_threshold|0=off,1=on|read/write|
|0xff01|0x0231|561|t.enum8|alarm_options|0=nothing,1=alarm,2=close,3=close and alarm,4=no flowmeter|read|
|0xff01|0x0240|576|Array|flow_meter_config|12 elements (uint8)|read/write|
| | | | | |no flow meter = Array(type=AnonymousLVList, value=[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]) | |
| | | | | |FS4220 = Array(type=AnonymousLVList, value=[194, 17, 0, 0, 136, 119, 0, 0, 1, 0, 0, 0]) | |
| | | | | |FS4221 = Array(type=AnonymousLVList, value=[159, 38, 0, 0, 76, 85, 1, 0, 1, 0, 0, 0]) | |
| | | | | |FS4222 = Array(type=AnonymousLVList, value=[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]) | |
|0xff01|0x0241|577|t.uint32_t|alarm_disable_countdown|0 = off, 1 to 86400 seconds (up to 24 hrs)|read/write|
|0xff01|0x0250|592|t.uint32_t|power_source|0x0001d4c0 (120000)= DC power, 0x00000001 (1)=ACUPS, 0x00000000 (0)=Battery|read/write|
|0xff01|0x0251|593|t.uint32_t|emergency_power_source|0x0000003c (60)=battery + ACUPS, 0x00000001=ACUPS, 0x00000000=battery|read/write|
|0xff01|0x0252|594|t.uint32_t|abnormal_flow_duration|seconds ,900 (15 min) to 86400 (24hr)|read/write|
|0xff01|0x0253|595|t.bitmap16|abnormal_flow_action|0x0000= do nothing, 0x0001=send alert, 0x0003= close and send alert|read/write|
| --- | --- | --- | --- | --- | --- | ---|
|0x0006|0x0000|0|t.Bool|OnOff|1=on, 0=off|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.uint16_t|MeasuredValue, Temperature|celsius|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0404|0x0000|0|t.uint16_t|MeasuredValue, flowrate|L/hr|read/report|
|0x0404|0x0001|1|t.uint16_t|min_measured_value|0|read|
|0x0404|0x0002|2|t.uint16_t|max_measured_value|?|read|
|0x0404|0x0003|3|t.uint16_t|tolerance|?|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0500|0x0000|0|t.enum8|zone_state|1=enrolled, 0=not enrolled|read|
|0x0500|0x0002|2|t.bitmap16|zone_status|48=ok, 50=flow meter disconnected, 56=low battery, 58=flow and low batt|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0702|0x0000|0|t.uint48_t|flowVolumeDelivered|L/h|report/read|
|0x0702|0x0200|512|t.bitmap8|status|0=off, 1=off/armed, 2=on|read|
|0x0702|0x0300|768|t.enum8|unit_of_measure|7=L/h|read|
|0x0702|0x0301|769|t.uint24_t|multiplier|1|read|
|0x0702|0x0302|770|t.uint24_t|divisor|1000|read|
|0x0702|0x0306|774|t.bitmap8|metering_device_type|2 = Water Metering|read|
|0x0702|0x0400|1024|t.int24s|instantaneous_demand|0|report/read|

- **Leak Sensors**: (WL4200, WL4200S, WL4200C)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0003|3|t.uint16_t|firmware_number| |read|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read|
|0xff01|0x0030|48|t.uint8_t|unknown|0|read/write|
|0xff01|0x0031|49|t.uint16_t|unknown|696, 774, 1000|read/write|
|0xff01|0x0032|50|t.int16s|min_temperature_limit|300, celsius*100|read/write|
|0xff01|0x0033|51|t.int16s|max_temperature_limit|5000, celsius*100|read/write|
|0xff01|0x0034|52|t.bitmap8|device_status|0|read/report|
|0xff01|0x0035|53|t.uint16_t|sensor_status|24-29=unknown, 31-35 = probe disconnected, 71-78= ok, 79=min temp alert, 81=max temp alert,133=unknown alert|read|
|0xff01|0x0036|54|t.uint16_t|battery_type|7|read/write|
|0xff01|0x0080|128|t.uint32_t|unknown|16973824|read/report|
|0xff01|0xfffd|65533|t.uint16_t|cluster_revision|1|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0001|0x0020|32|t.uint8_t|Battery_voltage|voltage * 10|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.uint16_t|MeasuredValue, Temperature|celsius * 100|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0500|0x0002|2|t.bitmap16|zone_status|48=ok, 49=Leak_detected, 50=Probe_disconected, 51=leak_and_probe, 56=Low_battery, 58=Connector_low_bat|read/report|
|0x0500|0x0030|48|t.uint16_t|leak_alarm| 0=no leak, 1=leak|read|


- **Leak Sensors**: (WL4210)

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0003|3|t.uint16_t|firmware_number| |read/report|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read/report|
|0xff01|0x0030|48|t.uint8_t|unknown|0|read/write/report|
|0xff01|0x0031|49|t.uint16_t|unknown|696, 774, 1000|read/write/report|
|0xff01|0x0032|50|t.int16s|min_temperature_limit|300, celsius*100|read/write|
|0xff01|0x0033|51|t.int16s|max_temperature_limit|5000, celsius*100|read/write|
|0xff01|0x0034|52|t.bitmap8|device_status|0|read/report|
|0xff01|0x0035|53|t.uint16_t|sensor_status|14= ?, 24-29=unknown, 31-35 = probe disconnected, 71-78= ok, 79=min temp alert, 81=max temp alert,133=unknown alert|read/report|
|0xff01|0x0036|54|t.uint16_t|battery_type|7=|read/write/report|
|0xff01|0x0037|55|t.uint16_t|unknown|1000|read/write/report|
|0xff01|0x0038|56|t.enum8|probe_connected|0=disconected, 1=connected|read/report|
|0xff01|0x0039|57|t.enum8|probe_type|0=internal, 1=external_probe|read/write/report|
|0xff01|0x0080|128|t.uint32_t|unknown|16973824|read/report|
|0xff01|0x0200|512|t.bitmap32|dev_status|0x00000000|read/report|
|0xff01|0x020A|522|t.uint32_t|unknown|0|read/report|
|0xff01|0xfffd|65533|t.uint16_t|cluster_revision|1|read|
| --- | --- | --- | --- | --- | --- | ---|
|0x0001|0x0020|32|t.uint8_t|Battery_voltage|voltage * 10|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.uint16_t|MeasuredValue, Temperature|celsius * 100|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0500|0x0002|2|t.bitmap16|zone_status|48=ok, 49=Leak_detected, 50=Probe_disconected, 51=leak_and_probe, 56=Low_battery, 58=Connector_low_bat|read/report|
|0x0500|0x0030|48|t.uint16_t|leak_alarm| 0=no leak, 1=leak|read|

- **Tank level monitor**: (LM4110-ZB) 

|Cluster|Attributes|Atribute decimal|Data type|Fonction |Value|Access|
| --- | --- | --- | --- | --- | --- | ---|
|0x0001|0x0020|32|t.uint8_t|battery voltage|54, volt*10|read/report|
|0x0001|0x0021|33|t.uint8_t|remaining battey percentage|%|read/report|
|0x0001|0x003e|62|t.bitmap32|battery_alarm_state|0=ok, 1=weak battery|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x0402|0x0000|0|t.int16s|MeasuredValue, device Temperature|celsius * 100|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0x000c|0x0055|85|t.uint16_t|Present value, angle| angle of the gauge needle in degree|read/report|
| --- | --- | --- | --- | --- | --- | ---|
|0xff01|0x0003|3|t.uint16_t|firmware_number| |read|
|0xff01|0x0004|4|t.CharacterString|firmware_version| |read|
|0xff01|0x0030|48|t.uint8_t|Unknown|60|report/read/write|
|0xff01|0x0080|128|t.uint32_t|Unknown|0|read/report|
|0xff01|0x0200|512|t.bitmap32|dev_status| 0x00000000| read/report|
|0xff01|0xfffd|65533|t.uint16_t|cluster_revision| |report/read|

Propane level is reported as gauge needle angle cluster 0x000c, attribute 0x0055. There is no % value. In neviweb this is calculated depending on gauge type 5-95 or 10-80. If you need to set an alarm at 20% tank capacity then target angle 182 for 5-95 and 10-80 gauge. For 30% value 5-95 = 221 and 10-80 = 216. 

# Devices reporting

Device reporting allow device to report any changes that occur on some cluster attributes. If your device was connected to Neviweb before you don't need to activate reporting, except for light and dimmer double tap and long press reporting. If your device is bran new then it should be necessary to implement device reporting. To proceed you can do it by installing ZHA Toolkit (https://github.com/mdeweerd/zha-toolkit) **v0.8.31** or higher, and following example below:

Following are the cluster/attributes set for reproting in Neviweb:

- Thermostat:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- |---| --- |
|Occupancy|0x0003|0x0400|0x10|1|65000|1| 
|local temperature|0x0201|0x0000|0x29|19|300|25| 
|heating demand|0x0201|0x0008|0x0020|11|301|10| 
|occupied heating setpoint|0x0201|0x0012|0x0029|8|302|40| 
|report gfci status|0xFF01|0x0115|0x30|10|3600|1|
|floor limit status|0xFF01|0x010C|0x30|10|3600|1| 

- Light and dimmer:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|onOff|0x0006|0x0000|0x10|0|599|null|
|CurrentLevel|0x0008|0x0000|0x20|3|602|0x01|
|double click|0xff01|0x0054|0x10|0|0|1|

- load control RM3250ZB:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|onOff|0x0006|0x0000|0x10|0|600|null|
|ActivePower|0x0B04|0x050B|0x29|60|599|0x64|
|Energy reading |0x0702|0x0000|0x29|59|1799|int|

- Valve:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|Battery %|(0x0001|0x0020|0x20|60|3600|1|
|on/off|0x0006|0x0000|0x10|0|600|null|
|Flowrate|0x0404|0x0000|T.uint16_t|30|600|flow change|
|water volume|0x0702|0x0000|t.uint48_t|59|1799|volume change|

- Leak sensors:

|Data|Cluster|Attribute|format|min time|max time|minimum change|
| --- | --- | --- | --- | --- | --- | --- |
|battery percentage|0x0001|0x0021|0x20|30|43200|1| 
|temperature min|0x0402|0x0000|0x29|30|3600|300|  
|battery Alarm State|0x0001|0x003E|0x1b|30|3600|1|

- Tank monitor LM4110-ZB:

|Data|Cluster|Attribute|format|min time|max time|minimum change|Note|
| --- | --- | --- | --- | --- | --- | --- | ---|
|status|0x0001|0x003e|0x1b|60|43688|1| 
|remaining battey percentage|0x0001|0x0021|0x20|0|65535|1|
|battery voltage|0x0001|0x0020|0x20|60|43646|1|
|battery alarm|0x003E|0x1B|60|43688|1|
|present value, angle|0x000c|0x0055|0x39|5|3666|1|Value of -2 = probe disconected
|device temperature|0x0402|0x0000|0x29|60|3678|1|(only if temperature goes below 5oC)

- Calypso RM3500ZB:

|Data|Cluster|Attribute|format|min time|max time|minimum change|Note|
| --- | --- | --- | --- | --- | --- | --- | ---|
|water temperature|0x0402|0x0000|0x29|30|580|100|
|Water leak sensor state|0x0500|0x0002|0x19|0|
|Heater On/off|0x0006|0x0000|0x10|0|600|null|
|ActivePower|0x0B04|0x050B|0x29|30|600|0x64|
|Energy reading|0x0702|0x0000|0x29|299|1799|int|
|Safety water temp reporting|0xFF01|0x0076|DataType.UINT8|0|86400|null|

- TH1134ZB-HC

|Data|Cluster|Attribute|format|min time|max time|minimum change|Note|
| --- | --- | --- | --- | --- | --- | --- | ---|
|OccupiedHeatingSetpoint|0x0201|0x0012| |10|21726| |null|
|OccupiedCoolingSetpoint|0x0201|0x0011| |10|22035| |null|
|PiHeatingDemand|0x0201|0x0008| |10|3976| |null|
|SystemMode|0x0201|0x001C| |5|1800| |null|
|LocalTemperature|0x0201|0x0000| |0|65535| |null|
|fan mode|0x0202|0x0000| |5|0| |null|
|ReportLocalTemperature|0xff01|0x012D| |10|4055| |null|
| |0xff01|0x0262| |5|0| |null|
| |0xff01|0x0263| |5|0| |null|
|current_load|0xff01|0x0070| |10|43268| |null|
|status|0xff01|0x0200| |10|0| |null|
|hc_model_mac_addr|0xff01|0x0267| |5|64800| |null|
| |0xff01|0x013B| |0|65535| |null|

# Setting the flow meter model for your VA422xZB valve 2n gen.
To add your flow meter to your valve, you need to use the service ZHA Toolkit: Write Attribute. The data to set the flow meter is written in an attr_type array. The command is different for each type of flow meter: (It is possible that ZHA will throw an error for the read_after_write portion but the attribut will be updated correctly).
- FS4220: (3/4 inch)
```
service: zha_toolkit.attr_write
data:
  ieee: 50:0b:91:40:00:03:ed:b0 <-- your valve ieee
  endpoint: 1
  cluster: 0xff01
  attribute: 0x0240
  attr_type: 0x48
  attr_val: [32, 12, 0, 194, 17, 0, 0, 136, 119, 0, 0, 1, 0, 0, 0]
  read_before_write: false
  read_after_write: true
```
- FS4221: (one inch)
```
service: zha_toolkit.attr_write
data:
  ieee: 50:0b:91:40:00:03:ed:b0 <-- your valve ieee
  endpoint: 1
  cluster: 0xff01
  attribute: 0x0240
  attr_type: 0x48
  attr_val: [32, 12, 0, 159, 38, 0, 0, 76, 85, 1, 0, 1, 0, 0, 0]
  read_before_write: false
  read_after_write: true
```
- FS4222: (1.5 inch)
```
service: zha_toolkit.attr_write
data:
  ieee: 50:0b:91:40:00:03:ed:b0 <-- your valve ieee
  endpoint: 1
  cluster: 0xff01
  attribute: 0x0240
  attr_type: 0x48
  attr_val: [32, 12, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
  read_before_write: false
  read_after_write: true
```
- No flow meter:
```
service: zha_toolkit.attr_write
data:
  ieee: 50:0b:91:40:00:03:ed:b0 <-- your valve ieee
  endpoint: 1
  cluster: 0xff01
  attribute: 0x0240
  attr_type: 0x48
  attr_val: [32, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
  read_before_write: false
  read_after_write: true
```

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
triggers:
  - trigger: event
    event_type: zha_event
    event_data:
      device_ieee: 50:0b:91:40:00:03:db:c2
      cluster_id: 65281
      args:
        attribute_id: 84
        attribute_name: action_report
        value: 4
condition: []
actions:
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

# LM4110-ZB setup for angle and level % reporting :
This sensor is a sleepy device. That mean the device is sleeping and wake up at specific interval to report his state. When it is sleeping it is impossible to reach hit.
We can't send any command to that devive except when it is awake.
To be able to configure the device you need to install ZHA-TOOLKIT component. This will allow to do all operations to setup the device.

the steps to configure your LM4110-ZB sensor is as follow:

### setup reporting:

```
service: zha_toolkit.execute
data:
  ieee: «your LM4110 ieee »
  command: conf_report
  endpoint: 1
  cluster: 0x000c
  attribute: 0x0055
  min_interval: 5
  max_interval: 3757
  reportable_change: 1
  tries: 100
  event_done: zha_done
```

Check your log until you get :

'success': True, 'result_conf': [[ConfigureReportingResponseRecord(status=0)]]

zha-toolkit will submit the command until it reach 100 retry or zha_done event.

### bind reporting:

Once you have it correctly, you need to bind your LM410ZB to your
zigbee gateway so the report is sent to the correct place:

```
service: zha_toolkit.bind_ieee
data:
  ieee: «your LM4110 ieee »
  command_data: «your zigbee gateway ieee »
  cluster: 0x000c
  endpoint: 1
  dst_endpoint: 1
  tries: 100
  event_done: zha_done
```

service: zha_toolkit.execute can be replaced by service: zha_toolkit.conf_report. In that case remove the «command: conf_report line».
The most important is to retry many time to catch the moment the LM4110 is awake.

### setup automation to catch angle reporting:

To get the angle value you can try this method:

```
- platform: sql
  db_url: sqlite:////config/zigbee.db
  scan_interval: 10
  queries:
    - name: current_angle
      query: "SELECT value FROM attributes_cache_v7 where ieee = 'your LM4110 ieee' and cluster = 12 and attrid = 85"
      column: "value"
```

or you can use this method if you don't want to setup the sql platform:

```
service: zha_toolkit.execute
data:
  command: attr_read
  ieee: «your LM4110 ieee »
  cluster: 0x000c
  attribute: 0x0055
  state_id: sensor.current_angle
  allow_create: True
  tries: 100
```

This automation will create the sensor.current_angle or any other name you want.

```
- id: '1692841759194'
  alias: Lecture niveau propane
  description: Lecture du niveau de réservoir à chaque heure
  triggers:
    - trigger: time_pattern
      hours: "/1"
  condition: []
  actions:
    action:
      - service: zha_toolkit.execute
        data:
          command: attr_read
          ieee: "«your LM4110 ieee »"
          cluster: 12
          attribute: 85
          state_id: sensor.current_angle
          allow_create: true
          tries: 100
  mode: single
```

### Do the calculation to transfert angle to % level:
There are two different tank gauge, scale from 10 to 80 (R3D 10-80) or scale from 5 to 95 (R3D 5-95). Calculation is different for each one.

- First set gauge type and value offset. For this you need to create input_number and input_text to set those value in <b>configuration.yaml</b>
```
input_number:
  gauge_offset:
    name: "gauge offset"
    initial: 2
    min: 1
    max: 4
    step: 1
```

```
input_text:
  tank_gauge:
    name: "tank gauge"
    initial: "10-80" # or "5-95"
```
- Calculates propane tank % level according to value returned by Sinope device (for R3D 10-80 gauge or R3D 5-95 gauge)
```
template:
  - triggers:
      - trigger: time_pattern
        hours: "/5"
  - sensor:
      - name: "Tank remaining level"
        unit_of_measurement: "%"
        unique_id: sensor.tank_remaining_level
        icon: mdi:propane-tank
        state_class: measurement
        state: >
          {% set gauge = states('input_text.tank_gauge') %} # must match the above input_text name
          {% set angle = states('sensor.current_angle') | float %}
          {% set offset = states('input_number.gauge_offset') | float %} # must match the above input_number name
          {% if (gauge == "10-80") %}
            {% set x_min = 110 | float %}
            {% set x_max = 406 | float %}
            {% set delta = 46 | float %}
            {% set low = 10 | float %}
            {% set high = 80 | float %}
          {% else %}
            {% set x_min = 120 | float %}
            {% set x_max = 415 | float %}
            {% set delta = 56 | float %} #could be 55 or 56, change value if % level is not accurate
            {% set low = 5 | float %}
            {% set high = 95 | float %}
          {% endif %}

          {% if ((delta <= angle) and (70 >= angle)) %}
            {{ (((delta-x_min)/(x_max-x_min)*(high-low))+low+offset) | round(0) }}
          {% elif ((0 <= angle) and (delta > angle)) %}
            {{ (((angle)+360-x_min)/(x_max-x_min)*(high-low)+low+offset) | round(0) }}
          {% else %}
            {{ (((angle)-x_min)/(x_max-x_min)*(high-low)+low+offset) | round(0) }}
          {% endif %}
```

# Automation examples:

In this section we include various examples of automations availables via blueprints you can use in HA.
The blueprints are located in automation/blueprints subdirectory. You need to copy them to HA config/blueprints/automation/sinope-zha. 
If the directory does not exists just create it. Then all automations blueprints will be availables via Parameters / automations and scenes / Blueprints tab. 
Follow the instructions to create your automations.

Availables automations are availables there:
![blueprints](automation/blueprints)

- send_outdoor_temperature:
  - Celsius: ![send temperature celcius](automation/blueprints/send_outdoor_temperature.yaml)
  - Farenheight: ![send temperature farenheight](automation/blueprints/send_outdoor_farenheight_temperature.yaml)

You can use either 0xff01 or 65281 in automation. You can send temperature on regular timely basis or when the outside temperature change. Do not pass over 60 minutes or thermostat display will go back to setpoint display. You can change that delay with the outdoor_temp_timeout attribute 0x0011.

  - setting the outside temperature sensor:

You can use any temperature source, local or remote.
```
  - platform: template
    sensor:
      - name: "local_temp"
        unit_of_measurement: '°C'
        device_class: temperature
        state_class: measurement
        state: "{{ state_attr('weather.openweathermap', 'temperature') }}"
```
- Sending time to your thermostats. This is now done automatically by ZHA.
  - ![send time](automation/blueprints/send_time_to_thermostats.yaml)
- Setting the little icon Eco to flash on the thermostat during peak. To stop the icon flashing make another automation with value: -128 at the end of peak period.
  - ![show dr logo](automation/blueprints/show_dr_logo.yaml)
  - ![Hide dr logo](automation/blueprints/stop_dr_logo.yaml)
- Send weather icons codes to TH1134ZB-HC thermostat using Openweathermap conditions codes: (see ![icons](www))
  - In that case you need to set two automations as the weather conditions codes are the same for day time and night time but the icons on the thermostat are different.
    - ![show day time icons](automation/blueprints/update_icon_openweathermap_day.yaml)
    - ![show night time icons](automation/blueprints/update_icon_openweathermap_night.yaml)
- Send weather icons codes to TH1134ZB-HC thermostat using Environment Canada weather conditions codes:
  - In that case you need only one automation:
    - ![show icons](automation/blueprints/update_icon_env_canada.yaml)  

# Device hard reset:
- Thermostats:

    - Raise the temperature until the display change.
    - Push the two button until CLR appear on the screen.
    - Push once the upper button to get YES on the display.
    - Push both button simutanously and release immediately. DONE should appear on the screen.
    - The thermostat will restart with factory setup.

## Buy me a coffee
If you want to make donation as appreciation of my work, you can do so via PayPal. Thank you!
[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/phytoressources/)
