"""Module to handle quirks of the Sinopé Technologies water leak sensor and level monitor.

It add manufacturer attributes for IasZone cluster for the water leak alarm.
Supported devices are WL4200, WL4200S and LM4110-ZB
"""

import logging
from typing import Final

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.sinope import SINOPE, SINOPE_MANUFACTURER_CLUSTER_ID
from zhaquirks.sinope.switch import (
    SinopeTechnologiesMeteringCluster,
    SinopeTechnologiesBasicCluster,
    EnergySource,
)

import zigpy.profiles.zha as zha_p
import zigpy.types as t

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
    PERCENTAGE,
    DEGREE,
)

from zigpy.zcl.clusters.general import (
    AnalogInput,
    Basic,
    Identify,
    Ota,
    PollControl,
    PowerConfiguration,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic
from zigpy.zcl.clusters.measurement import TemperatureMeasurement
from zigpy.zcl.clusters.security import IasZone
from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.foundation import (
    BaseAttributeDefs,
    ZCLAttributeDef,
    ZCL_CLUSTER_REVISION_ATTR,
)


class LeakStatus(t.enum8):
    """Leak_status values."""

    Dry = 0x00
    Leak = 0x01


class DeviceStatus(t.bitmap32):
    """Device general status."""

    Ok = 0x00000000
    Temp_sensor = 0x00000020


class ZoneStatus(t.uint16_t):
    """IAS zone status"""

    Ok = 0x0030
    Connector_1 = 0x0031
    Connector_2 = 0x0032
    Low_battery = 0x0038
    Connector_low_bat = 0x003a


class SinopeManufacturerCluster(CustomCluster):
    """SinopeManufacturerCluster manufacturer cluster."""

    DeviceStatus: Final = DeviceStatus

    cluster_id: Final[t.uint16_t] = SINOPE_MANUFACTURER_CLUSTER_ID
    name: Final = "SinopeManufacturerCluster"
    ep_attribute: Final = "sinope_manufacturer_specific"

    class AttributeDefs(BaseAttributeDefs):
        """Sinope Manufacturer Cluster Attributes."""

        firmware_number: Final = ZCLAttributeDef(
            id=0x0003, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        firmware_version: Final = ZCLAttributeDef(
            id=0x0004, type=t.CharacterString, access="r", is_manufacturer_specific=True
        )
        unknown_attr_1: Final = ZCLAttributeDef(
            id=0x0030, type=t.uint8_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_2: Final = ZCLAttributeDef(
            id=0x0031, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        min_temperature_limit: Final = ZCLAttributeDef(
            id=0x0032, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        max_temperature_limit: Final = ZCLAttributeDef(
            id=0x0033, type=t.int16s, access="rw", is_manufacturer_specific=True
        )
        device_status: Final = ZCLAttributeDef(
            id=0x0034, type=t.bitmap8, access="rp", is_manufacturer_specific=True
        )
        unknown_attr_3: Final = ZCLAttributeDef(
            id=0x0035, type=t.uint16_t, access="r", is_manufacturer_specific=True
        )
        battery_type: Final = ZCLAttributeDef(
            id=0x0036, type=t.uint16_t, access="rw", is_manufacturer_specific=True
        )
        unknown_attr_4: Final = ZCLAttributeDef(
            id=0x0080, type=t.uint32_t, access="r", is_manufacturer_specific=True
        )
        status: Final = ZCLAttributeDef(
            id=0x0200, type=DeviceStatus, access="rp", is_manufacturer_specific=True
        )
        cluster_revision: Final = ZCL_CLUSTER_REVISION_ATTR


class SinopeTechnologiesIasZoneCluster(CustomCluster, IasZone):
    """SinopeTechnologiesIasZoneCluster custom cluster."""

    LeakStatus: Final = LeakStatus
    ZoneStatus: Final = ZoneStatus

    class AttributeDefs(IasZone.AttributeDefs):
        """Sinope Manufacturer IasZone Cluster Attributes."""

        zone_status: Final = ZCLAttributeDef(
            id=0x0002, type=ZoneStatus, access="p", is_manufacturer_specific=True
        )
        leak_status: Final = ZCLAttributeDef(
            id=0x0030, type=LeakStatus, access="rw", is_manufacturer_specific=True
        )


(
    # <SimpleDescriptor endpoint=1 profile=260 device_type=1026
    # device_version=0 input_clusters=[0, 1, 3, 1026, 1280, 2821, 65281]
    # output_clusters=[3, 25]>
    QuirkBuilder(SINOPE, "WL4200")
    .applies_to(SINOPE, "WL4200S")
    .replaces(SinopeTechnologiesIasZoneCluster)
    .replaces(SinopeManufacturerCluster)
    .enum( # power source
        attribute_name=SinopeTechnologiesBasicCluster.AttributeDefs.power_source.name,
        cluster_id=SinopeTechnologiesBasicCluster.cluster_id,
        enum_class=EnergySource,
        translation_key="power_source",
        fallback_name="Power source",
        entity_type=EntityType.STANDARD,
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
    .add_to_registry()
)

(
    # <SimpleDescriptor endpoint=1 profile=260 device_type=1026
    # device_version=0 input_clusters=[0, 1, 3, 20, 1026, 1280, 2821, 65281]
    # output_clusters=[3, 25]>
    QuirkBuilder(SINOPE, "WL4200")
    .applies_to(SINOPE, "WL4200S")
    .replaces(SinopeTechnologiesIasZoneCluster)
    .replaces(SinopeManufacturerCluster)
    .binary_sensor(# Device status
        "device_status",
        SinopeManufacturerCluster.cluster_id,
        endpoint_id=1,
        device_class=BinarySensorDeviceClass.TAMPER,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="device_status",
        fallback_name="Device status",
    )
    .enum( # Power source
        attribute_name=SinopeTechnologiesBasicCluster.AttributeDefs.power_source.name,
        cluster_id=SinopeTechnologiesBasicCluster.cluster_id,
        enum_class=EnergySource,
        translation_key="power_source",
        fallback_name="Power source",
        entity_type=EntityType.STANDARD,
    )
    .number( # Checkin interval
        PollControl.AttributeDefs.checkin_interval.name,
        PollControl.cluster_id,
        step=60,
        min_value=3600,
        max_value=21600,
        unit=UnitOfTime.SECONDS,
        translation_key="checkin_interval",
        fallback_name="Checkin interval",
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
    .add_to_registry()
)

(
    # <SimpleDescriptor endpoint=1 profile=260 device_type=0
    # device_version=0 input_clusters=[0, 1, 3, 12, 32, 1026, 2821, 65281]
    # output_clusters=[25]>
    QuirkBuilder(SINOPE, "LM4110-ZB")
    .replaces(SinopeManufacturerCluster)
    .binary_sensor( # status
        "status",
        SinopeManufacturerCluster.cluster_id,
        endpoint_id=1,
        device_class=BinarySensorDeviceClass.TAMPER,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="status",
        fallback_name="Status",
    )
    .sensor( # Battery voltage
        PowerConfiguration.AttributeDefs.battery_voltage.name,
        PowerConfiguration.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        reporting_config=ReportingConfig(
            min_interval=60, max_interval=43200, reportable_change=1
        ),
        translation_key="battery_voltage",
        fallback_name="Battery voltage",
    )
    .sensor( # Gauge angle
        AnalogInput.AttributeDefs.present_value.name,
        AnalogInput.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        unit=DEGREE,
        device_class=SensorDeviceClass.VOLUME_STORAGE,
        reporting_config=ReportingConfig(
            min_interval=5, max_interval=3600, reportable_change=1
        ),
        translation_key="gauge_angle",
        fallback_name="Gauge angle",
    )
    .add_to_registry()
)
