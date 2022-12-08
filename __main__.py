# encoding:     utf-8
# author:       Mohamed Fariz Founder of (FOSS KINGDOM)
# version:      v20221128
# language:     Python v3.10.8
# project_name: TailorMate

# Full forms

# wa        Whatsapp
# yt        YouTube
# ca        Configuration App
# btn       Button
# db        Database
# ph        Phone
# passwd    Password
# lbl       Label
# tot       Total
# ico       Icon
# tm        TailorMater

# NOTES

# Files and media (Apps with this permission can access photos, media and files on your device):
# config.ini
# database.db
# secret.key

# email_validator.validate_email function requires internet connection.
# It helps to check the domain address server is existing or not.

# TODO: int:03d check.
# TODO: send order completion message.
# TODO: send delayed order message.

# Video reference:
# https://www.youtube.com/watch?v=cs6GHOdIZ4E
# https://www.youtube.com/watch?v=XW65JTd8UgI
# https://www.youtube.com/watch?v=jnrCpA1xJPQ
# https://www.youtube.com/watch?v=B-9Ah4dpKJk

# Website reference:
# https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
# https://www.pythontutorial.net/tkinter/tkinter-combobox/
# https://www.tutorialspoint.com/How-do-I-calculate-number-of-days-between-two-dates-using-Python
# https://www.liveagent.com/templates/order-confirmation/
# https://stackoverflow.com/questions/59520520/remove-a-character-on-the-left-of-the-cursor-in-tkinter-entry-widget-in-python-3
# https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding
# https://www.geeksforgeeks.org/response-status_code-python-requests/
# https://pythonexamples.org/python-get-unique-characters-in-a-string/
# https://www.omnicalculator.com/other/password-entropy
# https://www.w3schools.com/python/ref_func_sorted.asp#:~:text=The%20sorted()%20function%20returns,string%20values%20AND%20numeric%20values.
# https://stackoverflow.com/questions/1801668/convert-a-list-with-strings-all-to-lowercase-or-uppercase
# https://www.codingem.com/remove-spaces-from-string-in-python/
# https://www.w3schools.com/html/html_lists_unordered.asp


def play_bell_sound(master, bell_var):
    if bell_var.get():
        master.bell()


def clrscr():
    if os_env == "Linux":
        terminal(command="clear")

    elif os_env == "Windows":
        terminal(command="cls")

    else:
        pass


def clean_cache():
    cache_file_path: str = join(BASE_PATH, "__pycache__")

    if isdir(s=cache_file_path):
        print(F_GREEN + "[INFO]\tCleaning cache files, Please wait...")
        rmtree(path=cache_file_path)


def update_configuration(section: str, option: str, value) -> None:
    config.set(section=section, option=option, value=value)

    config_file = open(file=config_file_path, mode="w")
    config.write(fp=config_file)
    config_file.close()


def toggle_root_passwd():
    if toggle_root_passwd_var.get():
        ca_passwd_entry1.config(show="")
        ca_passwd_entry2.config(show="")

    else:
        ca_passwd_entry1.config(show="*")
        ca_passwd_entry2.config(show="*")


def toggle_smtp_passwd():
    if toggle_smtp_passwd_var.get():
        smtp_passwd_entry.config(show="")

    else:
        smtp_passwd_entry.config(show="*")


def validate_root_passwd():
    ca_passwd_lbl1.config(fg="#000")

    root_passwd1: str = ca_passwd_var1.get()
    root_passwd2: str = ca_passwd_var2.get()

    if not root_passwd1:
        print(F_YELLOW + "[INFO]\tPlease create a new root password...")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please create a new root password...",
        )
        ca.deiconify()

        return None

    if len(root_passwd1) < 8:
        print(F_RED + "[INFO]\tUse 8 characters or more for your password!")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Use 8 characters or more for your password!",
        )
        ca.deiconify()

        return None

    if not root_passwd1 == root_passwd2:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tPassword doesn't match, Please try again...")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Password doesn't match, Please try again...",
        )
        ca.deiconify()

        return None

    return encrypt_root_passwd(passwd=root_passwd1)


def check_passwd_strength():
    passwd_strength_btn.config(text="Checking...", state=DISABLED)
    passwd_strength_btn.update()

    entropy_lbl.config(text="* Entropy: 0.00 bit(s)")
    passwd_strength_lbl.config(text="* Strength: NA")

    if validate_root_passwd() is None:
        ca_tab_view.select(tab_id=2)

        ca_passwd_lbl1.config(fg="red")
        ca_passwd_entry1.focus()

        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

        return None

    root_passwd: str = ca_passwd_var1.get()

    if ca_hibp_var.get():
        try:
            hashed_passwd = sha1(root_passwd.encode()).hexdigest().lower()
            first_5_hash_chars = hashed_passwd[0:5]
            remaining_hash = hashed_passwd[5:]

            response = request(
                method="GET",
                url=f"https://api.pwnedpasswords.com/range/{first_5_hash_chars}",
            ).text.split(sep="\r\n")

            for _ in response:
                response_list: list = _.split(sep=":")

                if response_list[0].lower() == remaining_hash:
                    print(
                        F_RED
                        + f"[WARN]\tOh no — pwned! This password has been seen {response_list[1]} times before"
                    )

                    ca.withdraw()
                    play_bell_sound(master=ca, bell_var=ca_bell_var)
                    showwarning(
                        title=f"TailorMate {__version__}",
                        message=f"Oh no — pwned! This password has been seen {response_list[1]} times before",
                    )
                    ca.deiconify()

                    ca_tab_view.select(tab_id=2)

                    ca_passwd_lbl1.config(fg="red")
                    ca_passwd_entry1.focus()

                    passwd_strength_lbl.config(text="* Strength: [WEAK]")
                    passwd_strength_btn.config(text="Check Strength", state=NORMAL)

                    return None

        except ConnectTimeout as connect_timeout:
            print(F_BLUE + "=" * 80)
            print(F_RED + "Error Code: requests.exceptions.ConnectTimeout")
            print(F_RED + f"[ERROR]\t{connect_timeout}")
            print(F_BLUE + "=" * 80)

            ca.withdraw()
            play_bell_sound(master=ca, bell_var=ca_bell_var)
            showwarning(
                title=f"TailorMate {__version__}",
                message="Error Code: requests.exceptions.ConnectTimeout\n\n"
                "Connection Timed Out! Failed to connect https://api.pwnedpasswords.com/\n\n"
                "Unable to check for pwned password.",
            )
            ca.deiconify()

            ca_tab_view.select(tab_id=2)

            passwd_strength_lbl.config(
                text="* Strength: Failed to check for pwned password!"
            )
            passwd_strength_btn.config(text="Check Strength", state=NORMAL)

            return None

        except ConnectionError as connection_error:
            print(F_BLUE + "=" * 80)
            print(F_RED + "Error Code: requests.exceptions.ConnectionError")
            print(F_RED + f"[ERROR]\t{connection_error}")
            print(F_BLUE + "=" * 80)

            ca.withdraw()
            play_bell_sound(master=ca, bell_var=ca_bell_var)
            showwarning(
                title=f"TailorMate {__version__}",
                message="Error Code: requests.exceptions.ConnectionError\n\n"
                "Hmm. We’re having trouble finding https://api.pwnedpasswords.com/\n\n"
                "Unable to check for pwned password.",
            )
            ca.deiconify()

            ca_tab_view.select(tab_id=2)

            passwd_strength_lbl.config(
                text="* Strength: Failed to check for pwned password!"
            )
            passwd_strength_btn.config(text="Check Strength", state=NORMAL)

            return None

    # +-------------------------------------+
    # | Total no. of possible characters    |
    # +-----------------------+-------------+
    # | (Upper Case)          | 26          |
    # | (Lower Case)          | 26          |
    # | (Numbers)             | 10          |
    # | (Special Characters)  | 32          |
    # | (Space)               | 01          |
    # +-----------------------+-------------+
    # | Total                 | 95          |
    # +-----------------------+-------------+

    unique_characters: set = set(root_passwd)
    pool_size: int = len(unique_characters)
    passwd_length: int = len(root_passwd)

    entropy: float = round(passwd_length * log(pool_size) / log(2), 2)
    entropy_lbl.config(text=f"* Entropy: {entropy} bit(s)")

    if 0 <= entropy < 18:
        print(F_RED + "[WARN]\tExtremely weak password. Improve it! 😨")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showwarning(
            title=f"TailorMate {__version__}",
            message=f"Extremely weak password. Improve it! 😨",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=2)

        ca_passwd_lbl1.config(fg="red")
        ca_passwd_entry1.focus()

        passwd_strength_lbl.config(
            text="* Strength: Extremely weak password. Improve it! 😨"
        )
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

        return None

    if 18 <= entropy < 28:
        print(
            F_YELLOW + "[WARN]\tWeak password. Think about choosing a stronger one! 😟"
        )

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showwarning(
            title=f"TailorMate {__version__}",
            message=f"Weak password. Think about choosing a stronger one! 😟",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=2)

        ca_passwd_lbl1.config(fg="red")
        ca_passwd_entry1.focus()

        passwd_strength_lbl.config(
            text="* Strength: Weak password. Think about choosing a stronger one! 😟"
        )
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

        return None

    if 28 <= entropy < 36:
        print(
            F_GREEN
            + "[INFO]\tReasonable password. It will do for non-vital accounts! 😐"
        )

        passwd_strength_lbl.config(
            text="* Strength: Reasonable password. It will do for non-vital accounts! 😐"
        )
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

    if 36 <= entropy < 60:
        print(F_GREEN + "[INFO]\tStrong password. Well done! 🙂")

        passwd_strength_lbl.config(text="* Strength: Strong password. Well done! 🙂")
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

    if 60 <= entropy < 128:
        print(F_GREEN + "[INFO]\tVery strong password. Excellent job! 😁")

        passwd_strength_lbl.config(
            text="* Strength: Very strong password. Excellent job! 😁"
        )
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

    if entropy >= 128:
        print(F_GREEN + "[INFO]\tExtremely strong password. A bit overkill, really! 😅")

        passwd_strength_lbl.config(
            text="* Strength: Extremely strong password. A bit overkill, really! 😅"
        )
        passwd_strength_btn.config(text="Check Strength", state=NORMAL)

    passwd_strength_btn.config(text="Check Strength", state=NORMAL)

    return not None


def update_theme_color() -> None:  # This static function only works on setting configuration
    ca_selected_theme: str = ca_theme_var.get()

    if ca_selected_theme == themes_list[0] or (
        ca_selected_theme == themes_list[2] and isLight()
    ):
        ca_theme_table.config(bg="#fff", fg="#000")
        ca_theme_table["menu"].config(bg="#fff", fg="#000")

    elif ca_selected_theme == themes_list[1] or (
        ca_selected_theme == themes_list[2] and isDark()
    ):
        ca_theme_table.config(bg="#000", fg="#fff")
        ca_theme_table["menu"].config(bg="#000", fg="#fff")


def create_configuration() -> None:
    ca_save_btn.config(text="Saving...", state=DISABLED)
    ca_save_btn.update()

    ####################################################################################################################

    if not eula_var.get():
        print(F_RED + "[INFO]\tPlease accept the license agreement.")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please accept the license agreement.",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=0)

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ####################################################################################################################

    if not isfile(path=private_key_path):
        print(F_GREEN + "[INFO]\tGenerating new private key...")
        gen_private_key(key_path=private_key_path)

    ####################################################################################################################

    ca_name_lbl.config(fg="#000")
    business_name: str = business_name_var.get().strip().upper()

    if not business_name:
        print(F_YELLOW + "[INFO]\tPlease enter your legal business name.")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please enter your legal business name.",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=1)

        ca_name_lbl.config(fg="red")
        ca_name_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ####################################################################################################################

    business_type: str = business_type_var.get()

    ####################################################################################################################

    ca_country_lbl.config(fg="#000")
    ca_selected_country: str = ca_country_var.get()

    if not ca_selected_country.lower() in [_.lower() for _ in country_names]:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tInvalid country selection, Please try again...")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Invalid country selection, Please try again...",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=1)

        ca_country_lbl.config(fg="red")

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ####################################################################################################################

    ca_ph_lbl.config(fg="#000")
    ph: str or None = validate_ph(ph_no_var=ca_ph_var, master=ca, bell_var=ca_bell_var)

    if ph is None:
        ca_tab_view.select(tab_id=1)

        ca_ph_lbl.config(fg="red")
        ca_ph_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ####################################################################################################################

    ca_website_lbl.config(fg="#000")
    business_website: str = ca_website_var.get().strip().lower()

    if business_website:
        try:
            status_code: int = get(url=business_website).status_code

            if status_code == 200:
                print(F_GREEN + "[INFO]\tURL Response Status: 200 (OK)")

            elif status_code == 404:
                print(F_BLUE + "=" * 80)
                print(F_RED + "[ERROR]\tURL Response Status: 404 (NOT FOUND)")
                print(F_BLUE + "=" * 80)

                ca.withdraw()
                play_bell_sound(master=ca, bell_var=ca_bell_var)
                showwarning(
                    title=f"TailorMate {__version__}",
                    message="URL Response Status: 404 (NOT FOUND)",
                )
                ca.deiconify()

                ca_tab_view.select(tab_id=1)

                ca_website_lbl.config(fg="red")
                ca_website_entry.focus()

                ca_save_btn.config(text="Save", state=NORMAL)

                return None

            else:
                print(F_BLUE + "=" * 80)
                print(F_RED + f"[ERROR]\tURL Response Status: {status_code}")
                print(F_BLUE + "=" * 80)

                ca.withdraw()
                play_bell_sound(master=ca, bell_var=ca_bell_var)
                showwarning(
                    title=f"TailorMate {__version__}",
                    message=f"URL Response Status: {status_code}",
                )
                ca.deiconify()

                ca_tab_view.select(tab_id=1)

                ca_website_lbl.config(fg="red")
                ca_website_entry.focus()

                ca_save_btn.config(text="Save", state=NORMAL)

                return None

        except MissingSchema as missing_schema:
            print(F_BLUE + "=" * 80)
            print(F_RED + "Error Code: requests.exceptions.MissingSchema")
            print(F_RED + f"[ERROR]\t{missing_schema}")
            print(F_BLUE + "=" * 80)

            ca.withdraw()
            play_bell_sound(master=ca, bell_var=ca_bell_var)
            showwarning(
                title=f"TailorMate {__version__}",
                message=f"Error Code: requests.exceptions.MissingSchema\n\n{missing_schema}",
            )
            ca.deiconify()

            ca_tab_view.select(tab_id=1)

            ca_website_lbl.config(fg="red")
            ca_website_entry.focus()

            ca_save_btn.config(text="Save", state=NORMAL)

            return None

        except ConnectTimeout as connect_timeout:
            print(F_BLUE + "=" * 80)
            print(F_RED + "Error Code: requests.exceptions.ConnectTimeout")
            print(F_RED + f"[ERROR]\t{connect_timeout}")
            print(F_BLUE + "=" * 80)

            ca.withdraw()
            play_bell_sound(master=ca, bell_var=ca_bell_var)
            showwarning(
                title=f"TailorMate {__version__}",
                message="Error Code: requests.exceptions.ConnectTimeout\n\n"
                f"The connection has timed out! Failed to load {business_website}",
            )
            ca.deiconify()

            ca_tab_view.select(tab_id=1)

            ca_website_lbl.config(fg="red")
            ca_website_entry.focus()

            ca_save_btn.config(text="Save", state=NORMAL)

            return None

        except ConnectionError as connection_error:
            print(F_BLUE + "=" * 80)
            print(F_RED + "Error Code: requests.exceptions.ConnectionError")
            print(F_RED + f"[ERROR]\t{connection_error}")
            print(F_BLUE + "=" * 80)

            ca.withdraw()
            play_bell_sound(master=ca, bell_var=ca_bell_var)
            showwarning(
                title=f"TailorMate {__version__}",
                message="Error Code: requests.exceptions.ConnectionError\n\n"
                f"Hmm. We’re having trouble finding {business_website}",
            )
            ca.deiconify()

            ca_tab_view.select(tab_id=1)

            ca_website_lbl.config(fg="red")
            ca_website_entry.focus()

            ca_save_btn.config(text="Save", state=NORMAL)

            return None

    ####################################################################################################################

    root_passwd: str or None = validate_root_passwd()

    if root_passwd is None:
        ca_tab_view.select(tab_id=2)

        ca_passwd_lbl1.config(fg="red")
        ca_passwd_entry1.focus()

        ca_save_btn.config(text="Save", state=NORMAL)
        return None

    ####################################################################################################################

    if check_passwd_strength() is None:
        ca_save_btn.config(text="Save", state=NORMAL)
        return None

    ####################################################################################################################

    smtp_email_lbl.config(fg="#000")
    ca_smtp_email: str = smtp_email_var.get().strip().lower()

    if not ca_smtp_email:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tPLease enter your E-mail address.")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please enter your email address.",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_email_lbl.config(fg="red")
        smtp_email_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    try:
        ca_smtp_email = validate_email(
            email=ca_smtp_email, check_deliverability=False
        ).email

    except EmailNotValidError as email_not_valid_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: email_validator.EmailNotValidError")
        print(F_RED + f"[ERROR]\t{email_not_valid_error}")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(title=f"TailorMate {__version__}", message=f"{email_not_valid_error}")
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_email_lbl.config(fg="red")
        smtp_email_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    split_email: list = ca_smtp_email.split(sep="@")

    email_username: str = split_email[0]
    email_domain_address: str = split_email[1]

    if not email_domain_address == "gmail.com":
        print(F_RED + "[INFO]\tWe only handles Gmail address for now.")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="We only handles Gmail address for now.",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_email_lbl.config(fg="red")
        smtp_email_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    if len(email_username) < 6 or len(email_username) > 30:
        print(F_RED + "[INFO]\tInvalid email address, Please try again...")

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Invalid email address, Please try again...",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_email_lbl.config(fg="red")
        smtp_email_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    if (
        email_username == "arsehole"
        or email_username == "bastard"
        or email_username == "beaver"
        or email_username == "bollock"
        or email_username == "dickhead"
        or email_username == "goddam"
        or email_username == "hooker"
        or email_username == "hotmail"
        or email_username == "microsoft"
        or email_username == "outlook"
        or email_username == "pervert"
        or email_username == "pissed"
        or email_username == "pussies"
        or email_username == "punani"
        or email_username == "sample"
        or email_username == "username"
        or email_username == "vagina"
        or email_username.__contains__("account")
        or email_username.__contains__("admin")
        or email_username.__contains__("asshole")
        or email_username.__contains__("bitch")
        or email_username.__contains__("bullshit")
        or email_username.__contains__("cunt")
        or email_username.__contains__("fuck")
        or email_username.__contains__("gmail")
        or email_username.__contains__("google")
        or email_username.__contains__("pussy")
    ):
        print(
            F_RED
            + "[INFO]\tInvalid email address! This username isn't allowed. Try again."
        )

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Invalid email address! This username isn't allowed. Try again.",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_email_lbl.config(fg="red")
        smtp_email_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ####################################################################################################################

    smtp_passwd_lbl.config(fg="#000")
    ca_smtp_passwd: str = smtp_passwd_var.get()

    if not ca_smtp_passwd:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tPlease enter your password!")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}", message="Please enter your password!"
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_passwd_lbl.config(fg="red")
        smtp_passwd_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    if not len(ca_smtp_passwd) == 16 or not ca_smtp_passwd.isalpha():
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tIncorrect SMTP password! Please try again...")
        print(F_BLUE + "=" * 80)

        ca.withdraw()
        play_bell_sound(master=ca, bell_var=ca_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Incorrect Password! Please try again..",
        )
        ca.deiconify()

        ca_tab_view.select(tab_id=3)

        smtp_passwd_lbl.config(fg="red")
        smtp_passwd_entry.focus()

        ca_save_btn.config(text="Save", state=NORMAL)

        return None

    ca_smtp_passwd = encrypt_smtp_passwd(data=ca_smtp_passwd, key_path=private_key_path)

    ####################################################################################################################

    config.add_section(section="userprofile")
    update_configuration(
        section="userprofile", option="business_name", value=business_name
    )
    update_configuration(
        section="userprofile", option="business_type", value=business_type
    )
    update_configuration(
        section="userprofile", option="country", value=ca_selected_country
    )
    update_configuration(section="userprofile", option="phone", value=ph)
    update_configuration(
        section="userprofile", option="business_website", value=business_website
    )

    ####################################################################################################################

    config.add_section(section="root_password")
    update_configuration(section="root_password", option="password", value=root_passwd)

    ####################################################################################################################

    config.add_section(section="smtp_server")
    update_configuration(section="smtp_server", option="email", value=ca_smtp_email)
    update_configuration(section="smtp_server", option="password", value=ca_smtp_passwd)

    ####################################################################################################################

    config.add_section(section="options")
    update_configuration(
        section="options", option="weeks_number", value=str(ca_weeks_number_var.get())
    )
    update_configuration(
        section="options",
        option="other_month_days",
        value=str(ca_other_month_days_var.get()),
    )
    update_configuration(
        section="options", option="check_mxdns_record", value=str(ca_mxdns_var.get())
    )
    update_configuration(
        section="options", option="play_sound", value=str(ca_bell_var.get())
    )

    ca_selected_theme: str = ca_theme_var.get()

    if ca_selected_theme == themes_list[0]:
        update_configuration(section="options", option="theme", value="light")

    elif ca_selected_theme == themes_list[1]:
        update_configuration(section="options", option="theme", value="dark")

    else:
        update_configuration(section="options", option="theme", value="system_default")

    ####################################################################################################################

    print(F_GREEN + "[INFO]\tConfiguration file created successfully...")

    ca_save_btn.config(text="Save", state=NORMAL)
    ca.destroy()

    ####################################################################################################################


def exit_ca() -> None:
    ca.destroy()

    clean_cache()

    print(F_RED + "Bye...")

    clrscr()
    terminate()


def virtual_keyboard_entry(key: str):
    if sa_passwd_entry.selection_present():
        sa_passwd_entry.delete(first="sel.first", last="sel.last")

    position: int = sa_passwd_entry.index(index=INSERT)
    sa_passwd_entry.insert(index=position, string=key)
    sa_passwd_entry.focus()


def virtual_keyboard_backspace():
    if sa_passwd_entry.selection_present():
        sa_passwd_entry.delete(first="sel.first", last="sel.last")

    else:
        position: int = sa_passwd_entry.index(index=INSERT)
        sa_passwd_entry.delete(first=position - 1)

    sa_passwd_entry.focus()


def virtual_keyboard_delete():
    if sa_passwd_entry.selection_present():
        sa_passwd_entry.delete(first="sel.first", last="sel.last")

    else:
        position: int = sa_passwd_entry.index(index=INSERT)
        sa_passwd_entry.delete(first=position + 1)

    sa_passwd_entry.focus()


def configure_caps_lock():
    if caps_lock_state.get():
        q_btn.config(text="q", command=lambda: virtual_keyboard_entry(key="q"))
        q_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="q")
        )

        w_btn.config(text="w", command=lambda: virtual_keyboard_entry(key="w"))
        w_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="w")
        )

        e_btn.config(text="e", command=lambda: virtual_keyboard_entry(key="e"))
        e_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="e")
        )

        r_btn.config(text="r", command=lambda: virtual_keyboard_entry(key="r"))
        r_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="r")
        )

        t_btn.config(text="t", command=lambda: virtual_keyboard_entry(key="t"))
        t_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="t")
        )

        y_btn.config(text="y", command=lambda: virtual_keyboard_entry(key="y"))
        y_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="y")
        )

        u_btn.config(text="u", command=lambda: virtual_keyboard_entry(key="u"))
        u_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="u")
        )

        i_btn.config(text="i", command=lambda: virtual_keyboard_entry(key="i"))
        i_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="i")
        )

        o_btn.config(text="o", command=lambda: virtual_keyboard_entry(key="o"))
        o_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="o")
        )

        p_btn.config(text="p", command=lambda: virtual_keyboard_entry(key="p"))
        p_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="p")
        )

        a_btn.config(text="a", command=lambda: virtual_keyboard_entry(key="a"))
        a_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="a")
        )

        s_btn.config(text="s", command=lambda: virtual_keyboard_entry(key="s"))
        s_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="s")
        )

        d_btn.config(text="d", command=lambda: virtual_keyboard_entry(key="d"))
        d_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="d")
        )

        f_btn.config(text="f", command=lambda: virtual_keyboard_entry(key="f"))
        f_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="f")
        )

        g_btn.config(text="g", command=lambda: virtual_keyboard_entry(key="g"))
        g_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="g")
        )

        h_btn.config(text="h", command=lambda: virtual_keyboard_entry(key="h"))
        h_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="h")
        )

        j_btn.config(text="j", command=lambda: virtual_keyboard_entry(key="j"))
        j_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="j")
        )

        k_btn.config(text="k", command=lambda: virtual_keyboard_entry(key="k"))
        k_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="k")
        )

        l_btn.config(text="l", command=lambda: virtual_keyboard_entry(key="l"))
        l_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="l")
        )

        z_btn.config(text="z", command=lambda: virtual_keyboard_entry(key="z"))
        z_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="z")
        )

        x_btn.config(text="x", command=lambda: virtual_keyboard_entry(key="x"))
        x_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="x")
        )

        c_btn.config(text="c", command=lambda: virtual_keyboard_entry(key="c"))
        c_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="c")
        )

        v_btn.config(text="v", command=lambda: virtual_keyboard_entry(key="v"))
        v_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="v")
        )

        b_btn.config(text="b", command=lambda: virtual_keyboard_entry(key="b"))
        b_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="b")
        )

        n_btn.config(text="n", command=lambda: virtual_keyboard_entry(key="n"))
        n_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="n")
        )

        m_btn.config(text="m", command=lambda: virtual_keyboard_entry(key="m"))
        m_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="m")
        )

        caps_lock_btn.config(text="Caps Lock OFF")
        caps_lock_btn.bind(
            sequence="<Return>",
            func=lambda event: caps_lock_btn.config(text="Caps Lock OFF"),
        )

    else:
        q_btn.config(text="Q", command=lambda: virtual_keyboard_entry(key="Q"))
        q_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="Q")
        )

        w_btn.config(text="W", command=lambda: virtual_keyboard_entry(key="W"))
        w_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="W")
        )

        e_btn.config(text="E", command=lambda: virtual_keyboard_entry(key="E"))
        e_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="E")
        )

        r_btn.config(text="R", command=lambda: virtual_keyboard_entry(key="R"))
        r_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="R")
        )

        t_btn.config(text="T", command=lambda: virtual_keyboard_entry(key="T"))
        t_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="T")
        )

        y_btn.config(text="Y", command=lambda: virtual_keyboard_entry(key="Y"))
        y_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="Y")
        )

        u_btn.config(text="U", command=lambda: virtual_keyboard_entry(key="U"))
        u_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="U")
        )

        i_btn.config(text="I", command=lambda: virtual_keyboard_entry(key="I"))
        i_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="I")
        )

        o_btn.config(text="O", command=lambda: virtual_keyboard_entry(key="O"))
        o_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="O")
        )

        p_btn.config(text="P", command=lambda: virtual_keyboard_entry(key="P"))
        p_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="P")
        )

        a_btn.config(text="A", command=lambda: virtual_keyboard_entry(key="A"))
        a_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="A")
        )

        s_btn.config(text="S", command=lambda: virtual_keyboard_entry(key="S"))
        s_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="S")
        )

        d_btn.config(text="D", command=lambda: virtual_keyboard_entry(key="D"))
        d_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="D")
        )

        f_btn.config(text="F", command=lambda: virtual_keyboard_entry(key="F"))
        f_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="F")
        )

        g_btn.config(text="G", command=lambda: virtual_keyboard_entry(key="G"))
        g_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="G")
        )

        h_btn.config(text="H", command=lambda: virtual_keyboard_entry(key="H"))
        h_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="H")
        )

        j_btn.config(text="J", command=lambda: virtual_keyboard_entry(key="J"))
        j_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="J")
        )

        k_btn.config(text="K", command=lambda: virtual_keyboard_entry(key="K"))
        k_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="K")
        )

        l_btn.config(text="L", command=lambda: virtual_keyboard_entry(key="L"))
        l_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="L")
        )

        z_btn.config(text="Z", command=lambda: virtual_keyboard_entry(key="Z"))
        z_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="Z")
        )

        x_btn.config(text="X", command=lambda: virtual_keyboard_entry(key="X"))
        x_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="X")
        )

        c_btn.config(text="C", command=lambda: virtual_keyboard_entry(key="C"))
        c_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="C")
        )

        v_btn.config(text="V", command=lambda: virtual_keyboard_entry(key="V"))
        v_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="V")
        )

        b_btn.config(text="B", command=lambda: virtual_keyboard_entry(key="B"))
        b_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="B")
        )

        n_btn.config(text="N", command=lambda: virtual_keyboard_entry(key="N"))
        n_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="N")
        )

        m_btn.config(text="M", command=lambda: virtual_keyboard_entry(key="M"))
        m_btn.bind(
            sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="M")
        )

        caps_lock_btn.config(text="Caps Lock ON")
        caps_lock_btn.bind(
            sequence="<Return>",
            func=lambda event: caps_lock_btn.config(text="Caps Lock ON"),
        )

    caps_lock_state.set(value=not caps_lock_state.get())


