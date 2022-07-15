def exit_app() -> None:
    if not askyesno(
        title=f"SRM Fashion {__version__}",
        message="Are you sure? do you really want to quit?",
    ):
        return None

    conn.close()
    app.destroy()

    if isdir(s=cache_file_path):
        rmtree(path=cache_file_path)

    terminate()


def fetch_data() -> None:
    customer_data = treeview_db.item(item=treeview_db.focus()).get("values")

    clear_entry()

    name_var.set(value=customer_data[0])
    phone_var.set(value=customer_data[1])
    email_var.set(value=customer_data[2])
    dob_var.set(value=customer_data[3])

    if customer_data[4] == gender_options[0]:
        gender_var.set(value=gender_options[0])

    elif customer_data[4] == gender_options[1]:
        gender_var.set(value=gender_options[1])

    else:
        gender_var.set(value=gender_options[2])


def update_database() -> None:
    treeview_db.delete(*treeview_db.get_children())

    c.execute("select * from customers")

    for _ in c.fetchall():
        treeview_db.insert(parent="", index="end", values=_)

    total_customers = len(treeview_db.get_children())

    if total_customers:
        total_customers_label.config(text=f"{total_customers} customer(s) found!")

        search_button.config(state="normal")
        delete_button.config(state="normal")
        update_button.config(state="normal")

    else:
        total_customers_label.config(text="No customer(s) found!")

        search_button.config(state="disabled")
        delete_button.config(state="disabled")
        update_button.config(state="disabled")


def validate_name() -> (str | None):
    name_label.config(fg="black")
    name: str = name_var.get().strip().title()

    if not name:
        name_label.config(fg="red")
        name_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter the customer name.",
        )
        return None

    return name


def validate_phone() -> (str | None):
    phone_label.config(fg="black")
    phone: str = phone_var.get().strip()

    if not phone:
        phone_label.config(fg="red")
        phone_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}", message="Please enter the phone number."
        )
        return None

    try:
        number_object = parse(number=phone)
        phone: str = format_number(numobj=number_object, num_format=1)

    except NumberParseException as number_parse_exception:
        phone_label.config(fg="red")
        phone_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}",
            message=str(number_parse_exception),
        )
        return None

    if not is_valid_number(numobj=number_object):
        phone_label.config(fg="red")
        phone_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter the correct mobile number.",
        )
        return None

    return phone


def validate_email() -> (str | None):
    email_label.config(fg="black")
    email: str = email_var.get().strip().lower()

    if email:
        split_email: list = email.split(sep="@")
        if len(split_email) == 2:
            email_username: str = split_email[0]
            email_domain_address: str = split_email[1]
            if not email_username or not email_domain_address:
                email_label.config(fg="red")
                email_entry.focus()

                showinfo(
                    title=f"SRM Fashion {__version__}",
                    message="Invalid email address, Please try again...",
                )
                return None

        else:
            email_label.config(fg="red")
            email_entry.focus()

            showinfo(
                title=f"SRM Fashion {__version__}",
                message="Invalid email address, Please try again...",
            )
            return None

    return email


def create_entry() -> None:
    name: str | None = validate_name()
    if name is None:
        return None

    phone: str | None = validate_phone()
    if phone is None:
        return None

    email: str | None = validate_email()
    if email is None:
        return None

    dob: str = dob_var.get().strip()
    gender: str = gender_var.get()

    try:
        c.execute(
            f"""insert into customers values (
            '{name}', '{phone}', '{email}', '{dob}', '{gender}'
            )"""
        )

    except IntegrityError as integrity_error:
        phone_label.config(fg="red")
        phone_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"{integrity_error}\n{phone} This mobile number already exist.",
        )
        return None

    conn.commit()
    update_database()

    clear_entry()

    showinfo(
        title=f"SRM Fashion {__version__}", message="Database appended successfully..."
    )


