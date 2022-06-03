from peewee import Model, TextField, CharField, IntegerField, DateTimeField, ForeignKeyField, FloatField
from .machine import Machine
from datetime import datetime
from config import DATABASE


class GPU(Model):
    name = CharField(verbose_name="GPU Name")
    machine = ForeignKeyField(model=Machine, verbose_name="Machine")
    min_freq = IntegerField(verbose_name="GPU min frequency in kHz")
    max_freq = IntegerField(verbose_name="GPU max frequency in kHz")

    class Meta:
        database = DATABASE


class GPUMeasurement(Model):
    gpu = ForeignKeyField(model=GPU, verbose_name="Assoc. GPU")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    frq = FloatField(verbose_name="GPU frequency at measurement time", null=True)
    val = IntegerField(verbose_name="GPU status", null=True)

    class Meta:
        database = DATABASE
