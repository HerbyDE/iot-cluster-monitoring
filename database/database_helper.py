# this python file is for connecting to our edge_monitoring database
import psycopg2
from peewee import *
from playhouse.db_url import connect

database = PostgresqlDatabase(database="edge_monitoring", user="monitoring", password="monitoring",
                              host="172.24.18.12", autorollback=True)


class BaseModel(Model):
    class Meta:
        database = database


def start_db(models: list, database: PostgresqlDatabase) -> None:
    database.connect()
    print("reached start_db")
    database.create_tables(models, safe=True)


def teardown_db(models, database: PostgresqlDatabase):
    database.connect()
    database.drop_tables(models)

# cur.execute("""SELECT * FROM devices""")
# query_results = cur.fetchall()
# print(query_results)
