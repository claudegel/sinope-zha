"""Module to handle quirks of the Sinopé Technologies thermostats.

Manufacturer specific cluster implements attributes to control displaying
of outdoor temperature, setting occupancy on/off and setting device time.
"""

from typing import Final

import zigpy.profiles.zha as zha_p
from zigpy.quirks import CustomCluster, CustomDevice
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    Ota,
    PowerConfiguration,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic, ElectricalMeasurement
from zigpy.zcl.clusters.hvac import Fan, Thermostat, UserInterface
from zigpy.zcl.clusters.measurement import TemperatureMeasurement
from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.foundation import Array

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.sinope import SINOPE, SINOPE_MANUFACTURER_CLUSTER_ID


class KeypadLock(t.enum8):
    """Keypad_lockout values."""

    Unlocked = 0x00
    Locked = 0x01
    Partial_lock = 0x02


class Display(t.enum8):
    """Config_2nd_display values."""

    Auto = 0x00
    Setpoint = 0x01
    Outside_temperature = 0x02
    Room_temperature = 0x04


class FloorMode(t.enum8):
    """Air_floor_mode values."""

    Air_by_floor = 0x01
    Floor = 0x02


class AuxMode(t.enum8):
    """Aux_output_mode values."""

    Off = 0x00
    On_15m = 0x01
    On_15s = 0x02
    Exp_module = 0x03


class PumpStatus(t.uint8_t):
    """Pump protection status."""

    Off = 0x00
    On = 0x01


class LimitStatus(t.uint8_t):
    """Floor limit status values."""

    Ok = 0x00
    Low_reached = 0x01
    Max_reached = 0x02
    Max_air_reached = 0x03


class SensorType(t.enum8):
    """Temp_sensor_type values."""

    Sensor_10k = 0x00
    Sensor_12k = 0x01


class TimeFormat(t.enum8):
    """Time_format values."""

    Format_24h = 0x00
    Format_12h = 0x01


class WeatherIcon(t.enum8):
    """weather_icons values."""

    Cloud = 0x05
    Cloud2 = 0x08
    Cloud3 = 0x09
    Cloudfog = 0x11
    Cloudlightning = 0x0B
    Cloudlightning2 = 0x0C
    Cloudmoon = 0x13
    Cloudmoon2 = 0x14
    Cloudmoon3 = 0x15
    Cloudrain = 0x0A
    Cloudrain2 = 0x1C
    Cloudrain3 = 0x1D
    Cloudrainmoon = 0x17
    Cloudrainmoon2 = 0x18
    Cloudrainmoon3 = 0x19
    Cloudrainmoon4 = 0x1F
    Cloudrainmoon5 = 0x21
    Cloudrainsun = 0x06
    Cloudrainsun2 = 0x07
    Cloudrainsun3 = 0x1E
    Cloudrainsun4 = 0x20
    Cloudsnow = 0x0D
    Cloudsnow2 = 0x0E
    Cloudsnow3 = 0x0F
    Cloudsnow4 = 0x10
    Cloudsnow5 = 0x16
    Cloudsnow6 = 0x1A
    Cloudsun = 0x03
    Cloudsun2 = 0x04
    Hide = 0x00
    Moonstar = 0x12
    Sun = 0x01
    Sun2 = 0x02


class GfciStatus(t.enum8):
    """Gfci_status values."""

    Ok = 0x00
    Error = 0x01


class SystemMode(t.enum8):
    """System mode values."""

    Off = 0x00
    Auto = 0x01
    Cool = 0x03
    Heat = 0x04


class PumpDuration(t.enum8):
    """Pump protection duration period values."""

    T5 = 0x05
    T10 = 0x0A
    T15 = 0x0F
    T20 = 0x14
    T30 = 0x1E
    T60 = 0x3C


class CycleLength(t.uint16_t):
    """Cycle length, 15 sec (15) or 15 min (900 sec)."""

    Sec_15 = 0x000F
    Min_15 = 0x0384


