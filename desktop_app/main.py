import tkinter as tk
import uuid
from tkinter import ttk
from models import DBOrder
from create_excel import paste_to_order, paste_to_warranty
from datetime import datetime


def open_order():
    Order()


def select_name_for_warranty():
    db_options_select = ' WHERE is_fixed = "0"'
    SetClient(db_options_select)


def select_all_order():
    db_options_select = ''
    SetClient(db_options_select)


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='grey', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img1 = tk.PhotoImage(file='static/img/Contact.gif')
        self.add_img2 = tk.PhotoImage(file='static/img/Clipboard.gif')
        self.add_img3 = tk.PhotoImage(file='static/img/Copy2.gif')
        self.add_img4 = tk.PhotoImage(file='static/img/Refresh.gif')
        btn_open_dialog = tk.Button(toolbar, text='Прийомка', command=open_order, bg='#414146', bd=0,
                                    compound=tk.TOP, image=self.add_img1)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_open_dialog = tk.Button(toolbar, text='Гарантійка', command=select_name_for_warranty, bg='#414146', bd=0,
                                    compound=tk.TOP, image=self.add_img2)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_open_dialog = tk.Button(toolbar, text='Всі талони', command=select_all_order, bg='#414146', bd=0,
                                    compound=tk.TOP, image=self.add_img3)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_open_dialog = tk.Button(toolbar, text='Оновити DB', command=self.upload_db, bg='#414146', bd=0,
                                    compound=tk.TOP, image=self.add_img4)
        btn_open_dialog.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, column=('ID', 'is_fixed', 'brand', 'package', 'breakage', 'name', 'phone_number'),
                                 height=15, show='headings')
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('is_fixed', width=30, anchor=tk.CENTER)
        self.tree.column('brand', width=120, anchor=tk.CENTER)
        self.tree.column('package', width=150, anchor=tk.CENTER)
        self.tree.column('breakage', width=100, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('phone_number', width=140, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('is_fixed', text='Fix')
        self.tree.heading('brand', text='Модель')
        self.tree.heading('package', text='Комплектація')
        self.tree.heading('breakage', text='Опис несправності')
        self.tree.heading('name', text='П.І.Б. клієнта')
        self.tree.heading('phone_number', text='Контактний')

        self.tree.pack()

    def record_order(self, brand, package, breakage, name, phone_number, date):
        slug = str(uuid.uuid1())
        self.db.insert_order(brand, package, breakage, name, phone_number, date, slug)
        paste_to_order(brand, name, phone_number, package, breakage, date, slug)
        self.view_records()

    def record_warranty(self, id, break_fix, price, warranty, date):
        self.db.insert_warranty(id, break_fix, price, warranty, date)
        paste_to_warranty(id, break_fix, date, price, warranty)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''
        SELECT * FROM repair_shop_clientcard
        ORDER BY id DESC''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def upload_db(self):
        pass


class Order(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('New')
        self.geometry('750x250+400+300')
        self.resizable(False, False)

        label_brand = tk.Label(self, text='Модель')
        label_brand.place(x=20, y=10)
        self.entry_brand = ttk.Entry(self, width=70)
        self.entry_brand.place(x=150, y=10)

        label_package = tk.Label(self, text='Комплектація')
        label_package.place(x=20, y=50)
        self.entry_package = ttk.Entry(self, width=70)
        self.entry_package.place(x=150, y=50)

        label_breakage = tk.Label(self, text='Поломка')
        label_breakage.place(x=20, y=90)
        self.entry_breakage = ttk.Entry(self, width=70)
        self.entry_breakage.place(x=150, y=90)

        label_name = tk.Label(self, text='П.І.Б.')
        label_name.place(x=20, y=130)
        self.entry_name = ttk.Entry(self, width=70)
        self.entry_name.place(x=150, y=130)

        label_phone = tk.Label(self, text='Номер телефона')
        label_phone.place(x=20, y=170)
        self.entry_phone = ttk.Entry(self, width=70)
        self.entry_phone.place(x=150, y=170)

        btn_cancel = ttk.Button(self, text='вихід', command=self.destroy)
        btn_cancel.place(x=650, y=210)

        btn_ok = ttk.Button(self, text='друк', command=self.destroy)
        btn_ok.place(x=550, y=210)
        btn_ok.bind(
            '<Button-1>', lambda event: self.view.record_order(
                self.entry_brand.get(), self.entry_package.get(), self.entry_breakage.get(),
                self.entry_name.get(), self.entry_phone.get(), datetime.now()
            )
        )

        self.grab_set()
        self.focus_set()


class SetClient(tk.Toplevel):
    def __init__(self, db_options_select):
        super().__init__(root)
        self.db_options_select = db_options_select
        self.db = db
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('New')
        self.geometry('450x150+400+300')
        self.resizable(False, False)
        client_list = []
        self.db.c.execute(f'''SELECT name, id FROM repair_shop_clientcard{self.db_options_select}''')
        for i in self.db.c.fetchall():
            client_list.append(i[0])
        val = tuple(set(client_list))

        self.combobox = ttk.Combobox(self)
        self.combobox['values'] = val
        self.combobox.current(0)
        self.combobox.place(x=20, y=30)

        btn_ok = ttk.Button(self, text='додати', command=self.open_warranty)
        btn_ok.place(x=350, y=110)

    def open_warranty(self):
        name = self.combobox.get()
        Warranty(name)
        self.destroy()


class Warranty(tk.Toplevel):
    def __init__(self, name):
        super().__init__(root)
        self.name = name
        self.db = db
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('New')
        self.geometry('750x350+400+300')
        self.resizable(False, False)
        client_list = []
        self.db.c.execute(
            f'''SELECT name, id, brand, breakage, break_fix, price, warranty FROM repair_shop_clientcard
             WHERE is_fixed = "0" and name = "{self.name}"''')
        for i in self.db.c.fetchall():
            client_list.append(f'id:{i[1]} ({i[2]}) {i[3]}')
        val = tuple(client_list)

        label_name = tk.Label(self, text=f'{self.name}', font=("Aerial", 16))
        label_name.place(x=200, y=10)

        label_id = tk.Label(self, text='список ремонтів')
        label_id.place(x=20, y=90)
        self.combobox = ttk.Combobox(self, width=75)
        self.combobox['values'] = val
        self.combobox.current(0)
        self.combobox.place(x=20, y=110)

        label_break_fix = tk.Label(self, text='Проведений ремонт')
        label_break_fix.place(x=20, y=150)
        self.entry_break_fix = ttk.Entry(self, width=76)
        self.entry_break_fix.place(x=20, y=170)

        label_price = tk.Label(self, text='Ціна')
        label_price.place(x=20, y=210)
        self.entry_price = ttk.Entry(self, width=20)
        self.entry_price.place(x=20, y=230)

        label_warranty = tk.Label(self, text='Гарантія')
        label_warranty.place(x=20, y=270)
        self.entry_warranty = ttk.Entry(self, width=20)
        self.entry_warranty.place(x=20, y=290)

        btn_cancel = ttk.Button(self, text='вихід', command=self.destroy)
        btn_cancel.place(x=650, y=310)

        btn_ok = ttk.Button(self, text='друк', command=self.print_warranty)
        btn_ok.place(x=550, y=310)
        btn_ok.bind(
            '<Button-1>', lambda event: self.view.record_warranty(
                self.combobox.get(), self.entry_break_fix.get(), self.entry_price.get(),
                self.entry_warranty.get(), datetime.now()
            )
        )

        self.grab_set()
        self.focus_set()

    def print_warranty(self):
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    db = DBOrder()
    app = Main(root)
    app.pack()
    root.title("Repair Shop")
    root.geometry("750x500+300+200")
    root.resizable(False, False)
    root.mainloop()