"""Module to handle quirks of the Sinopé Technologies switches.

Supported devices, SP2600ZB, SP2610ZB, RM3250ZB, RM3500ZB,
VA4200WZ, VA4201WZ, VA4200ZB, VA4201ZB, VA4220ZB, VA4221ZB and MC3100ZB,
2nd gen VA4220ZB, VA4221ZB with flow meeter FS4220, FS4221.
"""

from typing import Final

import zigpy.profiles.zha as zha_p
import zigpy.types as t

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.sinope import (
    SINOPE,
    SINOPE_MANUFACTURER_CLUSTER_ID,
    CustomDeviceTemperatureCluster,
)

from zigpy.quirks import CustomCluster, CustomDevice
from zigpy.quirks.v2 import (
    BinarySensorDeviceClass,
    EntityType,
    QuirkBuilder,
    ReportingConfig,
    SensorDeviceClass,
    SensorStateClass,
)
from zigpy.quirks.v2.homeassistant import (
    UnitOfTemperature,
    UnitOfTime,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfVolumeFlowRate,
    PERCENTAGE,
)
from zigpy.zcl.foundation import (
    Array,
    BaseAttributeDefs,
    ZCLAttributeDef,
    ZCL_CLUSTER_REVISION_ATTR,
)
from zigpy.zcl.clusters.general import (
    Basic,
    BinaryInput,
    DeviceTemperature,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    PowerConfiguration,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic, ElectricalMeasurement
from zigpy.zcl.clusters.lightlink import LightLink
from zigpy.zcl.clusters.measurement import (
    FlowMeasurement,
    RelativeHumidity,
    TemperatureMeasurement,
)
from zigpy.zcl.clusters.security import IasZone
from zigpy.zcl.clusters.smartenergy import Metering


class KeypadLock(t.enum8):
    """Keypad_lockout values."""

    Unlocked = 0x00
    Locked = 0x01
    Partial_lock = 0x02


class FlowAlarm(t.enum8):
    """Abnormal flow alarm."""

    Off = 0x00
    On = 0x01


class AlarmAction(t.enum8):
    """Flow alarm action."""

    Nothing = 0x00
    Notify = 0x01
    Close = 0x02
    Close_notify = 0x03
    No_flow = 0x04


class PowerSource(t.uint32_t):
    """Valve power source types."""

    Battery = 0x00000000
    ACUPS_01 = 0x00000001
    DC_power = 0x0001D4C0


class EmergencyPower(t.uint32_t):
    """Valve emergency power source types."""

    Battery = 0x00000000
    ACUPS_01 = 0x00000001
    Battery_ACUPS_01 = 0x0000003C


class AbnormalAction(t.bitmap16):
    """Action in case of abnormal flow detected."""

    Nothing = 0x0000
    Close_valve = 0x0001
    Close_notify = 0x0003


class ColdStatus(t.enum8):
    """Cold_load_pickup_status values."""

    Active = 0x00
    Off = 0x01


class FlowDuration(t.uint32_t):
    """Abnormal flow duration."""

    M_15 = 0x00000384
    M_30 = 0x00000708
    M_45 = 0x00000A8C
    M_60 = 0x00000E10
    M_75 = 0x00001194
    M_90 = 0x00001518
    H_3 = 0x00002A30
    H_6 = 0x00005460
    H_12 = 0x0000A8C0
    H_24 = 0x00015180


class InputDelay(t.uint16_t):
    """Delay for on/off input."""

    Off = 0x0000
    M_1 = 0x003C
    M_2 = 0x0078
    M_5 = 0x012C
    M_10 = 0x0258
    M_15 = 0x0384
    M_30 = 0x0708
    H_1 = 0x0E10
    H_2 = 0x1C20
    H_3 = 0x2A30


class EnergySource(t.enum8):
    """Power source."""

    Unknown = 0x0000
    DC_mains = 0x0001
    Battery = 0x0003
    DC_source = 0x0004
    ACUPS_01 = 0x0081
    ACUPS01 = 0x0082


class ValveStatus(t.bitmap8):
    """Valve_status."""

    Off = 0x00
    Off_armed = 0x01
    On = 0x02


class UnitOfMeasure(t.enum8):
    """Unit_of_measure."""

    KWh = 0x00
    Lh = 0x07


class SinopeManufacturerCluster(CustomCluster):
    """SinopeManufacturerCluster manufacturer cluster."""

    KeypadLock: Final = KeypadLock
    FlowAlarm: Final = FlowAlarm
    AlarmAction: Final = AlarmAction
    PowerSource: Final = PowerSource
    EmergencyPower: Final = EmergencyPower
    AbnormalAction: Final = AbnormalAction
    ColdStatus: Final = ColdStatus
    FlowDuration: Final = FlowDuration
#    FlowMeter: Final = FlowMeter
    InputDelay: Final = InputDelay

    cluster_id: Final[t.uint16_t] = SINOPE_MANUFACTURER_CLUSTER_ID
    name: Final = "SinopeManufacturerCluster"
    ep_attribute: Final = "sinope_manufacturer_specific"

    class AttributeDefs(BaseAttributeDefs):
        """Sinope Manufacturer Cluster Attributes."""

        unknown_attr_1: Final = ZCLAttributeDef(
            id=0x0001, type=t.Bool, access="rw", is_manufacturer_specific=True
        )
        keypad_lockout: Final = ZCLAttributeDef(
            id=0x0002, type=KeypadLock, access="rw", is_manufacturer_specific=True
        )
        firmware_number: Final = ZCLAttributeDef(
            id=0x0003, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        firmware_version: Final = ZCLAttributeDef(
            id=0x0004,
            type=t.CharacterString,
            access="r",
            is_manufacturer_specific=True,
        )
        outdoor_temp: Final = ZCLAttributeDef(
            id=0x0010, type=t.int16s, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_2: Final = ZCLAttributeDef(
            id=0x0013, type=t.enum8, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_3: Final = ZCLAttributeDef(
            id=0x0030, type=t.uint8_t, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_4: Final = ZCLAttributeDef(
            id=0x0035, type=t.uint16_t, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_5: Final = ZCLAttributeDef(
            id=0x0037, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_6: Final = ZCLAttributeDef(
            id=0x0038, type=t.enum8, access="rp", is_manufacturer_specific=True
        )
        connected_load: Final = ZCLAttributeDef(
            id=0x0060, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        current_load: Final = ZCLAttributeDef(
            id=0x0070, type=t.bitmap8, access="r", is_manufacturer_specific=True
        )
        unknown_attr_7: Final = ZCLAttributeDef(
            id=0x0074, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        dr_config_water_temp_min: Final = ZCLAttributeDef(
            id=0x0076, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        dr_config_water_temp_time: Final = ZCLAttributeDef(
            id=0x0077, type=t.uint8_t, access="rwp", is_manufacturer_specific=True
        )
        dr_wt_time_on: Final = ZCLAttributeDef(
            id=0x0078, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_8: Final = ZCLAttributeDef(
            id=0x0079, type=t.bitmap8, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_9: Final = ZCLAttributeDef(
            id=0x007A, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_10: Final = ZCLAttributeDef(
            id=0x007B, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        min_measured_temp: Final = ZCLAttributeDef(
            id=0x007C, type=t.int16s, access="rp", is_manufacturer_specific=True
        )
        max_measured_temp: Final = ZCLAttributeDef(
            id=0x007D, type=t.int16s, access="rp", is_manufacturer_specific=True
        )
        water_temp_protection_type: Final = ZCLAttributeDef(
            id=0x007E, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_11: Final = ZCLAttributeDef(
            id=0x0080, type=t.uint32_t, access="rp", is_manufacturer_specific=True
        )
        current_summation_delivered: Final = ZCLAttributeDef(
            id=0x0090, type=t.uint32_t, access="rp", is_manufacturer_specific=True
        )
        timer: Final = ZCLAttributeDef(
            id=0x00A0, type=t.uint32_t, access="rwp", is_manufacturer_specific=True
        )
        timer_countdown: Final = ZCLAttributeDef(
            id=0x00A1, type=t.uint32_t, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_12: Final = ZCLAttributeDef(
            id=0x00B0, type=t.Bool, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_13: Final = ZCLAttributeDef(
            id=0x0101, type=Array, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_14: Final = ZCLAttributeDef(
            id=0x012A, type=t.enum8, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_15: Final = ZCLAttributeDef(
            id=0x012C, type=Array, access="rp", is_manufacturer_specific=True
        )
        status: Final = ZCLAttributeDef(
            id=0x0200, type=t.bitmap32, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_16: Final = ZCLAttributeDef(
            id=0x0202, type=t.enum8, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_17: Final = ZCLAttributeDef(
            id=0x0203, type=t.enum8, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_18: Final = ZCLAttributeDef(
            id=0x0220, type=t.bitmap16, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_19: Final = ZCLAttributeDef(
            id=0x0221, type=t.bitmap16, access="rp", is_manufacturer_specific=True
        )
        alarm_flow_threshold: Final = ZCLAttributeDef(
            id=0x0230, type=FlowAlarm, access="rw", is_manufacturer_specific=True
        )
        alarm_options: Final = ZCLAttributeDef(
            id=0x0231, type=AlarmAction, access="r", is_manufacturer_specific=True
        )
        flow_meter_config: Final = ZCLAttributeDef(
            id=0x0240, type=Array, access="rw", is_manufacturer_specific=True
        )
        valve_countdown: Final = ZCLAttributeDef(
            id=0x0241, type=t.uint32_t, access="rw", is_manufacturer_specific=True
        )
        power_source: Final = ZCLAttributeDef(
            id=0x0250, type=PowerSource, access="rw", is_manufacturer_specific=True
        )
        emergency_power_source: Final = ZCLAttributeDef(
            id=0x0251, type=EmergencyPower, access="rw", is_manufacturer_specific=True
        )
        abnormal_flow_duration: Final = ZCLAttributeDef(
            id=0x0252, type=FlowDuration, access="rw", is_manufacturer_specific=True
        )
        abnormal_flow_action: Final = ZCLAttributeDef(
            id=0x0253, type=AbnormalAction, access="rw", is_manufacturer_specific=True
        )
        max_measured_value: Final = ZCLAttributeDef(
            id=0x0280, type=t.int16s, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_20: Final = ZCLAttributeDef(
            id=0x0281, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        unknown_attr_21: Final = ZCLAttributeDef(
            id=0x0282, type=t.uint16_t, access="rwp", is_manufacturer_specific=True
        )
        cold_load_pickup_status: Final = ZCLAttributeDef(
            id=0x0283, type=ColdStatus, access="r", is_manufacturer_specific=True
        )
        cold_load_pickup_remaining_time: Final = ZCLAttributeDef(
            id=0x0284, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        input_on_delay: Final = ZCLAttributeDef(
            id=0x02A0, type=InputDelay, access="rw", is_manufacturer_specific=True
        )
        input_off_delay: Final = ZCLAttributeDef(
            id=0x02A1, type=InputDelay, access="rw", is_manufacturer_specific=True
        )
        cluster_revision: Final = ZCL_CLUSTER_REVISION_ATTR


class SinopeTechnologiesBasicCluster(CustomCluster, Basic):
    """SinopetechnologiesBasicCluster custom cluster ."""

    EnergySource: Final = EnergySource

    class AttributeDefs(Basic.AttributeDefs):
        """Sinope Manufacturer Basic Cluster Attributes."""

        power_source: Final = ZCLAttributeDef(
            id=0x0007, type=EnergySource, access="r", is_manufacturer_specific=True
        )


class SinopeTechnologiesMeteringCluster(CustomCluster, Metering):
    """SinopeTechnologiesMeteringCluster custom cluster."""

    ValveStatus: Final = ValveStatus
    UnitOfMeasure: Final = UnitOfMeasure

    DIVISOR = 0x0302
    _CONSTANT_ATTRIBUTES = {DIVISOR: 1000}

    class AttributeDefs(Metering.AttributeDefs):
        """Sinope Manufacturer Metering Cluster Attributes."""

        status: Final = ZCLAttributeDef(
            id=0x0200, type=ValveStatus, access="r", is_manufacturer_specific=True
        )
        unit_of_measure: Final = ZCLAttributeDef(
            id=0x0300, type=UnitOfMeasure, access="r", is_manufacturer_specific=True
        )


class SinopeTechnologiesFlowMeasurementCluster(CustomCluster, FlowMeasurement):
    """Custom flow measurement cluster that divides value by 10."""

    def _update_attribute(self, attrid, value):
        if attrid == self.AttributeDefs.measured_value.id:
            value = value / 10
        super()._update_attribute(attrid, value)


(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=81, device_version=0,
    # input_clusters=[0, 3, 6, 1794, 2820, 65281]
    # output_clusters=[25]>
    QuirkBuilder(SINOPE, "SP2600ZB")
    .applies_to(SINOPE, "SP2610ZB")
    .replaces(SinopeTechnologiesMeteringCluster)
    .replaces(SinopeManufacturerCluster)
    .sensor( # Current summ delivered
        SinopeTechnologiesMeteringCluster.AttributeDefs.current_summ_delivered.name,
        SinopeTechnologiesMeteringCluster.cluster_id,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        reporting_config=ReportingConfig(
            min_interval=59, max_interval=1799, reportable_change=60
        ),
        translation_key="current_summ_delivered",
        fallback_name="Current summ delivered",
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=2, device_version=0,
    # input_clusters=[0, 3, 4, 5, 6, 1794, 2820, 2821, 65281]
    # output_clusters=[3, 4, 25]>
    QuirkBuilder(SINOPE, "RM3250ZB")
    .replaces(SinopeManufacturerCluster)
    .enum( # Keypad lock
        attribute_name=SinopeManufacturerCluster.AttributeDefs.keypad_lockout.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=KeypadLock,
        translation_key="keypad_lockout",
        fallback_name="Keypad lockout",
        entity_type=EntityType.CONFIG,
    )
    .number( # Timer
        SinopeManufacturerCluster.AttributeDefs.timer.name,
        SinopeManufacturerCluster.cluster_id,
        step=1,
        min_value=0,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="timer",
        fallback_name="Timer",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # current summ delivered
        SinopeTechnologiesMeteringCluster.AttributeDefs.current_summ_delivered.name,
        SinopeTechnologiesMeteringCluster.cluster_id,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        reporting_config=ReportingConfig(
            min_interval=59, max_interval=1799, reportable_change=60
        ),
        translation_key="current_summ_delivered",
        fallback_name="Current summ delivered",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Device status",
    )
    .sensor( # Timer countdown
        SinopeManufacturerCluster.AttributeDefs.timer_countdown.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTime.SECONDS,
        translation_key="timer_countdown",
        fallback_name="Timer countdown",
        entity_type=EntityType.DIAGNOSTIC,
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=2, device_version=0,
    # input_clusters=[0, 2, 3, 4, 5, 6, 1794, 2820, 2821, 65281]
    # output_clusters=[3, 4, 25]>
    QuirkBuilder(SINOPE, "RM3250ZB")
    .replaces(CustomDeviceTemperatureCluster)
    .replaces(SinopeManufacturerCluster)
    .enum( # Keypad lock
        attribute_name=SinopeManufacturerCluster.AttributeDefs.keypad_lockout.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=KeypadLock,
        translation_key="keypad_lockout",
        fallback_name="Keypad lockout",
        entity_type=EntityType.CONFIG,
    )
    .number( # Timer
        SinopeManufacturerCluster.AttributeDefs.timer.name,
        SinopeManufacturerCluster.cluster_id,
        step=1,
        min_value=0,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="timer",
        fallback_name="Timer",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # Device temperature
        CustomDeviceTemperatureCluster.AttributeDefs.current_temperature.name,
        CustomDeviceTemperatureCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        reporting_config=ReportingConfig(
            min_interval=59, max_interval=1799, reportable_change=60
        ),
        translation_key="current_temperature",
        fallback_name="Current temperature",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Device status",
    )
    .sensor( # Timer countdown
        SinopeManufacturerCluster.AttributeDefs.timer_countdown.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTime.SECONDS,
        translation_key="timer_countdown",
        fallback_name="Timer countdown",
        entity_type=EntityType.DIAGNOSTIC,
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=3, device_version=0,
    # input_clusters=[0, 1, 3, 4, 5, 6, 8, 2821, 65281]
    # output_clusters=[3, 25]>
    QuirkBuilder(SINOPE, "VA4200WZ")
    .applies_to(SINOPE, "VA4201WZ")
    .applies_to(SINOPE, "VA4200ZB")
    .applies_to(SINOPE, "VA4201ZB")
    .applies_to(SINOPE, "VA4220ZB")
    .applies_to(SINOPE, "VA4221ZB")
    .replaces(SinopeTechnologiesBasicCluster)
    .replaces(SinopeManufacturerCluster)
    .enum( # energy source
        attribute_name=SinopeTechnologiesBasicCluster.AttributeDefs.power_source.name,
        cluster_id=SinopeTechnologiesBasicCluster.cluster_id,
        enum_class=EnergySource,
        translation_key="power_source",
        fallback_name="Power source",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # Device temperature
        CustomDeviceTemperatureCluster.AttributeDefs.current_temperature.name,
        CustomDeviceTemperatureCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        reporting_config=ReportingConfig(
            min_interval=59, max_interval=1799, reportable_change=60
        ),
        translation_key="current_temperature",
        fallback_name="Current temperature",
    )
    .sensor( # battery percent
        PowerConfiguration.AttributeDefs.battery_percentage_remaining.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_percentage_remaining",
        fallback_name="Battery percentage remaining",
    )
    .sensor( # battery voltage
        PowerConfiguration.AttributeDefs.battery_voltage.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_voltage",
        fallback_name="Battery voltage",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Device status",
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
        # device_type=3, device_version=0,
        # input_clusters=[0, 1, 3, 4, 5, 6, 8, 1026, 1280, 1794, 2821, 65281]
        # output_clusters=[3, 6, 25]>
    QuirkBuilder(SINOPE, "VA4220ZB")
    .applies_to(SINOPE, "VA4221ZB")
    .replaces(SinopeTechnologiesBasicCluster)
    .replaces(SinopeTechnologiesFlowMeasurementCluster)
    .replaces(SinopeTechnologiesMeteringCluster)
    .replaces(SinopeManufacturerCluster)
    .enum( # Alarm action status
        attribute_name=SinopeManufacturerCluster.AttributeDefs.alarm_options.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=AlarmAction,
        translation_key="alarm_options",
        fallback_name="Alarm options",
        entity_type=EntityType.CONFIG,
    )
    .enum( # energy source
        attribute_name=SinopeTechnologiesBasicCluster.AttributeDefs.power_source.name,
        cluster_id=SinopeTechnologiesBasicCluster.cluster_id,
        enum_class=EnergySource,
        translation_key="power_source",
        fallback_name="Power source",
        entity_type=EntityType.DIAGNOSTIC,
    )
    .enum( # Flow alarm
        attribute_name=SinopeManufacturerCluster.AttributeDefs.alarm_flow_threshold.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=FlowAlarm,
        translation_key="alarm_flow",
        fallback_name="Alarm flow",
        entity_type=EntityType.CONFIG,
    )
    .enum( # Abnormal Flow action
        attribute_name=SinopeManufacturerCluster.AttributeDefs.abnormal_flow_action.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=AbnormalAction,
        translation_key="abnormal_flow_action",
        fallback_name="Abnormal flow action",
        entity_type=EntityType.CONFIG,
    )
    .number( # Abnormal Flow Duration
        SinopeManufacturerCluster.AttributeDefs.abnormal_flow_duration.name,
        SinopeManufacturerCluster.cluster_id,
        step=10,
        min_value=900,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="abnormal_flow_duration",
        fallback_name="Abnormal flow duration",
        entity_type=EntityType.CONFIG,
    )
    .number( # Valve countdown
        SinopeManufacturerCluster.AttributeDefs.valve_countdown.name,
        SinopeManufacturerCluster.cluster_id,
        step=10,
        min_value=300,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="valve_countdown",
        fallback_name="Valve countdown",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # Flow rate
        SinopeTechnologiesFlowMeasurementCluster.AttributeDefs.measured_value.name,
        SinopeTechnologiesFlowMeasurementCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=600, reportable_change=1
        ),
        translation_key="flow_rate",
        fallback_name="Flow rate",
    )
    .sensor( # battery percent
        PowerConfiguration.AttributeDefs.battery_percentage_remaining.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_percentage_remaining",
        fallback_name="Battery percentage remaining",
    )
    .sensor( # battery voltage
        PowerConfiguration.AttributeDefs.battery_voltage.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_voltage",
        fallback_name="Battery voltage",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Device status",
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=2, device_version=0,
    # input_clusters=[0, 1, 3, 4, 5, 6, 15, 1026, 1029, 2821, 65281]
    # output_clusters=[25]>
    QuirkBuilder(SINOPE, "MC3100ZB")
    .replaces(SinopeManufacturerCluster, endpoint_id=1)
    .replaces(SinopeManufacturerCluster, endpoint_id=2)
    .number( # Timer 1
        SinopeManufacturerCluster.AttributeDefs.timer.name,
        SinopeManufacturerCluster.cluster_id,
        endpoint_id=1,
        step=1,
        min_value=0,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="timer",
        fallback_name="Timer",
        entity_type=EntityType.CONFIG,
    )
    .number( # Timer 2
        SinopeManufacturerCluster.AttributeDefs.timer.name,
        SinopeManufacturerCluster.cluster_id,
        endpoint_id=2,
        step=1,
        min_value=0,
        max_value=86400,
        unit=UnitOfTime.SECONDS,
        translation_key="timer_2",
        fallback_name="Timer 2",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # battery percent
        PowerConfiguration.AttributeDefs.battery_percentage_remaining.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_percentage_remaining",
        fallback_name="Battery percentage remaining",
    )
    .sensor( # battery voltage
        PowerConfiguration.AttributeDefs.battery_voltage.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_voltage",
        fallback_name="Battery voltage",
    )
    .sensor( # outside temperature
        TemperatureMeasurement.AttributeDefs.measured_value.name,
        TemperatureMeasurement.cluster_id,
        endpoint_id=2,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        reporting_config=ReportingConfig(
            min_interval=60, max_interval=3678, reportable_change=1
        ),
        translation_key="external_temperature",
        fallback_name="External temperature",
    )
    .sensor( # device temperature
        TemperatureMeasurement.AttributeDefs.measured_value.name,
        TemperatureMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        reporting_config=ReportingConfig(
            min_interval=60, max_interval=3678, reportable_change=1
        ),
        translation_key="device_temperature",
        fallback_name="Device temperature",
    )
    .sensor( # Humidity
        RelativeHumidity.AttributeDefs.measured_value.name,
        RelativeHumidity.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        reporting_config=ReportingConfig(
            min_interval=60, max_interval=3678, reportable_change=1
        ),
        translation_key="humidity",
        fallback_name="Humidity",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Device status",
    )
    .switch(
        OnOff.AttributeDefs.on_off.name,
        OnOff.cluster_id,
        endpoint_id=2,
        translation_key="on_off_2",
        fallback_name="On Off 2",
        entity_type=EntityType.STANDARD,
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=260, device_version=0,
    # input_clusters=[0, 2, 3, 4, 5, 6, 1026, 1280, 1794, 2820, 2821, 65281]
    # output_clusters=[10, 25]>
    QuirkBuilder(SINOPE, "RM3500ZB")
    .replaces(CustomDeviceTemperatureCluster)
    .replaces(SinopeManufacturerCluster, endpoint_id=1)
    .binary_sensor( # leak status
        "zone_status",
        IasZone.cluster_id,
        endpoint_id=1,
        device_class=BinarySensorDeviceClass.TAMPER,
        entity_type=EntityType.DIAGNOSTIC,
        reporting_config=ReportingConfig(
            min_interval=0, max_interval=600, reportable_change=1
        ),
        translation_key="leak_status",
        fallback_name="Leak status",
    )
    .binary_sensor( # Cold load status
        "cold_load_pickup_status",
        SinopeManufacturerCluster.cluster_id,
        endpoint_id=1,
        device_class=BinarySensorDeviceClass.TAMPER,
        translation_key="cold_load_pickup_status",
        fallback_name="Cold load pickup status",
        entity_type=EntityType.CONFIG,
    )
    .enum( # Keypad lock
        attribute_name=SinopeManufacturerCluster.AttributeDefs.keypad_lockout.name,
        cluster_id=SinopeManufacturerCluster.cluster_id,
        enum_class=KeypadLock,
        translation_key="keypad_lockout",
        fallback_name="Keypad lockout",
        entity_type=EntityType.CONFIG,
    )
    .number( # water temp min limit
        SinopeManufacturerCluster.AttributeDefs.dr_config_water_temp_min.name,
        SinopeManufacturerCluster.cluster_id,
        step=1,
        min_value=0,
        max_value=55,
        unit=UnitOfTemperature.CELSIUS,
        translation_key="water_temp_min",
        fallback_name="Water temp min",
        entity_type=EntityType.CONFIG,
    )
    .sensor( # water temperature
        TemperatureMeasurement.AttributeDefs.measured_value.name,
        TemperatureMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=580, reportable_change=100
        ),
        translation_key="water_temperature",
        fallback_name="Water temperature",
    )
    .sensor( # Device status
        SinopeManufacturerCluster.AttributeDefs.status.name,
        SinopeManufacturerCluster.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        translation_key="status",
        fallback_name="Device status",
        entity_type=EntityType.DIAGNOSTIC,
    )
    .add_to_registry()
)

(
    # <SimpleDescriptor(endpoint=1, profile=260,
    # device_type=81, device_version=0,
    # input_clusters=[0, 3, 6, 1794, 2820, 4096, 65281]
    # output_clusters=[25, 4096]>
    QuirkBuilder(SINOPE, "SP2600ZB")
    .applies_to(SINOPE, "SP2610ZB")
    .replaces(SinopeTechnologiesMeteringCluster)
    .replaces(SinopeManufacturerCluster)
    .sensor( # current summ delivered
        SinopeTechnologiesMeteringCluster.AttributeDefs.current_summ_delivered.name,
        SinopeTechnologiesMeteringCluster.cluster_id,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        reporting_config=ReportingConfig(
            min_interval=59, max_interval=1799, reportable_change=60
        ),
        translation_key="current_summ_delivered",
        fallback_name="Current summ delivered",
    )
    .add_to_registry()
)
