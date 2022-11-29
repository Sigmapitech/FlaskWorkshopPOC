import hashlib
import os


def blake2b_with_salt(password: str, salt: str) -> str:
    pepper = os.getenv("PEPPER")
    auth_string = f"{password}{salt}{pepper}".encode("utf-8")
    return hashlib.blake2b(auth_string).hexdigest()
