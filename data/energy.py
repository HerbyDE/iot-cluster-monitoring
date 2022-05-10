from peewee import Model, TextField, CharField, IntegerField, FloatField, DateTimeField, IPField, ForeignKeyField

from datetime import datetime
from monitoring.config import DATABASE


class EnergyMonitor(Model):
    """
    Creates a monitoring instance for a device. You need a monitor for each device that measures power consumption.
    """
    experiment_name = CharField(verbose_name="Experiment Name")
    created = DateTimeField(verbose_name="Monitor Date & Time", default=datetime.now())
    device_name = CharField(verbose_name="Monitored device")
    device_ip = IPField(verbose_name="Device IP")
    remarks = TextField(verbose_name="Additional comments / remarks for the monitoring instance", null=True)

    class Meta:
        database = DATABASE


class EnergyMeasurement(Model):
    """
    Creates a database entry for a power measurement.
    """
    monitor = ForeignKeyField(model=EnergyMonitor, verbose_name="Linked Energy Monitor")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now())
    port = IntegerField(verbose_name="PoE Ethernet Port", null=True)
    power = CharField(verbose_name="Current energy consumption", null=True)
    max_avail_power = CharField(verbose_name="Max. possible energy consumption", null=True)
    current = CharField(verbose_name="Current current", null=True)
    voltage = CharField(verbose_name="Current voltage", null=True)
    pd_description = CharField(verbose_name="Power Delivery Additional Infos", null=True)

    class Meta:
        database = DATABASE

