def not_ready_yet() -> None:
    app.withdraw()
    showinfo(
        title=f"SRM Fashion {__version__}",
        message="This action is not ready yet, Still work in progress...",
    )
    app.deiconify()


def exit_app() -> None:
    app.withdraw()
    if not askyesno(
        title=f"SRM Fashion {__version__}",
        message="Are you sure? do you really want to quit?",
    ):
        app.deiconify()
        return None

    conn.close()
    app.destroy()

    if isdir(s=cache_file_path):
        print(Fore.GREEN + "INFO: Cleaning cache files, Please wait...")
        rmtree(path=cache_file_path)

    print(Fore.RED + "Bye...")

    if os_name == "Linux":
        terminal(command="clear")

    if os_name == "Windows":
        terminal(command="cls")

    terminate()


def pstat() -> None:
    cpu: float = cpu_percent()
    mem: float = virtual_memory().percent
    pwr: float = round(sensors_battery().percent, 1)
    clock: str = strftime("%I:%M:%S %p")

    pstat_label.config(
        text=f"CPU: {cpu}% | MEM {mem}% | PWR: {pwr}% | {username.title()} @ {clock}"
    )
    pstat_label.after(ms=1000, func=pstat)


def search_record() -> None:
    search: str = search_var.get().strip()

    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    name_entry.delete(first=0, last="end")
    phone_entry.delete(first=0, last="end")
    email_entry.delete(first=0, last="end")
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])

    if not search:
        update_database()
        return None

    total_records: list = list()

    try:
        number_object = parse(number=search)
        search: str = format_number(numobj=number_object, num_format=1)

        if is_valid_number(numobj=number_object):
            c.execute(f"select * from customers where phone like '%{search}%'")
            total_records = c.fetchall()

    except NumberParseException:
        c.execute(
            f"select * from customers where name like '%{search}%' or email like '%{search}%'"
        )
        total_records = c.fetchall()

    if not total_records:
        print(Fore.RED + "INFO: No records found!")
        app.withdraw()
        showinfo(title=f"SRM Fashion {__version__}", message="No records found!")
        app.deiconify()
        return None

    treeview_db.delete(*treeview_db.get_children())
    total_customers_label.config(text="No customer(s) found!")

    count: int = 0
    for _ in total_records:
        count: int = count + 1
        _: list = [count, _[0], _[1], _[2], _[3], _[4]]
        treeview_db.insert(parent="", index="end", values=_)

    total_customers: int = len(treeview_db.get_children())
    total_customers_label.config(text=f"{total_customers} customer(s) found!")


def clear_date() -> None:
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()


def fetch_data() -> None:
    customer_data: list = treeview_db.item(item=treeview_db.focus()).get("values")

    if not customer_data:
        return None

    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    name_var.set(value=customer_data[0])
    phone_var.set(value=customer_data[1])
    email_var.set(value=customer_data[2])

    try:
        day_selection.selection_set(date=customer_data[3])

    except ValueError:
        day_selection.selection_set(
            date=date(year=today.year - 18, month=today.month, day=today.day)
        )
        day_selection.selection_clear()

    if customer_data[4] == gender_options[0]:
        gender_var.set(value=gender_options[0])

    elif customer_data[4] == gender_options[1]:
        gender_var.set(value=gender_options[1])

    else:
        gender_var.set(value=gender_options[2])


def update_database() -> None:
    treeview_db.delete(*treeview_db.get_children())

    total_customers_label.config(text="No customer(s) found!")

    search_entry.config(state="disabled")
    search_button.config(state="disabled")
    delete_button.config(state="disabled")
    update_button.config(state="disabled")

    c.execute("select * from customers")
    count: int = 0
    for _ in c.fetchall():
        count: int = count + 1
        _: list = [count, _[0], _[1], _[2], _[3], _[4]]
        treeview_db.insert(parent="", index="end", values=_)

    total_customers: int = len(treeview_db.get_children())

    if total_customers:
        total_customers_label.config(text=f"{total_customers} customer(s) found!")

        search_entry.config(state="normal")
        search_button.config(state="normal")
        delete_button.config(state="normal")
        update_button.config(state="normal")


def validate_name() -> (str | None):
    name: str = name_var.get().strip().title()

    if not name:
        name_label.config(fg="red")
        name_entry.focus()

        print(Fore.RED + "INFO: Please enter the customer name.")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter the customer name.",
        )
        app.deiconify()
        return None

    return name


