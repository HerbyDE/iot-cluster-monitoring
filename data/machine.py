from peewee import Model, TextField, CharField, IntegerField, FloatField, DateTimeField, IPField, BooleanField
from datetime import datetime
from config import DATABASE


class Machine(Model):
    """
    This class creates a database entry for a device and registers key attributes.
    """
    name = CharField(verbose_name="Device name")
    ip = TextField(verbose_name="IP Address")
    mac_addr = CharField(verbose_name="MAC address", primary_key=True)
    device_architecture = TextField(verbose_name="Device Architecture")
    device_class = TextField(verbose_name="Device Type")
    operating_system = TextField(verbose_name="Device OS")
    storage = FloatField(verbose_name="Total available storage", null=True)
    bandwidth = FloatField(verbose_name="Total available bandwidth", null=True)
    has_gpu = BooleanField(verbose_name="Device has GPU", default=False)
    gpu_details = TextField(verbose_name="GPU details", null=True)
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)

    class Meta:
        database = DATABASE
