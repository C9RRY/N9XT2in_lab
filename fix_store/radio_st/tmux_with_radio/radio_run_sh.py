import subprocess
import time
# import sqlite3
import psycopg2
from pathlib import Path
from radio import cli

current_path = Path(__file__).resolve().parent.parent.parent
db_path = f'{Path(__file__).resolve().parent.parent.parent}/db.sqlite3'


def play_st():
    cycle = 0
    tmux_run = 0
    while True:
        cycle += 1
        conn = psycopg2.connect(dbname='lab_db', user='lab', password='fjfj', host='localhost')
        cursor = conn.cursor()
        sql = 'SELECT * FROM radio_st_radios' \
              ' WHERE ready_to_play = True '
        cursor.execute(sql)
        stations_info = cursor.fetchall()
        if stations_info:
            if stations_info[0][4] == 0 or cycle == 1:
                url = stations_info[0][2]
                station_id = stations_info[0][0]
                subprocess.call(['sh', f'{Path(__file__).resolve().parent}/radio.sh',
                                 f'{Path(__file__).resolve().parent}', f'{url}'])

                conn = psycopg2.connect(dbname='lab_db', user='lab', password='fjfj', host='localhost')
                cursor = conn.cursor()
                sql = f""" UPDATE radio_st_radios
                  SET play_now = True
                  WHERE id = {station_id }"""
                cursor.execute(sql)
                conn.commit()
                tmux_run = 1
        if not stations_info and tmux_run == 1:
            subprocess.call(['tmux', 'kill-session', '-t', 'first'])
            tmux_run = 0
        time.sleep(1)


if __name__ == '__main__':
    play_st()