def validate_phone() -> (str | None):
    phone: str = phone_var.get().strip()

    if not phone:
        phone_label.config(fg="red")
        phone_entry.focus()

        print(Fore.RED + "INFO: Please enter the phone number.")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}", message="Please enter the phone number."
        )
        app.deiconify()
        return None

    try:
        number_object = parse(number=phone)

    except NumberParseException as number_parse_exception:
        phone_label.config(fg="red")
        phone_entry.focus()

        print(Fore.RED + f"ERROR: {number_parse_exception}")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message=str(number_parse_exception),
        )
        app.deiconify()
        return None

    phone: str = format_number(numobj=number_object, num_format=1)

    if not is_valid_number(numobj=number_object):
        phone_label.config(fg="red")
        phone_entry.focus()

        print(Fore.RED + "INFO: Please enter the correct mobile number.")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please enter the correct mobile number.",
        )
        app.deiconify()
        return None

    return phone


def validate_email() -> (str | None):
    email: str = email_var.get().strip().lower()

    if email:
        split_email: list = email.split(sep="@")
        if len(split_email) == 2:
            email_username: str = split_email[0]
            email_domain_address: str = split_email[1]
            if not email_username or not email_domain_address:
                email_label.config(fg="red")
                email_entry.focus()

                print(Fore.RED + "INFO: Invalid email address, Please try again...")
                app.withdraw()
                showinfo(
                    title=f"SRM Fashion {__version__}",
                    message="Invalid email address, Please try again...",
                )
                app.deiconify()
                return None

        else:
            email_label.config(fg="red")
            email_entry.focus()

            print(Fore.RED + "INFO: Invalid email address, Please try again...")
            app.withdraw()
            showinfo(
                title=f"SRM Fashion {__version__}",
                message="Invalid email address, Please try again...",
            )
            app.deiconify()
            return None

    return email


def create_entry() -> None:
    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    name: str | None = validate_name()
    if name is None:
        return None

    phone: str | None = validate_phone()
    if phone is None:
        return None

    email: str | None = validate_email()
    if email is None:
        return None

    dob: str = day_selection.get_date()
    gender: str = gender_var.get()

    try:
        c.execute(
            """insert into customers values (
            ?, ?, ?, ?, ?
            )""",
            (name, phone, email, dob, gender),
        )

    except IntegrityError as integrity_error:
        phone_label.config(fg="red")
        phone_entry.focus()

        print(Fore.RED + "INFO: This mobile number already exists.")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"{integrity_error}\n{phone} This mobile number already exist.",
        )
        app.deiconify()
        return None

    conn.commit()
    update_database()

    name_entry.delete(first=0, last="end")
    phone_entry.delete(first=0, last="end")
    email_entry.delete(first=0, last="end")
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])

    name_entry.focus()

    print(Fore.GREEN + "INFO: Database appended successfully...")
    app.withdraw()
    showinfo(
        title=f"SRM Fashion {__version__}", message="Database appended successfully..."
    )
    app.deiconify()


def update_entry() -> None:
    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    selected_item: str = treeview_db.focus()

    if not selected_item:
        print(Fore.RED + "INFO: Please select a customer record!")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please select a customer record!",
        )
        app.deiconify()
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

    dob: str = day_selection.get_date()
    gender: str = gender_var.get()

    selected_id: str = treeview_db.item(selected_item).get("values")[1]

    try:
        c.execute(
            f"""update customers set name = ?, phone = ?, email = ?, dob = ?, gender = ? where phone = ?""",
            (name, phone, email, dob, gender, selected_id),
        )

    except IntegrityError as integrity_error:
        phone_label.config(fg="red")
        phone_entry.focus()

        print(Fore.RED + "INFO: This mobile number already exists.")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"{integrity_error}\n{phone} This mobile number already exist.",
        )
        app.deiconify()
        return None

    conn.commit()
    update_database()

    name_entry.delete(first=0, last="end")
    phone_entry.delete(first=0, last="end")
    email_entry.delete(first=0, last="end")
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])

    name_entry.focus()

    print(Fore.GREEN + "INFO: Database updated successfully...")
    app.withdraw()
    showinfo(
        title=f"SRM Fashion {__version__}", message="Database updated successfully..."
    )
    app.deiconify()


