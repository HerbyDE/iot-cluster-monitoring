# this python file is for connecting to our edge_monitoring database
import psycopg2
from peewee import PostgresqlDatabase


def start_db(models: list, database: PostgresqlDatabase) -> None:
    database.connect()
    database.create_tables(models, safe=True)


def teardown_db(models, database: PostgresqlDatabase):
    database.connect()
    database.drop_tables(models)


# cur.execute("""SELECT * FROM devices""")
# query_results = cur.fetchall()
# print(query_results)


