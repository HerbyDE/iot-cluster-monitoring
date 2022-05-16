# this python file is for connecting to our edge_monitoring database
import psycopg2
from peewee import *
from playhouse.db_url import connect

# try 172.24.18.12 for jetson 3 for testing in the same subnet, 131.159.52.50 is for the Monitoring VM
database = PostgresqlDatabase(database="edge_monitoring", user="monitoring", password="monitoring",
                              host="131.159.52.50", autorollback=True)


class BaseModel(Model):
    class Meta:
        database = database


def start_db(models: list, database: PostgresqlDatabase) -> None:
    database.connect()
    database.create_tables(models, safe=True)


def teardown_db(models, database: PostgresqlDatabase):
    database.connect()
    database.drop_tables(models)

# cur.execute("""SELECT * FROM devices""")
# query_results = cur.fetchall()
# print(query_results)
