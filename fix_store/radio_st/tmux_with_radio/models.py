import sqlite3
from pathlib import Path

current_path = Path(__file__).resolve().parent.parent.parent
db_path = f'{Path(__file__).resolve().parent.parent.parent}/db.sqlite3'


def db_disable_station():
    print(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = """ UPDATE radio_st_radios
      SET ready_to_play = 0, play_now = 0
      WHERE ready_to_play = 1 """
    cursor.execute(sql)
    conn.commit()


def db_enable_station(id):
    print(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f""" UPDATE radio_st_radios
      SET ready_to_play = 1
      WHERE id = {id}"""
    cursor.execute(sql)
    conn.commit()
