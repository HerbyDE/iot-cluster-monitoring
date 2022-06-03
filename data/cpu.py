from peewee import Model, FloatField, CharField, IntegerField, DateTimeField, ForeignKeyField, FloatField

from .machine import Machine
from datetime import datetime

from config import DATABASE


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
    freq_0 = FloatField(verbose_name="CPU frequency at measurement time", null=True)
    freq_1 = FloatField(verbose_name="CPU frequency at measurement time", null=True)
    freq_2 = FloatField(verbose_name="CPU frequency at measurement time", null=True)
    freq_3 = FloatField(verbose_name="CPU frequency at measurement time", null=True)
    user_0 = FloatField(verbose_name="CPU user utilization in percent", null=True)
    user_1 = FloatField(verbose_name="CPU user utilization in percent", null=True)
    user_2 = FloatField(verbose_name="CPU user utilization in percent", null=True)
    user_3 = FloatField(verbose_name="CPU user utilization in percent", null=True)
    nice_0 = FloatField(verbose_name="CPU nice utilization in percent", null=True)
    nice_1 = FloatField(verbose_name="CPU nice utilization in percent", null=True)
    nice_2 = FloatField(verbose_name="CPU nice utilization in percent", null=True)
    nice_3 = FloatField(verbose_name="CPU nice utilization in percent", null=True)
    system_0 = FloatField(verbose_name="CPU system utilization in percent", null=True)
    system_1 = FloatField(verbose_name="CPU system utilization in percent", null=True)
    system_2 = FloatField(verbose_name="CPU system utilization in percent", null=True)
    system_3 = FloatField(verbose_name="CPU system utilization in percent", null=True)
    idle_0 = FloatField(verbose_name="CPU idle in percent", null=True)
    idle_1 = FloatField(verbose_name="CPU idle in percent", null=True)
    idle_2 = FloatField(verbose_name="CPU idle in percent", null=True)
    idle_3 = FloatField(verbose_name="CPU idle in percent", null=True)

    class Meta:
        database = DATABASE
