# -*- coding: utf-8 -*-

from os import urandom
from re import fullmatch
from os import mkdir, path
from binascii import hexlify
from hashlib import pbkdf2_hmac
from base64 import b64decode, b64encode

from database_control import DatabaseControl
from profiles_db_control import ProfilesDbControl


class AccountControl(DatabaseControl):
    def __init__(self):
        self._DATABASE_DIR = "Databases"
        self._DATABASE_FILE = self._DATABASE_DIR + "/main_data.sqlite"

    def error_correction(self):
        if not path.exists(self._DATABASE_DIR):
            mkdir(self._DATABASE_DIR)

        self.open_db(file=self._DATABASE_FILE)
        self.execute_query("CREATE TABLE IF NOT EXISTS USER_PROFILES (PROFILE_NAME, PASSWORD)")
        self.close_db()

    def create_profile(self, profile_name, password):
        self.execute_query(
            "INSERT INTO USER_PROFILES VALUES (?, ?)", (
                b64encode(profile_name.encode("UTF-8")).decode("UTF-8"),
                self.encode_text(text=password)
            )
        )

    def delete_profile(self, profile_name):
        self.execute_query(
            "DELETE FROM USER_PROFILES WHERE PROFILE_NAME=?", (
                b64encode(profile_name.encode("UTF-8")).decode("UTF-8"),
            )
        )

    def get_profile_password(self, profile_name, is_encode=False):
        password = self.execute_query(
            "SELECT PASSWORD FROM USER_PROFILES WHERE PROFILE_NAME=?", (
                b64encode(profile_name.encode("UTF-8")).decode("UTF-8"),
            )
        )[0][0]

        if is_encode:
            return hexlify(b64decode(password))

        return password

    def check_profile(self, profile_name):
        return False if self.execute_query(
            "SELECT PROFILE_NAME FROM USER_PROFILES WHERE PROFILE_NAME=?", (
                b64encode(profile_name.encode("UTF-8")).decode("UTF-8"),
            )
        ) == [] else True

    def check_password(self, profile_name, password):
        profile_password = self.get_profile_password(profile_name)
        profile_password = b64decode(profile_password)

        new_key = pbkdf2_hmac("sha256", password.encode("utf-8"), profile_password[:32], 100000)

        if profile_password[32:] == new_key:
            return True
        return False

    def check_valid_text(self, text, valid_text=r"^[a-zA-Z0-9]{1}[a-zA-Z0-9_]{2,14}[a-zA-Z0-9]{1}$"):
        """ Default valid text e.g. "Test_User_228" - length: (min:4, max:16)
            BUT IMPOSSIBLE start and/or finish string with char "_" e.g. "_BAD_USER_NAME_123"
        """
        return fullmatch(valid_text, text)

    def encode_text(self, text, salt=None):
        salt = urandom(32) if salt is None else salt
        key = pbkdf2_hmac("sha256", text.encode("utf-8"), salt, 100000)
        return b64encode(salt + key).decode("UTF-8")