def update_entry() -> None:
    selected_item: str = treeview_db.focus()

    if not selected_item:
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please select a customer record!",
        )
        return None

    name: str | None = validate_name()
    if name is None:
        return None

    phone: str | None = validate_phone()
    if phone is None:
        return None

    email: str | None = validate_email()
    if email is None:
        return None

    dob: str = dob_var.get().strip()
    gender: str = gender_var.get()

    selected_id: str = treeview_db.item(selected_item).get("values")[1]

    try:
        c.execute(
            f"""update customers set name = '{name}', phone = '{phone}', email = '{email}', dob = '{dob}', gender = '{gender}' where phone = '{selected_id}'"""
        )

    except IntegrityError as integrity_error:
        phone_label.config(fg="red")
        phone_entry.focus()

        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"{integrity_error}\n{phone} This mobile number already exist.",
        )
        return None

    conn.commit()
    update_database()

    clear_entry()

    showinfo(
        title=f"SRM Fashion {__version__}", message="Database updated successfully..."
    )


def delete_entry() -> None:
    selected_item: str = treeview_db.focus()

    if not selected_item:
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please select a customer record!",
        )
        return None

    selected_id: str = treeview_db.item(selected_item).get("values")[1]

    c.execute(f"""delete from customers where phone = '{selected_id}'""")
    conn.commit()
    update_database()

    clear_entry()

    showinfo(
        title=f"SRM Fashion {__version__}", message="1 row deleted successfully..."
    )


def clear_entry() -> None:
    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    name_entry.delete(first=0, last="end")
    phone_entry.delete(first=0, last="end")
    email_entry.delete(first=0, last="end")
    dob_entry.delete(first=0, last="end")

    gender_var.set(gender_options[0])

    name_entry.focus()


