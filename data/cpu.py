from peewee import Model, TextField, CharField, IntegerField, DateTimeField, ForeignKeyField, PrimaryKeyField

from .machine import Machine
from datetime import datetime

from monitoring.config import DATABASE


class CPU(Model):
    name = CharField(verbose_name="CPU Name")
    machine = ForeignKeyField(model=Machine, verbose_name="Machine", primary_key=True)
    cores = IntegerField(verbose_name="Available CPU cores")
    min_freq = IntegerField(verbose_name="CPU min frequency")
    max_freq = IntegerField(verbose_name="CPU max frequency")

    class Meta:
        database = DATABASE


class CPUMeasurement(Model):
    cpu = ForeignKeyField(model=CPU, verbose_name="Assoc. CPU")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    freq = TextField(verbose_name="CPU frequency at measurement time", null=True)
    user = TextField(verbose_name="CPU user utilization in percent", null=True)
    nice = TextField(verbose_name="CPU nice utilization in percent", null=True)
    system = TextField(verbose_name="CPU system utilization in percent", null=True)
    idle = TextField(verbose_name="CPU idle in percent", null=True)

    class Meta:
        database = DATABASE