def delete_entry() -> None:
    if not treeview_db.get_children():
        return None

    name_label.config(fg="black")
    phone_label.config(fg="black")
    email_label.config(fg="black")

    selected_item: str = treeview_db.focus()

    if not selected_item:
        print(Fore.RED + "INFO: Please select a customer record!")
        app.withdraw()
        showinfo(
            title=f"SRM Fashion {__version__}",
            message="Please select a customer record!",
        )
        app.deiconify()
        return None

    app.withdraw()
    if not askyesno(
        title=f"SRM Fashion {__version__}",
        message="Are you sure? Do you want to delete the selected record?",
    ):
        app.deiconify()
        return None

    selected_id: str = treeview_db.item(selected_item).get("values")[1]

    c.execute(f"""delete from customers where phone = '{selected_id}'""")
    conn.commit()
    update_database()

    name_entry.delete(first=0, last="end")
    phone_entry.delete(first=0, last="end")
    email_entry.delete(first=0, last="end")
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])

    print(Fore.GREEN + "INFO: 1 record deleted successfully...")
    app.withdraw()
    showinfo(
        title=f"SRM Fashion {__version__}", message="1 record deleted successfully..."
    )
    app.deiconify()


def clear_entry() -> None:
    update_database()

    search_entry.delete(first=0, last="end")

    name_label.config(fg="black")
    name_entry.delete(first=0, last="end")

    phone_label.config(fg="black")
    phone_entry.delete(first=0, last="end")

    email_label.config(fg="black")
    email_entry.delete(first=0, last="end")

    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()

    gender_var.set(gender_options[0])

    name_entry.focus()


def donation_page() -> None:
    def exit_subwindow() -> None:
        new_window.destroy()
        app.deiconify()

    app.withdraw()
    new_window = Toplevel(master=app)
    new_window.protocol(name="WM_DELETE_WINDOW", func=exit_subwindow)
    new_window.bind(sequence="<Control-Q>", func=lambda event: exit_subwindow())
    new_window.bind(sequence="<Control-q>", func=lambda event: exit_subwindow())
    new_window.bind(sequence="<Escape>", func=lambda event: exit_subwindow())
    new_window.bind(sequence="<Alt-F4>", func=lambda event: exit_subwindow())
    new_window.iconphoto(False, PhotoImage(file=donation_icon_path))
    new_window.title(string="Donate Us!")
    new_window.resizable(width=False, height=False)
    new_window.config(bg=accent_color_light)

    Label(
        master=new_window,
        text=f"Hello {username.title()}, Welcome to SRM Fashion!",
        bg="black",
        fg="white",
    ).pack(side="top", fill="x")

    donation_labelframe: LabelFrame = LabelFrame(
        master=new_window,
        text="Donate Us",
        fg="red",
        bg=accent_color_light,
    )
    donation_labelframe.pack(padx=10, fill="both", expand=1)

    donation_textwidget: Text = Text(
        master=donation_labelframe, wrap="word", selectbackground="orange"
    )
    donation_textwidget.insert(
        index=1.0,
        chars="""\tFOSS KINGODM is powered by people like you. Contribute today and show 
your love for us! You can help maintain this software development by sending us 
a donation. It's a free and open-source software. 

\tI developed this application on my free time. So if you enjoy it, feel 
free to show your support. Created by FOSS Kingdom. Made with Love in Incredible 
India.

Get Involved:
\tWe are always evolving and welcome new ideas, partners, contributions 
and emails. We have a very optimistic view of the future. We are very fond of 
this lovely planet!

Donate:
\tWe strongly believe that, "When you give, you get back tenfold." Now, 
that's a great exchange rate!

What drives us? Why should I donate?
(Our mission, vision and goal):
Goal 1: No Poverty (To help end poverty.)
Goal 2: Zero Hunger (To feed the hungry.)
Goal 3: Good Health and Well-being (To provide good healthcare.)
Goal 4: Quality Education (To send more kids to school.)
Goal 5: Gender Equality (To empower women and girls.)
Goal 6: Clean Water and Sanitation (To give clean water.)
Goal 7: Affordable and Clean Energy (To develop renewable energy.)""",
    )
    donation_textwidget.config(state="disabled")
    donation_textwidget.pack(fill="both", expand=1, padx=10, pady=10)

    qrcode_image: PhotoImage = PhotoImage(file=qrcode_path).subsample(x=3, y=3)

    Label(
        master=new_window,
        text="Scan here to donate with Google Pay!",
        fg="red",
        compound="bottom",
        bg=accent_color_light,
        image=qrcode_image,
    ).pack()

    Label(
        master=new_window,
        text="UPI: gameworld2k18@oksbi",
        fg="red",
        bg=accent_color_light,
    ).pack()

    Label(
        master=new_window,
        text="""Name: MOHAMED FARIZ
A/C No: 0740301000082422
Bank: LAKSHMI VILAS BANK
Branch: THIRUTHURAIPOONDI
IFSC: LAVB0000740""",
        bg=accent_color_light,
    ).pack()

    close_button: Button = Button(
        master=new_window,
        text="Close",
        bg="red",
        fg="white",
        width=10,
        command=exit_subwindow,
    )
    close_button.bind(sequence="<Return>", func=lambda event: exit_subwindow())
    close_button.pack(pady=5)

    Label(
        master=new_window,
        text="Created by FOSS Kingdom | Made with Love in Incredible India.",
        bg="black",
        fg="white",
    ).pack(fill="x", side="bottom")

    new_window.mainloop()