try:
    from getpass import getuser
    from os.path import isdir, isfile, join, split
    from shutil import rmtree
    from sqlite3 import IntegrityError, connect
    from sys import exit as terminate
    from tkinter import (
        Button,
        Entry,
        Frame,
        Label,
        LabelFrame,
        OptionMenu,
        StringVar,
        Tk,
    )
    from tkinter.messagebox import askyesno, showinfo
    from tkinter.ttk import Notebook, Treeview

    from phonenumbers import format_number, is_valid_number, parse
    from phonenumbers.phonenumberutil import NumberParseException

    __version__: str = "v.20220716"
    total_orders: int = 0
    base_path: str = split(p=__file__)[0]
    database_path: str = join(base_path, "customers.db")
    cache_file_path: str = join(base_path, "__pycache__")

    if not isfile(path=database_path):
        conn = connect(database=database_path)
        c = conn.cursor()
        c.execute(
            """create table customers (
            name text not null,
            phone text not null primary key,
            email text,
            dob text,
            gender text not null
        )"""
        )
        conn.commit()
        conn.close()

    conn = connect(database=database_path)
    c = conn.cursor()

    app: Tk = Tk()
    app.resizable(width=False, height=False)
    app.title(string=f"SRM Fashion {__version__}")
    app.protocol(name="WM_DELETE_WINDOW", func=exit_app)
    app.bind(sequence="<Control-Q>", func=lambda event: exit_app())
    app.bind(sequence="<Control-q>", func=lambda event: exit_app())
    app.bind(sequence="<Escape>", func=lambda event: exit_app())
    app.config(bg="lightsteelblue2")

    search_var: StringVar = StringVar()
    name_var: StringVar = StringVar()
    phone_var: StringVar = StringVar()
    email_var: StringVar = StringVar()
    dob_var: StringVar = StringVar()
    gender_var: StringVar = StringVar()

    Label(
        master=app,
        text=f"Hello {getuser().title()}, Welcome to SRM Fashion!",
        bg="black",
        fg="white",
    ).pack(side="top", fill="x")

    tab_view: Notebook = Notebook(master=app)
    tab_view.pack(fill="both", expand=True)

    orders_frame: Frame = Frame(master=tab_view, bg="lightsteelblue2")
    orders_frame.pack()

    customers_frame: Frame = Frame(master=tab_view, bg="lightsteelblue2")
    customers_frame.pack()

    tab_view.add(child=orders_frame, text="Orders")
    tab_view.add(child=customers_frame, text="Customers")

    # Orders tab
    Label(
        master=orders_frame,
        text="Order List",
        font=("Times New Roman", 22, "underline"),
        bg="lightsteelblue2",
    ).pack(pady=10)

    if total_orders == 0:
        Label(
            master=orders_frame,
            text="You have zero orders!",
            fg="red",
            bg="lightsteelblue2",
        ).pack()

    lf1: LabelFrame = LabelFrame(
        master=orders_frame, text="Add Order", fg="red", bg="lightsteelblue2"
    )
    lf1.pack(side="bottom", padx=10, ipady=3, pady=5, fill="x")

    order_button: Button = Button(
        master=lf1,
        text="Add an Order",
        bg="black",
        fg="white",
        width=12,
        command=lambda: tab_view.select(tab_id=1),
    )
    order_button.bind(sequence="<Return>", func=lambda event: tab_view.select(tab_id=1))
    order_button.grid(row=0, column=0, padx=5)

    exit_button: Button = Button(
        master=lf1,
        text="Exit",
        bg="red",
        fg="white",
        width=12,
        command=exit_app,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_button.grid(row=0, column=1, padx=5)

    # Customers tab
    lf21: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Lookup",
        fg="red",
        bg="lightsteelblue2",
    )
    lf21.pack(padx=10, pady=5, ipady=3, fill="both", expand=1)

    lf22: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Search",
        fg="red",
        bg="lightsteelblue2",
    )
    lf22.pack(padx=10, pady=5, ipady=3, fill="both", expand=1)

    lf23: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Data",
        fg="red",
        bg="lightsteelblue2",
    )
    lf23.pack(padx=10, pady=5, ipady=3, fill="both", expand=1)

    lf24: LabelFrame = LabelFrame(
        master=customers_frame, text="Select Customer", fg="red", bg="lightsteelblue2"
    )
    lf24.pack(side="bottom", padx=5, pady=5, ipady=3, fill="both", expand=1)

    # Customer tab, Treeview section
    header_list: list = ["Name", "Phone", "Email", "D.O.B", "Gender"]

    treeview_db: Treeview = Treeview(
        master=lf21,
        show="headings",
        columns=header_list,
        selectmode="browse",
    )

    for _ in header_list:
        treeview_db.heading(column=_, text=_)

    treeview_db.column(column=0, width=130, minwidth=130, anchor="w")
    treeview_db.column(column=1, width=130, minwidth=130, anchor="center")
    treeview_db.column(column=2, width=225, minwidth=225, anchor="w")
    treeview_db.column(column=3, width=100, minwidth=100, anchor="center")
    treeview_db.column(column=4, width=80, minwidth=80, anchor="w")

    treeview_db.bind(sequence="<Double-1>", func=lambda event: fetch_data())
    treeview_db.pack(padx=15, pady=5)

    total_customers_label: Label = Label(master=lf21, fg="red", bg="lightsteelblue2")
    total_customers_label.pack()

    # Customer tab, Search section
    Label(master=lf22, text="Search", bg="lightsteelblue2").pack(
        side="left", padx=5, pady=5
    )
    Entry(master=lf22, textvariable=search_var).pack(side="left", padx=5, pady=5)

    search_button: Button = Button(
        master=lf22,
        text="Search",
        bg="green",
        fg="white",
        state="disabled",
        width=10,
    )
    search_button.pack(side="right", padx=5, pady=5)

    clear_search: Button = Button(
        master=lf22, text="Clear", width=10, bg="orange", fg="white"
    )
    clear_search.pack(side="right", padx=5, pady=5)

    # Customer tab, data section
    f21: Frame = Frame(master=lf23, bg="lightsteelblue2")
    f21.pack(padx=10, pady=5)

    name_label: Label = Label(
        master=f21,
        text="Enter Customer Name:",
        bg="lightsteelblue2",
    )
    name_label.grid(row=0, column=0, padx=5, sticky="w")
    name_entry: Entry = Entry(master=f21, width=25, textvariable=name_var)
    name_entry.grid(row=0, column=1, padx=5)

    phone_label: Label = Label(master=f21, text="Contact Number:", bg="lightsteelblue2")
    phone_label.grid(row=1, column=0, sticky="w")
    phone_entry: Entry = Entry(master=f21, width=25, textvariable=phone_var)
    phone_entry.grid(row=1, column=1)

    email_label: Label = Label(
        master=f21, text="Email (Optional):", bg="lightsteelblue2"
    )
    email_label.grid(row=2, column=0, sticky="w")
    email_entry: Entry = Entry(master=f21, width=25, textvariable=email_var)
    email_entry.grid(row=2, column=1)

    Label(
        master=f21,
        text="Date of Birth (Optional):",
        bg="lightsteelblue2",
    ).grid(row=3, column=0, sticky="w")
    dob_entry: Entry = Entry(f21, width=25, textvariable=dob_var)
    dob_entry.grid(row=3, column=1)

    Label(master=f21, text="Gender:", bg="lightsteelblue2").grid(
        row=4, column=0, sticky="w"
    )
    gender_options: list = ["Female", "Male", "Other"]
    gender_var.set(value=gender_options[0])
    OptionMenu(f21, gender_var, *gender_options).grid(
        row=4, column=1, sticky="w", padx=5
    )

    name_entry.bind(sequence="<Return>", func=lambda event: phone_entry.focus())
    phone_entry.bind(sequence="<Return>", func=lambda event: email_entry.focus())
    email_entry.bind(sequence="<Return>", func=lambda event: dob_entry.focus())

    f22: Frame = Frame(master=lf23, bg="lightsteelblue2")
    f22.pack(padx=5, pady=10, side="right")

    clear_data: Button = Button(
        master=f22,
        text="Clear",
        bg="black",
        fg="white",
        width=10,
        command=clear_entry,
    )
    clear_data.bind(sequence="<Return>", func=lambda event: clear_entry())
    clear_data.pack(padx=5, side="right")

    delete_button: Button = Button(
        master=f22,
        text="Delete",
        bg="red",
        fg="white",
        state="disabled",
        width=10,
        command=delete_entry,
    )
    delete_button.bind(sequence="<Return>", func=lambda event: delete_entry())
    delete_button.pack(padx=5, side="right")

    update_button: Button = Button(
        master=f22,
        text="Update",
        bg="orange",
        fg="white",
        state="disabled",
        width=10,
        command=update_entry,
    )
    update_button.bind(sequence="<Return>", func=lambda event: update_entry())
    update_button.pack(padx=5, side="right")

    create_button: Button = Button(
        master=f22,
        text="Create new",
        bg="green",
        fg="white",
        width=10,
        command=create_entry,
    )
    create_button.bind(sequence="<Return>", func=lambda event: create_entry())
    create_button.pack(padx=5, side="right")

    selection_button: Button = Button(
        master=lf24,
        text="Select",
        bg="black",
        fg="white",
        width=12,
        # command=not_ready_yet,
    )
    # selection_button.bind(sequence="<Return>", func=lambda event: not_ready_yet())
    selection_button.grid(row=0, column=0, padx=5)

    exit_button: Button = Button(
        master=lf24,
        text="Exit",
        bg="red",
        fg="white",
        width=12,
        command=exit_app,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_button.grid(row=0, column=1, padx=5)

    Label(
        master=app,
        text="Created by FOSS Kingdom | made with Love in Incredible India.",
        bg="black",
        fg="white",
    ).pack(side="bottom", fill="x")

    update_database()

    app.mainloop()

except KeyboardInterrupt:
    print("ERROR: KeyboardInterrupt occurred! Bye...")

except ModuleNotFoundError as module_not_found_error:
    print(f"ERROR: {module_not_found_error}")
