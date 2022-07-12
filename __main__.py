#!/usr/bin/env python3

# https://stackoverflow.com/questions/57133810/changing-tab-widgets-from-another-tab-in-tkinter
# https://www.abstractapi.com/guides/validate-phone-number-python


def exit_tk():
    app.withdraw()

    if askyesno(title="SRM Fashion", message="Are you sure do you want to quit?"):
        print(Fore.RED + "Bye!!!")
        database.close()
        app.destroy()
        terminate()

    else:
        app.deiconify()


def delete_record():
    selected_item = treeview_db.focus()

    if selected_item:
        row_dict = treeview_db.item(selected_item)
        row_values = row_dict.get("values")
        phone: str = row_values[1]

        treeview_db.delete(selected_item)

        cursor.execute(f"""DELETE FROM Customers where Phone = '{phone}'""")
        database.commit()

        _ = len(treeview_db.get_children())

        if _:
            total_customer_label.config(text=f"{_} customer(s) found!")

        else:
            total_customer_label.config(text="No customer(s) found!")

        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}", message="1 Row deleted successfully..."
        )
        app.deiconify()
        return

    else:
        print(Fore.YELLOW + f"INFO: Please select a customer record!")

        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please select a customer record!",
        )
        app.deiconify()
        return


def validate_and_save():
    if name_label["fg"] == "red":
        name_label.config(fg="black")

    if phone_label["fg"] == "red":
        phone_label.config(fg="black")

    if email_label["fg"] == "red":
        email_label.config(fg="black")

    name: str = name_entry.get().strip().title()
    phone: str = phone_entry.get().strip()
    email: str = email_entry.get().strip().lower()
    dob: str = dob_entry.get().strip()
    gender: str = gender_var.get()

    if name == "":
        name_label.config(fg="red")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter customer name.",
        )
        app.deiconify()
        return

    if phone == "":
        phone_label.config(fg="red")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter contact number.",
        )
        app.deiconify()
        return

    try:
        number_object = parse(number=phone)
        phone: str = format_number(
            numobj=number_object, num_format=PhoneNumberFormat.INTERNATIONAL
        )

    except NumberParseException as number_parse_exception:
        print(Fore.RED + f"ERROR: {number_parse_exception}")
        phone_label.config(fg="red")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"{number_parse_exception} Use with country codes. eg. +1-XXX-XXX-XXXX",
        )
        app.deiconify()
        return

    if not is_valid_number(numobj=number_object):
        phone_label.config(fg="red")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter the correct mobile number.",
        )
        app.deiconify()
        return

    if email != "":
        split_email = email.split(sep="@")
        if len(split_email) == 2:
            if not len(split_email[0]) or not len(split_email[1]):
                email_label.config(fg="red")
                app.withdraw()
                showinfo(
                    title=f"SRM Fashion {__version__}",
                    message="Invalid email address, Try again...",
                )
                app.deiconify()
                return

        else:
            email_label.config(fg="red")
            app.withdraw()
            showinfo(
                title=f"SRM Fashion {__version__}",
                message="Invalid email address, Try again...",
            )
            app.deiconify()
            return

    cursor.execute("""SELECT Phone FROM Customers""")
    for _ in cursor.fetchall():
        if _[0] == phone:
            app.withdraw()
            showinfo(
                title=f"SRM Fashion {__version__}",
                message=f"{phone} Contact already exists!",
            )
            app.deiconify()
            return

    cursor.execute(
        f"""INSERT INTO Customers VALUES (
    "{name}", "{phone}", "{email}", "{dob}", "{gender}"
    )"""
    )
    database.commit()

    total_customer_label.config(
        text=f"{len(treeview_db.get_children()) + 1} customer(s) found!"
    )
    treeview_db.insert(parent="", index="end", values=[name, phone, email, dob, gender])

    name_entry.delete(first=0, last=END)
    phone_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    dob_entry.delete(first=0, last=END)
    gender_var.set(value=gender_options[0])

    name_entry.focus()

    print(Fore.GREEN + "INFO: Database appended successfully...")

    app.withdraw()
    showinfo(title=f"SRM Fashion {__version__}", message="Data saved successfully!")
    app.deiconify()
    return


