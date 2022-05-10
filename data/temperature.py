from peewee import Model, TextField, CharField, IntegerField, DateTimeField, ForeignKeyField
from machine import Machine
from datetime import datetime
from config import DATABASE


class Temperature:
    machine = ForeignKeyField(model=Machine, verbose_name="Assoc. Machine", primary_key=True)

class TemperatureMeasurement:
    

    class Meta:
        database = DATABASE