def check_root_passwd() -> None:
    sa_passwd_lbl.config(fg="#000")

    passwd: bytes = sa_passwd_var.get().encode(encoding="utf-8")
    hashed_passwd: bytes = config.get(
        section="root_password", option="password"
    ).encode(encoding="utf-8")

    if not checkpw(passwd, hashed_passwd):
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tIncorrect Password! Please Try again...")
        print(F_BLUE + "=" * 80)

        sa_passwd_lbl.config(fg="red")
        sa_passwd_entry.delete(first=0, last=END)
        sa_passwd_entry.focus()

        sa.withdraw()
        showinfo(
            title=f"TailorMate {__version__}",
            message="Incorrect Password! Please try again...",
        )
        sa.deiconify()
        return None

    sa.destroy()
    return None


def exit_sa():
    sa.destroy()

    clean_cache()

    print(F_RED + "Bye...")

    clrscr()
    terminate()


def add_order():
    update_orders()
    update_customers()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    main_tab_view.select(tab_id=1)


def navigate_create_customer():
    update_orders()
    update_customers()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    main_tab_view.select(tab_id=1)
    name_entry.focus()


def navigate_search_customer():
    update_orders()
    update_customers()

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    main_tab_view.select(tab_id=1)
    search_entry.focus()


def update_weeknumbers_setting() -> None:
    weeks_number: bool = weeks_number_var.get()

    day_selection.config(showweeknumbers=weeks_number)
    delivery_date_selection.config(showweeknumbers=weeks_number)

    update_configuration(
        section="options", option="weeks_number", value=str(weeks_number)
    )


def update_othermonthdays_settings() -> None:
    other_month_days: bool = other_month_days_var.get()

    day_selection.config(showothermonthdays=other_month_days)
    delivery_date_selection.config(showothermonthdays=other_month_days)

    update_configuration(
        section="options", option="other_month_days", value=str(other_month_days)
    )


def get_resolution_size() -> None:
    print(tm.winfo_width(), tm.winfo_height())


def update_welcome_text():
    greetings_lbl.config(
        text=choice(
            [
                "你好",
                "hola!",
                "Hello!",
                "नमस्ते",
                "হ্যালো",
                "olá",
                "привет",
                "こんにちは",
                "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
                "xin chào",
                "नमस्कार",
                "హలో",
                "merhaba",
                "안녕하세요",
                "bonjour",
                "hallo!",
                "வணக்கம்",
                "ہیلو",
                "halo!",
                "ciao!",
            ]
        )
    )
    greetings_lbl.after(ms=5000, func=update_welcome_text)


def send_email(to_addr: str, subject: str, message):
    msg: EmailMessage = EmailMessage()
    msg["From"] = smtp_email
    msg["To"] = to_addr
    msg["Subject"] = subject
    # msg.set_content(message)
    msg.set_content(MIMEText(message, "html"))

    try:
        print(F_YELLOW + "[INFO]\tConnecting to smtp.gmail.com:587, Please wait...")
        setdefaulttimeout(10.0)
        server: SMTP = SMTP(host="smtp.gmail.com", port=587)
        # server: SMTP = SMTP(host="localhost", port=1025)
        server.ehlo()
        print(F_YELLOW + "[INFO]\tStarting TLS Handshake, Please wait...")
        server.starttls()
        server.ehlo()

        print(F_YELLOW + "[INFO]\tLogging in to your gmail account, Please wait...")
        server.login(user=smtp_email, password=smtp_passwd)
        print(F_GREEN + "[INFO]\tLogin success...")
        # msg: str = f"subject: {subject}\n\n{message}"
        # server.sendmail(from_addr=smtp_email, to_addrs=to_addr, msg=msg)
        server.send_message(msg=msg)
        print(F_GREEN + "[INFO]\tEmail sent successfully!")
        server.quit()

    except SMTPAuthenticationError as smtp_authentication_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: smtplib.SMTPAuthenticationError")
        print(F_RED + f"[ERROR]\tFailed to Login. {smtp_authentication_error}")
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=f"Failed to Login. {smtp_authentication_error}",
        )
        tm.deiconify()

    except gaierror as gai_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: sockets.gaierror")
        print(F_RED + f"[ERROR]\t{gai_error}! Failed to send email...")
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=f"{gai_error}! Failed to send email...",
        )
        tm.deiconify()

    # OSError: [Errno 101] Network is unreachable
    except OSError as os_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: OSError")
        print(F_RED + f"[ERROR]\t{os_error}! Failed to send email...")
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"Tailormate {__version__}",
            message=f"{os_error}! Failed to send email...",
        )
        tm.deiconify()


def validate_name(textvariable: str) -> (str or None):
    name: str = textvariable.strip().title()

    if not name:
        print(F_RED + "[INFO]\tPlease enter the customer name.")
        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please enter the customer name.",
        )
        tm.deiconify()
        return None

    return name


def validate_ph(ph_no_var, master, bell_var) -> (str or None):
    ph_no: str = ph_no_var.get().strip()

    if not ph_no:
        print(F_RED + "[INFO]\tPlease enter the phone number.")

        master.withdraw()
        play_bell_sound(master=master, bell_var=bell_var)
        showinfo(
            title=f"TailorMate {__version__}", message="Please enter the phone number."
        )
        master.deiconify()
        return None

    try:
        number_obj = parse(number=ph_no)

    except NumberParseException as number_parse_exception:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: phonenumbers.phonenumberutil.NumberParseException")
        print(F_RED + f"[ERROR]\t{number_parse_exception}")
        print(F_BLUE + "=" * 80)

        master.withdraw()
        play_bell_sound(master=master, bell_var=bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=str(number_parse_exception),
        )
        master.deiconify()
        return None

    ph_no: str = format_number(numobj=number_obj, num_format=1)

    if not is_valid_number(numobj=number_obj):
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tInvalid mobile number.")
        print(F_BLUE + "=" * 80)

        master.withdraw()
        play_bell_sound(master=master, bell_var=bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Invalid mobile number.",
        )
        master.deiconify()
        return None

    return ph_no


def validate_customer_email(textvariable: str) -> (str or None):
    email: str = textvariable.strip().lower()

    if not email:
        return email

    try:
        email = validate_email(email=email, check_deliverability=mxdns_var.get()).email

    except EmailNotValidError as email_not_valid_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: email_validator.EmailNotValidError")
        print(F_RED + f"[ERROR]\t{email_not_valid_error}")
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(title=f"TailorMate {__version__}", message=f"{email_not_valid_error}")
        tm.deiconify()

        return None

    split_email: list = email.split(sep="@")

    email_username: str = split_email[0]
    email_domain_address: str = split_email[1]

    if not email_username or not email_domain_address:
        print(F_RED + "[INFO]\tInvalid email address, Please try again...")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Invalid email address, Please try again...",
        )
        tm.deiconify()
        return None

    if email_domain_address == "gmail.com":
        if len(email_username) < 6 or len(email_username) > 30:
            print(F_RED + "[INFO]\tInvalid email address, Please try again...")

            tm.withdraw()
            play_bell_sound(master=tm, bell_var=tm_bell_var)
            showinfo(
                title=f"TailorMate {__version__}",
                message="Invalid email address, Please try again...",
            )
            tm.deiconify()
            return None

        if (
            email_username == "arsehole"
            or email_username == "bastard"
            or email_username == "beaver"
            or email_username == "bollock"
            or email_username == "dickhead"
            or email_username == "goddam"
            or email_username == "hooker"
            or email_username == "hotmail"
            or email_username == "microsoft"
            or email_username == "outlook"
            or email_username == "pervert"
            or email_username == "pissed"
            or email_username == "pussies"
            or email_username == "punani"
            or email_username == "sample"
            or email_username == "username"
            or email_username == "vagina"
            or email_username.__contains__("account")
            or email_username.__contains__("admin")
            or email_username.__contains__("asshole")
            or email_username.__contains__("bitch")
            or email_username.__contains__("bullshit")
            or email_username.__contains__("cunt")
            or email_username.__contains__("fuck")
            or email_username.__contains__("gmail")
            or email_username.__contains__("google")
            or email_username.__contains__("pussy")
        ):
            print(
                F_RED
                + "[INFO]\tInvalid email address! This username isn't allowed. Try again."
            )

            tm.withdraw()
            play_bell_sound(master=tm, bell_var=tm_bell_var)
            showinfo(
                title=f"TailorMate {__version__}",
                message="Invalid email address! This username isn't allowed. Try again.",
            )
            tm.deiconify()
            return None

    return email


def mark_completed():
    selected_item: str = orders_db.focus()

    if not selected_item:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tPlease select an order first!")
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}", message="Please select an order first!"
        )
        tm.deiconify()

        return None

    order_no: str = orders_db.item(selected_item).get("values")[1]
    rowid: int = int(order_no.replace("#TMO", str()))
    selected_status: str = orders_db.item(selected_item).get("values")[10]

    if selected_status == "Completed":
        print(F_GREEN + "[INFO]\tThis order is already completed!")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="This order is already completed!",
        )
        tm.deiconify()

        return None

    if selected_status == "In Progress":
        c.execute(f"""update orders set status = 'Completed' where rowid = {rowid}""")
        conn.commit()

        update_orders()


def product_delivered():
    pass


def update_orders() -> None:
    orders_db.delete(*orders_db.get_children())

    tot_orders_lbl.config(text="You have zero active orders!")
    active_orders_value.config(text="0 / $0")

    mark_as_completed_btn.config(state=DISABLED)
    product_delivered_btn.config(state=DISABLED)

    serial_no: int = int()
    tot_sales_amount: float = float()
    tot_completed_orders: int = int()
    tot_active_orders: int = int()

    c.execute("select rowid, * from orders")
    for _ in c.fetchall():
        serial_no = serial_no + 1
        order_no = f"#TMO{_[0]:03d}"
        customer_name = _[1]
        created_on = _[2]
        ph_number = _[3]
        item = _[4]
        stitching_type = _[5]
        # notes = _[6]
        cost = _[7]
        delivery_date = _[8]
        priority = _[9]
        status = _[10]

        _: list = [
            serial_no,
            order_no,
            customer_name,
            created_on,
            ph_number,
            item,
            stitching_type,
            cost,
            delivery_date,
            priority,
            status,
        ]

        tot_sales_amount: float = tot_sales_amount + cost

        d0 = date(
            year=int(delivery_date.split("/")[2]),
            month=int(delivery_date.split("/")[0]),
            day=int(delivery_date.split("/")[1]),
        )
        d1 = date(year=today.year, month=today.month, day=today.day)
        delta_d = (d0 - d1).days

        if status == "Completed":
            tot_completed_orders: int = tot_completed_orders + 1
            orders_db.insert(parent="", index=END, values=_, tags="completed")

        elif status == "In Progress":
            tot_active_orders: int = tot_active_orders + 1

            if delta_d <= 1:
                orders_db.insert(parent="", index=END, values=_, tags="danger")

            elif delta_d <= 3:
                orders_db.insert(parent="", index=END, values=_, tags="warning")

            elif serial_no % 2 == 0:
                orders_db.insert(parent="", index=END, values=_, tags="even")

            elif serial_no % 2 == 1:
                orders_db.insert(parent="", index=END, values=_, tags="odd")

    if len(orders_db.get_children()):
        orders_db.tag_configure(
            tagname="warning", background="orange", foreground="#fff"
        )
        orders_db.tag_configure(tagname="danger", background="red", foreground="#fff")
        orders_db.tag_configure(
            tagname="completed", background="green", foreground="#fff"
        )

        tot_orders_lbl.config(
            text=f"You have {tot_active_orders} active order(s) and {tot_completed_orders} completed order(s)!"
        )
        active_orders_value.config(text=f"{tot_active_orders} / ${tot_sales_amount}")

        mark_as_completed_btn.config(state=NORMAL)
        product_delivered_btn.config(state=NORMAL)


def update_customers() -> None:
    customers_db.delete(*customers_db.get_children())

    tot_customers_lbl.config(text="No customer(s) found! Create New.")

    search_entry.config(state=DISABLED)
    search_btn.config(state=DISABLED)
    delete_btn.config(state=DISABLED)
    update_btn.config(state=DISABLED)
    select_btn.config(state=DISABLED)

    name_entry3.config(state=DISABLED)
    ph_entry3.config(state=DISABLED)
    email_entry3.config(state=DISABLED)
    rb1.config(state=DISABLED)
    rb2.config(state=DISABLED)
    rb3.config(state=DISABLED)
    rb4.config(state=DISABLED)
    rb5.config(state=DISABLED)
    notes_entry.config(state=DISABLED)
    notes_entry.unbind(sequence="<Button-3>")
    cost_entry.config(state=DISABLED)
    priority_btn.config(state=DISABLED)
    save_item_btn.config(state=DISABLED)

    tot_customers_value.config(text="0")

    c.execute("select * from customers")

    serial_no: int = int()
    for _ in c.fetchall():
        serial_no: int = serial_no + 1
        name: str = _[0]
        created_on: str = _[1]
        # iso_code: str = _[2]
        ph: str = _[2]
        email: str = _[3]
        dob: str = _[4]
        gender: str = _[5]

        _: list = [serial_no, name, created_on, ph, email, dob, gender]

        if serial_no % 2 == 0:
            customers_db.insert(parent="", index=END, values=_, tags="even")

        elif serial_no % 2 == 1:
            customers_db.insert(parent="", index=END, values=_, tags="odd")

    tot_customers: int = len(customers_db.get_children())
    if tot_customers:
        tot_customers_lbl.config(text=f"{tot_customers} customer(s) found!")

        search_entry.config(state=NORMAL)
        search_btn.config(state=NORMAL)
        delete_btn.config(state=NORMAL)
        update_btn.config(state=NORMAL)
        select_btn.config(state=NORMAL)

        name_entry3.config(state=NORMAL)
        ph_entry3.config(state=NORMAL)
        email_entry3.config(state=NORMAL)
        rb1.config(state=NORMAL)
        rb2.config(state=NORMAL)
        rb3.config(state=NORMAL)
        rb4.config(state=NORMAL)
        rb5.config(state=NORMAL)
        notes_entry.config(state=NORMAL)
        notes_entry.bind(
            sequence="<Button-3>",
            func=lambda event: notes_popup_menu.tk_popup(
                x=event.x_root, y=event.y_root
            ),
        )
        cost_entry.config(state=NORMAL)
        priority_btn.config(state=NORMAL)
        save_item_btn.config(state=NORMAL)

        tot_customers_value.config(text=f"{tot_customers}")


def fetch_data() -> None:
    selected_id: str = customers_db.focus()

    if not selected_id:
        return None

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

    customer_data: list = customers_db.item(item=selected_id).get("values")
    name_var1.set(value=customer_data[1])
    # isd_code_var1.set(value="+" + str(customer_data[3]))
    ph_var1.set(value=customer_data[3])
    email_var1.set(value=customer_data[4])

    try:
        day_selection.selection_set(date=customer_data[5])

    except ValueError:
        day_selection.selection_set(
            date=date(year=today.year - 18, month=today.month, day=today.day)
        )
        day_selection.selection_clear()

    selected_gender: str = customer_data[6]

    if selected_gender == gender_options[0]:
        gender_var.set(value=gender_options[0])
        update_gender_color()

    elif selected_gender == gender_options[1]:
        gender_var.set(value=gender_options[1])
        update_gender_color()

    else:
        gender_var.set(value=gender_options[2])
        update_gender_color()


def search_record() -> None:
    update_orders()

    # 10-18-2022: We removed update_customers() function to avoid unwanted glitches
    # update_customers()

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    search: str = search_var.get().strip()

    if not search:
        update_customers()
        return None

    runtime_search_lbl.config(text="Searching for customer records...")
    runtime_search_lbl.update()

    try:
        number_object = parse(number=search)
        search: str = format_number(numobj=number_object, num_format=1)

        tot_records: list = list()

        if is_valid_number(numobj=number_object):
            c.execute(f"select * from customers where phone like '%{search}%'")
            tot_records = c.fetchall()

    except NumberParseException:
        c.execute(
            f"select * from customers where name like '%{search}%' or email like '%{search}%'"
        )
        tot_records = c.fetchall()

    customers_db.delete(*customers_db.get_children())
    tot_customers_lbl.config(text="No record found!")

    if not tot_records:
        print(F_RED + "[INFO]\tNo record found!")
        runtime_search_lbl.config(text=str())
        return None

    count: int = 0
    for _ in tot_records:
        count: int = count + 1
        name: str = _[0]
        created_on: str = _[1]
        # isd_code: str = _[2]
        ph: str = _[2]
        email: str = _[3]
        dob: str = _[4]
        gender: str = _[5]

        _: list = [count, name, created_on, ph, email, dob, gender]

        # runtime_search_lbl.config(text=name)
        # runtime_search_lbl.update()

        if count % 2 == 0:
            customers_db.insert(parent="", index=END, values=_, tags="even")

        else:
            customers_db.insert(parent="", index=END, values=_, tags="odd")

    tot_customers_lbl.config(text=f"{len(tot_records)} record(s) found!")
    runtime_search_lbl.config(text=str())


def clear_date() -> None:
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()


def update_gender_color() -> None:
    gender: str = gender_var.get()

    if gender == gender_options[0]:
        gender_table.config(bg="#C01493", activebackground="#FF1493")
        gender_table["menu"].config(bg="#C01493", activebackground="#FF1493")

    elif gender == gender_options[1]:
        gender_table.config(bg="#000080", activebackground="#2020C0")
        gender_table["menu"].config(bg="#000080", activebackground="#2020C0")

    else:
        gender_table.config(bg="#000", activebackground="#404040")
        gender_table["menu"].config(bg="#000", activebackground="#404040")


def create_entry() -> None:
    create_btn.config(text="Creating...", state=DISABLED)
    create_btn.update()

    update_orders()
    update_customers()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    name: str or None = validate_name(textvariable=name_var1.get())
    if name is None:
        name_lbl.config(fg="red")
        name_entry.focus()

        create_btn.config(text="Create New", state=NORMAL)

        return None

    # isd_code: str = isd_code_var1.get()
    ph: str or None = validate_ph(ph_no_var=ph_var1, master=tm, bell_var=tm_bell_var)
    if ph is None:
        ph_lbl2.config(fg="red")
        ph_entry.focus()

        create_btn.config(text="Create New", state=NORMAL)

        return None

    email: str or None = validate_customer_email(textvariable=email_var1.get())
    if email is None:
        email_lbl.config(fg="red")
        email_entry.focus()

        create_btn.config(text="Create New", state=NORMAL)

        return None

    dob: str = day_selection.get_date()
    gender: str = gender_var.get()

    try:
        c.execute(
            """insert into customers values (
            ?, ?, ?, ?, ?, ?
            )""",
            (name, strftime("%Y-%m-%d %H:%M:%S"), ph, email, dob, gender),
        )

    except IntegrityError as integrity_error:
        ph_lbl2.config(fg="red")
        ph_entry.focus()

        print(F_RED + "[INFO]\tThis mobile number already exists.")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=f"{integrity_error}\n{ph} This mobile number already exist.",
        )
        tm.deiconify()

        create_btn.config(text="Create New", state=NORMAL)

        return None

    conn.commit()

    if email:
        a_href: str = str()

        if merchant_website:
            a_href: str = f"""Visit us on our <a href={merchant_website}>Website</a>."""

        # DogerBlue = #1E90FF
        message: str = f"""
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:white; background-color:#1E90FF; font-family:courier; text-align:center; 
        text-shadow:2px 2px red;">
            <u>
                {shop_name}!
            </u>
        </h1>

        <h3 style="text-align:center;">
            💐💐💐 Hello {name}! 💐💐💐
        </h3>

        <hr>

        <div style="background-color:#BCD2EE; text-align:center; border:1px solid; width:100%; height:200px;">
            <img src="https://raw.githubusercontent.com/JahidFariz/TailorMate/main/assets/brand-logo-light.png"
            style="height:200px;"/>
        </div>

        <hr>

        <p>
            Welcome to <b>{shop_name}</b> Powered by <b>FOSS KINGDOM!</b> We're glad you have decided to join us. We're 
            about to start something exciting!

            <br><br>

            We want to make your onboard experience free of worry. Feel free to email us if you have any questions at 
            any point in time.
            
            <br><br>

            We're always looking forward to hearing from you. Your feedback will really help us to improve our product 
            and service, as we always aim to deliver exactly what our customers want.

            <br><br>

            Share your thoughts by replying to this email, or <a href=tel:{shop_contact}>Call</a>

            <br><br>

            {a_href}
            
            <br><br>
            
            I'm always happy to help and read our customers' suggestions.
            
            <br><br>

            - Team: {shop_name}!
        </p>

        <div style="color:white; background-color:black; text-align:center;">
            Created by FOSS KINGDOM. Made with 💗 in Incredible 🇮🇳.
        </div>
    </body>
</html>
"""

        send_email(to_addr=email, subject="Welcome onboard!", message=message)

    update_customers()

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()
    name_entry.focus()

    print(F_GREEN + "[INFO]\tDatabase appended successfully...")

    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    showinfo(
        title=f"TailorMate {__version__}", message="Database appended successfully..."
    )
    tm.deiconify()

    create_btn.config(text="Create New", state=NORMAL)


def update_entry() -> None:
    update_orders()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    selected_item: str = customers_db.focus()

    if not selected_item:
        print(F_RED + "[INFO]\tPlease select a customer record!")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please select a customer record!",
        )
        tm.deiconify()
        return None

    name: str or None = validate_name(textvariable=name_var1.get())
    if name is None:
        name_lbl.config(fg="red")
        name_entry.focus()
        return None

    # isd_code: str = isd_code_var1.get()
    ph: str or None = validate_ph(ph_no_var=ph_var1, master=tm, bell_var=tm_bell_var)
    if ph is None:
        ph_lbl2.config(fg="red")
        ph_entry.focus()
        return None

    email: str or None = validate_customer_email(textvariable=email_var1.get())
    if email is None:
        email_lbl.config(fg="red")
        email_entry.focus()
        return None

    dob: str = day_selection.get_date()
    gender: str = gender_var.get()

    selected_id: str = customers_db.item(selected_item).get("values")[3]

    try:
        c.execute(
            f"""update customers set 
            name = '{name}',
            phone = '{ph}',
            email = '{email}',
            dob = '{dob}',
            gender = '{gender}'
            where phone = '{selected_id}'"""
        )

    except IntegrityError as integrity_error:
        ph_lbl2.config(fg="red")
        ph_entry.focus()

        print(F_RED + "[INFO]\tThis mobile number already exists.")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=f"{integrity_error}\n{ph} This mobile number already exist.",
        )
        tm.deiconify()
        return None

    conn.commit()
    update_customers()

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    print(F_GREEN + "[INFO]\tDatabase updated successfully...")

    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    showinfo(
        title=f"TailorMate {__version__}", message="Database updated successfully..."
    )
    tm.deiconify()


def delete_entry() -> None:
    if not customers_db.get_children():
        return None

    update_orders()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    selected_item: str = customers_db.focus()

    if not selected_item:
        print(F_RED + "[INFO]\tPlease select a customer record!")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please select a customer record!",
        )
        tm.deiconify()
        return None

    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    if not askyesno(
        title=f"TailorMate {__version__}",
        message="Are you sure? Do you want to delete the selected record?",
    ):
        tm.deiconify()
        return None

    selected_id: str = customers_db.item(selected_item).get("values")[3]

    c.execute(f"""delete from customers where phone = '{selected_id}'""")
    conn.commit()
    update_customers()

    print(F_GREEN + "[INFO]\t1 record deleted successfully...")

    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    showinfo(
        title=f"TailorMate {__version__}", message="1 record deleted successfully..."
    )
    tm.deiconify()