try:
    print("INFO: Importing built-in libraries...")
    from getpass import getuser
    from os.path import isfile, join, split
    from sqlite3 import connect
    from sys import exit as terminate
    from tkinter import (
        BOTH,
        BOTTOM,
        BROWSE,
        CENTER,
        END,
        RIGHT,
        TOP,
        Button,
        Entry,
        Frame,
        Label,
        LabelFrame,
        OptionMenu,
        StringVar,
        Tk,
        W,
        X,
    )
    from tkinter.messagebox import askyesno, showinfo
    from tkinter.ttk import Notebook, Treeview

    print("INFO: Importing third party libraries...")
    from colorama import Fore, init
    from phonenumbers import PhoneNumberFormat, format_number, is_valid_number, parse
    from phonenumbers.phonenumberutil import NumberParseException

    print("INFO: Initializing colorama...")
    init(autoreset=True)

    __version__: str = "v.20220712"
    accent_color_light: str = "lightsteelblue2"
    total_orders: int = 0
    username: str = getuser()
    base_path: str = split(p=__file__)[0]
    database_path: str = join(base_path, "customers.db")

    if not isfile(path=database_path):
        print(Fore.GREEN + "INFO: Creating a new database...")
        database = connect(database=database_path)
        cursor = database.cursor()
        cursor.execute(
            """CREATE TABLE Customers (
             Name TEXT,
             Phone TEXT,
             Email TEXT,
             DOB TEXT,
             Gender TEXT
             )"""
        )
        database.commit()
        database.close()

    print(Fore.GREEN + "INFO: Reading database file...")
    database = connect(database=database_path)
    cursor = database.cursor()
    cursor.execute("""SELECT * FROM Customers""")
    customers_data: list = cursor.fetchall()

    print(Fore.GREEN + "INFO: Loading GUI application...")
    app: Tk = Tk()
    app.resizable(width=False, height=False)
    app.title(string=f"SRM Fashion {__version__}")
    app.protocol(name="WM_DELETE_WINDOW", func=exit_tk)
    app.bind(sequence="<Escape>", func=lambda event: exit_tk())
    app.config(bg=accent_color_light)

    Label(
        master=app,
        text=f"Hello {username.title()}, Welcome to SRM Fashion!",
        bg="black",
        fg="white",
    ).pack(side=TOP, fill=X)

    tab_view: Notebook = Notebook(master=app)
    tab_view.pack(fill=BOTH, expand=True)

    orders_frame: Frame = Frame(master=tab_view, bg=accent_color_light)
    orders_frame.pack()

    tab_view.add(child=orders_frame, text="Orders")

    Label(
        master=orders_frame,
        text="Order List",
        font=("Times New Roman", 22, "underline"),
        bg=accent_color_light,
    ).pack(pady=10)

    if total_orders == 0:
        Label(
            master=orders_frame,
            text="You have zero orders!",
            fg="red",
            bg=accent_color_light,
        ).pack()

    order_labelframe: LabelFrame = LabelFrame(
        master=orders_frame, text="Add Order", fg="red", bg=accent_color_light
    )
    order_labelframe.pack(side=BOTTOM, padx=10, pady=5, ipady=3, fill=X)

    order_button: Button = Button(
        master=order_labelframe,
        text="Add an Order",
        bg="black",
        fg="white",
        width=14,
        command=lambda: tab_view.select(tab_id=1),
    )
    order_button.bind(sequence="<Return>", func=lambda event: tab_view.select(tab_id=1))
    order_button.grid(row=0, column=0, padx=5)

    exit_button: Button = Button(
        master=order_labelframe,
        text="Exit",
        bg="red",
        fg="white",
        width=14,
        command=exit_tk,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_tk())
    exit_button.grid(row=0, column=1, padx=5)

    customers_frame: Frame = Frame(master=tab_view, bg=accent_color_light)
    customers_frame.pack()

    tab_view.add(child=customers_frame, text="Customers")

    customer_labelframe_1: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Select a Customers",
        fg="red",
        bg=accent_color_light,
    )
    customer_labelframe_1.pack(padx=10, pady=3, ipady=3, fill=X)

    Label(
        master=customer_labelframe_1,
        text="Select Customer",
        font=("Times New Roman", 22, "underline"),
        bg=accent_color_light,
    ).pack(pady=10)

    total_customer_label: Label = Label(
        master=customer_labelframe_1, fg="red", bg=accent_color_light
    )
    total_customer_label.pack()

    header_list: list = ["Name", "Phone", "Email", "D.O.B", "Gender"]
    treeview_db: Treeview = Treeview(
        master=customer_labelframe_1,
        show="headings",
        columns=header_list,
        selectmode=BROWSE,
    )

    for _ in header_list:
        treeview_db.heading(column=_, text=_)

    treeview_db.column(column=0, width=130, minwidth=130, anchor=W)
    treeview_db.column(column=1, width=130, minwidth=130, anchor=CENTER)
    treeview_db.column(column=2, width=225, minwidth=225, anchor=W)
    treeview_db.column(column=3, width=100, minwidth=100, anchor=CENTER)
    treeview_db.column(column=4, width=80, minwidth=80, anchor=W)

    for _ in customers_data:
        treeview_db.insert(parent="", index="end", values=_)

    treeview_db.pack(padx=20, pady=5)

    total_customers: int = len(treeview_db.get_children())

    delete_button: Button = Button(
        master=customer_labelframe_1,
        text="Delete Record",
        bg="red",
        fg="white",
        command=delete_record,
    )
    delete_button.bind(sequence="<Return>", func=lambda event: delete_record())
    delete_button.pack(side=RIGHT, padx=10, pady=5)

    if total_customers:
        total_customer_label.config(text=f"{total_customers} customer(s) found!")

    else:
        total_customer_label.config(text="No customer(s) found!")

    Label(master=customers_frame, text="or", bg=accent_color_light).pack()

    customer_labelframe_2: LabelFrame = LabelFrame(
        master=customers_frame, text="Add New Customer", fg="red", bg=accent_color_light
    )
    customer_labelframe_2.pack(padx=10, pady=3, ipady=3, fill=X)

    Label(
        master=customer_labelframe_2,
        text="Enter Details",
        font=("Times New Roman", 22, "underline"),
        bg=accent_color_light,
    ).pack(pady=10)

    customer_entry_frame: Frame = Frame(
        master=customer_labelframe_2, bg=accent_color_light
    )
    customer_entry_frame.pack(padx=10)

    name_label: Label = Label(
        master=customer_entry_frame,
        text="Enter Customer Name:",
        bg=accent_color_light,
    )
    name_label.grid(row=0, column=0, padx=5)
    name_entry: Entry = Entry(master=customer_entry_frame, width=25)
    name_entry.grid(row=0, column=1, padx=5)

    phone_label: Label = Label(
        master=customer_entry_frame, text="Contact Number:", bg=accent_color_light
    )
    phone_label.grid(row=1, column=0)
    phone_entry: Entry = Entry(master=customer_entry_frame, width=25)
    phone_entry.grid(row=1, column=1)

    email_label: Label = Label(
        master=customer_entry_frame, text="Email (Optional):", bg=accent_color_light
    )
    email_label.grid(row=2, column=0)
    email_entry: Entry = Entry(master=customer_entry_frame, width=25)
    email_entry.grid(row=2, column=1)

    Label(
        master=customer_entry_frame,
        text="Date of Birth (Optional):",
        bg=accent_color_light,
    ).grid(row=3, column=0)
    dob_entry: Entry = Entry(customer_entry_frame, width=25)
    dob_entry.grid(row=3, column=1)

    Label(master=customer_entry_frame, text="Gender:", bg=accent_color_light).grid(
        row=4, column=0
    )
    gender_options: list = ["Female", "Male", "Other"]
    gender_var: StringVar = StringVar()
    gender_var.set(value=gender_options[0])
    gender_dropdown = OptionMenu(customer_entry_frame, gender_var, *gender_options)
    gender_dropdown.grid(row=4, column=1)

    save_button: Button = Button(
        master=customer_labelframe_2,
        text="Save & Continue",
        bg="red",
        fg="white",
        command=validate_and_save,
    )
    save_button.bind(sequence="<Return>", func=lambda event: validate_and_save())
    save_button.pack(padx=10, pady=5, side=RIGHT)

    customer_labelframe: LabelFrame = LabelFrame(
        master=customers_frame, text="Select Customer", fg="red", bg=accent_color_light
    )
    customer_labelframe.pack(side=BOTTOM, padx=10, pady=5, ipady=3, fill=X)

    customer_button: Button = Button(
        master=customer_labelframe,
        text="Select Contact",
        bg="black",
        fg="white",
        width=14,
    )
    customer_button.grid(row=0, column=0, padx=5)

    exit_button: Button = Button(
        master=customer_labelframe,
        text="Exit",
        bg="red",
        fg="white",
        width=14,
        command=exit_tk,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_tk())
    exit_button.grid(row=0, column=1, padx=5)

    Label(
        master=app,
        text="Created by FOSS Kingdom | made with Love in Incredible India.",
        bg="black",
        fg="white",
    ).pack(side=BOTTOM, fill=X)

    app.mainloop()

except KeyboardInterrupt:
    print("ERROR: KeyboardInterrupt occurred! Bye...")

except ModuleNotFoundError as module_not_found_error:
    print(f"ERROR: {module_not_found_error}")
