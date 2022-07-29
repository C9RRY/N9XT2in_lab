# import sqlite3
import psycopg2
from pathlib import Path

current_path = Path(__file__).resolve().parent.parent.parent
db_path = f'{Path(__file__).resolve().parent.parent.parent}/db.sqlite3'


def db_disable_station():
    print(db_path)
    conn = psycopg2.connect(dbname='lab_db', user='lab', password='fjfj', host='localhost')
    cursor = conn.cursor()
    sql = """ UPDATE radio_st_radios
      SET ready_to_play = false, play_now = false
      WHERE ready_to_play = true """
    cursor.execute(sql)
    conn.commit()


def db_enable_station(id):
    print(db_path)
    conn = psycopg2.connect(dbname='lab_db', user='lab', password='fjfj', host='localhost')
    cursor = conn.cursor()
    sql = f""" UPDATE radio_st_radios
      SET ready_to_play = true
      WHERE id = {id}"""
    cursor.execute(sql)
    conn.commit()
