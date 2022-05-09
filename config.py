# for ansible script
# config options

import psycopg2
from peewee import PostgresqlDatabase

database = PostgresqlDatabase(database="edge_monitoring", user="monitoring", password="msrg2016!", host="131.159.52.50", autorollback=True)