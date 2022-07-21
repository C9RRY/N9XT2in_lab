import subprocess
import time
import sqlite3
from pathlib import Path

current_path = Path(__file__).resolve().parent.parent.parent
db_path = f'{Path(__file__).resolve().parent.parent.parent}/db.sqlite3'
print(db_path)


def play_st():
    cycle = 1
    tmux_run = 0
    while True:
        cycle += 1
        print('cycle', cycle)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        sql = 'SELECT * FROM radio_st_radios' \
              ' WHERE ready_to_play = 1 '
        cursor.execute(sql)
        stations_info = cursor.fetchall()
        if stations_info:
            print(stations_info)
            if stations_info[0][4] == 0:
                url = stations_info[0][2]
                station_id = stations_info[0][0]
                subprocess.call(['sh', f'{Path(__file__).resolve().parent}/radio.sh',
                                 f'{Path(__file__).resolve().parent}', f'{url}'])

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                sql = f""" UPDATE radio_st_radios
                  SET play_now = 1
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