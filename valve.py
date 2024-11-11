"""Module to handle quirks of the Sinopé Technologies valves.

Supported devices, VA4200WZ, VA4201WZ, VA4200ZB, VA4201ZB, 
VA4220ZB, VA4221ZB,
2nd gen VA4220ZB, VA4221ZB with flow meeter FS4220, FS4221.
"""

import zigpy.profiles.zha as zha_p
from zigpy.quirks import CustomCluster, CustomDevice
import zigpy.types as t
from zigpy.zcl.clusters.general import (
    Basic,
    DeviceTemperature,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    PowerConfiguration,
    Scenes,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic
from zigpy.zcl.clusters.measurement import (
    FlowMeasurement,
    TemperatureMeasurement,
)
from zigpy.zcl.clusters.security import IasZone
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
from zhaquirks.sinope import (
    SINOPE,
    SINOPE_MANUFACTURER_CLUSTER_ID,
    CustomDeviceTemperatureCluster,
)


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


class PowerSource(t.uint32_t):
    """Valve power source types."""

    Battery = 0x00000000
    ACUPS_01 = 0x00000001
    DC_power = 0x0001D4C0


class EnergySource(t.enum8):
    """Power source."""

    Unknown = 0x0000
    DC_mains = 0x0001
    Battery = 0x0003
    DC_source = 0x0004
    ACUPS_01 = 0x0081
    ACUPS01 = 0x0082


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


class ValveStatus(t.bitmap8):
    """valve_status."""

    Off = 0x00
    Off_armed = 0x01
    On = 0x02


class UnitOfMeasure(t.enum8):
    """unit_of_measure."""

    KWh = 0x00
    Lh = 0x07


class SinopeManufacturerCluster(CustomCluster):
    """SinopeManufacturerCluster manufacturer cluster."""

    FlowAlarm: Final = FlowAlarm
    AlarmAction: Final = AlarmAction
    PowerSource: Final = PowerSource
    EmergencyPower: Final = EmergencyPower
    AbnormalAction: Final = AbnormalAction
    FlowDuration: Final = FlowDuration

    cluster_id: Final[t.uint16_t] = SINOPE_MANUFACTURER_CLUSTER_ID
    name: Final = "SinopeManufacturerCluster"
    ep_attribute: Final = "sinope_manufacturer_specific"

    class AttributeDefs(foundation.BaseAttributeDefs):
        """Sinope Manufacturer Cluster Attributes."""

        unknown_attr_1: Final = foundation.ZCLAttributeDef(
            id=0x0001, type=t.Bool, access="rw", is_manufacturer_specific=True
        )
        firmware_number: Final = foundation.ZCLAttributeDef(
            id=0x0003, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        firmware_version: Final = foundation.ZCLAttributeDef(
            id=0x0004, type=t.CharacterString, access="r", is_manufacturer_specific=True
        )
        unknown_attr_5: Final = foundation.ZCLAttributeDef(
            id=0x0080, type=t.uint32_t, access="r", is_manufacturer_specific=True
        )
        unknown_attr_7: Final = foundation.ZCLAttributeDef(
            id=0x0101, type=Array, access="r", is_manufacturer_specific=True
        )
        status: Final = foundation.ZCLAttributeDef(
            id=0x0200, type=t.bitmap32, access="rp", is_manufacturer_specific=True
        )
        alarm_flow_threshold: Final = foundation.ZCLAttributeDef(
            id=0x0230, type=FlowAlarm, access="rw", is_manufacturer_specific=True
        )
        alarm_options: Final = foundation.ZCLAttributeDef(
            id=0x0231, type=AlarmAction, access="r", is_manufacturer_specific=True
        )
        flow_meter_config: Final = foundation.ZCLAttributeDef(
            id=0x0240, type=Array, access="rw", is_manufacturer_specific=True
        )
        valve_countdown: Final = foundation.ZCLAttributeDef(
            id=0x0241, type=t.uint32_t, access="rw", is_manufacturer_specific=True
        )
        power_source: Final = foundation.ZCLAttributeDef(
            id=0x0250, type=PowerSource, access="rw", is_manufacturer_specific=True
        )
        emergency_power_source: Final = foundation.ZCLAttributeDef(
            id=0x0251, type=EmergencyPower, access="rw", is_manufacturer_specific=True
        )
        abnormal_flow_duration: Final = foundation.ZCLAttributeDef(
            id=0x0252, type=FlowDuration, access="rw", is_manufacturer_specific=True
        )
        abnormal_flow_action: Final = foundation.ZCLAttributeDef(
            id=0x0253, type=AbnormalAction, access="rw", is_manufacturer_specific=True
        )
        cluster_revision: Final = foundation.ZCL_CLUSTER_REVISION_ATTR


class CustomBasicCluster(CustomCluster, Basic):
    """Custom Basic Cluster."""

    EnergySource: Final = EnergySource

    class AttributeDefs(Basic.AttributeDefs):
        """Sinope Manufacturer Basic Cluster Attributes."""

        power_source: Final = foundation.ZCLAttributeDef(
            id=0x0007, type=EnergySource, access="r", is_manufacturer_specific=True


class CustomMeteringCluster(CustomCluster, Metering):
    """Custom Metering Cluster."""

    ValveStatus: Final = ValveStatus
    UnitOfMeasure: Final = UnitOfMeasure

    DIVISOR = 0x0302
    _CONSTANT_ATTRIBUTES = {DIVISOR: 1000}

    class AttributeDefs(Metering.AttributeDefs):
        """Sinope Manufacturer Metering Cluster Attributes."""

        status: Final = foundation.ZCLAttributeDef(
            id=0x0200, type=ValveStatus, access="r", is_manufacturer_specific=True
        )
        unit_of_measure: Final = foundation.ZCLAttributeDef(
            id=0x0300, type=UnitOfMeasure, access="r", is_manufacturer_specific=True


class CustomFlowMeasurementCluster(CustomCluster, FlowMeasurement):
    """Custom flow measurement cluster that divides value by 10."""

    def _update_attribute(self, attrid, value):
        if attrid == self.AttributeDefs.measured_value.id:
            value = value / 10
        super()._update_attribute(attrid, value)


class SinopeTechnologiesValve(CustomDevice):
    """SinopeTechnologiesValve custom device."""

    signature = {
        # <SimpleDescriptor(endpoint=1, profile=260,
        # device_type=3, device_version=0,
        # input_clusters=[0, 1, 3, 4, 5, 6, 8, 2821, 65281]
        # output_clusters=[3, 25]>
        MODELS_INFO: [
            (SINOPE, "VA4200WZ"),
            (SINOPE, "VA4201WZ"),
            (SINOPE, "VA4200ZB"),
            (SINOPE, "VA4201ZB"),
            (SINOPE, "VA4220ZB"),
            (SINOPE, "VA4221ZB"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.LEVEL_CONTROLLABLE_OUTPUT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Ota.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    CustomBasicCluster,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Diagnostic.cluster_id,
                    SinopeManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Ota.cluster_id,
                ],
            }
        }
    }


class SinopeTechnologiesValveG2(CustomDevice):
    """SinopeTechnologiesValveG2 custom device."""

    signature = {
        # <SimpleDescriptor(endpoint=1, profile=260,
        # device_type=3, device_version=0,
        # input_clusters=[0, 1, 3, 4, 5, 6, 8, 1026, 1280, 1794, 2821, 65281]
        # output_clusters=[3, 6, 25]>
        MODELS_INFO: [
            (SINOPE, "VA4220ZB"),
            (SINOPE, "VA4221ZB"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha_p.PROFILE_ID,
                DEVICE_TYPE: zha_p.DeviceType.LEVEL_CONTROLLABLE_OUTPUT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    IasZone.cluster_id,
                    Metering.cluster_id,
                    Diagnostic.cluster_id,
                    SINOPE_MANUFACTURER_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    OnOff.cluster_id,
                    Ota.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    CustomBasicCluster,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    CustomFlowMeasurementCluster,
                    IasZone.cluster_id,
                    CustomMeteringCluster,
                    Diagnostic.cluster_id,
                    SinopeManufacturerCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    OnOff.cluster_id,
                    Ota.cluster_id,
                ],
            }
        }
    }
