import sqlite3
import re


db_path = '/home/f1r980y/PycharmProjects/N9XT2/fix_store/db.sqlite3'


class DBOrder:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.conn.commit()

    def insert_order(self, brand, package, breakage, name, phone_number, date, slug, is_fixed=False, master_id=1):
        in_date = date
        self.c.execute(
            '''INSERT INTO repair_shop_clientcard
            (is_fixed, brand, package, breakage, name, phone_number, in_date, master_id, slug)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (is_fixed, brand, package, breakage, name, phone_number, in_date, master_id, slug)
        )
        self.conn.commit()

    def insert_warranty(self, id, break_fix, price, warranty, date):
        re_digits = re.compile(r"\b\d+\b")
        id = re_digits.findall(id)[0]
        # self.c.execute(
        #     '''INSERT INTO repair_shop_clientcard(break_fix, price, warranty, out_date)
        #     VALUES(?, ?, ?, ?)''', (break_fix, price, warranty, date)
        # )
        self.c.execute(
            f'''UPDATE repair_shop_clientcard
            SET break_fix = ?, price = ?, warranty = ?, out_date = ?, is_fixed = ?
            WHERE id = {id}''', (break_fix, price, warranty, date, 1)
        )
        self.conn.commit()