class Occupancy(t.enum8):
    """Set_occupancy values."""

    Away = 0x00
    Home = 0x01


class Backlight(t.enum8):
    """Backlight_auto_dim_param values."""

    On_demand = 0x00
    Always_on = 0x01
    Bedroom = 0x02


class CycleOutput(t.uint16_t):
    """Main and aux cycle period values."""

    Sec_15 = 0x000F
    Min_5 = 0x012C
    Min_10 = 0x0258
    Min_15 = 0x0384
    Min_20 = 0x04B0
    Min_25 = 0x05DC
    Min_30 = 0x0708
    Off = 0xFFFF


class Language(t.enum8):
    """Display_language values."""

    En = 0x00
    Fr = 0x01


class SinopeTechnologiesManufacturerCluster(CustomCluster):
    """SinopeTechnologiesManufacturerCluster manufacturer cluster."""

    KeypadLock: Final = KeypadLock
    Display: Final = Display
    FloorMode: Final = FloorMode
    AuxMode: Final = AuxMode
    PumpStatus: Final = PumpStatus
    Language: Final = Language
    LimitStatus: Final = LimitStatus
    SensorType: Final = SensorType
    TimeFormat: Final = TimeFormat
    WeatherIcon: Final = WeatherIcon
    GfciStatus: Final = GfciStatus
    SystemMode: Final = SystemMode
    PumpDuration: Final = PumpDuration
    CycleLength: Final = CycleLength

    cluster_id: Final[t.uint16_t] = SINOPE_MANUFACTURER_CLUSTER_ID
    name: Final = "SinopeTechnologiesManufacturerCluster"
    ep_attribute: Final = "sinope_manufacturer_specific"

    class AttributeDefs(foundation.BaseAttributeDefs):
        """Sinope Manufacturer Cluster Attributes."""

        unknown_attr_1: Final = foundation.ZCLAttributeDef(
            id=0x0001, type=t.Bool, access="rwp", is_manufacturer_specific=True
        )
        keypad_lockout: Final = foundation.ZCLAttributeDef(
            id=0x0002, type=KeypadLock, access="rwp", is_manufacturer_specific=True
        )
        firmware_number: Final = foundation.ZCLAttributeDef(
            id=0x0003, type=t.uint16_t, access="rp", is_manufacturer_specific=True
        )
        firmware_version: Final = foundation.ZCLAttributeDef(
            id=0x0004,
            type=t.CharacterString,
            access="rp",
            is_manufacturer_specific=True,
        )
        display_language: Final = foundation.ZCLAttributeDef(
            id=0x0005, type=Language, access="rwp", is_manufacturer_specific=True
        )
        outdoor_temp: Final = foundation.ZCLAttributeDef(
            id=0x0010, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        outdoor_temp_timeout: Final = foundation.ZCLAttributeDef(
            id=0x0011, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        config_2nd_display: Final = foundation.ZCLAttributeDef(
            id=0x0012, type=Display, access="rwp", is_manufacturer_specific=True
        )
        weather_icons: Final = foundation.ZCLAttributeDef(
            id=0x0013, type=WeatherIcon, access="rwp", is_manufacturer_specific=True
        )
        secs_since_2k: Final = foundation.ZCLAttributeDef(
            id=0x0020, type=t.uint32_t, access="rwp", is_manufacturer_specific=True
        )
        current_load: Final = foundation.ZCLAttributeDef(
            id=0x0070, type=t.bitmap8, access="rp", is_manufacturer_specific=True
        )
        eco_delta_setpoint: Final = foundation.ZCLAttributeDef(
            id=0x0071, type=t.int8s, access="rwp", is_manufacturer_specific=True
        )
        eco_max_pi_heating_demand: Final = foundation.ZCLAttributeDef(
            id=0x0072, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        eco_safety_temperature_delta: Final = foundation.ZCLAttributeDef(
            id=0x0073, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_2: Final = foundation.ZCLAttributeDef(
            id=0x0075, type=t.bitmap32, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_3: Final = foundation.ZCLAttributeDef(
            id=0x0080, type=t.uint32_t, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_4: Final = foundation.ZCLAttributeDef(
            id=0x0100, type=t.uint8_t, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_5: Final = foundation.ZCLAttributeDef(
            id=0x0101, type=Array, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_6: Final = foundation.ZCLAttributeDef(
            id=0x0102, type=t.uint8_t, access="r", is_manufacturer_specific=True
        )
        unknown_attr_7: Final = foundation.ZCLAttributeDef(
            id=0x0103, type=Array, access="r", is_manufacturer_specific=True
        )
        setpoint: Final = foundation.ZCLAttributeDef(
            id=0x0104, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        air_floor_mode: Final = foundation.ZCLAttributeDef(
            id=0x0105, type=FloorMode, access="rw", is_manufacturer_specific=True
        )
        aux_output_mode: Final = foundation.ZCLAttributeDef(
            id=0x0106, type=AuxMode, access="rw", is_manufacturer_specific=True
        )
        floor_temperature: Final = foundation.ZCLAttributeDef(
            id=0x0107, type=t.int16s, access="r", is_manufacturer_specific=True
        )
        air_max_limit: Final = foundation.ZCLAttributeDef(
            id=0x0108, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        floor_min_setpoint: Final = foundation.ZCLAttributeDef(
            id=0x0109, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        floor_max_setpoint: Final = foundation.ZCLAttributeDef(
            id=0x010A, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        floor_sensor_type_param: Final = foundation.ZCLAttributeDef(
            id=0x010B, type=SensorType, access="rw", is_manufacturer_specific=True
        )
        floor_limit_status: Final = foundation.ZCLAttributeDef(
            id=0x010C, type=LimitStatus, access="rp", is_manufacturer_specific=True
        )
        room_temperature: Final = foundation.ZCLAttributeDef(
            id=0x010D, type=t.int16s, access="r", is_manufacturer_specific=True
        )
        time_format: Final = foundation.ZCLAttributeDef(
            id=0x0114, type=TimeFormat, access="rwp", is_manufacturer_specific=True
        )
        gfci_status: Final = foundation.ZCLAttributeDef(
            id=0x0115, type=GfciStatus, access="rp", is_manufacturer_specific=True
        )
        hvac_mode: Final = foundation.ZCLAttributeDef(
            id=0x0116, type=SystemMode, access="r", is_manufacturer_specific=True
        )
        unknown_attr_8: Final = foundation.ZCLAttributeDef(
            id=0x0117, type=Array, access="r", is_manufacturer_specific=True
        )
        aux_connected_load: Final = foundation.ZCLAttributeDef(
            id=0x0118, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        connected_load: Final = foundation.ZCLAttributeDef(
            id=0x0119, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        pump_protection_status: Final = foundation.ZCLAttributeDef(
            id=0x0128, type=PumpStatus, access="rw", is_manufacturer_specific=True
        )
        pump_protection_duration: Final = foundation.ZCLAttributeDef(
            id=0x012A, type=PumpDuration, access="rwp", is_manufacturer_specific=True
        )
        current_setpoint: Final = foundation.ZCLAttributeDef(
            id=0x012B, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_9: Final = foundation.ZCLAttributeDef(
            id=0x012C, type=Array, access="r", is_manufacturer_specific=True
        )
        report_local_temperature: Final = foundation.ZCLAttributeDef(
            id=0x012D, type=t.int16s, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_17: Final = foundation.ZCLAttributeDef(
            id=0x0130, type=t.bitmap8, access="rwp", is_manufacturer_specific=True
        )
        balance_point: Final = foundation.ZCLAttributeDef(
            id=0x0134, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_19: Final = foundation.ZCLAttributeDef(
            id=0x0135, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        timer_off: Final = foundation.ZCLAttributeDef(
            id=0x0136, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        abs_min_heat_setpoint_limit: Final = foundation.ZCLAttributeDef(
            id=0x0137, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_20: Final = foundation.ZCLAttributeDef(
            id=0x0138, type=t.bitmap16, access="rwp", is_manufacturer_specific=True
        )
        heat_lockout_temperature: Final = foundation.ZCLAttributeDef(
            id=0x0139, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        cool_lockout_temperature: Final = foundation.ZCLAttributeDef(
            id=0x013A, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_11: Final = foundation.ZCLAttributeDef(
            id=0x013B, type=t.bitmap8, access="rp", is_manufacturer_specific=True
        )
        status: Final = foundation.ZCLAttributeDef(
            id=0x0200, type=t.bitmap32, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_12: Final = foundation.ZCLAttributeDef(
            id=0x0202, type=t.enum8, access="r", is_manufacturer_specific=True
        )
        unknown_attr_22: Final = foundation.ZCLAttributeDef(
            id=0x0260, type=t.bitmap16, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_21: Final = foundation.ZCLAttributeDef(
            id=0x0261, type=t.bitmap16, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_24: Final = foundation.ZCLAttributeDef(
            id=0x0262, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_25: Final = foundation.ZCLAttributeDef(
            id=0x0263, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_26: Final = foundation.ZCLAttributeDef(
            id=0x0264, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_27: Final = foundation.ZCLAttributeDef(
            id=0x0265, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_28: Final = foundation.ZCLAttributeDef(
            id=0x0266, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        hc_model_mac_addr: Final = foundation.ZCLAttributeDef(
            id=0x0267, type=t.EUI64, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_29: Final = foundation.ZCLAttributeDef(
            id=0x0268, type=t.bitmap8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_42: Final = foundation.ZCLAttributeDef(
            id=0x0269, type=t.bitmap8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_31: Final = foundation.ZCLAttributeDef(
            id=0x026A, type=t.bitmap8, access="rwp", is_manufacturer_specific=True
        )
        min_heat_setpoint_limit: Final = foundation.ZCLAttributeDef(
            id=0x026B, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        max_heat_setpoint_limit: Final = foundation.ZCLAttributeDef(
            id=0x026C, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        min_cool_setpoint_limit: Final = foundation.ZCLAttributeDef(
            id=0x026D, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        max_cool_setpoint_limit: Final = foundation.ZCLAttributeDef(
            id=0x026E, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_10: Final = foundation.ZCLAttributeDef(
            id=0x0280, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        cycle_length: Final = foundation.ZCLAttributeDef(
            id=0x0281, type=CycleLength, access="rwp", is_manufacturer_specific=True
        )
        cool_cycle_length: Final = foundation.ZCLAttributeDef(
            id=0x0282, type=CycleLength, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_13: Final = foundation.ZCLAttributeDef(
            id=0x0283, type=t.enum8, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_14: Final = foundation.ZCLAttributeDef(
            id=0x0284, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_15: Final = foundation.ZCLAttributeDef(
            id=0x0285, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_16: Final = foundation.ZCLAttributeDef(
            id=0x0286, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_32: Final = foundation.ZCLAttributeDef(
            id=0xFF04, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_33: Final = foundation.ZCLAttributeDef(
            id=0xFF05, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_34: Final = foundation.ZCLAttributeDef(
            id=0xFF06, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_35: Final = foundation.ZCLAttributeDef(
            id=0xFF07, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_36: Final = foundation.ZCLAttributeDef(
            id=0xFF08, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_37: Final = foundation.ZCLAttributeDef(
            id=0xFF09, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_38: Final = foundation.ZCLAttributeDef(
            id=0xFF0A, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_39: Final = foundation.ZCLAttributeDef(
            id=0xFF0B, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_40: Final = foundation.ZCLAttributeDef(
            id=0xFF0C, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_41: Final = foundation.ZCLAttributeDef(
            id=0xFF0D, type=t.LVBytes, access="rp", is_manufacturer_specific=True
        )
        cluster_revision: Final = foundation.ZCL_CLUSTER_REVISION_ATTR


class SinopeTechnologiesThermostatCluster(CustomCluster, Thermostat):
    """SinopeTechnologiesThermostatCluster custom cluster."""

    Occupancy: Final = Occupancy
    Backlight: Final = Backlight
    CycleOutput: Final = CycleOutput

    class AttributeDefs(Thermostat.AttributeDefs):
        """Sinope Manufacturer Thermostat Cluster Attributes."""

        set_occupancy: Final = foundation.ZCLAttributeDef(
            id=0x0400, type=Occupancy, access="rw", is_manufacturer_specific=True
        )
        main_cycle_output: Final = foundation.ZCLAttributeDef(
            id=0x0401, type=CycleOutput, access="rw", is_manufacturer_specific=True
        )
        backlight_auto_dim_param: Final = foundation.ZCLAttributeDef(
            id=0x0402, type=Backlight, access="rw", is_manufacturer_specific=True
        )
        aux_cycle_output: Final = foundation.ZCLAttributeDef(
            id=0x0404, type=CycleOutput, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_1: Final = foundation.ZCLAttributeDef(
            id=0x0421, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_2: Final = foundation.ZCLAttributeDef(
            id=0x0422, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_3: Final = foundation.ZCLAttributeDef(
            id=0x0423, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_4: Final = foundation.ZCLAttributeDef(
            id=0x0424, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_5: Final = foundation.ZCLAttributeDef(
            id=0x0425, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_6: Final = foundation.ZCLAttributeDef(
            id=0x0426, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_7: Final = foundation.ZCLAttributeDef(
            id=0x0427, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_8: Final = foundation.ZCLAttributeDef(
            id=0x0428, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_9: Final = foundation.ZCLAttributeDef(
            id=0x0429, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_10: Final = foundation.ZCLAttributeDef(
            id=0x0430, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_11: Final = foundation.ZCLAttributeDef(
            id=0x0431, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_12: Final = foundation.ZCLAttributeDef(
            id=0x0432, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_13: Final = foundation.ZCLAttributeDef(
            id=0x0433, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_14: Final = foundation.ZCLAttributeDef(
            id=0x0434, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_15: Final = foundation.ZCLAttributeDef(
            id=0x0435, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_16: Final = foundation.ZCLAttributeDef(
            id=0x0436, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_18: Final = foundation.ZCLAttributeDef(
            id=0x0437, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_17: Final = foundation.ZCLAttributeDef(
            id=0x0439, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )


class SinopeTechnologiesElectricalMeasurementCluster(
    CustomCluster, ElectricalMeasurement
):
    """SinopeTechnologiesElectricalMeasurementCluster custom cluster."""

    class AttributeDefs(ElectricalMeasurement.AttributeDefs):
        """Sinope Manufacturer ElectricalMeasurement Cluster Attributes."""

        current_summation_delivered: Final = foundation.ZCLAttributeDef(
            id=0x0551, type=t.uint32_t, access="rwp", is_manufacturer_specific=True
        )
        aux_setpoint_min: Final = foundation.ZCLAttributeDef(
            id=0x0552, type=t.uint32_t, access="rw", is_manufacturer_specific=True
        )
        aux_setpoint_max: Final = foundation.ZCLAttributeDef(
            id=0x0553, type=t.uint32_t, access="rw", is_manufacturer_specific=True
        )


class SinopeTechnologiesThermostat(CustomDevice):
    """SinopeTechnologiesThermostat custom device."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769
        # device_version=0 input_clusters=[0, 3, 4, 5, 513, 516, 1026, 2820,
        # 2821, 65281] output_clusters=[65281, 25]>
        MODELS_INFO: [
            (SINOPE, "TH1123ZB"),
            (SINOPE, "TH1124ZB"),
            (SINOPE, "TH1500ZB"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, SINOPE_MANUFACTURER_CLUSTER_ID],
            },
            # <SimpleDescriptor endpoint=196 profile=49757 device_type=769
            # device_version=0 input_clusters=[1] output_clusters=[]>
            196: {
                PROFILE_ID: 0xC25D,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [PowerConfiguration.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesElectricalMeasurementCluster,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            },
            196: {INPUT_CLUSTERS: [PowerConfiguration.cluster_id]},
        }
    }


class SinopeTH1400ZB(CustomDevice):
    """TH1400ZB thermostat."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769 device_version=1
        # input_clusters=[0, 3, 4, 5, 513, 516, 1026, 1794, 2821, 65281]
        # output_clusters=[10, 65281, 25]>
        MODELS_INFO: [(SINOPE, "TH1400ZB")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        }
    }


class SinopeTH1300ZB(CustomDevice):
    """TH1300ZB thermostat."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769 device_version=1
        # input_clusters=[0, 3, 4, 5, 513, 516, 1026, 1794, 2820, 2821, 65281]
        # output_clusters=[10, 25, 65281]>
        MODELS_INFO: [(SINOPE, "TH1300ZB")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesElectricalMeasurementCluster,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        }
    }


class SinopeLineThermostats(CustomDevice):
    """TH1123ZB, TH1124ZB, TH1500ZB and OTH3600-GA-ZB thermostats."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769 device_version=1
        # input_clusters=[0, 3, 4, 5, 513, 516, 1026, 1794, 2820, 2821, 65281]
        # output_clusters=[10, 25, 65281]>
        MODELS_INFO: [
            (SINOPE, "TH1123ZB"),
            (SINOPE, "TH1124ZB"),
            (SINOPE, "TH1500ZB"),
            (SINOPE, "OTH3600-GA-ZB"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesElectricalMeasurementCluster,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
            }
        }
    }


class SinopeG2Thermostats(CustomDevice):
    """TH1123ZB-G2 and TH1124ZB-G2 thermostats."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769 device_version=1
        # input_clusters=[0, 3, 4, 5, 513, 516, 1026, 1794, 2820, 2821, 65281]
        # output_clusters=[3, 10, 25]>
        MODELS_INFO: [
            (SINOPE, "TH1123ZB-G2"),
            (SINOPE, "TH1124ZB-G2"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesElectricalMeasurementCluster,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            }
        }
    }


class SinopeHPThermostats(CustomDevice):
    """HP6000ZB-GE, HP6000ZB-HS and HP6000ZB-MA thermostats."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=775 device_version=1
        # input_clusters=[0, 3, 4, 5, 8, 513, 514, 516, 1026, 2821, 65281]
        # output_clusters=[25]>
        MODELS_INFO: [
            (SINOPE, "HP6000ZB-GE"),
            (SINOPE, "HP6000ZB-HS"),
            (SINOPE, "HP6000ZB-MA"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.MINI_SPLIT_AC,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    LevelControl.cluster_id,
                    Thermostat.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id],
            },
            2: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.MINI_SPLIT_AC,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    LevelControl.cluster_id,
                    Thermostat.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    LevelControl.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id],
            },
            2: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    LevelControl.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id],
            },
        }
    }


class SinopeHCThermostats(CustomDevice):
    """TH1134ZB-HC thermostats."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=769 device_version=1
        # input_clusters=[0, 3, 4, 5, 513, 514, 516, 1026, 1794, 2820, 2821, 65281]
        # output_clusters=[3, 10, 25]>
        MODELS_INFO: [(SINOPE, "TH1134ZB-HC")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Fan.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeTechnologiesElectricalMeasurementCluster,
                    SinopeTechnologiesThermostatCluster,
                    SinopeTechnologiesManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            }
        }
    }