try:
    print("INFO: Importing built-in modules...")
    from datetime import date, datetime
    from getpass import getuser
    from os import system as terminal
    from os.path import isdir, join, split
    from platform import system as os_env
    from random import choice
    from shutil import rmtree
    from sqlite3 import IntegrityError, OperationalError, connect
    from sys import exit as terminate
    from time import strftime, time
    from tkinter import (
        Button,
        Entry,
        Frame,
        Label,
        LabelFrame,
        Menu,
        OptionMenu,
        PhotoImage,
        Scrollbar,
        StringVar,
        Text,
        Tk,
        Toplevel,
    )
    from tkinter.messagebox import askyesno, showinfo
    from tkinter.ttk import Notebook, Treeview

    today: datetime = datetime.today()
    username = getuser()
    base_path: str = split(p=__file__)[0]
    # <a href="https://www.flaticon.com/free-icons/sewing" title="sewing icons">
    # Sewing icons created by ultimatearm - Flaticon
    # </a>
    logo_icon_path: str = join(base_path, "assets/sewing.png")
    database_path: str = join(base_path, "database.db")
    donation_icon_path: str = join(base_path, "assets/donation.png")
    qrcode_path: str = join(base_path, "assets/qr_code.png")
    cache_file_path: str = join(base_path, "__pycache__")
    order_icon_path: str = join(base_path, "assets/order.png")
    # <a href="https://www.flaticon.com/free-icons/target" title="target icons">
    # Target icons created by Freepik - Flaticon
    # </a>
    customers_icon_path: str = join(base_path, "assets/target.png")
    exit_icon_path: str = join(base_path, "assets/logout.png")
    # <a href="https://www.flaticon.com/free-icons/search" title="search icons">
    # Search icons created by Icon home - Flaticon
    # </a>
    search_icon_path: str = join(base_path, "assets/magnifying-glass.png")
    # <a href="https://www.flaticon.com/free-icons/user" title="user icons">
    # User icons created by uicon - Flaticon
    # </a>
    adduser_icon_path: str = join(base_path, "assets/add-user.png")
    # <a href="https://www.flaticon.com/free-icons/edit" title="edit icons">
    # Edit icons created by Pixel perfect - Flaticon
    # </a>
    edituser_icon_path: str = join(base_path, "assets/edit.png")
    # <a href="https://www.flaticon.com/free-icons/delete" title="delete icons">
    # Delete icons created by Andrean Prabowo - Flaticon
    # </a>
    removeuser_icon_path: str = join(base_path, "assets/delete-user.png")
    # <a href="https://www.flaticon.com/free-icons/delete" title="delete icons">
    # Delete icons created by Pixel perfect - Flaticon
    # </a>
    clear_icon_path: str = join(base_path, "assets/delete.png")
    os_name: str = os_env()
    start_time: float = time()

    print("INFO: Importing third-party modules...")
    from colorama import Fore, Style, init
    from phonenumbers import format_number, is_valid_number, parse
    from phonenumbers.phonenumberutil import NumberParseException
    from psutil import cpu_percent, sensors_battery, virtual_memory
    from pyfiglet import FigletFont, figlet_format
    from tkcalendar import Calendar

    print("INFO: Initializing colorama...")
    init(autoreset=True)

    total_ram = round(virtual_memory().total / (1024 * 1024 * 1024), 2)

    selected_font = choice(seq=FigletFont.getFonts())
    if selected_font:
        print(Fore.RED + figlet_format(text="SRM Fashion", font=selected_font))
        print(f"Pyfiglet Font: {selected_font}")
        print(
            Style.BRIGHT
            + "Created by FOSS Kingdom, Made with Love in Incredible India.\n"
        )

    __version__: str = "v.20220722 (alpha)"
    total_orders: int = 0
    accent_color_light: str = "lightsteelblue2"

    if os_name == "Linux":
        terminal(command="xtitle -q -t SRM Fashion")

    if os_name == "Windows":
        terminal(command="title SRM Fashion")

    print(Fore.GREEN + "INFO: Creating GUI application...")
    app: Tk = Tk()
    app.withdraw()
    app.iconphoto(False, PhotoImage(file=logo_icon_path))
    app.resizable(width=False, height=False)
    app.title(string=f"SRM Fashion {__version__}")
    app.protocol(name="WM_DELETE_WINDOW", func=exit_app)
    app.bind(sequence="<Control-Q>", func=lambda event: exit_app())
    app.bind(sequence="<Control-q>", func=lambda event: exit_app())
    app.bind(sequence="<Escape>", func=lambda event: exit_app())

    menu_bar: Menu = Menu(master=app)
    links_menu: Menu = Menu(master=menu_bar, tearoff=0)
    help_menu: Menu = Menu(master=menu_bar, tearoff=0)

    menu_bar.add_cascade(label="Links", menu=links_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    links_menu.add_command(label="Licence", command=not_ready_yet)
    links_menu.add_command(label="Source Code", command=not_ready_yet)
    links_menu.add_command(label="Issues", command=not_ready_yet)
    links_menu.add_command(label="Website", command=not_ready_yet)

    donation_icon: PhotoImage = PhotoImage(file=donation_icon_path).subsample(
        x=25, y=25
    )
    help_menu.add_command(
        label="Donate Us", command=donation_page, image=donation_icon, compound="left"
    )

    help_menu.add_separator()
    help_menu.add_command(label="About TailorMate", command=not_ready_yet)

    app.config(menu=menu_bar, bg=accent_color_light)

    search_var: StringVar = StringVar()
    name_var: StringVar = StringVar()
    phone_var: StringVar = StringVar()
    email_var: StringVar = StringVar()
    gender_var: StringVar = StringVar()

    print(Fore.RED + f"Hello {username.title()}, Welcome to SRM Fashion!")
    Label(
        master=app,
        text=f"Hello {username.title()}, Welcome to SRM Fashion!",
        bg="black",
        fg="white",
    ).pack(side="top", fill="x")

    tab_view: Notebook = Notebook(master=app)
    tab_view.pack(fill="both", expand=True)

    orders_frame: Frame = Frame(master=tab_view, bg=accent_color_light)
    orders_frame.pack()

    customers_frame: Frame = Frame(master=tab_view, bg=accent_color_light)
    customers_frame.pack()

    tab_view.add(child=orders_frame, text="Orders")
    tab_view.add(child=customers_frame, text="Customers")

    # Orders tab
    Label(
        master=orders_frame,
        text="Order List",
        font=("Times New Roman", 23, "underline"),
        bg=accent_color_light,
    ).pack(pady=10)

    if total_orders == 0:
        # https://www.un.org/en/observances/international-days-and-weeks

        if today.month == 1 and today.day == 1:
            msg: str = "New Year's Day."

        elif today.month == 1 and today.day == 4:
            msg: str = "Today is World Braille Day."

        elif today.month == 1 and today.day == 24:
            msg: str = "Today is International Day of Education."

        elif today.month == 2 and today.day == 2:
            msg: str = "Today is World Wetlands Day."

        elif today.month == 2 and today.day == 10:
            msg: str = "Today is World Pulses Day."

        elif today.month == 2 and today.day == 11:
            msg: str = "Today is International Day of Women and Girls in Science."

        elif today.month == 2 and today.day == 13:
            msg: str = "Today is World Radio Day."

        elif today.month == 2 and today.day == 14:
            msg: str = "Happy Valentine's Day."

        elif today.month == 2 and today.day == 20:
            msg: str = "Today is World Day of Social Justice."

        elif today.month == 2 and today.day == 21:
            msg: str = "Today is International Mother Language Day."

        elif today.month == 3 and today.month == 3:
            msg: str = "Today is World Wildlife Day."

        elif today.month == 3 and today.day == 8:
            msg: str = "Today is International Women's Day."

        elif today.month == 3 and today.day == 10:
            msg: str = "Today is International Day of Women Judges."

        elif today.month == 3 and today.day == 21:
            msg: str = "Today is International Day of Forests."

        elif today.month == 3 and today.day == 22:
            msg: str = "Today is World Water Day."

        elif today.month == 3 and today.day == 23:
            msg: str = "Today is World Meteorological Day."

        elif today.month == 3 and today.day == 24:
            msg: str = "Today is World Tuberculosis Day."

        elif today.month == 4 and today.day == 2:
            msg: str = "Today is World Autism Awareness Day."

        elif today.month == 4 and today.day == 5:
            msg: str = "Today is International Day of Conscience."

        elif today.month == 4 and today.day == 6:
            msg: str = "Today is International Day of Sports for Development and Peace."

        elif today.month == 4 and today.day == 7:
            msg: str = "Today is World Health Day."

        elif today.month == 4 and today.day == 12:
            msg: str = "Today is International Day of Human Space Flight."

        elif today.month == 4 and today.day == 21:
            msg: str = "Today is World Creativity and Innovation Day."

        elif today.month == 4 and today.day == 22:
            msg: str = "Today is International Mother Earth Day."

        elif today.month == 4 and today.day == 25:
            msg: str = "Today is World Malaria Day."

        elif today.month == 4 and today.day == 30:
            msg: str = "Today is International Jazz Day."

        elif today.month == 5 and today.day == 1:
            msg: str = "Today is International Worker's Day."

        elif today.month == 5 and today.day == 2:
            msg: str = "Today is World Tuna Day."

        elif today.month == 5 and today.day == 3:
            msg: str = "Today is World Press Freedom Day."

        # To be continued...

        elif today.month == 6 and today.day == 14:
            msg: str = "Today is World Blood Donor Day."

        elif today.month == 6 and today.day == 19:
            msg: str = "Happy Father's Day."

        elif today.month == 7 and today.day == 11:
            msg: str = "Today is World Population Day."

        elif today.month == 10 and today.day == 5:
            msg: str = "Today is Fariz's Birthday *(Founder of FOSS KINGDOM)"

        elif today.month == 12 and today.day == 1:
            msg: str = "Today is World AIDS Day."

        elif today.month == 12 and today.day == 25:
            msg: str = "Merry Christmas."

        elif today.month == 12 and today.day == 31:
            msg: str = "Happy New Year's Eve"

        else:
            msg: str = "#JusticeForSrimathi,  #Kallakurichi"

        print(Fore.RED + msg)
        Label(
            master=orders_frame,
            text=msg,
            bg="red",
        ).pack(fill="x")

        Label(
            master=orders_frame,
            text="You have zero orders!",
            fg="red",
            bg=accent_color_light,
        ).pack()

    lf1: LabelFrame = LabelFrame(
        master=orders_frame, text="Add Order", fg="red", bg=accent_color_light
    )
    lf1.pack(side="bottom", padx=10, ipady=3, pady=10, fill="x")

    order_icon: PhotoImage = PhotoImage(file=order_icon_path).subsample(x=24, y=24)
    order_button: Button = Button(
        master=lf1,
        text="Add an Order",
        bg="black",
        fg="white",
        width=115,
        command=lambda: tab_view.select(tab_id=1),
        image=order_icon,
        compound="left",
    )
    order_button.bind(sequence="<Return>", func=lambda event: tab_view.select(tab_id=1))
    order_button.grid(row=0, column=0, padx=5)

    exit_icon: PhotoImage = PhotoImage(file=exit_icon_path).subsample(x=24, y=24)
    exit_button: Button = Button(
        master=lf1,
        text="Exit",
        bg="red",
        fg="white",
        compound="left",
        width=115,
        command=exit_app,
        image=exit_icon,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_button.grid(row=0, column=1, padx=5)

    # Customers tab
    lf21: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Database",
        fg="red",
        bg=accent_color_light,
    )
    lf21.pack(padx=10, pady=5, ipady=3, fill="both", expand=1)

    lf22: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Lookup",
        fg="red",
        bg=accent_color_light,
    )
    lf22.pack(padx=10, pady=5, ipady=6, fill="both", expand=1)

    lf23: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Details",
        fg="red",
        bg=accent_color_light,
    )
    lf23.pack(padx=10, pady=5, ipady=3, fill="both", expand=1)

    lf24: LabelFrame = LabelFrame(
        master=customers_frame, text="Select Customer", fg="red", bg=accent_color_light
    )
    lf24.pack(side="bottom", padx=10, pady=10, ipady=3, fill="x")

    # Customer tab, Treeview section
    header_list: list = ["S.No", "Name", "Phone", "Email", "D.O.B", "Gender"]

    treeview_frame: Frame = Frame(master=lf21, bg=accent_color_light)
    treeview_frame.pack(padx=15, fill="both", expand=1)

    treeview_scroll: Scrollbar = Scrollbar(master=treeview_frame)
    treeview_scroll.pack(side="right", fill="y")

    treeview_db: Treeview = Treeview(
        master=treeview_frame,
        show="headings",
        columns=header_list,
        selectmode="browse",
        yscrollcommand=treeview_scroll.set,
    )

    for _ in header_list:
        treeview_db.heading(column=_, text=_)

    treeview_db.column(column=0, width=75, minwidth=75, anchor="center")
    treeview_db.column(column=1, width=150, minwidth=150, anchor="w")
    treeview_db.column(column=2, width=130, minwidth=130, anchor="center")
    treeview_db.column(column=3, width=225, minwidth=225, anchor="w")
    treeview_db.column(column=4, width=100, minwidth=100, anchor="center")
    treeview_db.column(column=5, width=80, minwidth=80, anchor="w")

    treeview_db.bind(sequence="<Double-1>", func=lambda event: fetch_data())
    treeview_db.bind(sequence="<Return>", func=lambda event: fetch_data())
    treeview_db.bind(sequence="<Delete>", func=lambda event: delete_entry())

    treeview_scroll.config(command=treeview_db.yview)
    treeview_db.pack(fill="both", expand=1)

    total_customers_label: Label = Label(master=lf21, fg="red", bg=accent_color_light)
    total_customers_label.pack()

    # Customer tab, Search section
    Label(master=lf22, text="Search:", bg=accent_color_light).pack(side="left", padx=10)
    search_entry: Entry = Entry(
        master=lf22, textvariable=search_var, width=25, state="disabled"
    )
    search_entry.bind(sequence="<Return>", func=lambda event: search_record())
    search_entry.pack(side="left", padx=25)

    search_icon: PhotoImage = PhotoImage(file=search_icon_path).subsample(x=24, y=24)
    search_button: Button = Button(
        master=lf22,
        text="Search",
        bg="red",
        fg="white",
        state="disabled",
        compound="left",
        width=115,
        command=search_record,
        image=search_icon,
    )
    search_button.bind(sequence="<Return>", func=lambda event: search_record())
    search_button.pack(side="right", padx=15)

    # Customer tab, data entry section
    f21: Frame = Frame(master=lf23, bg=accent_color_light)
    f21.pack(padx=10, pady=5, expand=1)

    name_label: Label = Label(
        master=f21,
        text="Customer Name:",
        bg=accent_color_light,
    )
    name_label.grid(row=0, column=0, sticky="w")
    name_entry: Entry = Entry(master=f21, width=30, textvariable=name_var)
    name_entry.grid(row=0, column=1, padx=5, sticky="w")

    phone_label: Label = Label(
        master=f21, text="Contact Number:", bg=accent_color_light
    )
    phone_label.grid(row=1, column=0, sticky="w")
    phone_entry: Entry = Entry(master=f21, width=30, textvariable=phone_var)
    phone_entry.grid(row=1, column=1, padx=5, sticky="w")

    email_label: Label = Label(
        master=f21, text="Email Address (Optional):", bg=accent_color_light
    )
    email_label.grid(row=2, column=0, sticky="w")
    email_entry: Entry = Entry(master=f21, width=30, textvariable=email_var)
    email_entry.grid(row=2, column=1, padx=5, sticky="w")

    Label(
        master=f21,
        text=f"Date of Birth (Optional):",
        bg=accent_color_light,
    ).grid(row=3, column=0, sticky="w")
    # ERROR: No module named 'babel.numbers'
    day_selection: Calendar = Calendar(
        master=f21,
        selectmode="day",
        date_pattern="dd/mm/yyyy",
        showweeknumbers=False,
        showothermonthdays=False,
        maxdate=date(year=today.year, month=today.month, day=today.day - 1),
        mindate=date(year=today.year - 100, month=today.month, day=today.day),
        year=today.year - 18,
        month=today.month,
        background="#212946",
    )
    day_selection.selection_clear()
    day_selection.grid(row=3, column=1, padx=5, pady=5)

    clear_date_button: Button = Button(
        master=f21,
        text="Clear Date",
        fg="white",
        bg="red",
        width=10,
        command=clear_date,
    )
    clear_date_button.bind(sequence="<Return>", func=lambda event: clear_date())
    clear_date_button.grid(row=3, column=2, padx=5, sticky="w")

    Label(master=f21, text="Gender:", bg=accent_color_light).grid(
        row=4, column=0, sticky="w"
    )
    gender_options: list = ["Female", "Male", "Other"]
    gender_var.set(value=gender_options[0])
    OptionMenu(f21, gender_var, *gender_options).grid(
        row=4, column=1, padx=5, sticky="w"
    )

    name_entry.bind(sequence="<Return>", func=lambda event: phone_entry.focus())
    phone_entry.bind(sequence="<Return>", func=lambda event: email_entry.focus())

    # customer tab data button section
    f22: Frame = Frame(master=lf23, bg=accent_color_light)
    f22.pack(padx=10, pady=5, ipady=3, side="right", fill="both", expand=1)

    clear_icon: PhotoImage = PhotoImage(file=clear_icon_path).subsample(x=24, y=24)
    clear_input_data: Button = Button(
        master=f22,
        text="Clear Input",
        bg="black",
        fg="white",
        compound="left",
        width=115,
        command=clear_entry,
        image=clear_icon,
    )
    clear_input_data.bind(sequence="<Return>", func=lambda event: clear_entry())
    clear_input_data.pack(padx=5, side="right")

    removeuser_icon: PhotoImage = PhotoImage(file=removeuser_icon_path).subsample(
        x=24, y=24
    )
    delete_button: Button = Button(
        master=f22,
        text="Delete",
        bg="red",
        fg="white",
        state="disabled",
        compound="left",
        width=115,
        command=delete_entry,
        image=removeuser_icon,
    )
    delete_button.bind(sequence="<Return>", func=lambda event: delete_entry())
    delete_button.pack(padx=5, side="right")

    edituser_icon: PhotoImage = PhotoImage(file=edituser_icon_path).subsample(
        x=24, y=24
    )
    update_button: Button = Button(
        master=f22,
        text="Update",
        bg="orange",
        fg="white",
        state="disabled",
        compound="left",
        width=115,
        command=update_entry,
        image=edituser_icon,
    )
    update_button.bind(sequence="<Return>", func=lambda event: update_entry())
    update_button.pack(padx=5, side="right")

    adduser_icon: PhotoImage = PhotoImage(file=adduser_icon_path).subsample(x=24, y=24)
    create_button: Button = Button(
        master=f22,
        text="Create New",
        bg="green",
        fg="white",
        compound="left",
        width=115,
        command=create_entry,
        image=adduser_icon,
    )
    create_button.bind(sequence="<Return>", func=lambda event: create_entry())
    create_button.pack(padx=5, side="right")

    customer_icon: PhotoImage = PhotoImage(file=customers_icon_path).subsample(
        x=24, y=24
    )
    selection_button: Button = Button(
        master=lf24,
        text="Select",
        bg="black",
        fg="white",
        compound="left",
        width=115,
        command=not_ready_yet,
        image=customer_icon,
    )
    selection_button.bind(sequence="<Return>", func=lambda event: not_ready_yet())
    selection_button.grid(row=0, column=0, padx=5)

    exit_button: Button = Button(
        master=lf24,
        text="Exit",
        bg="red",
        fg="white",
        compound="left",
        width=115,
        command=exit_app,
        image=exit_icon,
    )
    exit_button.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_button.grid(row=0, column=1, padx=5)

    print(Fore.RED + "Created by FOSS Kingdom | Made with Love in Incredible India.")
    Label(
        master=app,
        text="Created by FOSS Kingdom, Made with Love in Incredible India.",
        bg="black",
        fg="white",
    ).pack(side="bottom", fill="x")

    pstat_label: Label = Label(master=app, bg=accent_color_light)
    pstat_label.pack(side="left", fill="x", padx=10)

    boot_time_label: Label = Label(master=app, bg=accent_color_light)
    boot_time_label.pack(side="right", fill="x", padx=10)

    pstat()

    end_time: float = time()
    elapsed_time = end_time - start_time

    if elapsed_time < 1:
        print(
            Fore.GREEN
            + f"INFO: Booting Time: {round(elapsed_time * 1000, 2)} millisecond(s)"
        )
        boot_time_label.config(
            text=f"Booting Time: {round(elapsed_time * 1000, 2)} millisecond(s)"
        )

    else:
        print(Fore.GREEN + f"INFO: Booting Time: {round(elapsed_time, 3)} second(s)")
        boot_time_label.config(text=f"Booting Time {round(elapsed_time, 3)} second(s)")

    try:
        print(Fore.GREEN + "INFO: Reading database file...")
        conn = connect(database=database_path)
        c = conn.cursor()
        c.execute(
            """create table if not exists
            customers (
            name text not null,
            phone text not null primary key,
            email text,
            dob text,
            gender text not null
            )"""
        )
        conn.commit()

    except OperationalError as operational_error:
        print(Fore.RED + f"ERROR: {operational_error}")
        showinfo(
            title=f"SRM Fashion {__version__}",
            message=f"Sorry, an error occurred! {operational_error}",
        )
        app.destroy()

        if isdir(s=cache_file_path):
            print(Fore.GREEN + "INFO: Cleaning cache files, Please wait...")
            rmtree(path=cache_file_path)

        print(Fore.RED + "Bye...")

        if os_name == "Linux":
            terminal(command="clear")

        if os_name == "Windows":
            terminal(command="cls")

        terminate()

    update_database()

    app.deiconify()
    app.mainloop()

except KeyboardInterrupt:
    print("ERROR: KeyboardInterrupt occurred! Bye...")

except ModuleNotFoundError as module_not_found_error:
    print(f"ERROR: {module_not_found_error}")