def clear_entry() -> None:
    update_customers()
    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)

    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()

    gender_var.set(gender_options[0])
    update_gender_color()


def select_customer() -> None:
    update_orders()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    priority_var.set(value=False)

    selected_item: str = customers_db.focus()
    if not selected_item:
        print(F_RED + "[INFO]\tPlease select a customer record!")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please select a customer record!",
        )
        tm.deiconify()
        return None

    name_var2.set(value=customers_db.item(selected_item).get("values")[1])
    ph_var2.set(value=customers_db.item(selected_item).get("values")[3])
    email_var2.set(value=customers_db.item(selected_item).get("values")[4])

    clear_entry()
    main_tab_view.select(tab_id=2)


def update_items() -> None:
    items_list: tuple = (
        ["Churidar", "Women"],
        ["Frock", "Women"],
        ["Kurti", "Women"],
        ["Lehenga", "Women"],
        ["Midi", "Women"],
        ["Night Gown", "Women"],
        ["Nighty", "Women"],
        ["Pants", "Men"],
        ["Pattu Pavadai", "Women"],
        ["Salwar Kameez", "Women"],
        ["Saree Blouse", "Women"],
        ["Shirt", "Men"],
        ["Shorts", "Mne"],
        ["Sweater", "Both"],
        ["Under Skirt", "Women"],
        ["Woolen Scarf or Glove", "Both"],
        ["Other", "Both"],
    )

    serial_no: int = int()
    for _ in items_list:
        serial_no = serial_no + 1
        _ = [serial_no, _[0], _[1]]

        if serial_no % 2 == 0:
            items_db.insert(parent="", index=END, values=_, tags="even")

        else:
            items_db.insert(parent="", index=END, values=_, tags="odd")


def undo_notes_widget():
    try:
        notes_entry.edit_undo()

    except TclError as tcl_error:
        print(F_YELLOW + f"[INFO]\t{tcl_error}")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=str(tcl_error),
        )
        tm.deiconify()


def redo_notes_widget():
    try:
        notes_entry.edit_redo()

    except TclError as tcl_error:
        print(F_YELLOW + f"[INFO]\t{tcl_error}")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(title=f"TailorMate {__version__}", message=str(tcl_error))
        tm.deiconify()


def save_order():
    save_item_btn.config(text="Saving...", state=DISABLED)
    save_item_btn.update()

    update_orders()
    update_customers()

    search_entry.delete(first=0, last=END)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        name_lbl.config(fg="#000")
        ph_lbl2.config(fg="#000")
        email_lbl.config(fg="#000")

        name_lbl3.config(fg="#000")
        ph_lbl3.config(fg="#000")
        email_lbl3.config(fg="#000")
        cost_lbl.config(fg="#000")
        delivery_date_lbl.config(fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        name_lbl.config(fg="#fff")
        ph_lbl2.config(fg="#fff")
        email_lbl.config(fg="#fff")

        name_lbl3.config(fg="#fff")
        ph_lbl3.config(fg="#fff")
        email_lbl3.config(fg="#fff")
        cost_lbl.config(fg="#fff")
        delivery_date_lbl.config(fg="#fff")

    name_entry.delete(first=0, last=END)
    ph_entry.delete(first=0, last=END)
    email_entry.delete(first=0, last=END)
    day_selection.selection_set(
        date=date(year=today.year - 18, month=today.month, day=today.day)
    )
    day_selection.selection_clear()
    gender_var.set(value=gender_options[0])
    update_gender_color()

    selected_item: str = items_db.focus()

    if not selected_item:
        print(F_RED + "[INFO]\tPlease select an item!")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please select an item.",
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    item: str = items_db.item(selected_item).get("values")[1]

    name: str = validate_name(textvariable=name_var2.get())
    if not name:
        name_lbl3.config(fg="red")
        name_entry3.focus()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    ordered_date: str = strftime("%Y-%m-%d %H:%M:%S")

    ph: str = validate_ph(ph_no_var=ph_var2, master=tm, bell_var=tm_bell_var)
    if not ph:
        ph_lbl3.config(fg="red")
        ph_entry3.focus()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    email: str = validate_customer_email(textvariable=email_var2.get())
    if not email:
        email_lbl3.config(fg="red")
        email_entry3.focus()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    c.execute(f"""select * from customers where phone = '{ph}'""")
    selected_row = c.fetchone()

    if selected_row is None:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tNo customer record found in this number!")
        print(F_BLUE + "=" * 80)

        ph_lbl3.config(fg="red")
        ph_entry3.focus()

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="No customer found in this number!",
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    if not selected_row[0] == name:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tThe Customer's name mismatch!")
        print(F_BLUE + "=" * 80)

        name_lbl3.config(fg="red")
        name_entry3.focus()

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}", message="The Customer's name mismatch!"
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    if not selected_row[3] == email:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tThe Customer's email address mismatch!")
        print(F_BLUE + "=" * 80)

        email_lbl3.config(fg="red")
        email_entry3.focus()

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="The Customer's address mismatch!",
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    if stitch_var.get() == 1:
        stitch_opt: str = "Stitching"

    elif stitch_var.get() == 2:
        stitch_opt: str = "Material"

    elif stitch_var.get() == 3:
        stitch_opt: str = "Knitting"

    elif stitch_var.get() == 4:
        stitch_opt: str = "Embroidery"

    else:
        stitch_opt: str = "Alteration"

    notes: str = notes_entry.get(index1=1.0, index2=END).strip()

    if not cost_entry.get().strip():
        cost_var.set(value=0.0)

    cost = cost_var.get()
    if cost <= 0.0:
        cost_lbl.config(fg="red")
        cost_entry.focus()

        print(F_BLUE + "=" * 80)
        print(
            F_RED
            + f"[ERROR]\tThe total cost amount cannot be zero or lesser than zero."
        )
        print(F_BLUE + "=" * 80)

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            f"TailorMate {__version__}",
            message="The total cost amount cannot be zero or lesser than zero.",
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    delivery_date: str = delivery_date_selection.get_date()
    if not delivery_date:
        print(F_BLUE + "=" * 80)
        print(F_RED + "[ERROR]\tPlease select the delivery date.")
        print(F_BLUE + "=" * 80)

        delivery_date_lbl.config(fg="red")

        tm.withdraw()
        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message="Please select the delivery date.",
        )
        tm.deiconify()

        save_item_btn.config(text="Save", state=NORMAL)
        return None

    if priority_var.get():
        priority: str = "High"

    else:
        priority: str = "Low"

    c.execute(
        """insert into orders values (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )""",
        (
            name,
            ordered_date,
            ph,
            item,
            stitch_opt,
            notes,
            cost,
            delivery_date,
            priority,
            "In Progress",
        ),
    )
    conn.commit()

    c.execute("select rowid from orders")
    order_no: str = f"#TMO{c.fetchall()[-1][0]:03d}"

    if email:
        a_href: str = str()

        if merchant_website:
            a_href: str = f"""Visit us on our <a href={merchant_website}>Website</a>."""

        message: str = f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color:white; background-color:#1E90FF; font-family:courier; text-align:center; 
                text-shadow:2px 2px red;">
                    <u>
                        {shop_name}!
                    </u>
                </h1>

                <h3 style="text-align:center;">
                    💐💐💐 Hello {name}! 💐💐💐
                </h3>

                <hr>

                <div style="background-color:#BCD2EE; text-align:center; border:1px solid; width:100%; height:200px;">
                    <img src="https://raw.githubusercontent.com/JahidFariz/TailorMate/main/assets/brand-logo-light.png"
                    style="height:200px;"/>
                </div>

                <hr>

                <p>
                    We're happy to let you know that we've received your order.

                    <h2 style="font-family:courier; text-align:center;">
                        <u>
                            *** ORDER SUMMARY: ***
                        </u>
                    </h2>

                    <ul>
                        <li>
                            Order No: {order_no}
                        </li>

                        <li>
                            Ordered Date & Time: {ordered_date}
                        </li>

                        <li>
                            Status: In Progress
                        </li>

                        <li>
                            Item: {item}
                        </li>

                        <li>
                            Order Type: {stitch_opt}
                        </li>

                        <li>
                            Order Total: ${cost}
                        </li>

                        <li>
                            Expected Delivery Date: {delivery_date}
                        </li>
                    </ul>

                    Thank you for placing your order! We hope you enjoyed our service with us and that you will visit 
                    us again soon.

                    <br><br>

                    Share your thoughts by replying to this email, or <a href=tel:{shop_contact}>Call</a>

                    <br><br>

                    {a_href}

                    <br><br>

                    I'm always happy to help and read our customers' suggestions.

                    <br><br>

                    - Team: {shop_name}!
                </p>

                <div style="color:white; background-color:black; text-align:center;">
                    Created by FOSS KINGDOM. Made with 💗 in Incredible 🇮🇳.
                </div>
            </body>
        </html>
        """

        send_email(to_addr=email, subject="Order Received!", message=message)

    update_orders()

    name_entry3.delete(first=0, last=END)
    ph_entry3.delete(first=0, last=END)
    email_entry3.delete(first=0, last=END)
    stitch_var.set(value=1)
    notes_entry.delete(index1=1.0, index2=END)
    cost_var.set(value=0.0)
    delivery_date_selection.selection_set(
        date=date(year=today.year, month=today.month, day=today.day)
    )
    delivery_date_selection.selection_clear()
    save_item_btn.config(text="Save", state=NORMAL)

    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    showinfo(title=f"TailorMate {__version__}", message="Order saved successfully!")
    tm.deiconify()

    main_tab_view.select(tab_id=0)


def rgb_to_hex(rgb):
    return "%02x%02x%02x" % rgb


def cpu_stat():
    cpu: float = cpu_percent()

    r: int = round(cpu * 2.55)
    g: int = 255 - r

    color_code: str = "#" + rgb_to_hex((r, g, 0))
    cpu_lbl.config(text=f"CPU: {cpu}%", bg=color_code)
    cpu_lbl.after(ms=1000, func=cpu_stat)


def mem_stat():
    mem: float = virtual_memory().percent

    r: int = round(mem * 2.55)
    g: int = 255 - r

    color_code: str = "#" + rgb_to_hex((r, g, 0))
    mem_lbl.config(text=f"MEM: {mem}%", bg=color_code)
    mem_lbl.after(ms=1000, func=mem_stat)


def pwr_stat():
    try:
        pwr_float: float = round(sensors_battery().percent, 1)
        pwr: int = int(pwr_float)
        g: int = int(pwr * 2.55)
        r: int = 255 - g

        color_code: str = "#" + rgb_to_hex((r, g, 0))

        pwr_lbl.config(text=f"PWR: {pwr_float}%", bg=color_code)
        pwr_lbl.after(ms=1000, func=pwr_stat)

    except AttributeError:
        pass


def time_stat() -> None:
    clock: str = strftime("%I:%M:%S %p")

    time_lbl.config(text=f"{whoami.title()} @ {clock}")
    time_lbl.after(ms=1000, func=time_stat)


def switch2dark() -> None:  # This is the main dark theme function
    tm.config(bg=accent_color_dark)
    menubar.config(bg=accent_color_dark, fg="#fff")
    file_menu.config(bg=accent_color_dark, fg="#fff")
    options_menu.config(bg=accent_color_dark, fg="#fff")
    calendar_menu.config(bg=accent_color_dark, fg="#fff")
    settings_menu.config(bg=accent_color_dark, fg="#fff")
    theme_menu.config(bg=accent_color_dark, fg="#fff")
    links_menu.config(bg=accent_color_dark, fg="#fff")
    help_menu.config(bg=accent_color_dark, fg="#fff")
    orders_frame.config(bg=accent_color_dark)
    customers_frame.config(bg=accent_color_dark)
    items_frame.config(bg=accent_color_dark)
    stats_frame.config(bg=accent_color_dark)
    greetings_lbl.config(bg=accent_color_dark, fg="#fff")
    lf11.config(bg=accent_color_dark)
    treeview_frame1.config(bg=accent_color_dark)
    orders_db.tag_configure(
        tagname="odd", background=accent_color_dark, foreground="#fff"
    )
    orders_db.tag_configure(tagname="even", background="#2A3459", foreground="#fff")
    tot_orders_lbl.config(bg=accent_color_dark)
    f11.config(bg=accent_color_dark)
    mark_as_completed_btn.config(bg="green", activebackground="#20C020")
    product_delivered_btn.config(bg="#000080", activebackground="#2020C0")
    lf12.config(bg=accent_color_dark)
    order_btn.config(bg="#000", activebackground="#404040")
    exit_btn1.config(activebackground="#C02020", bg="#800000")
    lf21.config(bg=accent_color_dark)
    lf22.config(bg=accent_color_dark)
    lf23.config(bg=accent_color_dark)
    lf24.config(bg=accent_color_dark)
    treeview_frame2.config(bg=accent_color_dark)
    customers_db.tag_configure(
        tagname="odd", background=accent_color_dark, foreground="#fff"
    )
    customers_db.tag_configure(tagname="even", background="#2A3459", foreground="#fff")
    tot_customers_lbl.config(bg=accent_color_dark)
    search_lbl.config(bg=accent_color_dark, fg="#fff")
    search_entry.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    runtime_search_lbl.config(bg=accent_color_dark, fg="#fff")
    search_btn.config(activebackground="#C02020", bg="#800000")
    f2.config(bg=accent_color_dark)
    f21.config(bg=accent_color_dark)
    f22.config(bg=accent_color_dark)
    name_lbl.config(bg=accent_color_dark, fg="#fff")
    name_entry.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    ph_lbl2.config(bg=accent_color_dark, fg="#fff")
    ph_entry.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    email_lbl.config(bg=accent_color_dark, fg="#fff")
    email_entry.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    dob_lbl.config(bg=accent_color_dark, fg="#fff")
    gender_lbl.config(bg=accent_color_dark, fg="#fff")
    create_btn.config(activebackground="#20C020", bg="green")
    update_btn.config(activebackground="#FF8020", bg="#C08000")
    delete_btn.config(activebackground="#C02020", bg="#800000")
    clear_date_btn.config(activebackground="#404040", bg="#000")
    clear_inputs_btn.config(activebackground="#404040", bg="#000")
    select_btn.config(activebackground="#404040", bg="#000")
    exit_btn2.config(activebackground="#C02020", bg="#800000")
    lf31.config(bg=accent_color_dark)
    treeview_frame3.config(bg=accent_color_dark)
    items_db.tag_configure(
        tagname="odd", background=accent_color_dark, foreground="#fff"
    )
    items_db.tag_configure(tagname="even", background="#2A3459", foreground="#fff")
    info_lbl.config(bg=accent_color_dark)
    lf32.config(bg=accent_color_dark)
    f3.config(bg=accent_color_dark)
    f31.config(bg=accent_color_dark)
    f32.config(bg=accent_color_dark)
    name_lbl3.config(bg=accent_color_dark, fg="#fff")
    name_entry3.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    ph_lbl3.config(bg=accent_color_dark, fg="#fff")
    ph_entry3.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    email_lbl3.config(bg=accent_color_dark, fg="#fff")
    email_entry3.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    order_type_lbl.config(bg=accent_color_dark, fg="#fff")
    rb1.config(bg="#fff")
    rb2.config(bg="#fff")
    rb3.config(bg="#fff")
    rb4.config(bg="#fff")
    rb5.config(bg="#fff")
    notes_lbl.config(bg=accent_color_dark, fg="#fff")
    notes_entry.config(bg="#2A3459", fg="#fff", highlightcolor="blue")
    notes_popup_menu.config(bg=accent_color_dark, fg="#fff")
    cost_lbl.config(bg=accent_color_dark, fg="#fff")
    cost_entry.config(
        bg="#2A3459", fg="#fff", highlightcolor="blue", insertbackground="red"
    )
    delivery_date_lbl.config(bg=accent_color_dark, fg="#fff")
    priority_lbl.config(bg=accent_color_dark, fg="#fff")
    priority_btn.config(bg="#fff")
    lf33.config(bg=accent_color_dark)
    lf4.config(bg=accent_color_dark)
    f41.config(bg=accent_color_dark)
    tot_customers_lbl4.config(bg=accent_color_dark, fg="#fff")
    tot_customers_value.config(bg=accent_color_dark, fg="#fff")
    active_orders_lbl.config(bg=accent_color_dark, fg="#fff")
    active_orders_value.config(bg=accent_color_dark, fg="#fff")
    completed_orders_lbl.config(bg=accent_color_dark, fg="#fff")
    completed_orders_value.config(bg=accent_color_dark, fg="#fff")
    belated_delivered_lbl.config(bg=accent_color_dark, fg="#fff")
    belated_delivered_value.config(bg=accent_color_dark, fg="#fff")
    amount_earned_lbl.config(bg=accent_color_dark, fg="#fff")
    amount_earned_value.config(bg=accent_color_dark, fg="#fff")
    pwr_lbl.config(bg=accent_color_dark)
    time_lbl.config(bg=accent_color_dark, fg="#fff")
    boot_time_lbl.config(bg=accent_color_dark, fg="#fff")
    tree_style.configure(
        style="Treeview",
        background="#2A3459",
        foreground="#fff",
        fieldbackground=accent_color_dark,
    )


def switch2light() -> None:  # This is the main light theme function
    tm.config(bg=accent_color_light)
    menubar.config(bg="#d9d9d9", fg="#000")
    file_menu.config(bg="#d9d9d9", fg="#000")
    options_menu.config(bg="#d9d9d9", fg="#000")
    calendar_menu.config(bg="#d9d9d9", fg="#000")
    settings_menu.config(bg="#d9d9d9", fg="#000")
    theme_menu.config(bg="#d9d9d9", fg="#000")
    links_menu.config(bg="#d9d9d9", fg="#000")
    help_menu.config(bg="#d9d9d9", fg="#000")
    orders_frame.config(bg=accent_color_light)
    customers_frame.config(bg=accent_color_light)
    items_frame.config(bg=accent_color_light)
    stats_frame.config(bg=accent_color_light)
    greetings_lbl.config(bg=accent_color_light, fg="#000")
    lf11.config(bg=accent_color_light)
    treeview_frame1.config(bg=accent_color_light)
    orders_db.tag_configure(
        tagname="odd", background=accent_color_light, foreground="#000"
    )
    orders_db.tag_configure(tagname="even", background="#fff", foreground="#000")
    tot_orders_lbl.config(bg=accent_color_light)
    f11.config(bg=accent_color_light)
    mark_as_completed_btn.config(activebackground="green", bg="#20C020")
    product_delivered_btn.config(activebackground="#000080", bg="#2020C0")
    lf12.config(bg=accent_color_light)
    order_btn.config(activebackground="#000", bg="#404040", activeforeground="#fff")
    exit_btn1.config(bg="#C02020", activebackground="#800000")
    lf21.config(bg=accent_color_light)
    lf22.config(bg=accent_color_light)
    lf23.config(bg=accent_color_light)
    lf24.config(bg=accent_color_light)
    treeview_frame2.config(bg=accent_color_light)
    customers_db.tag_configure(tagname="even", background="#fff", foreground="#000")
    customers_db.tag_configure(
        tagname="odd", background=accent_color_light, foreground="#000"
    )
    tot_customers_lbl.config(bg=accent_color_light)
    search_lbl.config(bg=accent_color_light, fg="#000")
    search_entry.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    runtime_search_lbl.config(bg=accent_color_light, fg="#000")
    search_btn.config(bg="#C02020", activebackground="#800000")
    f2.config(bg=accent_color_light)
    f21.config(bg=accent_color_light)
    f22.config(bg=accent_color_light)
    name_lbl.config(bg=accent_color_light, fg="#000")
    name_entry.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    ph_lbl2.config(bg=accent_color_light, fg="#000")
    ph_entry.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    email_lbl.config(bg=accent_color_light, fg="#000")
    email_entry.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    dob_lbl.config(bg=accent_color_light, fg="#000")
    gender_lbl.config(bg=accent_color_light, fg="#000")
    create_btn.config(bg="#20C020", activebackground="green")
    update_btn.config(bg="#FF8020", activebackground="#C08000")
    delete_btn.config(bg="#C02020", activebackground="#800000")
    clear_date_btn.config(bg="#404040", activebackground="#000")
    clear_inputs_btn.config(bg="#404040", activebackground="#000")
    select_btn.config(bg="#404040", activebackground="#000")
    exit_btn2.config(bg="#C02020", activebackground="#800000")
    lf31.config(bg=accent_color_light)
    treeview_frame3.config(bg=accent_color_light)
    items_db.tag_configure(
        tagname="odd", background=accent_color_light, foreground="#000"
    )
    items_db.tag_configure(tagname="even", background="#fff", foreground="#000")
    info_lbl.config(bg=accent_color_light)
    lf32.config(bg=accent_color_light)
    f3.config(bg=accent_color_light)
    f31.config(bg=accent_color_light)
    f32.config(bg=accent_color_light)
    name_lbl3.config(bg=accent_color_light, fg="#000")
    name_entry3.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    ph_lbl3.config(bg=accent_color_light, fg="#000")
    ph_entry3.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    email_lbl3.config(bg=accent_color_light, fg="#000")
    email_entry3.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    order_type_lbl.config(bg=accent_color_light, fg="#000")
    rb1.config(bg=accent_color_light)
    rb2.config(bg=accent_color_light)
    rb3.config(bg=accent_color_light)
    rb4.config(bg=accent_color_light)
    rb5.config(bg=accent_color_light)
    notes_lbl.config(bg=accent_color_light, fg="#000")
    notes_entry.config(bg="#fff", fg="#000", highlightcolor="#000")
    notes_popup_menu.config(bg="#d9d9d9", fg="#000")
    cost_lbl.config(bg=accent_color_light, fg="#000")
    cost_entry.config(
        bg="#fff", fg="#000", highlightcolor="#000", insertbackground="#000"
    )
    delivery_date_lbl.config(bg=accent_color_light, fg="#000")
    priority_lbl.config(bg=accent_color_light, fg="#000")
    priority_btn.config(bg=accent_color_light)
    lf33.config(bg=accent_color_light)
    lf4.config(bg=accent_color_light)
    f41.config(bg=accent_color_light)
    tot_customers_lbl4.config(bg=accent_color_light, fg="#000")
    tot_customers_value.config(bg=accent_color_light, fg="#000")
    active_orders_lbl.config(bg=accent_color_light, fg="#000")
    active_orders_value.config(bg=accent_color_light, fg="#000")
    completed_orders_lbl.config(bg=accent_color_light, fg="#000")
    completed_orders_value.config(bg=accent_color_light, fg="#000")
    belated_delivered_lbl.config(bg=accent_color_light, fg="#000")
    belated_delivered_value.config(bg=accent_color_light, fg="#000")
    amount_earned_lbl.config(bg=accent_color_light, fg="#000")
    amount_earned_value.config(bg=accent_color_light, fg="#000")
    pwr_lbl.config(bg=accent_color_light)
    time_lbl.config(bg=accent_color_light, fg="#000")
    boot_time_lbl.config(bg=accent_color_light, fg="#000")
    tree_style.configure(
        style="Treeview",
        background="#fff",
        foreground="#000",
        fieldbackground=accent_color_light,
    )


def configure_theme_color():
    if theme_var.get() == "light":
        update_configuration(section="options", option="theme", value="light")
        switch2light()

    elif theme_var.get() == "dark":
        update_configuration(section="options", option="theme", value="dark")
        switch2dark()

    elif theme_var.get() == "system_default":
        if isLight():
            update_configuration(
                section="options", option="theme", value="system_default"
            )
            switch2light()

        elif isDark():
            update_configuration(
                section="options", option="theme", value="system_default"
            )
            switch2dark()


def exit_toplevel(toplevel):
    toplevel.destroy()
    main_tab_view.select(tab_id=0)
    tm.deiconify()


def stain_solutions():
    def get_result():
        if stain_var.get().strip().lower() == stain_types[0].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/98.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[1].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/1.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[2].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/118.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[3].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/32.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[4].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/2.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[5].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/33.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[6].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/187.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[7].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/99.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[8].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/100.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[9].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/123.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[10].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/101.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[11].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/3.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[12].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/4.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[13].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/102.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        elif stain_var.get().strip().lower() == stain_types[14].lower():
            file = open(file=join(BASE_PATH, "stain_solutions/34.txt"), mode="r")
            content: str = file.read()
            file.close()

            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.insert(index=1.0, chars=content)
            st0.config(state=DISABLED)

        else:
            st0.config(state=NORMAL)
            st0.delete(index1=1.0, index2=END)
            st0.config(state=DISABLED)

    tm.withdraw()

    stain_solutions_window = Toplevel(master=tm)
    stain_solutions_window.iconphoto(False, TkPhotoImage(file=stain_solutions_ico_path))
    stain_solutions_window.protocol(
        name="WM_DELETE_WINDOW",
        func=lambda: exit_toplevel(toplevel=stain_solutions_window),
    )
    stain_solutions_window.bind(
        sequence="<Control-Q>",
        func=lambda event: exit_toplevel(toplevel=stain_solutions_window),
    )
    stain_solutions_window.bind(
        sequence="<Control-q>",
        func=lambda event: exit_toplevel(toplevel=stain_solutions_window),
    )
    stain_solutions_window.bind(
        sequence="<Escape>",
        func=lambda event: exit_toplevel(toplevel=stain_solutions_window),
    )
    stain_solutions_window.bind(
        sequence="<Alt-F4>",
        func=lambda event: exit_toplevel(toplevel=stain_solutions_window),
    )
    stain_solutions_window.title(
        string="Stain Solutions (University of Illinois Extension)"
    )
    stain_solutions_window.resizable(width=True, height=True)

    Label(
        master=stain_solutions_window,
        text=f"Hello {whoami.title()}, Welcome to {shop_name}!",
        bg="#000",
        fg="#fff",
    ).pack(side=TOP, fill=X)

    stain_solutions_info: Label = Label(
        master=stain_solutions_window,
        text="We have put together a comprehensive list of stain solutions.\n"
        "Each solution contains the supplies you will need and the preferred method for cleaning the stain.",
    )
    stain_solutions_info.pack()

    Label(
        master=stain_solutions_window,
        text="Treat stains as soon as possible after staining.\n"
        "The older the stain, the more difficult it will be to remove.",
        bg="orange",
        fg="#fff",
    ).pack(fill=X)

    Label(
        master=stain_solutions_window,
        text="All stain removal methods should be applied prior to laundering washable garments.\n"
        "Stains that have been laundered and dried are almost impossible to remove.",
        bg="red",
        fg="#fff",
    ).pack(fill=X)

    stain_types: list = [
        "Adhesive tape",
        "After shave lotion",
        "Airplane glue",
        "Alcoholic beverages",
        "Antiperspirant",
        "Apples",
        "Ashes",
        "Asphalt",
        "Auto wax",
        "Automobile grease",
        "Automotive oil",
        "Baby food",
        "Baby formula",
        "Baby oil",
        "Bananas",
        "Barbeque sauce",
        "Beer",
        "Beets",
        "Berries (cranberries, raspberries, strawberries)",
        "Bird droppings",
        "Black walnut",
        "Bleach",
        "Blood",
        "Blueberry",
        "Bluing",
        "Blush (makeup)",
        "Broccoli",
        "Butter",
        "Cake frosting",
        "Calamine lotion",
        "Candle wax",
        "Candy",
        "Car wax",
        "Carrot",
        "Castor oil",
        "Catsup",
        "Chalk",
        "Charcoal",
        "Cheese, cheese sauce",
        "Cherry",
        "Chewing gum",
        "Child's drink mix",
        "Chili sauce",
        "Chocolate, cocoa",
        "Clay Stains on Baseball Uniforms",
        "Cod liver oil",
        "Coffee (no cream)",
        "Coffee with cream",
        "Cola",
        "Collar/cuff soil",
        "Cologne and perfume",
        "Concealer (makeup)",
        "Contact glue",
        "Cooking oil",
        "Corn syrup",
        "Correction fluid (typewriter) and white out",
        "Cosmetics",
        "Cottage cheese",
        "Cough syrup",
        "Cranberry juice/sauce",
        "Crayon",
        "Cream",
        "Cream soups",
        "Curry",
        "Deodorant",
        "Dirt",
        "Dye transfer (color bleeding in wash)",
        "Dyes (not red)",
        "Egg white",
        "Egg yolk",
        "Epoxy glue",
        "Eye drops",
        "Eye Shadow",
        "Eyeliner",
        "Fabric dye (except red and yellow)",
        "Fabric dye, red",
        "Fabric softener",
        "Face powder",
        "Feces and excrement",
        "Felt tip marker",
        "Felt-tip pen (permanent ink may not come out)",
        "Felt-tip water color pen",
        "Fish slime",
        "Flavored Drink",
        "Floor wax",
        "Food coloring (except red and yellow)",
        "Food coloring, red",
        "Fruit",
        "Fruit juice (apple, grape, orange)",
        "Fruit punch",
        "Furniture polish, wax",
        "Gasoline",
        "Gelatin",
        "Grape juice",
        "Graphite",
        "Grass",
        "Gravy",
        "Grease",
        "Hair conditioner",
        "Hair dye, black or brown",
        "Hair dye, red",
        "Hair gel",
        "Hair oil",
        "Hair spray",
        "Hand lotion",
        "Honey",
        "Ice cream",
        "India ink",
        "Ink (fountain)",
        "Ink, red",
        "Iodine",
        "Jams/jelly/preserves",
        "Lacquer",
        "Lard",
        "Lemon juice",
        "Lighter fluid",
        "Lime juice",
        "Lipstick and lip-balm",
        "Lotion (body, bath, hand)",
        "Machine or mineral oil",
        "Makeup – water based",
        "Make-up (oil based)",
        "Mango",
        "Maple syrup",
        "Margarine",
        "Mascara (make up)",
        "Mayonnaise",
        "Medicine (alcohol based)",
        "Medicine (oil based)",
        "Melon",
        "Mercurochrome",
        "Mildew",
        "Milk",
        "Mixed drinks",
        "Molasses",
        "Motor oil",
        "Mouthwash",
        "Mucous",
        "Mud",
        "Mustard",
        "Nail polish",
        "Nail polish remover",
        "Nose drops",
        "Ointment, salve",
        "Olive oil",
        "Onion",
        "Orange juice",
        "Paint (oil based)",
        "Paint, solvent or water based",
        "Peaches",
        "Peanut butter",
        "Peanut oil",
        "Pears",
        "Pencil",
        "Perspiration",
        "Petroleum Jelly",
        "Pine resin",
        "Play-dough",
        "Pollen",
        "Potatoes (mashed)",
        "Pudding",
        "Putty",
        "Raspberry",
        "Red dye",
        "Relish",
        "Rubber cement",
        "Rust",
        "Salad dressing",
        "Salsa",
        "Sap",
        "School glue",
        "Scorch",
        "Shaving cream",
        "Sherbet",
        "Shoe dye",
        "Shoe polish",
        "Shortening",
        "Smoke",
        "Soft drinks",
        "Soot",
        "Soups containing meat",
        "Soups containing vegetables",
        "Sour cream",
        "Soy sauce",
        "Spaghetti sauce",
        "Squash",
        "Stamp pad ink (except red and yellow)",
        "Stamp pad ink, red",
        "Starch",
        "Steak sauce",
        "Strawberry",
        "Sunscreen (oil based)",
        "Suntan Lotion (oil based)",
        "Suntan/screen cream",
        "Super glue",
        "Sweet potato",
        "Tape residue",
        "Tar",
        "Tea",
        "Tempera paint",
        "Tobacco",
        "Tomato juice",
        "Tomato-based products",
        "Toner",
        "Toothpaste",
        "Tree sap",
        "Unknown or mystery",
        "Urine",
        "Vegetable oil",
        "Vinegar (with color)",
        "Vomit",
        "Washable ink",
        "Water spots",
        "Water-based glue",
        "Watercolor paint (except red or yellow)",
        "Watercolor paint, red",
        "Wax",
        "Whiskey",
        "White glue or school paste",
        "Wine",
        "Worcestershire sauce",
        "Yellow dye",
        "Yellowing , dinginess or graying, general soil buildup, white or gray streaks",
        "Yogurt",
        "Zucchini",
    ]
    # Perfume (https://web.extension.illinois.edu/stain/staindetail.cfm?ID=211)

    lf0: LabelFrame = LabelFrame(
        master=stain_solutions_window,
        text="Stain Solutions",
        fg="red",
    )
    lf0.pack(padx=10, pady=5, expand=1, fill=BOTH)

    stain_var: StringVar = StringVar()
    stain_combobox: Combobox = Combobox(
        master=lf0, textvariable=stain_var, values=stain_types
    )
    stain_combobox.bind(
        sequence="<<ComboboxSelected>>", func=lambda event: get_result()
    )
    stain_combobox.pack(padx=10, pady=5, fill=X)

    st0: ScrolledText = ScrolledText(
        master=lf0,
        wrap=WORD,
        selectbackground="orange",
    )
    st0.config(state=DISABLED)
    st0.pack(fill=BOTH, padx=10, pady=5, expand=1)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        stain_solutions_window.config(bg=accent_color_light)
        stain_solutions_info.config(bg=accent_color_light, fg="#000")
        lf0.config(bg=accent_color_light)
        st0.config(bg="#fff", fg="#000")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        stain_solutions_window.config(bg=accent_color_dark)
        stain_solutions_info.config(bg=accent_color_dark, fg="#fff")
        lf0.config(bg=accent_color_dark)
        st0.config(bg="#2A3459", fg="#fff")

    stain_solutions_window.mainloop()


def donation_page() -> None:
    tm.withdraw()

    donation_app = Toplevel(master=tm)
    donation_app.protocol(
        name="WM_DELETE_WINDOW", func=lambda: exit_toplevel(toplevel=donation_app)
    )
    donation_app.bind(
        sequence="<Control-Q>",
        func=lambda event: exit_toplevel(toplevel=donation_app),
    )
    donation_app.bind(
        sequence="<Control-q>",
        func=lambda event: exit_toplevel(toplevel=donation_app),
    )
    donation_app.bind(
        sequence="<Escape>", func=lambda event: exit_toplevel(toplevel=donation_app)
    )
    donation_app.bind(
        sequence="<Alt-F4>", func=lambda event: exit_toplevel(toplevel=donation_app)
    )
    donation_app.iconphoto(False, TkPhotoImage(file=donation_ico_path))
    donation_app.title(string="Donate Us!")
    donation_app.resizable(width=True, height=True)

    Label(
        master=donation_app,
        text=f"Hello {whoami.title()}, Welcome to {shop_name}!",
        bg="#000",
        fg="#fff",
    ).pack(side=TOP, fill=X)

    lf0: LabelFrame = LabelFrame(
        master=donation_app,
        text="Donate Us",
        fg="red",
    )
    lf0.pack(padx=10, pady=5, expand=1, fill=BOTH)

    tw0: ScrolledText = ScrolledText(
        master=lf0,
        wrap=WORD,
        selectbackground="orange",
    )

    file = open(file=join(BASE_PATH, "assets/donation.txt"), mode="r")
    content = file.read()
    file.close()

    tw0.insert(index=1.0, chars=content)
    tw0.config(state=DISABLED)
    tw0.pack(fill=BOTH, expand=1, padx=10, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/qr_code.png")).resize(
        size=(213, 213)
    )
    qrcode_img: PhotoImage = PhotoImage(image=_)

    scan_lbl: Label = Label(
        master=donation_app,
        text="Scan here to donate with Google Pay!",
        fg="red",
    )
    scan_lbl.pack()

    upi_lbl: Label = Label(
        master=donation_app,
        text="UPI: gameworld2k18@oksbi",
        fg="red",
        compound=TOP,
        image=qrcode_img,
    )
    upi_lbl.pack()

    bank_detail_lbl: Label = Label(
        master=donation_app,
        text="""Name: MOHAMED FARIZ
