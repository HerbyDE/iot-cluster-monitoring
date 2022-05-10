from peewee import Model, TextField, DateTimeField, ForeignKeyField, DoubleField
from machine import Machine
from datetime import datetime
from config import DATABASE


class Temperature:
    machine = ForeignKeyField(model=Machine, verbose_name="Assoc. Machine", primary_key=True)

    class Meta:
        database = DATABASE


class TemperatureMeasurement:
    timestamp = DateTimeField(verbose_name="Measurement timestamp", default=datetime.now)
    current = DoubleField(verbose_name="Current temperature")
    high = DoubleField(verbose_name="Highest temperature")
    critical = DoubleField(verbose_name="Critical temperature")
    label = TextField(verbose_name="Label of the sensor")

    class Meta:
        database = DATABASE
