from peewee import Model, TextField, DateTimeField, ForeignKeyField, BigIntegerField, FloatField

from .machine import Machine
from datetime import datetime
from monitoring.config import DATABASE


class Memory(Model):
    machine = ForeignKeyField(model=Machine, verbose_name="Assoc. Machine", primary_key=True)
    total = BigIntegerField(verbose_name="Total memory")
    total_swap = BigIntegerField(verbose_name="Swap size")
    comments = TextField(verbose_name="Comments & remarks regarding memory")

    class Meta:
        database = DATABASE


class MemoryMeasurement(Model):
    memory = ForeignKeyField(model=Memory, verbose_name="Memory")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    available = BigIntegerField(verbose_name="Available memory")
    free = BigIntegerField(verbose_name="Free physical memory")
    used = BigIntegerField(verbose_name="Used physical memory")
    percent = FloatField(verbose_name="Used physical memory in pct", null=True)
    wired = BigIntegerField(verbose_name="Wired memory", null=True)
    swap_free = BigIntegerField(verbose_name="Free swap", null=True)
    swap_used = BigIntegerField(verbose_name="Used swap", null=True)

    class Meta:
        database = DATABASE