A/C No: 0740301000082422
Bank: LAKSHMI VILAS BANK
Branch: THIRUTHURAIPOONDI
IFSC: LAVB0000740""",
    )
    bank_detail_lbl.pack()

    close_btn: Button = Button(
        master=donation_app,
        text="Close",
        fg="#fff",
        activeforeground="#fff",
        width=10,
        command=lambda: exit_toplevel(toplevel=donation_app),
    )
    close_btn.bind(
        sequence="<Return>", func=lambda event: exit_toplevel(toplevel=donation_app)
    )
    close_btn.pack(pady=5)

    Label(
        master=donation_app,
        text="Created by FOSS Kingdom / Made with Love in Incredible India.",
        bg="#000",
        fg="#fff",
    ).pack(fill=X, side=BOTTOM)

    if theme_var.get() == "light" or (
        theme_var.get() == "system_default" and isLight()
    ):
        donation_app.config(bg=accent_color_light)
        lf0.config(bg=accent_color_light)
        tw0.config(bg="#fff", fg="#000")
        scan_lbl.config(bg=accent_color_light)
        upi_lbl.config(bg=accent_color_light)
        bank_detail_lbl.config(bg=accent_color_light)
        close_btn.config(activebackground="#800000", bg="#C02020")

    elif theme_var.get() == "dark" or (
        theme_var.get() == "system_default" and isDark()
    ):
        donation_app.config(bg=accent_color_dark)
        lf0.config(bg=accent_color_dark)
        tw0.config(bg="#000", fg="#fff")
        scan_lbl.config(bg=accent_color_dark)
        upi_lbl.config(bg=accent_color_dark)
        bank_detail_lbl.config(bg=accent_color_dark)
        close_btn.config(bg="#800000", activebackground="#C02020")

    donation_app.mainloop()


def exit_app() -> None:
    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)

    if not askyesno(
        title=f"TailorMate {__version__}",
        message="Are you sure? do you really want to quit?",
    ):
        tm.deiconify()
        return None

    conn.close()
    tm.destroy()
    clean_cache()
    print(F_RED + "Bye...")

    clrscr()
    terminate()


def not_ready_yet() -> None:
    tm.withdraw()
    play_bell_sound(master=tm, bell_var=tm_bell_var)
    showinfo(
        title=f"TailorMate {__version__}",
        message="This action is not ready yet, Still work in progress...",
    )
    tm.deiconify()


try:
    print("[INFO]\tImporting built-in modules...")
    from configparser import ConfigParser
    from datetime import date, datetime
    from email.message import EmailMessage
    from email.mime.text import MIMEText
    from getpass import getuser
    from hashlib import sha1
    from math import log
    from os import mkdir
    from os import system as terminal
    from os.path import isdir, isfile, join
    from pathlib import Path
    from platform import system as os_environment
    from random import choice
    from shutil import rmtree
    from smtplib import SMTP, SMTPAuthenticationError
    from socket import gaierror, setdefaulttimeout
    from sqlite3 import IntegrityError, OperationalError, connect
    from sys import exit as terminate
    from threading import Thread
    from time import strftime, time
    from tkinter import (
        BooleanVar,
        Button,
        Checkbutton,
        DoubleVar,
        Entry,
        Frame,
        IntVar,
        Label,
        LabelFrame,
        Menu,
        OptionMenu,
    )
    from tkinter import PhotoImage as TkPhotoImage
    from tkinter import Radiobutton, Scrollbar, StringVar, TclError, Tk, Toplevel
    from tkinter.constants import (
        BOTH,
        BOTTOM,
        BROWSE,
        CENTER,
        DISABLED,
        END,
        HORIZONTAL,
        INSERT,
        LEFT,
        NORMAL,
        NSEW,
        RIGHT,
        TOP,
        WORD,
        E,
        W,
        X,
        Y,
    )
    from tkinter.messagebox import askyesno, showinfo, showwarning
    from tkinter.scrolledtext import ScrolledText
    from tkinter.ttk import Button as TTK_Button
    from tkinter.ttk import Combobox, Notebook
    from tkinter.ttk import Style as TkStyle
    from tkinter.ttk import Treeview
    from webbrowser import open as browser

    t0: float = time()
    elapsed_time: float = float()
    config: ConfigParser = ConfigParser()
    today: datetime = datetime.today()
    whoami: str = getuser()
    BASE_PATH: Path = Path(__file__).parent
    stain_solutions_ico_path: str = join(BASE_PATH, "assets/dirty-shirt.png")
    donation_ico_path: str = join(BASE_PATH, "assets/donation.png")
    os_env: str = os_environment()

    print("[INFO]\tImporting third-party modules...")
    from bcrypt import checkpw
    from colorama import Fore, Style, init
    from darkdetect import isDark, isLight
    from email_validator import EmailNotValidError, validate_email
    from phonenumbers import format_number, is_valid_number, parse
    from phonenumbers.phonenumberutil import NumberParseException
    from PIL import Image
    from PIL.ImageTk import PhotoImage
    from psutil import cpu_percent, sensors_battery, virtual_memory
    from pyfiglet import FigletFont, figlet_format
    from requests import get, request
    from requests.exceptions import ConnectionError, ConnectTimeout, MissingSchema
    from tkcalendar import Calendar
    from ttkthemes import ThemedTk

    print("[INFO]\tInitializing colorama...")
    init(autoreset=True)

    F_GREEN: str = Fore.GREEN
    F_YELLOW: str = Fore.YELLOW
    F_RED: str = Fore.RED
    F_BLUE: str = Fore.BLUE

    S_BRIGHT: str = Style.BRIGHT

    print(F_GREEN + "[INFO]\tImporting custom modules, Please wait...")
    from countrycodes import country_list
    from private import (
        InvalidToken,
        decrypt_smtp_passwd,
        encrypt_root_passwd,
        encrypt_smtp_passwd,
        gen_private_key,
    )

    print(F_GREEN + "[INFO]\tImporting hidden modules, Please wait...")
    import PIL._tkinter_finder
    from babel import numbers

    country_names: list = list()
    # isd_codes: list = list()

    for _ in country_list:
        country_names.append(f"{_[0]} ({_[1]})")
        # isd_codes.append(_[1])

    # isd_codes: set = set(isd_codes)
    # isd_codes: list = sorted(isd_codes)

    if os_env == "Linux":
        if not isdir(s=f"/home/{whoami}/.config/TailorMate/"):
            mkdir(path=f"/home/{whoami}/.config/TailorMate/")

        config_file_path: str = f"/home/{whoami}/.config/TailorMate/config.ini"
        database_file_path: str = f"/home/{whoami}/.config/TailorMate/database.db"
        private_key_path: str = f"/home/{whoami}/.config/TailorMate/secret.key"

    elif os_env == "Windows":
        if not isdir(s=f"C:\\Users\\{whoami}\\TailorMate\\"):
            mkdir(path=f"C:\\Users\\{whoami}\\TailorMate\\")

        config_file_path: str = f"C:\\Users\\{whoami}\\TailorMate\\config.ini"
        database_file_path: str = f"C:\\Users\\{whoami}\\TailorMate\\database.db"
        private_key_path: str = f"C:\\Users\\{whoami}\\TailorMate\\secret.key"

    else:
        config_file_path: str = join(BASE_PATH, "config.ini")
        database_file_path: str = join(BASE_PATH, "database.db")
        private_key_path: str = join(BASE_PATH, "secret.key")

    __version__: str = "v.20221128 (Alpha-LTS)"
    accent_color_light: str = "lightsteelblue2"
    accent_color_dark: str = "#212946"

    business_types: list = [
        "Limited liability partnership",
        "Sole proprietorship",
        "Partnership",
        "Public Company",
        "Private Company",
        "Other",
    ]
    themes_list: list = ["Light theme", "Dark theme", "Use device theme"]
    header_list1: list = [
        "S.No",
        "Order No.",
        "Name",
        "Created On",
        "Phone No.",
        "Item",
        "Stitching Type",
        "Cost ($)",
        "Delivery Date",
        "Priority",
        "Status",
    ]
    header_list2: list = [
        "S.No",
        "Name",
        "Created On",
        "Phone No.",
        "Email Address",
        "D.O.B",
        "Gender",
    ]
    gender_options: list = ["Female", "Male", "Other"]
    header_list3: list = ["S.No", "All Items", "Categories"]

    if os_env == "Linux":
        terminal(command="xtitle -q -t TailorMate")

    if os_env == "Windows":
        terminal(command="title TailorMate")

    if not isfile(path=config_file_path):
        print(F_GREEN + "[INFO]\tLoading configuration app, Please wait...")

        ca: Tk = Tk()
        ca.withdraw()
        ca.title(string=f"TailorMate {__version__}")
        ca.iconphoto(False, TkPhotoImage(file=join(BASE_PATH, "assets/sewing.png")))
        ca.resizable(width=False, height=False)
        ca.config(bg=accent_color_light)
        ca.protocol(name="WM_DELETE_WINDOW", func=exit_ca)
        ca.bind(sequence="<Escape>", func=lambda event: exit_ca())
        ca.bind(sequence="<Control-Q>", func=lambda event: exit_ca())
        ca.bind(sequence="<Control-q>", func=lambda event: exit_ca())

        eula_var: BooleanVar = BooleanVar()
        eula_var.set(value=False)
        business_name_var: StringVar = StringVar()
        business_type_var: StringVar = StringVar()
        business_type_var.set(value=business_types[0])
        ca_ph_var: StringVar = StringVar()
        ca_website_var: StringVar = StringVar()
        ca_country_var: StringVar = StringVar()
        ca_passwd_var1: StringVar = StringVar()
        ca_passwd_var2: StringVar = StringVar()
        toggle_root_passwd_var: BooleanVar = BooleanVar()
        toggle_root_passwd_var.set(value=False)
        ca_hibp_var: BooleanVar = BooleanVar()
        ca_hibp_var.set(value=True)
        smtp_email_var: StringVar = StringVar()
        smtp_passwd_var: StringVar = StringVar()
        toggle_smtp_passwd_var: BooleanVar = BooleanVar()
        toggle_smtp_passwd_var.set(value=False)
        ca_weeks_number_var: BooleanVar = BooleanVar()
        ca_weeks_number_var.set(value=False)
        ca_other_month_days_var: BooleanVar = BooleanVar()
        ca_other_month_days_var.set(value=False)
        ca_bell_var: BooleanVar = BooleanVar()
        ca_bell_var.set(value=True)
        ca_mxdns_var: BooleanVar = BooleanVar()
        ca_mxdns_var.set(value=True)
        ca_theme_var: StringVar = StringVar()
        ca_theme_var.set(value=themes_list[2])

        _: Image = Image.open(fp=join(BASE_PATH, "assets/right-arrow.png")).resize(
            size=(20, 20)
        )
        next_ico: PhotoImage = PhotoImage(image=_)

        _: Image = Image.open(fp=join(BASE_PATH, "assets/left-arrow.png")).resize(
            size=(20, 20)
        )
        previous_ico: PhotoImage = PhotoImage(image=_)

        _: Image = Image.open(fp=join(BASE_PATH, "assets/diskette.png")).resize(
            size=(20, 20)
        )
        save_ico: PhotoImage = PhotoImage(image=_)

        _: Image = Image.open(fp=join(BASE_PATH, "assets/share.png")).resize(
            size=(15, 15)
        )
        redirect_ico: PhotoImage = PhotoImage(image=_)

        Label(
            master=ca,
            text=f"Hello {whoami.title()}, Welcome to TailorMate!",
            bg="#000",
            fg="#fff",
        ).pack(side=TOP, fill=X)

        ca_tab_view: Notebook = Notebook(master=ca)
        ca_tab_view.pack(fill=BOTH, expand=1)

        ca_eula_frame: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_eula_frame.pack()

        ca_business_frame: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_business_frame.pack()

        ca_passwd_frame: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_passwd_frame.pack()

        ca_smtp_frame: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_smtp_frame.pack()

        ca_social_media_frame: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_social_media_frame.pack()

        ca_other_settings: Frame = Frame(master=ca_tab_view, bg=accent_color_light)
        ca_other_settings.pack()

        ca_tab_view.add(child=ca_eula_frame, text="License Agreement")
        ca_tab_view.add(child=ca_business_frame, text="User Configuration")
        ca_tab_view.add(child=ca_passwd_frame, text="Password Configuration")
        ca_tab_view.add(child=ca_smtp_frame, text="SMTP Configuration")
        ca_tab_view.add(child=ca_social_media_frame, text="Social Media")
        ca_tab_view.add(child=ca_other_settings, text="Other Settings")

        ca.bind(
            sequence="<Alt-KeyPress-1>", func=lambda event: ca_tab_view.select(tab_id=0)
        )
        ca.bind(
            sequence="<Alt-KeyPress-2>", func=lambda event: ca_tab_view.select(tab_id=1)
        )
        ca.bind(
            sequence="<Alt-KeyPress-3>", func=lambda event: ca_tab_view.select(tab_id=2)
        )
        ca.bind(
            sequence="<Alt-KeyPress-4>", func=lambda event: ca_tab_view.select(tab_id=3)
        )
        ca.bind(
            sequence="<Alt-KeyPress-5>", func=lambda event: ca_tab_view.select(tab_id=4)
        )
        ca.bind(
            sequence="<Alt-KeyPress-6>", func=lambda event: ca_tab_view.select(tab_id=5)
        )

        lf01: LabelFrame = LabelFrame(
            master=ca_eula_frame,
            text="License Agreement",
            bg=accent_color_light,
            fg="red",
        )
        lf01.pack(padx=10, pady=5, fill=BOTH, expand=1)

        ca_license_text: ScrolledText = ScrolledText(
            master=lf01, selectbackground="orange"
        )
        license_file = open(file=join(BASE_PATH, "LICENSE"), mode="r")
        ca_license_text.insert(index=1.0, chars=license_file.read())
        license_file.close()
        ca_license_text.config(state=DISABLED)
        ca_license_text.pack(padx=10, pady=5, fill=BOTH, expand=1)

        eula_btn: Checkbutton = Checkbutton(
            master=lf01,
            text="I accept the license agreement",
            bg=accent_color_light,
            activebackground=accent_color_light,
            variable=eula_var,
        )
        eula_btn.pack(padx=10, anchor=E)

        ca_bottom_frame1: Frame = Frame(master=lf01, bg=accent_color_light)
        ca_bottom_frame1.pack(side=BOTTOM, pady=5, fill=X)

        ca_next_btn1: Button = Button(
            master=ca_bottom_frame1,
            text="Next",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=RIGHT,
            width=120,
            image=next_ico,
            command=lambda: ca_tab_view.select(tab_id=1),
        )
        ca_next_btn1.pack(padx=10, side=RIGHT)

        eula_btn.bind(sequence="<Up>", func=lambda event: ca_next_btn1.focus())
        eula_btn.bind(sequence="<Down>", func=lambda event: ca_next_btn1.focus())
        ca_next_btn1.bind(sequence="<Up>", func=lambda event: eula_btn.focus())
        ca_next_btn1.bind(sequence="<Down>", func=lambda event: eula_btn.focus())
        ca_next_btn1.bind(
            sequence="<Return>", func=lambda event: ca_tab_view.select(tab_id=1)
        )

        lf02: LabelFrame = LabelFrame(
            master=ca_business_frame,
            text="Configure your Business",
            bg=accent_color_light,
            fg="red",
        )
        lf02.pack(padx=10, pady=5, fill=BOTH, expand=1)

        f02: Frame = Frame(master=lf02, bg=accent_color_light)
        f02.pack(pady=5)

        ca_name_lbl: Label = Label(
            master=f02, text="Legal Name of Business:", bg=accent_color_light
        )
        ca_name_lbl.grid(row=0, column=0, padx=5, sticky=W)
        ca_name_entry: Entry = Entry(
            master=f02,
            width=35,
            textvariable=business_name_var,
            selectbackground="orange",
        )
        ca_name_entry.grid(row=0, column=1, padx=5, sticky=W)

        Label(master=f02, text="Business Type:", bg=accent_color_light).grid(
            row=1, column=0, padx=5, sticky=W
        )
        business_type_om: OptionMenu = OptionMenu(
            f02, business_type_var, *business_types
        )
        business_type_om.config(bg="purple", fg="#fff")
        business_type_om["menu"].config(bg="purple")
        business_type_om.grid(row=1, column=1, padx=5, sticky=NSEW)

        ca_country_lbl: Label = Label(
            master=f02, text="Country and Dialing Code:", bg=accent_color_light
        )
        ca_country_lbl.grid(row=2, column=0, padx=5, sticky=W)

        # country_list: tuple = load_pickle_file(file=join(base_path, "country.pkl"))

        # try:
        #     print(
        #         F_GREEN + "[INFO]\tConnecting to https://ipinfo.io/ Please wait..."
        #     )
        #     ipinfo_response = get(url="https://ipinfo.io/").json()

        #     iso_code: str = ipinfo_response["country"]
        #     print(F_GREEN + f"[INFO]\tCountry ISO Code: {iso_code}")

        #     country_list_length: int = len(country_list)

        #     for index in range(country_list_length):
        #         if iso_code == iso_codes[index]:
        #             ca_country_var.set(value=country_names[index])

        # except ConnectionError:
        #     pass

        # country_names_entry: AutocompleteEntry = AutocompleteEntry(master=f02, width=30, completevalues=country_names)
        # country_names_entry.grid(row=2, column=1, padx=5)

        country_name_cb: Combobox = Combobox(
            master=f02, textvariable=ca_country_var, values=country_names
        )
        country_name_cb.grid(row=2, column=1, padx=5, sticky=NSEW)

        ca_ph_lbl: Label = Label(
            master=f02, text="Phone Number:", bg=accent_color_light
        )
        ca_ph_lbl.grid(row=3, column=0, padx=5, sticky=W)

        ca_ph_entry: Entry = Entry(
            master=f02, width=35, selectbackground="orange", textvariable=ca_ph_var
        )
        ca_ph_entry.grid(row=3, column=1, padx=5, sticky=W)

        ca_website_lbl: Label = Label(
            master=f02, text="Website (Optional):", bg=accent_color_light
        )
        ca_website_lbl.grid(row=4, column=0, padx=5, sticky=W)
        ca_website_entry: Entry = Entry(
            master=f02,
            width=35,
            textvariable=ca_website_var,
            selectbackground="orange",
        )
        ca_website_entry.grid(row=4, column=1, padx=5, sticky=W)

        ca_name_entry.bind(sequence="<Up>", func=lambda event: ca_website_entry.focus())
        ca_name_entry.bind(sequence="<Down>", func=lambda event: ca_ph_entry.focus())

        ca_ph_entry.bind(sequence="<Up>", func=lambda event: ca_name_entry.focus())
        ca_ph_entry.bind(sequence="<Down>", func=lambda event: ca_website_entry.focus())

        ca_website_entry.bind(sequence="<Up>", func=lambda event: ca_ph_entry.focus())
        ca_website_entry.bind(
            sequence="<Down>", func=lambda event: ca_name_entry.focus()
        )

        Label(
            master=lf02,
            text="Note: Internet connection required to verify your website is active and running.",
            fg="red",
            bg=accent_color_light,
        ).pack()

        ca_bottom_frame2: Frame = Frame(master=lf02, bg=accent_color_light)
        ca_bottom_frame2.pack(side=BOTTOM, pady=5, fill=X)

        ca_previous_btn2: Button = Button(
            master=ca_bottom_frame2,
            text="Previous",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=previous_ico,
            command=lambda: ca_tab_view.select(tab_id=0),
        )
        ca_previous_btn2.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=0),
        )
        ca_previous_btn2.pack(padx=10, side=LEFT)

        ca_next_btn2: Button = Button(
            master=ca_bottom_frame2,
            text="Next",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=RIGHT,
            width=120,
            image=next_ico,
            command=lambda: ca_tab_view.select(tab_id=2),
        )
        ca_next_btn2.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=2),
        )
        ca_next_btn2.pack(padx=10, side=RIGHT)

        ca_previous_btn2.bind(
            sequence="<Up>", func=lambda event: ca_website_entry.focus()
        )
        ca_previous_btn2.bind(
            sequence="<Left>", func=lambda event: ca_next_btn2.focus()
        )
        ca_previous_btn2.bind(
            sequence="<Right>", func=lambda event: ca_next_btn2.focus()
        )

        ca_next_btn2.bind(sequence="<Up>", func=lambda event: ca_website_entry.focus())
        ca_next_btn2.bind(
            sequence="<Left>", func=lambda event: ca_previous_btn2.focus()
        )
        ca_next_btn2.bind(
            sequence="<Right>", func=lambda event: ca_previous_btn2.focus()
        )

        lf03: LabelFrame = LabelFrame(
            master=ca_passwd_frame,
            text="Root Password",
            bg=accent_color_light,
            fg="red",
        )
        lf03.pack(padx=10, pady=5, fill=BOTH, expand=1, ipady=3)

        f03: Frame = Frame(master=lf03, bg=accent_color_light)
        f03.pack(pady=5)

        ca_passwd_lbl1: Label = Label(
            master=f03, text="Create a Strong Password:", bg=accent_color_light
        )
        ca_passwd_lbl1.grid(row=0, column=0, padx=5, sticky=W)
        ca_passwd_entry1: Entry = Entry(
            master=f03,
            width=25,
            show="*",
            textvariable=ca_passwd_var1,
            selectbackground="orange",
        )
        ca_passwd_entry1.grid(row=0, column=1, padx=5, sticky=W)

        ca_passwd_lbl2: Label = Label(
            master=f03, text="Re-type your Password:", bg=accent_color_light
        )
        ca_passwd_lbl2.grid(row=1, column=0, padx=5, sticky=W)
        ca_passwd_entry2: Entry = Entry(
            master=f03,
            width=25,
            show="*",
            textvariable=ca_passwd_var2,
            selectbackground="orange",
        )
        ca_passwd_entry2.grid(row=1, column=1, padx=5, sticky=W)

        ca_show_root_passwd: Checkbutton = Checkbutton(
            master=f03,
            text="Show root password",
            bg=accent_color_light,
            activebackground=accent_color_light,
            variable=toggle_root_passwd_var,
            command=toggle_root_passwd,
        )
        ca_show_root_passwd.grid(row=2, column=1, padx=5, sticky=W)

        ca_passwd_entry1.bind(
            sequence="<Return>",
            func=lambda event: ca_passwd_entry2.focus(),
        )
        ca_passwd_entry1.bind(
            sequence="<Up>", func=lambda event: ca_show_root_passwd.focus()
        )
        ca_passwd_entry1.bind(
            sequence="<Down>", func=lambda event: ca_passwd_entry2.focus()
        )
        ca_passwd_entry2.bind(
            sequence="<Up>", func=lambda event: ca_passwd_entry1.focus()
        )
        ca_passwd_entry2.bind(
            sequence="<Down>", func=lambda event: ca_show_root_passwd.focus()
        )
        ca_show_root_passwd.bind(
            sequence="<Up>", func=lambda event: ca_passwd_entry2.focus()
        )
        ca_show_root_passwd.bind(
            sequence="<Down>", func=lambda event: ca_passwd_entry1.focus()
        )

        Label(
            master=lf03,
            text="Check your password strength and security:",
            fg="red",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)

        Checkbutton(
            master=lf03,
            text="Use HIBP API to check for pwned password *",
            bg=accent_color_light,
            activebackground=accent_color_light,
            variable=ca_hibp_var,
        ).pack(padx=5, anchor=W)

        entropy_lbl: Label = Label(
            master=lf03,
            text="* Entropy: 0.00 bit(s)",
            bg=accent_color_light,
        )
        entropy_lbl.pack(padx=5, anchor=W)

        # Label(
        #     master=lf03,
        #     text="Formula for Password Entropy: E = L * log(R) / log(2)",
        #     bg=accent_color_light,
        # ).pack()
        # Label(
        #     master=lf03,
        #     text="Where L = Password length, i.e., the number of characters in the password;",
        #     bg=accent_color_light,
        # ).pack()
        # Label(
        #     master=lf03,
        #     text="Where R = Size of pool, unique characters from which we build the password;",
        #     bg=accent_color_light,
        # ).pack()

        passwd_strength_lbl: Label = Label(
            master=lf03, text="* Strength: NA", bg=accent_color_light
        )
        passwd_strength_lbl.pack(padx=5, anchor=W)

        _: Image = Image.open(fp=join(BASE_PATH, "assets/key.png")).resize(
            size=(18, 18)
        )
        key_ico: PhotoImage = PhotoImage(image=_)
        passwd_strength_btn: Button = Button(
            master=lf03,
            text="Check Strength",
            activebackground="green",
            fg="#fff",
            bg="#20C020",
            activeforeground="#fff",
            compound=LEFT,
            width=125,
            image=key_ico,
            command=check_passwd_strength,
        )
        passwd_strength_btn.bind(
            sequence="<Return>", func=lambda event: check_passwd_strength()
        )
        passwd_strength_btn.pack()

        Label(
            master=lf03,
            text="Note: HIBP API requires internet connection.",
            fg="red",
            bg=accent_color_light,
        ).pack()
        Label(
            master=lf03, text="Master Password Tips:", bg=accent_color_light, fg="red"
        ).pack(padx=5, anchor=W)
        Label(
            master=lf03,
            text="* The master password is the only password, that you have to remember.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf03,
            text="* Do not include personal data (like birthdays).",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf03,
            text="* Do not use character sequences from the keyboard.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf03,
            text="* Try to make it as long as possible for you.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf03,
            text="* If you wish you can write it down and keep it in a safe place.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)

        ca_bottom_frame3: Frame = Frame(master=lf03, bg=accent_color_light)
        ca_bottom_frame3.pack(side=BOTTOM, pady=5, fill=X)

        ca_previous_btn3: Button = Button(
            master=ca_bottom_frame3,
            text="Previous",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=previous_ico,
            command=lambda: ca_tab_view.select(tab_id=1),
        )
        ca_previous_btn3.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=1),
        )
        ca_previous_btn3.pack(padx=10, side=LEFT)

        ca_next_btn3: Button = Button(
            master=ca_bottom_frame3,
            text="Next",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=RIGHT,
            width=120,
            image=next_ico,
            command=lambda: ca_tab_view.select(tab_id=3),
        )
        ca_next_btn3.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=3),
        )
        ca_next_btn3.pack(padx=10, side=RIGHT)

        ca_previous_btn3.bind(
            sequence="<Left>", func=lambda event: ca_next_btn3.focus()
        )
        ca_previous_btn3.bind(
            sequence="<Right>", func=lambda event: ca_next_btn3.focus()
        )

        ca_next_btn3.bind(
            sequence="<Left>", func=lambda event: ca_previous_btn3.focus()
        )
        ca_next_btn3.bind(
            sequence="<Right>", func=lambda event: ca_previous_btn3.focus()
        )

        lf04: LabelFrame = LabelFrame(
            bg=accent_color_light,
            fg="red",
            master=ca_smtp_frame,
            text="Configure SMTP Server",
        )
        lf04.pack(padx=10, pady=5, fill=BOTH, expand=1, ipady=3)

        f04: Frame = Frame(master=lf04, bg=accent_color_light)
        f04.pack(pady=5)

        smtp_email_lbl: Label = Label(
            master=f04, text="Gmail Address:", bg=accent_color_light
        )
        smtp_email_lbl.grid(row=0, column=0, padx=5, sticky=W)
        smtp_email_entry: Entry = Entry(
            master=f04, width=30, textvariable=smtp_email_var, selectbackground="orange"
        )
        smtp_email_entry.grid(row=0, column=1, padx=5, sticky=W)

        smtp_passwd_lbl: Label = Label(
            master=f04, text="SMTP App Password:", bg=accent_color_light
        )
        smtp_passwd_lbl.grid(row=1, column=0, padx=5, sticky=W)
        smtp_passwd_entry: Entry = Entry(
            master=f04,
            width=30,
            show="*",
            textvariable=smtp_passwd_var,
            selectbackground="orange",
        )
        smtp_passwd_entry.grid(row=1, column=1, padx=5, sticky=W)

        ca_show_smtp_passwd: Checkbutton = Checkbutton(
            master=f04,
            text="Show SMTP password",
            bg=accent_color_light,
            activebackground=accent_color_light,
            variable=toggle_smtp_passwd_var,
            command=toggle_smtp_passwd,
        )
        ca_show_smtp_passwd.grid(row=2, column=1, padx=5, sticky=W)

        smtp_email_entry.bind(
            sequence="<Return>", func=lambda event: smtp_passwd_entry.focus()
        )
        smtp_email_entry.bind(
            sequence="<Up>", func=lambda event: ca_show_smtp_passwd.focus()
        )
        smtp_email_entry.bind(
            sequence="<Down>", func=lambda event: smtp_passwd_entry.focus()
        )
        smtp_passwd_entry.bind(
            sequence="<Up>", func=lambda event: smtp_email_entry.focus()
        )
        smtp_passwd_entry.bind(
            sequence="<Down>", func=lambda event: ca_show_smtp_passwd.focus()
        )
        ca_show_smtp_passwd.bind(
            sequence="<Up>", func=lambda event: smtp_passwd_entry.focus()
        )
        ca_show_smtp_passwd.bind(
            sequence="<Down>", func=lambda event: smtp_email_entry.focus()
        )

        # Label(
        #     master=lf03,
        #     text=" What is SMTP server? Why do we ask for your email address and password?",
        #     bg=accent_color_light,
        #     fg="red",
        # ).pack(padx=5, anchor=W)
        # Label(
        #     master=lf03,
        #     text="SMTP stands for Simple Mail Transfer Protocol. It helps you to send automatic emails like "
        #     "greetings, order status, and offer messages to your client seamlessly.",
        #     bg="red",
        #     fg="#fff",
        #     wraplength=485,
        #     anchor=W,
        # ).pack(padx=5, fill=X)

        Label(
            master=lf04,
            text="Note: Internet connection required to configure the SMTP server",
            fg="red",
            bg=accent_color_light,
        ).pack()

        f041: Frame = Frame(master=lf04, bg=accent_color_light)
        f041.pack(padx=5, pady=5, anchor=W)

        Label(
            master=f041, text="Steps to follow:", fg="red", bg=accent_color_light
        ).grid(row=0, column=0, sticky=W)

        Label(
            master=f041,
            text="Step 1: Don't forget to turn ON",
            bg=accent_color_light,
        ).grid(row=1, column=0, padx=2, sticky=W)

        two_step_verification_btn: Button = Button(
            master=f041,
            text="2-Step Verification",
            activebackground="green",
            fg="#fff",
            bg="#20C020",
            activeforeground="#fff",
            width=150,
            compound=RIGHT,
            image=redirect_ico,
            command=lambda: browser(
                url="https://myaccount.google.com/signinoptions/two-step-verification"
            ),
        )
        two_step_verification_btn.bind(
            sequence="<Return>",
            func=lambda event: browser(
                url="https://myaccount.google.com/signinoptions/two-step-verification"
            ),
        )
        two_step_verification_btn.grid(row=1, column=1, padx=2)

        Label(
            master=f041,
            text="Step 2: Click here to generate",
            bg=accent_color_light,
        ).grid(row=2, column=0, padx=2, sticky=W)

        # https://support.google.com/accounts?p=less-secure-apps&hl=en
        app_passwds_btn: Button = Button(
            master=f041,
            text="SMTP App Password",
            activebackground="green",
            fg="#fff",
            bg="#20C020",
            activeforeground="#fff",
            compound=RIGHT,
            width=150,
            image=redirect_ico,
            command=lambda: browser(url="https://myaccount.google.com/apppasswords"),
        )
        app_passwds_btn.bind(
            sequence="<Return>",
            func=lambda event: browser(url="https://myaccount.google.com/apppasswords"),
        )
        app_passwds_btn.grid(row=2, column=1, padx=2)

        two_step_verification_btn.bind(
            sequence="<Up>", func=lambda event: app_passwds_btn.focus()
        )
        two_step_verification_btn.bind(
            sequence="<Down>", func=lambda event: app_passwds_btn.focus()
        )

        app_passwds_btn.bind(
            sequence="<Up>", func=lambda event: two_step_verification_btn.focus()
        )
        app_passwds_btn.bind(
            sequence="<Down>", func=lambda event: two_step_verification_btn.focus()
        )

        Label(
            master=lf04,
            text="We Respect your Privacy:",
            bg=accent_color_light,
            fg="red",
        ).pack(padx=5, anchor=W)
        Label(
            master=lf04,
            text="*  We only handles Gmail address for now.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf04,
            text="*  We never share your password with anyone.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)
        Label(
            master=lf04,
            text="*  Don't worry, We don't send spam messages.",
            bg=accent_color_light,
        ).pack(padx=5, anchor=W)

        ca_bottom_frame4: Frame = Frame(master=lf04, bg=accent_color_light)
        ca_bottom_frame4.pack(side=BOTTOM, pady=5, fill=X)

        ca_previous_btn4: Button = Button(
            master=ca_bottom_frame4,
            text="Previous",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=previous_ico,
            command=lambda: ca_tab_view.select(tab_id=2),
        )
        ca_previous_btn4.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=2),
        )
        ca_previous_btn4.pack(padx=10, side=LEFT)

        ca_next_btn4: Button = Button(
            master=ca_bottom_frame4,
            text="Next",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=RIGHT,
            width=120,
            image=next_ico,
            command=lambda: ca_tab_view.select(tab_id=4),
        )
        ca_next_btn4.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=4),
        )
        ca_next_btn4.pack(padx=10, side=RIGHT)

        ca_previous_btn4.bind(
            sequence="<Left>", func=lambda event: ca_next_btn4.focus()
        )
        ca_previous_btn4.bind(
            sequence="<Right>", func=lambda event: ca_next_btn4.focus()
        )

        ca_next_btn4.bind(
            sequence="<Left>", func=lambda event: ca_previous_btn4.focus()
        )
        ca_next_btn4.bind(
            sequence="<Right>", func=lambda event: ca_previous_btn4.focus()
        )

        lf05: LabelFrame = LabelFrame(
            master=ca_social_media_frame,
            text="Social Media Accounts (Optional)",
            fg="red",
            bg=accent_color_light,
        )
        lf05.pack(padx=10, pady=5, fill=BOTH, expand=1, ipady=3)

        f05: Frame = Frame(master=lf05, bg=accent_color_light)
        f05.pack()

        fb_lbl: Label = Label(master=f05, text="Facebook URL:", bg=accent_color_light)
        fb_lbl.grid(row=0, column=0, padx=5, sticky=W)
        fb_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        fb_entry.grid(row=0, column=1, padx=5, sticky=W)
        _: Image = Image.open(
            fp=join(BASE_PATH, "assets/facebook-circular-logo.png")
        ).resize(size=(20, 20))
        fb_ico: PhotoImage = PhotoImage(image=_)
        fb_btn: Button = Button(
            master=f05,
            text="Open Facebook",
            bg="#4867AA",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=fb_ico,
        )
        fb_btn.grid(row=0, column=2, padx=5, sticky=W)

        github_lbl: Label = Label(master=f05, text="GitHub URL:", bg=accent_color_light)
        github_lbl.grid(row=1, column=0, padx=5, sticky=W)
        github_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        github_entry.grid(row=1, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/github.png")).resize(
            size=(20, 20)
        )
        github_ico: PhotoImage = PhotoImage(image=_)
        github_btn: Button = Button(
            master=f05,
            text="Open GitHub",
            bg="#000",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=github_ico,
        )
        github_btn.grid(row=1, column=2, padx=5, sticky=W)

        ig_lbl: Label = Label(master=f05, text="Instagram URL:", bg=accent_color_light)
        ig_lbl.grid(row=2, column=0, padx=5, sticky=W)
        ig_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        ig_entry.grid(row=2, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/instagram.png")).resize(
            size=(20, 20)
        )
        ig_ico: PhotoImage = PhotoImage(image=_)
        ig_btn: Button = Button(
            master=f05,
            text="Open Instagram",
            bg="#E0306E",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=ig_ico,
        )
        ig_btn.grid(row=2, column=2, padx=5, sticky=W)

        linkedin_lbl: Label = Label(
            master=f05, text="LinkedIn URL:", bg=accent_color_light
        )
        linkedin_lbl.grid(row=3, column=0, padx=5, sticky=W)
        linkedin_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        linkedin_entry.grid(row=3, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/linkedin.png")).resize(
            size=(20, 20)
        )
        linkedin_ico: PhotoImage = PhotoImage(image=_)
        linkedin_btn: Button = Button(
            master=f05,
            text="Open LinkedIn",
            bg="#0077B5",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=linkedin_ico,
        )
        linkedin_btn.grid(row=3, column=2, padx=5, sticky=W)

        reddit_lbl: Label = Label(master=f05, text="Reddit URL:", bg=accent_color_light)
        reddit_lbl.grid(row=4, column=0, padx=5, sticky=W)
        reddit_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        reddit_entry.grid(row=4, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/reddit.png")).resize(
            size=(20, 20)
        )
        reddit_ico: PhotoImage = PhotoImage(image=_)
        reddit_btn: Button = Button(
            master=f05,
            text="Open Reddit",
            bg="#FF4500",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=reddit_ico,
        )
        reddit_btn.grid(row=4, column=2, padx=5, sticky=W)

        twitter_lbl: Label = Label(
            master=f05, text="Twitter URL:", bg=accent_color_light
        )
        twitter_lbl.grid(row=5, column=0, padx=5, sticky=W)
        twitter_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        twitter_entry.grid(row=5, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/twitter.png")).resize(
            size=(20, 20)
        )
        twitter_ico: PhotoImage = PhotoImage(image=_)
        twitter_btn: Button = Button(
            master=f05,
            text="Open Twitter",
            bg="#1DA1F2",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=twitter_ico,
        )
        twitter_btn.grid(row=5, column=2, padx=5, sticky=W)

        wa_lbl: Label = Label(
            master=f05, text="Whatsapp Number:", bg=accent_color_light
        )
        wa_lbl.grid(row=6, column=0, padx=5, sticky=W)
        wa_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        wa_entry.grid(row=6, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/whatsapp.png")).resize(
            size=(20, 20)
        )
        wa_ico: PhotoImage = PhotoImage(image=_)
        wa_btn: Button = Button(
            master=f05,
            text="Open Whatsapp",
            bg="green",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=wa_ico,
        )
        wa_btn.grid(row=6, column=2, padx=5, sticky=W)

        yt_lbl: Label = Label(master=f05, text="YouTube URL:", bg=accent_color_light)
        yt_lbl.grid(row=7, column=0, padx=5, sticky=W)
        yt_entry: Entry = Entry(master=f05, width=25, selectbackground="orange")
        yt_entry.grid(row=7, column=1, padx=5, sticky=W)
        _: Image = Image.open(fp=join(BASE_PATH, "assets/youtube.png")).resize(
            size=(20, 20)
        )
        yt_ico: PhotoImage = PhotoImage(image=_)
        yt_btn: Button = Button(
            master=f05,
            text="Open YouTube",
            bg="red",
            fg="#fff",
            compound=LEFT,
            width=125,
            image=yt_ico,
        )
        yt_btn.grid(row=7, column=2, padx=5, sticky=W)

        fb_entry.bind(sequence="<Return>", func=lambda event: github_entry.focus())
        github_entry.bind(sequence="<Return>", func=lambda event: ig_entry.focus())
        ig_entry.bind(sequence="<Return>", func=lambda event: linkedin_entry.focus())
        linkedin_entry.bind(
            sequence="<Return>", func=lambda event: reddit_entry.focus()
        )
        reddit_entry.bind(sequence="<Return>", func=lambda event: twitter_entry.focus())
        twitter_entry.bind(sequence="<Return>", func=lambda event: wa_entry.focus())
        wa_entry.bind(sequence="<Return>", func=lambda event: yt_entry.focus())

        fb_entry.bind(sequence="<Up>", func=lambda event: yt_entry.focus())
        fb_entry.bind(sequence="<Down>", func=lambda event: github_entry.focus())
        fb_entry.bind(sequence="<Left>", func=lambda event: fb_btn.focus())
        fb_entry.bind(sequence="<Right>", func=lambda event: fb_btn.focus())

        fb_btn.bind(sequence="<Up>", func=lambda event: yt_btn.focus())
        fb_btn.bind(sequence="<Down>", func=lambda event: github_btn.focus())
        fb_btn.bind(sequence="<Left>", func=lambda event: fb_entry.focus())
        fb_btn.bind(sequence="<Right>", func=lambda event: fb_entry.focus())

        github_entry.bind(sequence="<Up>", func=lambda event: fb_entry.focus())
        github_entry.bind(sequence="<Down>", func=lambda event: ig_entry.focus())
        github_entry.bind(sequence="<Left>", func=lambda event: github_btn.focus())
        github_entry.bind(sequence="<Right>", func=lambda event: github_btn.focus())

        github_btn.bind(sequence="<Up>", func=lambda event: fb_btn.focus())
        github_btn.bind(sequence="<Down>", func=lambda event: ig_btn.focus())
        github_btn.bind(sequence="<Left>", func=lambda event: github_entry.focus())
        github_btn.bind(sequence="<Right>", func=lambda event: github_entry.focus())

        ig_entry.bind(sequence="<Up>", func=lambda event: github_entry.focus())
        ig_entry.bind(sequence="<Down>", func=lambda event: linkedin_entry.focus())
        ig_entry.bind(sequence="<Left>", func=lambda event: ig_btn.focus())
        ig_entry.bind(sequence="<Right>", func=lambda event: ig_btn.focus())

        ig_btn.bind(sequence="<Up>", func=lambda event: github_btn.focus())
        ig_btn.bind(sequence="<Down>", func=lambda event: reddit_btn.focus())
        ig_btn.bind(sequence="<Left>", func=lambda event: ig_entry.focus())
        ig_btn.bind(sequence="<Right>", func=lambda event: ig_entry.focus())

        linkedin_entry.bind(sequence="<Up>", func=lambda event: ig_entry.focus())
        linkedin_entry.bind(sequence="<Down>", func=lambda event: reddit_entry.focus())
        linkedin_entry.bind(sequence="<Left>", func=lambda event: linkedin_btn.focus())
        linkedin_entry.bind(sequence="<Right>", func=lambda event: linkedin_btn.focus())

        linkedin_btn.bind(sequence="<Up>", func=lambda event: ig_btn.focus())
        linkedin_btn.bind(sequence="<Down>", func=lambda event: reddit_btn.focus())
        linkedin_btn.bind(sequence="<Left>", func=lambda event: linkedin_entry.focus())
        linkedin_btn.bind(sequence="<Right>", func=lambda event: linkedin_entry.focus())

        reddit_entry.bind(sequence="<Up>", func=lambda event: linkedin_entry.focus())
        reddit_entry.bind(sequence="<Down>", func=lambda event: twitter_entry.focus())
        reddit_entry.bind(sequence="<Left>", func=lambda event: reddit_btn.focus())
        reddit_entry.bind(sequence="<Right>", func=lambda event: reddit_btn.focus())

        reddit_btn.bind(sequence="<Up>", func=lambda event: linkedin_btn.focus())
        reddit_btn.bind(sequence="<Down>", func=lambda event: twitter_btn.focus())
        reddit_btn.bind(sequence="<Left>", func=lambda event: reddit_entry.focus())
        reddit_btn.bind(sequence="<Right>", func=lambda event: reddit_entry.focus())

        twitter_entry.bind(sequence="<Up>", func=lambda event: reddit_entry.focus())
        twitter_entry.bind(sequence="<Down>", func=lambda event: wa_entry.focus())
        twitter_entry.bind(sequence="<Left>", func=lambda event: twitter_btn.focus())
        twitter_entry.bind(sequence="<Right>", func=lambda event: twitter_btn.focus())

        twitter_btn.bind(sequence="<Up>", func=lambda event: reddit_btn.focus())
        twitter_btn.bind(sequence="<Down>", func=lambda event: wa_btn.focus())
        twitter_btn.bind(sequence="<Left>", func=lambda event: twitter_entry.focus())
        twitter_btn.bind(sequence="<Right>", func=lambda event: twitter_entry.focus())

        wa_entry.bind(sequence="<Up>", func=lambda event: twitter_entry.focus())
        wa_entry.bind(sequence="<Down>", func=lambda event: yt_entry.focus())
        wa_entry.bind(sequence="<Left>", func=lambda event: wa_btn.focus())
        wa_entry.bind(sequence="<Right>", func=lambda event: wa_btn.focus())

        wa_btn.bind(sequence="<Up>", func=lambda event: twitter_btn.focus())
        wa_btn.bind(sequence="<Down>", func=lambda event: yt_btn.focus())
        wa_btn.bind(sequence="<Left>", func=lambda event: wa_entry.focus())
        wa_btn.bind(sequence="<Right>", func=lambda event: wa_entry.focus())

        yt_entry.bind(sequence="<Up>", func=lambda event: wa_entry.focus())
        yt_entry.bind(sequence="<Down>", func=lambda event: fb_entry.focus())
        yt_entry.bind(sequence="<Left>", func=lambda event: yt_btn.focus())
        yt_entry.bind(sequence="<Right>", func=lambda event: yt_btn.focus())

        yt_btn.bind(sequence="<Up>", func=lambda event: wa_btn.focus())
        yt_btn.bind(sequence="<Down>", func=lambda event: fb_btn.focus())
        yt_btn.bind(sequence="<Left>", func=lambda event: yt_entry.focus())
        yt_btn.bind(sequence="<Right>", func=lambda event: yt_entry.focus())

        ca_bottom_frame5: Frame = Frame(master=lf05, bg=accent_color_light)
        ca_bottom_frame5.pack(side=BOTTOM, pady=5, fill=X)

        ca_previous_btn5: Button = Button(
            master=ca_bottom_frame5,
            text="Previous",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=previous_ico,
            command=lambda: ca_tab_view.select(tab_id=3),
        )
        ca_previous_btn5.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=3),
        )
        ca_previous_btn5.pack(padx=10, side=LEFT)

        ca_next_btn5: Button = Button(
            master=ca_bottom_frame5,
            text="Next",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=RIGHT,
            width=120,
            image=next_ico,
            command=lambda: ca_tab_view.select(tab_id=5),
        )
        ca_next_btn5.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=5),
        )
        ca_next_btn5.pack(padx=10, side=RIGHT)

        ca_previous_btn5.bind(
            sequence="<Left>", func=lambda event: ca_next_btn5.focus()
        )
        ca_previous_btn5.bind(
            sequence="<Right>", func=lambda event: ca_next_btn5.focus()
        )
        ca_next_btn5.bind(
            sequence="<Left>", func=lambda event: ca_previous_btn5.focus()
        )
        ca_next_btn5.bind(
            sequence="<Right>", func=lambda event: ca_previous_btn5.focus()
        )

        lf06: LabelFrame = LabelFrame(
            master=ca_other_settings,
            text="Other Settings",
            bg=accent_color_light,
            fg="red",
        )
        lf06.pack(padx=10, pady=5, fill=BOTH, expand=1, ipady=3)

        f06: Frame = Frame(master=lf06, bg=accent_color_light)
        f06.pack(pady=5)

        f061: Frame = Frame(master=f06, bg=accent_color_light)
        f061.pack()

        ca_cb1: Checkbutton = Checkbutton(
            master=f061,
            text="Show Weeks Number on Calendar",
            bg=accent_color_light,
            variable=ca_weeks_number_var,
        )
        ca_cb1.grid(row=0, column=0, sticky=W)

        ca_cb2: Checkbutton = Checkbutton(
            master=f061,
            text="Show Other Month Days on Calendar",
            bg=accent_color_light,
            variable=ca_other_month_days_var,
        )
        ca_cb2.grid(row=1, column=0, sticky=W)

        ca_cb3: Checkbutton = Checkbutton(
            master=f061,
            text="Check MX DNS record on email validation *",
            bg=accent_color_light,
            variable=ca_mxdns_var,
        )
        ca_cb3.grid(row=2, column=0, sticky=W)

        ca_cb4: Checkbutton = Checkbutton(
            master=f061,
            text="Play Alert Sound",
            bg=accent_color_light,
            variable=ca_bell_var,
        )
        ca_cb4.grid(row=3, column=0, sticky=W)

        ca_cb1.bind(sequence="<Up>", func=lambda event: ca_cb4.focus())
        ca_cb1.bind(sequence="<Down>", func=lambda event: ca_cb2.focus())

        ca_cb2.bind(sequence="<Up>", func=lambda event: ca_cb1.focus())
        ca_cb2.bind(sequence="<Down>", func=lambda event: ca_cb3.focus())

        ca_cb3.bind(sequence="<Up>", func=lambda event: ca_cb2.focus())
        ca_cb3.bind(sequence="<Down>", func=lambda event: ca_cb4.focus())

        ca_cb4.bind(sequence="<Up>", func=lambda event: ca_cb3.focus())
        ca_cb4.bind(sequence="<Down>", func=lambda event: ca_cb1.focus())

        f062: Frame = Frame(master=f06, bg=accent_color_light)
        f062.pack()

        Label(master=f062, text="Theme Appearance:", bg=accent_color_light).grid(
            row=0, column=0, padx=5
        )

        ca_theme_table: OptionMenu = OptionMenu(
            f062,
            ca_theme_var,
            *themes_list,
            command=lambda event: update_theme_color(),
        )
        ca_theme_table.config(width=15)

        if isDark():
            ca_theme_table.config(bg="#000", fg="#fff")
            ca_theme_table["menu"].config(bg="#000", fg="#fff")

        if isLight():
            ca_theme_table.config(bg="#fff", fg="#000")
            ca_theme_table["menu"].config(bg="#fff", fg="#000")

        ca_theme_table.grid(row=0, column=1, padx=5)

        Label(
            master=lf06,
            text="Note: Internet connection required to check MX DNS record.",
            fg="red",
            bg=accent_color_light,
        ).pack()

        ca_bottom_frame6: Frame = Frame(master=lf06, bg=accent_color_light)
        ca_bottom_frame6.pack(side=BOTTOM, pady=5, fill=X)

        ca_previous_btn6: Button = Button(
            master=ca_bottom_frame6,
            text="Previous",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=previous_ico,
            command=lambda: ca_tab_view.select(tab_id=4),
        )
        ca_previous_btn6.bind(
            sequence="<Return>",
            func=lambda event: ca_tab_view.select(tab_id=4),
        )
        ca_previous_btn6.pack(padx=10, side=LEFT)

        ca_save_btn: Button = Button(
            master=ca_bottom_frame6,
            text="Save",
            activebackground="#800000",
            bg="#C02020",
            activeforeground="#fff",
            fg="#fff",
            compound=LEFT,
            width=120,
            image=save_ico,
            command=create_configuration,
        )
        ca_save_btn.pack(padx=10, side=RIGHT)

        ca_previous_btn6.bind(sequence="<Left>", func=lambda event: ca_save_btn.focus())
        ca_previous_btn6.bind(
            sequence="<Right>", func=lambda event: ca_save_btn.focus()
        )
        ca_save_btn.bind(sequence="<Left>", func=lambda event: ca_previous_btn6.focus())
        ca_save_btn.bind(
            sequence="<Right>", func=lambda event: ca_previous_btn6.focus()
        )

        Label(
            master=ca,
            text="Created by FOSS Kingdom / Made with Love in Incredible India.",
            bg="#000",
            fg="#fff",
        ).pack(side=BOTTOM, fill=X)

        ca.deiconify()

        delta_time: float = time() - t0
        elapsed_time: float = elapsed_time + delta_time

        ca.mainloop()

    t0: float = time()

    ####################################################################################################################

    print(F_GREEN + "[INFO]\tReading configuration file, Please wait...")
    config.read(filenames=config_file_path)

    shop_name: str = config.get(section="userprofile", option="business_name").upper()
    shop_contact: str = config.get(section="userprofile", option="phone").replace(
        " ", str()
    )
    country: str = config.get(section="userprofile", option="country")
    current_theme: str = config.get(section="options", option="theme")

    ####################################################################################################################

    selected_font = choice(seq=FigletFont.getFonts())
    print(F_BLUE + "=" * 80)
    print(F_RED + figlet_format(text=shop_name, font=selected_font))
    print(F_BLUE + f"Pyfiglet Font: {selected_font}")
    print(F_GREEN + S_BRIGHT + f"Hello {whoami.title()}, Welcome to {shop_name}!")
    print(
        F_GREEN
        + S_BRIGHT
        + "Created by FOSS Kingdom / Made with Love in Incredible India."
    )
    print(F_BLUE + "=" * 80)

    ####################################################################################################################

    sa: ThemedTk = ThemedTk(theme="blue")
    sa.attributes("-topmost", True)
    sa.withdraw()
    sa.iconphoto(False, TkPhotoImage(file=join(BASE_PATH, "assets/padlock.png")))
    sa.resizable(width=False, height=False)
    sa.title(string="Security Authentication!")
    sa.protocol(name="WM_DELETE_WINDOW", func=exit_sa)
    sa.bind(sequence="<Control-Q>", func=lambda event: exit_sa())
    sa.bind(sequence="<Control-q>", func=lambda event: exit_sa())
    sa.bind(sequence="<Escape>", func=lambda event: exit_sa())

    Label(
        master=sa,
        text=f"Hello {whoami.title()}, Welcome to {shop_name}!",
        bg="#000",
        fg="#fff",
    ).pack(side=TOP, fill=X)

    sa_passwd_var: StringVar = StringVar()

    sa_frame1: Frame = Frame(master=sa)
    sa_frame1.pack(pady=10)

    sa_passwd_lbl: Label = Label(
        master=sa_frame1,
        text="Please enter your password:",
    )
    sa_passwd_lbl.grid(row=0, column=0, padx=10)

    sa_passwd_entry: Entry = Entry(
        master=sa_frame1,
        width=25,
        textvariable=sa_passwd_var,
        selectbackground="orange",
        show="*",
    )
    sa_passwd_entry.bind(sequence="<Return>", func=lambda event: check_root_passwd())
    sa_passwd_entry.grid(row=0, column=1, padx=10)
    sa_passwd_entry.focus()

    sa_frame2: Frame = Frame(master=sa)
    sa_frame2.pack(pady=10)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/enter.png")).resize(size=(20, 20))
    login_ico: PhotoImage = PhotoImage(image=_)
    sa_login_btn: Button = Button(
        master=sa_frame2,
        text="Login",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        image=login_ico,
        command=check_root_passwd,
    )
    sa_login_btn.bind(sequence="<Return>", func=lambda event: check_root_passwd())
    sa_login_btn.grid(row=0, column=0, padx=10)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/logout.png")).resize(size=(20, 20))
    exit_ico: PhotoImage = PhotoImage(image=_)
    sa_exit_btn: Button = Button(
        master=sa_frame2,
        text="Exit",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        image=exit_ico,
        command=exit_sa,
    )
    sa_exit_btn.bind(sequence="<Return>", func=lambda event: exit_sa())
    sa_exit_btn.grid(row=0, column=1, padx=10)

    sa_login_btn.bind(sequence="<Left>", func=lambda event: sa_exit_btn.focus())
    sa_login_btn.bind(sequence="<Right>", func=lambda event: sa_exit_btn.focus())
    sa_login_btn.bind(sequence="<Up>", func=lambda event: sa_passwd_entry.focus())
    sa_exit_btn.bind(sequence="<Left>", func=lambda event: sa_login_btn.focus())
    sa_exit_btn.bind(sequence="<Right>", func=lambda event: sa_login_btn.focus())
    sa_exit_btn.bind(sequence="<Up>", func=lambda event: sa_passwd_entry.focus())

    vklf: LabelFrame = LabelFrame(master=sa, text="Virtual Keyboard", fg="red")
    vklf.pack(padx=10, pady=10)

    vkf1: Frame = Frame(master=vklf)
    vkf1.grid(row=0, column=0, padx=5, pady=1)

    vkf2: Frame = Frame(master=vklf)
    vkf2.grid(row=1, column=0, padx=5, pady=1)

    vkf3: Frame = Frame(master=vklf)
    vkf3.grid(row=2, column=0, padx=5, pady=1)

    vkf4: Frame = Frame(master=vklf)
    vkf4.grid(row=3, column=0, padx=5, pady=1)

    vkf5: Frame = Frame(master=vklf)
    vkf5.grid(row=4, column=0, padx=5, pady=1)

    vkf6: Frame = Frame(master=vklf)
    vkf6.grid(row=5, column=0, padx=5, pady=1)

    spc_char_btn1: TTK_Button = TTK_Button(
        master=vkf1, text="`", width=2, command=lambda: virtual_keyboard_entry(key="`")
    )
    spc_char_btn1.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="`")
    )
    spc_char_btn1.grid(row=0, column=0, padx=1)

    spc_char_btn2: TTK_Button = TTK_Button(
        master=vkf1, text="!", width=2, command=lambda: virtual_keyboard_entry(key="!")
    )
    spc_char_btn2.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="!")
    )
    spc_char_btn2.grid(row=0, column=1, padx=1)

    spc_char_btn3: TTK_Button = TTK_Button(
        master=vkf1, text="@", width=2, command=lambda: virtual_keyboard_entry(key="@")
    )
    spc_char_btn3.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="@")
    )
    spc_char_btn3.grid(row=0, column=2, padx=1)

    spc_char_btn4: TTK_Button = TTK_Button(
        master=vkf1, text="#", width=2, command=lambda: virtual_keyboard_entry(key="#")
    )
    spc_char_btn4.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="#")
    )
    spc_char_btn4.grid(row=0, column=3, padx=1)

    spc_char_btn5: TTK_Button = TTK_Button(
        master=vkf1, text="$", width=2, command=lambda: virtual_keyboard_entry(key="$")
    )
    spc_char_btn5.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="$")
    )
    spc_char_btn5.grid(row=0, column=4, padx=1)

    spc_char_btn6: TTK_Button = TTK_Button(
        master=vkf1, text="%", width=2, command=lambda: virtual_keyboard_entry(key="%")
    )
    spc_char_btn6.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="%")
    )
    spc_char_btn6.grid(row=0, column=5, padx=1)

    spc_char_btn7: TTK_Button = TTK_Button(
        master=vkf1, text="^", width=2, command=lambda: virtual_keyboard_entry(key="^")
    )
    spc_char_btn7.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="^")
    )
    spc_char_btn7.grid(row=0, column=6, padx=1)

    spc_char_btn8: TTK_Button = TTK_Button(
        master=vkf1, text="&", width=2, command=lambda: virtual_keyboard_entry(key="&")
    )
    spc_char_btn8.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="&")
    )
    spc_char_btn8.grid(row=0, column=7, padx=1)

    spc_char_btn9: TTK_Button = TTK_Button(
        master=vkf1, text="*", width=2, command=lambda: virtual_keyboard_entry(key="*")
    )
    spc_char_btn9.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="*")
    )
    spc_char_btn9.grid(row=0, column=8, padx=1)

    spc_char_btn10: TTK_Button = TTK_Button(
        master=vkf1, text="(", width=2, command=lambda: virtual_keyboard_entry(key="(")
    )
    spc_char_btn10.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="(")
    )
    spc_char_btn10.grid(row=0, column=9, padx=1)

    spc_char_btn11: TTK_Button = TTK_Button(
        master=vkf1, text=")", width=2, command=lambda: virtual_keyboard_entry(key=")")
    )
    spc_char_btn11.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=")")
    )
    spc_char_btn11.grid(row=0, column=10, padx=1)

    spc_char_btn12: TTK_Button = TTK_Button(
        master=vkf1, text="-", width=2, command=lambda: virtual_keyboard_entry(key="-")
    )
    spc_char_btn12.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="-")
    )
    spc_char_btn12.grid(row=0, column=11, padx=1)

    spc_char_btn13: TTK_Button = TTK_Button(
        master=vkf1, text="=", width=2, command=lambda: virtual_keyboard_entry(key="=")
    )
    spc_char_btn13.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="=")
    )
    spc_char_btn13.grid(row=0, column=12, padx=1)

    spc_char_btn14: TTK_Button = TTK_Button(
        master=vkf1, text="[", width=2, command=lambda: virtual_keyboard_entry(key="[")
    )
    spc_char_btn14.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="[")
    )
    spc_char_btn14.grid(row=0, column=13, padx=1)

    spc_char_btn15: TTK_Button = TTK_Button(
        master=vkf1, text="]", width=2, command=lambda: virtual_keyboard_entry(key="]")
    )
    spc_char_btn15.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="]")
    )
    spc_char_btn15.grid(row=0, column=14, padx=1)

    spc_char_btn16: TTK_Button = TTK_Button(
        master=vkf1,
        text="\\",
        width=2,
        command=lambda: virtual_keyboard_entry(key="\\"),
    )
    spc_char_btn16.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="\\")
    )
    spc_char_btn16.grid(row=0, column=15, padx=1)

    spc_char_btn17: TTK_Button = TTK_Button(
        master=vkf1, text=";", width=2, command=lambda: virtual_keyboard_entry(key=";")
    )
    spc_char_btn17.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=";")
    )
    spc_char_btn17.grid(row=1, column=0, padx=1)

    spc_char_btn18: TTK_Button = TTK_Button(
        master=vkf1, text="'", width=2, command=lambda: virtual_keyboard_entry(key="'")
    )
    spc_char_btn18.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="'")
    )
    spc_char_btn18.grid(row=1, column=1, padx=1)

    spc_char_btn19: TTK_Button = TTK_Button(
        master=vkf1, text=",", width=2, command=lambda: virtual_keyboard_entry(key=",")
    )
    spc_char_btn19.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=",")
    )
    spc_char_btn19.grid(row=1, column=2, padx=1)

    spc_char_btn20: TTK_Button = TTK_Button(
        master=vkf1, text=".", width=2, command=lambda: virtual_keyboard_entry(key=".")
    )
    spc_char_btn20.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=".")
    )
    spc_char_btn20.grid(row=1, column=3, padx=1)

    spc_char_btn21: TTK_Button = TTK_Button(
        master=vkf1, text="/", width=2, command=lambda: virtual_keyboard_entry(key="/")
    )
    spc_char_btn21.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="/")
    )
    spc_char_btn21.grid(row=1, column=4, padx=1)

    spc_char_btn22: TTK_Button = TTK_Button(
        master=vkf1, text="~", width=2, command=lambda: virtual_keyboard_entry(key="~")
    )
    spc_char_btn22.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="~")
    )
    spc_char_btn22.grid(row=1, column=5, padx=1)

    spc_char_btn23: TTK_Button = TTK_Button(
        master=vkf1, text="_", width=2, command=lambda: virtual_keyboard_entry(key="_")
    )
    spc_char_btn23.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="_")
    )
    spc_char_btn23.grid(row=1, column=6, padx=1)

    spc_char_btn24: TTK_Button = TTK_Button(
        master=vkf1, text="+", width=2, command=lambda: virtual_keyboard_entry(key="+")
    )
    spc_char_btn24.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="+")
    )
    spc_char_btn24.grid(row=1, column=7, padx=1)

    spc_char_btn25: TTK_Button = TTK_Button(
        master=vkf1, text="{", width=2, command=lambda: virtual_keyboard_entry(key="{")
    )
    spc_char_btn25.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="{")
    )
    spc_char_btn25.grid(row=1, column=8, padx=1)

    spc_char_btn26: TTK_Button = TTK_Button(
        master=vkf1, text="}", width=2, command=lambda: virtual_keyboard_entry(key="}")
    )
    spc_char_btn26.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="}")
    )
    spc_char_btn26.grid(row=1, column=9, padx=1)

    spc_char_btn27: TTK_Button = TTK_Button(
        master=vkf1, text="|", width=2, command=lambda: virtual_keyboard_entry(key="|")
    )
    spc_char_btn27.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="|")
    )
    spc_char_btn27.grid(row=1, column=10, padx=1)

    spc_char_btn28: TTK_Button = TTK_Button(
        master=vkf1, text=":", width=2, command=lambda: virtual_keyboard_entry(key=":")
    )
    spc_char_btn28.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=":")
    )
    spc_char_btn28.grid(row=1, column=11, padx=1)

    spc_char_btn29: TTK_Button = TTK_Button(
        master=vkf1, text='"', width=2, command=lambda: virtual_keyboard_entry(key='"')
    )
    spc_char_btn29.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key='"')
    )
    spc_char_btn29.grid(row=1, column=12, padx=1)

    spc_char_btn30: TTK_Button = TTK_Button(
        master=vkf1, text="<", width=2, command=lambda: virtual_keyboard_entry(key="<")
    )
    spc_char_btn30.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="<")
    )
    spc_char_btn30.grid(row=1, column=13, padx=1)

    spc_char_btn31: TTK_Button = TTK_Button(
        master=vkf1, text=">", width=2, command=lambda: virtual_keyboard_entry(key=">")
    )
    spc_char_btn31.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key=">")
    )
    spc_char_btn31.grid(row=1, column=14, padx=1)

    spc_char_btn32: TTK_Button = TTK_Button(
        master=vkf1, text="?", width=2, command=lambda: virtual_keyboard_entry(key="?")
    )
    spc_char_btn32.bind(
        sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="?")
    )
    spc_char_btn32.grid(row=1, column=15, padx=1)

    btn_1: TTK_Button = TTK_Button(
        master=vkf2, text="1", width=2, command=lambda: virtual_keyboard_entry(key="1")
    )
    btn_1.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="1"))
    btn_1.grid(row=0, column=0, padx=1)

    btn2: TTK_Button = TTK_Button(
        master=vkf2, text="2", width=2, command=lambda: virtual_keyboard_entry(key="2")
    )
    btn2.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="2"))
    btn2.grid(row=0, column=1, padx=1)

    btn_3: TTK_Button = TTK_Button(
        master=vkf2, text="3", width=2, command=lambda: virtual_keyboard_entry(key="3")
    )
    btn_3.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="3"))
    btn_3.grid(row=0, column=2, padx=1)

    btn_4: TTK_Button = TTK_Button(
        master=vkf2, text="4", width=2, command=lambda: virtual_keyboard_entry(key="4")
    )
    btn_4.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="4"))
    btn_4.grid(row=0, column=3, padx=1)

    btn_5: TTK_Button = TTK_Button(
        master=vkf2, text="5", width=2, command=lambda: virtual_keyboard_entry(key="5")
    )
    btn_5.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="5"))
    btn_5.grid(row=0, column=4, padx=1)

    btn_6: TTK_Button = TTK_Button(
        master=vkf2, text="6", width=2, command=lambda: virtual_keyboard_entry(key="6")
    )
    btn_6.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="6"))
    btn_6.grid(row=0, column=5, padx=1)

    btn_7: TTK_Button = TTK_Button(
        master=vkf2, text="7", width=2, command=lambda: virtual_keyboard_entry(key="7")
    )
    btn_7.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="7"))
    btn_7.grid(row=0, column=6, padx=1)

    btn_8: TTK_Button = TTK_Button(
        master=vkf2, text="8", width=2, command=lambda: virtual_keyboard_entry(key="8")
    )
    btn_8.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="8"))
    btn_8.grid(row=0, column=7, padx=1)

    btn_9: TTK_Button = TTK_Button(
        master=vkf2, text="9", width=2, command=lambda: virtual_keyboard_entry(key="9")
    )
    btn_9.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="9"))
    btn_9.grid(row=0, column=8, padx=1)

    btn_0: TTK_Button = TTK_Button(
        master=vkf2, text="0", width=2, command=lambda: virtual_keyboard_entry(key="0")
    )
    btn_0.bind(sequence="<Return>", func=lambda event: virtual_keyboard_entry(key="0"))
    btn_0.grid(row=0, column=9, padx=1)

    q_btn: TTK_Button = TTK_Button(
        master=vkf3, text="Q", width=2, command=lambda: virtual_keyboard_entry(key="Q")
    )
    q_btn.grid(row=0, column=0, padx=1)

    w_btn: TTK_Button = TTK_Button(
        master=vkf3, text="W", width=2, command=lambda: virtual_keyboard_entry(key="W")
    )
    w_btn.grid(row=0, column=1, padx=1)

    e_btn: TTK_Button = TTK_Button(
        master=vkf3, text="E", width=2, command=lambda: virtual_keyboard_entry(key="E")
    )
    e_btn.grid(row=0, column=2, padx=1)

    r_btn: TTK_Button = TTK_Button(
        master=vkf3, text="R", width=2, command=lambda: virtual_keyboard_entry(key="R")
    )
    r_btn.grid(row=0, column=3, padx=1)

    t_btn: TTK_Button = TTK_Button(
        master=vkf3, text="T", width=2, command=lambda: virtual_keyboard_entry(key="T")
    )
    t_btn.grid(row=0, column=4, padx=1)

    y_btn: TTK_Button = TTK_Button(
        master=vkf3, text="Y", width=2, command=lambda: virtual_keyboard_entry(key="Y")
    )
    y_btn.grid(row=0, column=5, padx=1)

    u_btn: TTK_Button = TTK_Button(
        master=vkf3, text="U", width=2, command=lambda: virtual_keyboard_entry(key="U")
    )
    u_btn.grid(row=0, column=6, padx=1)

    i_btn: TTK_Button = TTK_Button(
        master=vkf3, text="I", width=2, command=lambda: virtual_keyboard_entry(key="I")
    )
    i_btn.grid(row=0, column=7, padx=1)

    o_btn: TTK_Button = TTK_Button(
        master=vkf3, text="O", width=2, command=lambda: virtual_keyboard_entry(key="O")
    )
    o_btn.grid(row=0, column=8, padx=1)

    p_btn: TTK_Button = TTK_Button(
        master=vkf3, text="P", width=2, command=lambda: virtual_keyboard_entry(key="P")
    )
    p_btn.grid(row=0, column=9, padx=1)

    a_btn: TTK_Button = TTK_Button(
        master=vkf4, text="A", width=2, command=lambda: virtual_keyboard_entry(key="A")
    )
    a_btn.grid(row=0, column=0, padx=1)

    s_btn: TTK_Button = TTK_Button(
        master=vkf4, text="S", width=2, command=lambda: virtual_keyboard_entry(key="S")
    )
    s_btn.grid(row=0, column=1, padx=1)

    d_btn: TTK_Button = TTK_Button(
        master=vkf4, text="D", width=2, command=lambda: virtual_keyboard_entry(key="D")
    )
    d_btn.grid(row=0, column=2, padx=1)

    f_btn: TTK_Button = TTK_Button(
        master=vkf4, text="F", width=2, command=lambda: virtual_keyboard_entry(key="F")
    )
    f_btn.grid(row=0, column=3, padx=1)

    g_btn: TTK_Button = TTK_Button(
        master=vkf4, text="G", width=2, command=lambda: virtual_keyboard_entry(key="G")
    )
    g_btn.grid(row=0, column=4, padx=1)

    h_btn: TTK_Button = TTK_Button(
        master=vkf4, text="H", width=2, command=lambda: virtual_keyboard_entry(key="H")
    )
    h_btn.grid(row=0, column=5, padx=1)

    j_btn: TTK_Button = TTK_Button(
        master=vkf4, text="J", width=2, command=lambda: virtual_keyboard_entry(key="J")
    )
    j_btn.grid(row=0, column=6, padx=1)

    k_btn: TTK_Button = TTK_Button(
        master=vkf4, text="K", width=2, command=lambda: virtual_keyboard_entry(key="K")
    )
    k_btn.grid(row=0, column=7, padx=1)

    l_btn: TTK_Button = TTK_Button(
        master=vkf4, text="L", width=2, command=lambda: virtual_keyboard_entry(key="L")
    )
    l_btn.grid(row=0, column=8, padx=1)

    z_btn: TTK_Button = TTK_Button(
        master=vkf5, text="Z", width=2, command=lambda: virtual_keyboard_entry(key="Z")
    )
    z_btn.grid(row=0, column=0, padx=1)

    x_btn: TTK_Button = TTK_Button(
        master=vkf5, text="X", width=2, command=lambda: virtual_keyboard_entry(key="X")
    )
    x_btn.grid(row=0, column=1, padx=1)

    c_btn: TTK_Button = TTK_Button(
        master=vkf5, text="C", width=2, command=lambda: virtual_keyboard_entry(key="C")
    )
    c_btn.grid(row=0, column=2, padx=1)

    v_btn: TTK_Button = TTK_Button(
        master=vkf5, text="V", width=2, command=lambda: virtual_keyboard_entry(key="V")
    )
    v_btn.grid(row=0, column=3, padx=1)

    b_btn: TTK_Button = TTK_Button(
        master=vkf5, text="B", width=2, command=lambda: virtual_keyboard_entry(key="B")
    )
    b_btn.grid(row=0, column=4, padx=1)

    n_btn: TTK_Button = TTK_Button(
        master=vkf5, text="N", width=2, command=lambda: virtual_keyboard_entry(key="N")
    )
    n_btn.grid(row=0, column=5, padx=1)

    m_btn: TTK_Button = TTK_Button(
        master=vkf5, text="M", width=2, command=lambda: virtual_keyboard_entry(key="M")
    )
    m_btn.grid(row=0, column=6, padx=1)

    esc_btn: TTK_Button = TTK_Button(master=vkf6, text="Escape", command=exit_sa)
    esc_btn.grid(row=0, column=0, padx=1)

    caps_lock_state: BooleanVar = BooleanVar()
    caps_lock_state.set(value=True)

    caps_lock_btn: TTK_Button = TTK_Button(
        master=vkf6, text="Caps Lock ON", width=12, command=configure_caps_lock
    )
    caps_lock_btn.grid(row=0, column=1, padx=1)

    spacebar_btn: TTK_Button = TTK_Button(
        master=vkf6, text="Spacebar", command=lambda: virtual_keyboard_entry(key=" ")
    )
    spacebar_btn.grid(row=0, column=2, padx=1)

    backspace_btn: TTK_Button = TTK_Button(
        master=vkf6, text="Backspace", command=virtual_keyboard_backspace
    )
    backspace_btn.grid(row=0, column=3, padx=1)

    del_btn: TTK_Button = TTK_Button(
        master=vkf6, text="Delete", command=virtual_keyboard_delete
    )
    del_btn.grid(row=0, column=4, padx=1)

    enter_btn: TTK_Button = TTK_Button(
        master=vkf6, text="Enter", command=check_root_passwd
    )
    enter_btn.grid(row=0, column=5, padx=1)

    Label(
        master=sa,
        text="Created by FOSS Kingdom / Made with Love in Incredible India.",
        bg="#000",
        fg="#fff",
    ).pack(fill=X, side=BOTTOM)

    delta_time: float = time() - t0
    elapsed_time: float = elapsed_time + delta_time

    if current_theme == "light" or (current_theme == "system_default" and isLight()):
        sa.config(bg=accent_color_light)
        sa_frame1.config(bg=accent_color_light)
        sa_passwd_lbl.config(bg=accent_color_light, fg="#000")
        sa_passwd_entry.config(bg="#fff", fg="#000", insertbackground="#000")
        sa_frame2.config(bg=accent_color_light)
        sa_login_btn.config(bg="#20C020", activebackground="green")
        sa_exit_btn.config(bg="#C02020", activebackground="#800000")
        vklf.config(bg=accent_color_light)
        vkf1.config(bg=accent_color_light)
        vkf2.config(bg=accent_color_light)
        vkf3.config(bg=accent_color_light)
        vkf4.config(bg=accent_color_light)
        vkf5.config(bg=accent_color_light)
        vkf6.config(bg=accent_color_light)

    elif current_theme == "dark" or (current_theme == "system_default" and isDark()):
        sa.config(bg=accent_color_dark)
        sa_frame1.config(bg=accent_color_dark)
        sa_passwd_lbl.config(bg=accent_color_dark, fg="#fff")
        sa_passwd_entry.config(bg="#2A3459", fg="#fff", insertbackground="red")
        sa_frame2.config(bg=accent_color_dark)
        sa_login_btn.config(activebackground="#20C020", bg="green")
        sa_exit_btn.config(activebackground="#C02020", bg="#800000")
        vklf.config(bg=accent_color_dark)
        vkf1.config(bg=accent_color_dark)
        vkf2.config(bg=accent_color_dark)
        vkf3.config(bg=accent_color_dark)
        vkf4.config(bg=accent_color_dark)
        vkf5.config(bg=accent_color_dark)
        vkf6.config(bg=accent_color_dark)

    sa.deiconify()
    sa.mainloop()

    ####################################################################################################################

    merchant_website: str = config.get(section="userprofile", option="business_website")

    smtp_email: str = config.get(section="smtp_server", option="email")

    try:
        smtp_passwd: str = decrypt_smtp_passwd(
            token=config.get(section="smtp_server", option="password"),
            key_path=private_key_path,
        )

    except InvalidToken as invalid_token:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: private.InvalidToken")
        print(F_RED + f"[ERROR]\tInvalidToken: {invalid_token}")
        print(F_BLUE + "=" * 80)

        showinfo(
            title=f"TailorMate {__version__}", message=f"InvalidToken: {invalid_token}"
        )

        clean_cache()

        print(F_RED + "Bye...")

        clrscr()
        terminate()

    except ValueError as value_error:
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: ValueError")
        print(F_RED + f"[ERROR]\tValueError: {value_error}")
        print(F_BLUE + "=" * 80)

        showinfo(
            title=f"TailorMate {__version__}", message=f"ValueError: {value_error}"
        )

        clean_cache()

        print(F_RED + "Bye...")

        clrscr()
        terminate()

    ####################################################################################################################

    t0: float = time()

    print(F_GREEN + "[INFO]\tCreating GUI application...")
    tm: Tk = Tk()
    tm.withdraw()

    tm.iconphoto(False, TkPhotoImage(file=join(BASE_PATH, "assets/sewing.png")))
    tm.resizable(width=True, height=True)
    tm.title(string=shop_name + "!")
    tm.protocol(name="WM_DELETE_WINDOW", func=exit_app)
    tm.bind(sequence="<Control-Q>", func=lambda event: exit_app())
    tm.bind(sequence="<Control-q>", func=lambda event: exit_app())
    tm.bind(sequence="<Escape>", func=lambda event: exit_app())

    tm.bind(sequence="<Control-N>", func=lambda event: navigate_create_customer())
    tm.bind(sequence="<Control-n>", func=lambda event: navigate_create_customer())

    tm.bind(sequence="<Control-F>", func=lambda event: navigate_search_customer())
    tm.bind(sequence="<Control-f>", func=lambda event: navigate_search_customer())

    tree_style: TkStyle = TkStyle(master=tm)

    search_var: StringVar = StringVar()
    name_var1: StringVar = StringVar()
    name_var2: StringVar = StringVar()
    ph_var1: StringVar = StringVar()
    ph_var2: StringVar = StringVar()
    email_var1: StringVar = StringVar()
    email_var2: StringVar = StringVar()
    gender_var: StringVar = StringVar()
    gender_var.set(value=gender_options[0])
    stitch_var: IntVar = IntVar()
    cost_var: DoubleVar = DoubleVar()
    cost_var.set(value=0.0)
    priority_var: BooleanVar = BooleanVar()
    priority_var.set(value=False)
    weeks_number_var: BooleanVar = BooleanVar()
    weeks_number_var.set(
        value=config.getboolean(section="options", option="weeks_number")
    )
    other_month_days_var: BooleanVar = BooleanVar()
    other_month_days_var.set(
        value=config.getboolean(section="options", option="other_month_days")
    )
    tm_bell_var: BooleanVar = BooleanVar()
    tm_bell_var.set(value=config.getboolean(section="options", option="play_sound"))
    theme_var: StringVar = StringVar()
    theme_var.set(value=current_theme)
    mxdns_var: BooleanVar = BooleanVar()
    mxdns_var.set(
        value=config.getboolean(section="options", option="check_mxdns_record")
    )

    _: Image = Image.open(fp=join(BASE_PATH, "assets/logout.png")).resize(size=(20, 20))
    exit_ico: PhotoImage = PhotoImage(image=_)

    # Creating and configure main menu
    menubar: Menu = Menu(master=tm)
    tm.config(menu=menubar)

    # Creating file menu
    file_menu: Menu = Menu(master=menubar, tearoff=False)
    file_menu.add_command(
        label="Add New Customer", accelerator="Ctrl+N", command=navigate_create_customer
    )
    file_menu.add_command(
        label="Search Existing Customer",
        accelerator="Ctrl+F",
        command=navigate_search_customer,
    )
    file_menu.add_separator()

    menubar.add_cascade(label="File", menu=file_menu)

    # Creating options menu
    options_menu: Menu = Menu(master=menubar, tearoff=False)

    # Creating calendar menu under options menu
    calendar_menu: Menu = Menu(master=options_menu, tearoff=False)

    calendar_menu.add_checkbutton(
        label="Show Weeks number",
        onvalue=True,
        offvalue=False,
        variable=weeks_number_var,
        command=update_weeknumbers_setting,
    )
    calendar_menu.add_checkbutton(
        label="Show Other Month Days",
        onvalue=True,
        offvalue=False,
        variable=other_month_days_var,
        command=update_othermonthdays_settings,
    )

    options_menu.add_cascade(label="Calendar Preference", menu=calendar_menu)

    settings_menu: Menu = Menu(master=options_menu, tearoff=False)

    settings_menu.add_checkbutton(
        label="Play Alert Sound",
        onvalue=True,
        offvalue=False,
        variable=tm_bell_var,
        command=lambda: update_configuration(
            section="options", option="play_sound", value=str(tm_bell_var.get())
        ),
    )

    settings_menu.add_checkbutton(
        label="Check MX-DNS Record",
        onvalue=True,
        offvalue=False,
        variable=mxdns_var,
        command=lambda: update_configuration(
            section="options", option="check_mxdns_record", value=str(mxdns_var.get())
        ),
    )

    options_menu.add_cascade(label="Settings Preference", menu=settings_menu)

    # Creating theme menu under options menu
    theme_menu: Menu = Menu(master=options_menu, tearoff=False)

    theme_menu.add_radiobutton(
        label=themes_list[0],
        value="light",
        variable=theme_var,
        command=configure_theme_color,
    )
    theme_menu.add_radiobutton(
        label=themes_list[1],
        value="dark",
        variable=theme_var,
        command=configure_theme_color,
    )
    theme_menu.add_radiobutton(
        label=themes_list[2],
        value="system_default",
        variable=theme_var,
        command=configure_theme_color,
    )

    options_menu.add_cascade(label="Theme Appearance", menu=theme_menu)

    options_menu.add_separator()
    options_menu.add_command(label="Get App Size", command=get_resolution_size)

    menubar.add_cascade(label="Options", menu=options_menu)

    # Creating links menu
    links_menu: Menu = Menu(master=menubar, tearoff=False)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/license.png")).resize(
        size=(20, 20)
    )
    licence_ico: PhotoImage = PhotoImage(image=_)
    links_menu.add_command(
        label="Licence GPL-v3.0",
        command=not_ready_yet,
        image=licence_ico,
        compound=LEFT,
    )

    _: Image = Image.open(fp=join(BASE_PATH, "assets/programming.png")).resize(
        size=(20, 20)
    )
    source_code_ico: PhotoImage = PhotoImage(image=_)
    links_menu.add_command(
        label="Source Code",
        command=lambda: browser(url="https://github.com/JahidFariz/TailorMate"),
        image=source_code_ico,
        compound=LEFT,
    )

    _: Image = Image.open(fp=join(BASE_PATH, "assets/bug-report.png")).resize(
        size=(20, 20)
    )
    bug_report_ico: PhotoImage = PhotoImage(image=_)
    links_menu.add_command(
        label="Issues",
        command=lambda: browser(url="https://github.com/JahidFariz/TailorMate/issues"),
        image=bug_report_ico,
        compound=LEFT,
    )

    _: Image = Image.open(fp=join(BASE_PATH, "assets/web-link.png")).resize(
        size=(20, 20)
    )
    website_ico: PhotoImage = PhotoImage(image=_)
    links_menu.add_command(
        label="Website",
        command=lambda: browser(url="https://jahidfariz.github.io/"),
        image=website_ico,
        compound=LEFT,
    )

    menubar.add_cascade(label="Links", menu=links_menu)

    # Creating Help menu
    _: Image = Image.open(fp=stain_solutions_ico_path).resize(size=(20, 20))
    stain_solutions_ico: PhotoImage = PhotoImage(image=_)
    help_menu: Menu = Menu(master=menubar, tearoff=False)
    help_menu.add_command(
        label="Stain Solutions",
        command=stain_solutions,
        compound=LEFT,
        image=stain_solutions_ico,
    )

    _: Image = Image.open(fp=donation_ico_path).resize(size=(20, 20))
    donation_ico: PhotoImage = PhotoImage(image=_)
    help_menu.add_command(
        label="Donate Us", command=donation_page, image=donation_ico, compound=LEFT
    )
    help_menu.add_separator()
    help_menu.add_command(label="About TailorMate", command=not_ready_yet)

    menubar.add_cascade(label="Help", menu=help_menu)

    Label(
        master=tm,
        text=f"Hello {whoami.title()}, Welcome to {shop_name}!",
        bg="#000",
        fg="#fff",
    ).pack(side=TOP, fill=X)

    # https://www.un.org/en/observances/international-days-and-weeks
    if today.month == 1 and today.day == 1:
        Label(master=tm, text="New Year's Day.", bg="yellow").pack(fill=X)

    elif today.month == 1 and today.day == 4:
        Label(master=tm, text="Today is World Braille Day.", bg="yellow").pack(fill=X)

    elif today.month == 1 and today.day == 24:
        Label(
            master=tm,
            text="Today is International Day of Education.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 2 and today.day == 2:
        Label(master=tm, text="Today is World Wetlands Day.", bg="yellow").pack(fill=X)

    elif today.month == 2 and today.day == 10:
        Label(master=tm, text="Today is World Pulses Day.", bg="yellow").pack(fill=X)

    elif today.month == 2 and today.day == 11:
        Label(
            master=tm,
            text="Today is International Day of Women and Girls in Science.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 2 and today.day == 13:
        Label(master=tm, text="Today is World Radio Day.", bg="yellow").pack(fill=X)

    elif today.month == 2 and today.day == 14:
        Label(master=tm, text="Happy Valentine's Day.", bg="yellow").pack(fill=X)

    elif today.month == 2 and today.day == 20:
        Label(
            master=tm, text="Today is World Day of Social Justice.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 2 and today.day == 21:
        Label(
            master=tm,
            text="Today is International Mother Language Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 3 and today.month == 3:
        Label(master=tm, text="Today is World Wildlife Day.", bg="yellow").pack(fill=X)

    elif today.month == 3 and today.day == 8:
        Label(master=tm, text="Today is International Women's Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 3 and today.day == 10:
        Label(
            master=tm,
            text="Today is International Day of Women Judges.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 3 and today.day == 21:
        Label(
            master=tm, text="Today is International Day of Forests.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 3 and today.day == 22:
        Label(master=tm, text="Today is World Water Day.", bg="yellow").pack(fill=X)

    elif today.month == 3 and today.day == 23:
        Label(master=tm, text="Today is World Meteorological Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 3 and today.day == 24:
        Label(master=tm, text="Today is World Tuberculosis Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 4 and today.day == 2:
        Label(master=tm, text="Today is World Autism Awareness Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 4 and today.day == 5:
        Label(
            master=tm,
            text="Today is International Day of Conscience.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 4 and today.day == 6:
        Label(
            master=tm,
            text="Today is International Day of Sports for Development and Peace.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 4 and today.day == 7:
        Label(master=tm, text="Today is World Health Day.", bg="yellow").pack(fill=X)

    elif today.month == 4 and today.day == 12:
        Label(
            master=tm,
            text="Today is International Day of Human Space Flight.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 4 and today.day == 21:
        Label(
            master=tm,
            text="Today is World Creativity and Innovation Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 4 and today.day == 22:
        Label(
            master=tm,
            text="Today is International Mother Earth Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 4 and today.day == 25:
        Label(master=tm, text="Today is World Malaria Day.", bg="yellow").pack(fill=X)

    elif today.month == 4 and today.day == 30:
        Label(master=tm, text="Today is International Jazz Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 1:
        Label(master=tm, text="Today is International Worker's Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 2:
        Label(master=tm, text="Today is World Tuna Day.", bg="yellow").pack(fill=X)

    elif today.month == 5 and today.day == 3:
        Label(master=tm, text="Today is World Press Freedom Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 10:
        Label(
            master=tm, text="Today is International Day of Argania.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 5 and today.day == 12:
        Label(
            master=tm,
            text="Today is International Day of Plant Health.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 5 and today.day == 14:
        Label(master=tm, text="Today is World Migratory Bird Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 15:
        Label(
            master=tm, text="Today is International Day of Families.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 5 and today.day == 16:
        Label(master=tm, text="Today is International Day of Light.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 17:
        Label(
            master=tm,
            text="Today is International Day of Telecommunication and Information Society Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 5 and today.day == 20:
        Label(master=tm, text="Today is World Bee Day.", bg="yellow").pack(fill=X)

    elif today.month == 5 and today.day == 21:
        Label(master=tm, text="Today is International Tea Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 5 and today.day == 22:
        Label(
            master=tm,
            text="Today is International Day for Biological Diversity.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 5 and today.day == 23:
        Label(
            master=tm,
            text="Today is International Day to End Obstetric Fistula.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 5 and today.day == 29:
        Label(
            master=tm,
            text="Today is International Day of UN Peacekeepers.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 5 and today.day == 31:
        Label(master=tm, text="Today is World No-Tobacco Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 1:
        Label(
            master=tm, text="Today is World Global Day of Parents.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 6 and today.day == 3:
        Label(master=tm, text="Today is World Bicycle Day.", bg="yellow").pack(fill=X)

    elif today.month == 6 and today.day == 4:
        Label(
            master=tm,
            text="Today is International Day of Innocent Children Victims of Aggression.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 5:
        Label(master=tm, text="Today is World Environment Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 6:
        Label(master=tm, text="Today is Russian Language Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 7:
        Label(master=tm, text="Today is Russian Language Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 8:
        Label(master=tm, text="Today is World Oceans Day.", bg="yellow").pack(fill=X)

    elif today.month == 6 and today.day == 12:
        Label(
            master=tm,
            text="Today is World Day Against Child Labour.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 13:
        Label(
            master=tm,
            text="Today is International Albinism Awareness Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 14:
        Label(master=tm, text="Today is World Blood Donor Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 15:
        Label(
            master=tm,
            text="Today is World Elder Abuse Awareness Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 16:
        Label(
            master=tm, text="Today is World Elder Abuse Awareness Day.", bg="yellow"
        ).pack(fill=X)

    elif today.month == 6 and today.day == 17:
        Label(
            master=tm,
            text="Today is World Day to Combat Desertification and Drought.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 18:
        Label(
            master=tm,
            text="Today is International Day for Countering Hate Speech.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 19:
        Label(
            master=tm,
            text="Today is International Day for the Elimination of Sexual Violence in Conflict.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 20:
        Label(master=tm, text="Today is World Refugee Day.", bg="yellow").pack(fill=X)

    elif today.month == 6 and today.day == 21:
        Label(master=tm, text="Today is International Day of Yoga.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 6 and today.day == 23:
        Label(
            master=tm,
            text="Today is United Nations Public Service Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 26:
        Label(
            master=tm,
            text="Today is International Day Against Drug Abuse and Illicit Trafficking.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 27:
        Label(
            master=tm,
            text="Today is Micro-, Small and Medium-sized Enterprise Day.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 29:
        Label(
            master=tm,
            text="Today is International Day of The Tropics.",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 6 and today.day == 30:
        Label(master=tm, text="Today is International Asteroid Day.", bg="yellow").pack(
            fill=X
        )

    # To be continued...

    elif today.month == 7 and today.day == 11:
        Label(master=tm, text="Today is World Population Day.", bg="yellow").pack(
            fill=X
        )

    elif today.month == 10 and today.day == 5:
        Label(
            master=tm,
            text="Today is Fariz's Birthday *(Founder of FOSS KINGDOM)",
            bg="yellow",
        ).pack(fill=X)

    elif today.month == 12 and today.day == 1:
        Label(master=tm, text="Today is World AIDS Day.", bg="yellow").pack(fill=X)

    elif today.month == 12 and today.day == 25:
        Label(master=tm, text="Merry Christmas.", bg="yellow").pack(fill=X)

    elif today.month == 12 and today.day == 31:
        Label(master=tm, text="Happy New Year's Eve", bg="yellow").pack(fill=X)

    main_tab_view: Notebook = Notebook(master=tm)
    main_tab_view.pack(fill=BOTH, expand=1)

    orders_frame: Frame = Frame(master=main_tab_view)
    orders_frame.pack()

    customers_frame: Frame = Frame(master=main_tab_view)
    customers_frame.pack()

    items_frame: Frame = Frame(master=main_tab_view)
    items_frame.pack()

    stats_frame: Frame = Frame(master=main_tab_view)
    stats_frame.pack()

    main_tab_view.add(child=orders_frame, text="Orders")
    main_tab_view.add(child=customers_frame, text="Customers")
    main_tab_view.add(child=items_frame, text="Items")
    main_tab_view.add(child=stats_frame, text="Stats")

    # https://mail.python.org/pipermail/tkinter-discuss/2013-September/003488.html
    tm.bind(
        sequence="<Alt-KeyPress-1>", func=lambda event: main_tab_view.select(tab_id=0)
    )
    tm.bind(
        sequence="<Alt-KeyPress-2>", func=lambda event: main_tab_view.select(tab_id=1)
    )
    tm.bind(
        sequence="<Alt-KeyPress-3>", func=lambda event: main_tab_view.select(tab_id=2)
    )
    tm.bind(
        sequence="<Alt-KeyPress-4>", func=lambda event: main_tab_view.select(tab_id=3)
    )

    # Orders tab
    greetings_lbl: Label = Label(
        master=orders_frame,
        font=("Times New Roman", 23, "bold"),
    )
    greetings_lbl.pack(pady=10)
    update_welcome_text()

    lf11: LabelFrame = LabelFrame(
        master=orders_frame,
        text="Order Database",
        fg="red",
    )
    lf11.pack(padx=10, side=TOP, fill=BOTH)

    treeview_frame1: Frame = Frame(master=lf11)
    treeview_frame1.pack(padx=15, fill=X)

    x_axis_scrollbar: Scrollbar = Scrollbar(master=treeview_frame1, orient=HORIZONTAL)
    x_axis_scrollbar.pack(side=BOTTOM, fill=X)

    y_axis_scrollbar: Scrollbar = Scrollbar(master=treeview_frame1)
    y_axis_scrollbar.pack(side=RIGHT, fill=Y)

    orders_db: Treeview = Treeview(
        master=treeview_frame1,
        show="headings",
        columns=header_list1,
        selectmode=BROWSE,
        xscrollcommand=x_axis_scrollbar.set,
        yscrollcommand=y_axis_scrollbar.set,
    )

    for _ in header_list1:
        orders_db.heading(column=_, text=_)

    orders_db.column(column=0, width=70, minwidth=70, anchor=CENTER)  # Serial Number
    orders_db.column(column=1, width=90, minwidth=90, anchor=CENTER)  # Order No
    orders_db.column(column=2, width=150, minwidth=150, anchor=W)  # Name
    orders_db.column(column=3, width=155, minwidth=155, anchor=CENTER)  # Created on
    orders_db.column(column=4, width=130, minwidth=130, anchor=CENTER)  # Phone Number
    orders_db.column(column=5, width=110, minwidth=110, anchor=CENTER)  # Item
    orders_db.column(column=6, width=130, minwidth=130, anchor=CENTER)  # Stitching type
    orders_db.column(column=7, width=80, minwidth=80, anchor=CENTER)  # Cost
    orders_db.column(column=8, width=115, minwidth=115, anchor=CENTER)  # Delivery Date
    orders_db.column(column=9, width=80, minwidth=80, anchor=CENTER)  # Priority
    orders_db.column(column=10, width=100, minwidth=100, anchor=W)  # Status

    x_axis_scrollbar.config(command=orders_db.yview)
    y_axis_scrollbar.config(command=orders_db.yview)

    orders_db.pack(fill=X)

    tot_orders_lbl: Label = Label(master=lf11, fg="red")
    tot_orders_lbl.pack()

    f11: Frame = Frame(master=lf11)
    f11.pack(pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/checked.png")).resize(
        size=(20, 20)
    )
    completed_ico: PhotoImage = PhotoImage(image=_)
    mark_as_completed_btn: Button = Button(
        master=f11,
        text="Mark as Completed",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=150,
        image=completed_ico,
        command=mark_completed,
    )
    mark_as_completed_btn.grid(row=0, column=0, padx=10)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/package-delivered.png")).resize(
        size=(20, 20)
    )
    product_delivered_ico: PhotoImage = PhotoImage(image=_)
    product_delivered_btn: Button = Button(
        master=f11,
        text="Product Delivered",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=150,
        image=product_delivered_ico,
        command=product_delivered,
    )
    product_delivered_btn.grid(row=0, column=1, padx=10)

    lf12: LabelFrame = LabelFrame(
        master=orders_frame,
        text="Add Order",
        fg="red",
    )
    lf12.pack(side=BOTTOM, padx=10, ipady=3, pady=5, fill=X)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/order.png")).resize(size=(20, 20))
    order_ico: PhotoImage = PhotoImage(image=_)
    order_btn: Button = Button(
        master=lf12,
        text="Add an Order",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        image=order_ico,
        command=add_order,
    )
    order_btn.bind(sequence="<Return>", func=lambda event: add_order())
    order_btn.grid(row=0, column=0, padx=5)

    exit_btn1: Button = Button(
        master=lf12,
        text="Exit",
        fg="#fff",
        compound=LEFT,
        activeforeground="#fff",
        width=125,
        image=exit_ico,
        command=exit_app,
    )
    exit_btn1.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_btn1.grid(row=0, column=1, padx=5)

    # Customers tab
    lf21: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Database",
        fg="red",
    )
    lf21.pack(padx=10, pady=5, side=TOP, fill=BOTH)

    lf22: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Lookup",
        fg="red",
    )
    lf22.pack(padx=10, pady=5, ipady=5, fill=BOTH)

    lf23: LabelFrame = LabelFrame(
        master=customers_frame,
        text="Customer Details",
        fg="red",
    )
    lf23.pack(padx=10, pady=5, ipady=5, fill=BOTH)

    lf24: LabelFrame = LabelFrame(
        master=customers_frame, text="Select Customer", fg="red"
    )
    lf24.pack(side=BOTTOM, padx=10, pady=5, ipady=3, fill=X)

    # Customer tab, Treeview section
    treeview_frame2: Frame = Frame(master=lf21)
    treeview_frame2.pack(padx=15, fill=X)

    x_axis_scrollbar: Scrollbar = Scrollbar(master=treeview_frame2, orient=HORIZONTAL)
    x_axis_scrollbar.pack(side=BOTTOM, fill=X)

    y_axis_scrollbar: Scrollbar = Scrollbar(master=treeview_frame2)
    y_axis_scrollbar.pack(side=RIGHT, fill=Y)

    customers_db: Treeview = Treeview(
        master=treeview_frame2,
        show="headings",
        columns=header_list2,
        selectmode=BROWSE,
        yscrollcommand=y_axis_scrollbar.set,
        xscrollcommand=x_axis_scrollbar.set,
    )

    for _ in header_list2:
        customers_db.heading(column=_, text=_)

    # Serial Number
    customers_db.column(column=0, width=70, minwidth=70, anchor=CENTER)
    # Name
    customers_db.column(column=1, width=150, minwidth=150, anchor=W)
    # Created on
    customers_db.column(column=2, width=155, minwidth=155, anchor=CENTER)
    # Phone Number
    customers_db.column(column=3, width=130, minwidth=130, anchor=CENTER)
    # Email
    customers_db.column(column=4, width=315, minwidth=315, anchor=CENTER)
    # Date of Birth
    customers_db.column(column=5, width=95, minwidth=95, anchor=CENTER)
    # Gender
    customers_db.column(column=6, width=75, minwidth=75, anchor=W)

    customers_db.bind(sequence="<Double-1>", func=lambda event: fetch_data())
    customers_db.bind(sequence="<Return>", func=lambda event: select_customer())
    customers_db.bind(sequence="<Delete>", func=lambda event: delete_entry())

    x_axis_scrollbar.config(command=customers_db.xview)
    y_axis_scrollbar.config(command=customers_db.yview)
    customers_db.pack(fill=X)

    tot_customers_lbl: Label = Label(master=lf21, fg="red")
    tot_customers_lbl.pack()

    # Customer tab, Search section
    search_lbl: Label = Label(master=lf22, text="Search by (name, phone, email):")
    search_lbl.pack(side=LEFT, padx=10)

    search_entry: Entry = Entry(
        master=lf22,
        textvariable=search_var,
        width=25,
        selectbackground="orange",
    )
    search_entry.bind(sequence="<Return>", func=lambda event: search_record())
    search_entry.pack(side=LEFT, padx=10)

    search_entry.bind(sequence="<Control-F>", func=lambda event: not_ready_yet())
    search_entry.bind(sequence="<Control-f>", func=lambda event: not_ready_yet())

    runtime_search_lbl: Label = Label(master=lf22)
    runtime_search_lbl.pack(side=LEFT, padx=10)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/magnifying-glass.png")).resize(
        size=(20, 20)
    )
    search_ico: PhotoImage = PhotoImage(image=_)
    search_btn: Button = Button(
        master=lf22,
        text="Search",
        fg="#fff",
        compound=LEFT,
        activeforeground="#fff",
        width=125,
        command=search_record,
        image=search_ico,
    )
    search_btn.bind(sequence="<Return>", func=lambda event: search_record())
    search_btn.pack(side=RIGHT, padx=5)

    # Customer details tab
    f2: Frame = Frame(master=lf23)
    f2.pack()

    f21: Frame = Frame(master=f2)
    f21.grid(row=0, column=0, padx=10)

    f22: Frame = Frame(master=f2)
    f22.grid(row=0, column=1, padx=10)

    name_lbl: Label = Label(
        master=f21,
        text="Customer Full Name:",
    )
    name_lbl.grid(row=0, column=0, sticky=W)
    name_entry: Entry = Entry(
        master=f21,
        width=30,
        textvariable=name_var1,
        selectbackground="orange",
    )
    name_entry.grid(row=0, column=1, padx=5, sticky=W)

    ph_lbl2: Label = Label(master=f21, text="Contact Number:")
    ph_lbl2.grid(row=1, column=0, sticky=W)

    ph_entry: Entry = Entry(
        master=f21,
        width=30,
        textvariable=ph_var1,
        selectbackground="orange",
    )
    ph_entry.grid(row=1, column=1, padx=5, sticky=W)

    email_lbl: Label = Label(master=f21, text="Email Address (Optional):")
    email_lbl.grid(row=2, column=0, sticky=W)
    email_entry: Entry = Entry(
        master=f21,
        width=30,
        textvariable=email_var1,
        selectbackground="orange",
    )
    email_entry.grid(row=2, column=1, padx=5, sticky=W)

    name_entry.bind(sequence="<Return>", func=lambda event: ph_entry.focus())
    ph_entry.bind(sequence="<Return>", func=lambda event: email_entry.focus())

    name_entry.bind(sequence="<Up>", func=lambda event: email_entry.focus())
    name_entry.bind(sequence="<Down>", func=lambda event: ph_entry.focus())

    ph_entry.bind(sequence="<Up>", func=lambda event: name_entry.focus())
    ph_entry.bind(sequence="<Down>", func=lambda event: email_entry.focus())

    email_entry.bind(sequence="<Up>", func=lambda event: ph_entry.focus())
    email_entry.bind(sequence="<Down>", func=lambda event: name_entry.focus())

    dob_lbl: Label = Label(
        master=f21,
        text=f"Date of Birth (Optional):",
    )
    dob_lbl.grid(row=3, column=0, sticky=W)
    # ERROR: No module named 'babel.numbers'
    day_selection: Calendar = Calendar(
        master=f21,
        selectmode="day",
        date_pattern="mm/dd/yyyy",
        showweeknumbers=weeks_number_var.get(),
        showothermonthdays=other_month_days_var.get(),
        maxdate=date(year=today.year, month=today.month, day=today.day),
        mindate=date(year=today.year - 100, month=today.month, day=today.day),
        year=today.year - 18,
        month=today.month,
        background="#2A3459",
        selectbackground="#2A3459",
        cursor="hand2",
    )
    day_selection.selection_clear()
    day_selection.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=NSEW)

    gender_lbl: Label = Label(master=f21, text="Gender:")
    gender_lbl.grid(row=4, column=0, sticky=W)
    gender_table: OptionMenu = OptionMenu(
        f21, gender_var, *gender_options, command=lambda event: update_gender_color()
    )
    gender_table.config(
        bg="#C01493",
        fg="#fff",
        activebackground="#FF1493",
        width=8,
    )
    gender_table["menu"].config(bg="#C01493", fg="#fff", activebackground="#FF1493")
    gender_table.grid(row=4, column=1, columnspan=2, padx=5, sticky=W)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/add-user.png")).resize(
        size=(20, 20)
    )
    adduser_ico: PhotoImage = PhotoImage(image=_)
    create_btn: Button = Button(
        master=f22,
        text="Create New",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        command=create_entry,
        image=adduser_ico,
    )
    create_btn.bind(sequence="<Return>", func=lambda event: create_entry())
    create_btn.grid(row=0, column=0, padx=5, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/edit.png")).resize(size=(20, 20))
    edit_user_ico: PhotoImage = PhotoImage(image=_)
    update_btn: Button = Button(
        master=f22,
        text="Update Selected",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        command=update_entry,
        image=edit_user_ico,
    )
    update_btn.bind(sequence="<Return>", func=lambda event: update_entry())
    update_btn.grid(row=1, column=0, padx=5, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/delete-user.png")).resize(
        size=(20, 20)
    )
    remove_user_ico: PhotoImage = PhotoImage(image=_)
    delete_btn: Button = Button(
        master=f22,
        text="Delete Selected",
        fg="#fff",
        compound=LEFT,
        activeforeground="#fff",
        width=125,
        command=delete_entry,
        image=remove_user_ico,
    )
    delete_btn.bind(sequence="<Return>", func=lambda event: delete_entry())
    delete_btn.grid(row=2, column=0, padx=5, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/calendar.png")).resize(
        size=(20, 20)
    )
    calendar_ico: PhotoImage = PhotoImage(image=_)
    clear_date_btn: Button = Button(
        master=f22,
        text="Clear Date",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        image=calendar_ico,
        command=clear_date,
    )
    clear_date_btn.bind(sequence="<Return>", func=lambda event: clear_date())
    clear_date_btn.grid(row=3, column=0, padx=5, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/clear.png")).resize(size=(16, 16))
    clear_ico: PhotoImage = PhotoImage(image=_)
    clear_inputs_btn: Button = Button(
        master=f22,
        text="Clear Input",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        command=clear_entry,
        image=clear_ico,
    )
    clear_inputs_btn.bind(sequence="<Return>", func=lambda event: clear_entry())
    clear_inputs_btn.grid(row=4, column=0, padx=5, pady=5)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/target.png")).resize(size=(20, 20))
    customer_ico: PhotoImage = PhotoImage(image=_)
    select_btn: Button = Button(
        master=lf24,
        text="Select",
        fg="#fff",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        command=select_customer,
        image=customer_ico,
    )
    select_btn.bind(sequence="<Return>", func=lambda event: select_customer())
    select_btn.grid(row=0, column=0, padx=5)

    exit_btn2: Button = Button(
        master=lf24,
        text="Exit",
        fg="#fff",
        compound=LEFT,
        activeforeground="#fff",
        width=125,
        command=exit_app,
        image=exit_ico,
    )
    exit_btn2.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_btn2.grid(row=0, column=1, padx=5)

    # Items Tab
    lf31: LabelFrame = LabelFrame(master=items_frame, text="Select Item", fg="red")
    lf31.pack(padx=10, pady=5, side=TOP, fill=BOTH)

    treeview_frame3: Frame = Frame(master=lf31)
    treeview_frame3.pack()

    treeview_scroll: Scrollbar = Scrollbar(master=treeview_frame3)
    treeview_scroll.pack(side=RIGHT, fill=Y)

    items_db: Treeview = Treeview(
        master=treeview_frame3,
        show="headings",
        columns=header_list3,
        selectmode=BROWSE,
        yscrollcommand=treeview_scroll.set,
    )

    for _ in header_list3:
        items_db.heading(column=_, text=_)

    items_db.column(column=0, width=70, minwidth=70, anchor=CENTER)
    items_db.column(column=1, width=175, minwidth=175, anchor=W)
    items_db.column(column=2, width=100, minwidth=100, anchor=W)

    treeview_scroll.config(command=items_db.yview)
    items_db.pack()

    info_lbl: Label = Label(
        master=lf31,
        text="Can't find the item you are looking for? Please report the missing items to the developer.",
        fg="red",
    )
    info_lbl.pack(side=BOTTOM)

    lf32: LabelFrame = LabelFrame(master=items_frame, text="New Stitch Item", fg="red")
    lf32.pack(padx=10, pady=5, ipady=5, fill=BOTH)

    f3: Frame = Frame(master=lf32)
    f3.pack()

    f31: Frame = Frame(master=f3)
    f31.pack(side=LEFT, padx=15, pady=2)

    f32: Frame = Frame(master=f3)
    f32.pack(side=RIGHT, padx=15, pady=2)

    name_lbl3: Label = Label(master=f31, text="Customer Full Name:")
    name_lbl3.grid(row=0, column=0, padx=5, sticky=W)
    name_entry3: Entry = Entry(
        master=f31,
        width=30,
        textvariable=name_var2,
        selectbackground="orange",
    )
    name_entry3.grid(row=0, column=1, padx=5, sticky=W)

    ph_lbl3: Label = Label(master=f31, text="Contact Number:")
    ph_lbl3.grid(row=1, column=0, padx=5, sticky=W)
    ph_entry3: Entry = Entry(
        master=f31,
        width=30,
        textvariable=ph_var2,
        selectbackground="orange",
    )
    ph_entry3.grid(row=1, column=1, padx=5)

    email_lbl3: Label = Label(master=f31, text="Email Address:")
    email_lbl3.grid(row=2, column=0, padx=5, sticky=W)
    email_entry3: Entry = Entry(
        master=f31, width=30, selectbackground="orange", textvariable=email_var2
    )
    email_entry3.grid(row=2, column=1, padx=5, sticky=W)

    name_entry3.bind(sequence="<Return>", func=lambda event: ph_entry3.focus())
    ph_entry3.bind(sequence="<Return>", func=lambda event: email_entry3.focus())

    name_entry3.bind(sequence="<Up>", func=lambda event: email_entry3.focus())
    name_entry3.bind(sequence="<Down>", func=lambda event: ph_entry3.focus())

    ph_entry3.bind(sequence="<Up>", func=lambda event: name_entry3.focus())
    ph_entry3.bind(sequence="<Down>", func=lambda event: email_entry3.focus())

    email_entry3.bind(sequence="<Up>", func=lambda event: ph_entry3.focus())
    email_entry3.bind(sequence="<Down>", func=lambda event: name_entry3.focus())

    order_type_lbl: Label = Label(master=f32, text="Order Type:")
    order_type_lbl.grid(row=0, column=0, padx=5, pady=2, sticky=W)

    stitch_var.set(value=1)
    rb1: Radiobutton = Radiobutton(
        master=f32,
        width=10,
        text="Stitching",
        variable=stitch_var,
        value=1,
    )
    rb1.grid(row=0, column=1, pady=2)
    rb2: Radiobutton = Radiobutton(
        master=f32,
        width=10,
        text="Material",
        variable=stitch_var,
        value=2,
    )
    rb2.grid(row=0, column=2, pady=2)
    rb3: Radiobutton = Radiobutton(
        master=f32,
        width=10,
        text="Knitting",
        variable=stitch_var,
        value=3,
    )
    rb3.grid(row=0, column=3, pady=2)
    rb4: Radiobutton = Radiobutton(
        master=f32,
        width=10,
        text="Embroidery",
        variable=stitch_var,
        value=4,
    )
    rb4.grid(row=0, column=4, pady=2)
    rb5: Radiobutton = Radiobutton(
        master=f32, width=10, text="Alteration", variable=stitch_var, value=5
    )
    rb5.grid(row=0, column=5, pady=2)

    rb1.bind(sequence="<Left>", func=lambda event: rb4.focus())
    rb1.bind(sequence="<Right>", func=lambda event: rb2.focus())

    rb2.bind(sequence="<Left>", func=lambda event: rb1.focus())
    rb2.bind(sequence="<Right>", func=lambda event: rb3.focus())

    rb3.bind(sequence="<Left>", func=lambda event: rb2.focus())
    rb3.bind(sequence="<Right>", func=lambda event: rb4.focus())

    rb4.bind(sequence="<Left>", func=lambda event: rb3.focus())
    rb4.bind(sequence="<Right>", func=lambda event: rb5.focus())

    rb5.bind(sequence="<Left>", func=lambda event: rb4.focus())
    rb5.bind(sequence="<Right>", func=lambda event: rb1.focus())

    notes_lbl: Label = Label(master=f32, text="Special Instructions (Optional):")
    notes_lbl.grid(row=1, column=0, columnspan=6, pady=(2, 0), sticky=W)
    notes_entry: ScrolledText = ScrolledText(
        master=f32,
        height=7,
        undo=True,
        wrap=WORD,
        selectbackground="orange",
    )
    notes_entry.grid(row=2, column=0, columnspan=6, pady=(0, 2), sticky=NSEW)

    notes_popup_menu: Menu = Menu(master=notes_entry, tearoff=False)
    notes_popup_menu.add_command(
        label="Undo", accelerator="Ctrl+Z", command=undo_notes_widget
    )
    notes_popup_menu.add_command(
        label="Redo", accelerator="Ctrl+Shift+Z", command=redo_notes_widget
    )
    notes_popup_menu.add_separator()
    notes_popup_menu.add_command(label="Cut", accelerator="Ctrl+X")
    notes_popup_menu.add_command(label="Copy", accelerator="Ctrl+C")
    notes_popup_menu.add_command(label="Paste", accelerator="Ctrl+V")
    notes_popup_menu.add_separator()
    notes_popup_menu.add_command(label="Select All", accelerator="Ctrl+A")
    notes_popup_menu.add_command(label="Clear Selected")

    cost_lbl: Label = Label(master=f32, text="Stitching Charge ($):")
    cost_lbl.grid(row=3, column=0, padx=5, pady=2, sticky=W)
    cost_entry: Entry = Entry(
        master=f32,
        width=10,
        textvariable=cost_var,
        justify=CENTER,
        selectbackground="orange",
    )
    cost_entry.grid(row=3, column=1, columnspan=5, pady=2, sticky=W)

    delivery_date_lbl: Label = Label(master=f32, text="Delivery Date:")
    delivery_date_lbl.grid(row=4, column=0, padx=5, pady=2, sticky=W)
    delivery_date_selection: Calendar = Calendar(
        master=f32,
        selectmode="day",
        date_pattern="mm/dd/yyyy",
        showweeknumbers=weeks_number_var.get(),
        showothermonthdays=other_month_days_var.get(),
        mindate=date(year=today.year, month=today.month, day=today.day),
        year=today.year,
        month=today.month,
        background="#2A3459",
        selectbackground="#2A3459",
        cursor="hand2",
    )
    delivery_date_selection.selection_clear()
    delivery_date_selection.grid(row=4, column=1, columnspan=5, pady=2, sticky=W)

    priority_lbl: Label = Label(master=f32, text="Priority:")
    priority_lbl.grid(row=5, column=0, padx=5, pady=2, sticky=W)
    priority_btn: Checkbutton = Checkbutton(
        master=f32,
        width=15,
        text="Mark as Urgent",
        variable=priority_var,
    )
    priority_btn.grid(row=5, column=1, columnspan=5, pady=2, sticky=W)

    lf33: LabelFrame = LabelFrame(master=items_frame, text="Save Item", fg="red")
    lf33.pack(side=BOTTOM, padx=10, pady=5, ipady=3, fill=X)

    _: Image = Image.open(fp=join(BASE_PATH, "assets/diskette.png")).resize(
        size=(20, 20)
    )
    save_ico: PhotoImage = PhotoImage(image=_)
    save_item_btn: Button = Button(
        master=lf33,
        text="Save",
        bg="#000",
        fg="#fff",
        activebackground="#404040",
        activeforeground="#fff",
        compound=LEFT,
        width=125,
        command=save_order,
        image=save_ico,
    )
    save_item_btn.bind(sequence="<Return>", func=lambda event: save_order())
    save_item_btn.grid(row=0, column=0, padx=5)

    exit_btn: Button = Button(
        master=lf33,
        text="Exit",
        bg="#800000",
        fg="#fff",
        compound=LEFT,
        activebackground="#C02020",
        activeforeground="#fff",
        width=125,
        command=exit_app,
        image=exit_ico,
    )
    exit_btn.bind(sequence="<Return>", func=lambda event: exit_app())
    exit_btn.grid(row=0, column=1, padx=5)

    lf4: LabelFrame = LabelFrame(master=stats_frame, text="My Stats Profile", fg="red")
    lf4.pack(padx=10, pady=5, ipady=4, side=TOP, fill=BOTH)

    f41: Frame = Frame(master=lf4)
    f41.pack()

    tot_customers_lbl4: Label = Label(master=f41, text="Total No. of Customers:")
    tot_customers_lbl4.grid(row=0, column=0, sticky=W, padx=15)

    tot_customers_value: Label = Label(master=f41, text="0")
    tot_customers_value.grid(row=0, column=1, sticky=W, padx=15)

    active_orders_lbl: Label = Label(master=f41, text="Total Active Orders:")
    active_orders_lbl.grid(row=1, column=0, sticky=W, padx=15)

    active_orders_value: Label = Label(master=f41, text="0 / $0")
    active_orders_value.grid(row=1, column=1, sticky=W, padx=15)

    completed_orders_lbl: Label = Label(
        master=f41, text="Total No. of Completed Orders:"
    )
    completed_orders_lbl.grid(row=2, column=0, sticky=W, padx=15)

    completed_orders_value: Label = Label(master=f41, text=0)
    completed_orders_value.grid(row=2, column=1, sticky=W, padx=15)

    belated_delivered_lbl: Label = Label(
        master=f41, text="Total No. of Belated Delivered Orders:"
    )
    belated_delivered_lbl.grid(row=3, column=0, sticky=W, padx=15)

    belated_delivered_value: Label = Label(master=f41, text="0")
    belated_delivered_value.grid(row=3, column=1, sticky=W, padx=15)

    amount_earned_lbl: Label = Label(master=f41, text="Total Amount Earned:")
    amount_earned_lbl.grid(row=5, column=0, sticky=W, padx=15)

    amount_earned_value: Label = Label(master=f41, text="$0")
    amount_earned_value.grid(row=5, column=1, sticky=W, padx=15)

    Label(
        master=tm,
        text="Created by FOSS Kingdom / Made with Love in Incredible India.",
        bg="#000",
        fg="#fff",
    ).pack(side=BOTTOM, fill=X)

    cpu_lbl: Label = Label(master=tm)
    cpu_lbl.pack(side=LEFT, fill=X, ipadx=3)
    cpu_stat()

    mem_lbl: Label = Label(master=tm)
    mem_lbl.pack(side=LEFT, fill=X, ipadx=3)
    mem_stat()

    pwr_lbl: Label = Label(master=tm)
    pwr_lbl.pack(side=LEFT, fill=X, ipadx=3)
    pwr_stat()

    time_lbl: Label = Label(master=tm)
    time_lbl.pack(side=LEFT, fill=X, ipadx=3)
    time_stat()

    boot_time_lbl: Label = Label(master=tm)
    boot_time_lbl.pack(side=RIGHT, fill=X, padx=10)

    try:
        print(F_GREEN + "[INFO]\tReading database file...")
        conn = connect(database=database_file_path)
        c = conn.cursor()
        c.execute(
            """create table if not exists orders (
            name text not null,
            created_on text not null,
            phone text not null,
            item text not null,
            stitch_option text not null,
            notes text,
            cost real not null,
            delivery_date text not null,
            priority text not null,
            status text not null
            )"""
        )
        conn.commit()
        c.execute(
            """create table if not exists customers (
            name text not null,
            created_on text not null,
            phone text not null primary key,
            email text,
            dob text,
            gender text not null
            )"""
        )
        conn.commit()

    except OperationalError as operational_error:  # Unknown exception ??
        print(F_BLUE + "=" * 80)
        print(F_RED + "Error Code: sqlite3.OperationalError")
        print(F_RED + f"[ERROR]\t{operational_error}")
        print(F_BLUE + "=" * 80)

        play_bell_sound(master=tm, bell_var=tm_bell_var)
        showinfo(
            title=f"TailorMate {__version__}",
            message=f"Sorry, an error occurred! {operational_error}",
        )
        tm.destroy()

        clean_cache()

        print(F_RED + "Bye...")

        clrscr()
        terminate()

    update_orders()
    update_customers()
    update_items()

    if current_theme == "light" or (current_theme == "system_default" and isLight()):
        switch2light()

    elif current_theme == "dark" or (current_theme == "system_default" and isDark()):
        switch2dark()

    delta_time = time() - t0
    elapsed_time: float = elapsed_time + delta_time

    if elapsed_time < 1:
        print(
            F_GREEN
            + f"[INFO]\tBooting Time: {round(elapsed_time * 1000, 2)} millisecond(s)"
        )
        boot_time_lbl.config(
            text=f"Booting Time: {round(elapsed_time * 1000, 2)} millisecond(s)"
        )

    else:
        print(F_GREEN + f"[INFO]\tBooting Time: {round(elapsed_time, 3)} second(s)")
        boot_time_lbl.config(text=f"Booting Time {round(elapsed_time, 3)} second(s)")

    tm.deiconify()
    tm.mainloop()

except KeyboardInterrupt:
    print("\n" + "=" * 80)
    print("Error Code: KeyboardInterrupt")
    print("[ERROR]\tKeyboardInterrupt occurred! Bye...")
    print("=" * 80)

except ModuleNotFoundError as module_not_found_error:
    print("=" * 80)
    print("Error Code: ModuleNotFoundError")
    print(f"[ERROR]\t{module_not_found_error}")
    print("=" * 80)
