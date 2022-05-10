from peewee import Model, TextField, CharField, IntegerField, DateTimeField, ForeignKeyField, PrimaryKeyField

from .machine import Machine
from datetime import datetime

from config import DATABASE


class GPU(Model):
    name = CharField(verbose_name="GPU Name")
    machine = ForeignKeyField(model=Machine, verbose_name="Machine", primary_key=True)
    cores = IntegerField(verbose_name="Available GPU cores")
    min_freq = IntegerField(verbose_name="GPU min frequency")
    max_freq = IntegerField(verbose_name="GPU max frequency")

    class Meta:
        database = DATABASE


class GPUMeasurement(Model):
    gpu = ForeignKeyField(model=GPU, verbose_name="Assoc. GPU")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    freq = TextField(verbose_name="GPU frequency at measurement time", null=True)
    user = TextField(verbose_name="GPU user utilization in percent", null=True)
    nice = TextField(verbose_name="GPU nice utilization in percent", null=True)
    system = TextField(verbose_name="GPU system utilization in percent", null=True)
    idle = TextField(verbose_name="GPU idle in percent", null=True)

    class Meta:
        database = DATABASE

