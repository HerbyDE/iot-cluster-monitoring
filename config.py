# for ansible script
# config options
import psycopg2
from peewee import PostgresqlDatabase

DATABASE = PostgresqlDatabase(database="edge_monitoring", user="monitoring", password="monitoring", host="131.159.52.50", autorollback=True)

LAUNCH_VAR = None
STOP_VAR = None
# TODO: environment variable for measurement frequency