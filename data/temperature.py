from peewee import Model, TextField, DateTimeField, ForeignKeyField, DoubleField
from .machine import Machine
from datetime import datetime
from config import DATABASE


class Temperature(Model):
    machine = ForeignKeyField(model=Machine, verbose_name="Assoc. Machine", primary_key=True)
    label = TextField(verbose_name="Label of the sensor", null=True)
    high = DoubleField(verbose_name="Highest temperature", null=True)
    critical = DoubleField(verbose_name="Critical temperature")

    class Meta:
        database = DATABASE


class TemperatureMeasurement(Model):
    temp = ForeignKeyField(model=Temperature, verbose_name="Assoc. Temperature")
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    current = DoubleField(verbose_name="Current temperature")

    class Meta:
        database = DATABASE
