from bcrypt import gensalt, hashpw
from cryptography.fernet import Fernet, InvalidToken


def encrypt_root_passwd(passwd: str):
    return hashpw(passwd.encode(encoding="utf-8"), gensalt()).decode(encoding="utf-8")


def gen_private_key(key_path: str):
    private_key_file = open(file=key_path, mode="wb")
    private_key_file.write(Fernet.generate_key())
    private_key_file.close()


def load_private_key(private_key_path: str):
    private_key_file = open(file=private_key_path, mode="rb")
    private_key: bytes = private_key_file.read()
    private_key_file.close()

    return private_key


def encrypt_smtp_passwd(data: str, key_path: str):
    fernet: Fernet = Fernet(key=load_private_key(private_key_path=key_path))

    return fernet.encrypt(data.encode(encoding="utf-8")).decode(encoding="utf-8")


def decrypt_smtp_passwd(token: str, key_path: str):
    fernet: Fernet = Fernet(key=load_private_key(private_key_path=key_path))

    try:
        return fernet.decrypt(token.encode(encoding="utf-8")).decode(encoding="utf-8")

    except InvalidToken:
        raise InvalidToken("Failed to Decrypt SMTP Password.")

    except ValueError as value_error:
        raise ValueError(f"{value_error}. Failed to Decrypt SMTP Password.")
