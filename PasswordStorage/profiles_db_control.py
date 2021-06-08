# -*- coding: utf-8 -*-

from os import mkdir, path, remove
from binascii import hexlify
from hashlib import pbkdf2_hmac
from base64 import b64decode, b64encode

from cryptographer import Cryptographer
from database_control import DatabaseControl


class ProfileControl:
    def add_profile(self, profile_name, password, service, folder=None):
        folder = self._DEFAULT_PROFILES_FOLDER if folder is None else folder
        try:
            new_profile_id = self.execute_query("SELECT MAX(`ID`) FROM %s" % folder)[0][0] + 1
        except (IndexError, TypeError):
            new_profile_id = 0

        self.execute_query(
            "INSERT INTO %s VALUES (?, ?, ?, ?)"  % folder, (
                new_profile_id,
                Cryptographer.encode_text(profile_name, self._encryption_key).decode("UTF-8"),
                Cryptographer.encode_text(password, self._encryption_key).decode("UTF-8"),
                b64encode(service.encode("UTF-8")).decode("UTF-8")
            )
        )

    def delete_profile(self, profile_id, folder=None):
        folder = self._DEFAULT_PROFILES_FOLDER if folder is None else folder

        self.execute_query("DELETE FROM %s WHERE ID=?" % folder, (profile_id, ))

    def change_profile(self, profile_name, password):
        pass

    def get_profiles(self, folder=None, filter={}):
        folder = self._DEFAULT_PROFILES_FOLDER if folder is None else folder

        return [
            (
                profile[0],
                Cryptographer.decode_text(profile[1], self._encryption_key),
                Cryptographer.decode_text(profile[2], self._encryption_key),
                b64decode(profile[3]).decode("UTF-8")
            ) for profile in self.execute_query("SELECT * FROM %s" % folder)
        ]


class ProfilesDbControl(DatabaseControl, ProfileControl):
    def __init__(self):
        self._DATABASE_DIR = "Databases"
        self._database_file = ""
        self._profile_name = ""

        self._encryption_key = ""

        self._DEFAULT_PROFILES_FOLDER = "ALL_PROFILES"

    def get_default_folder(self):
        return self._DEFAULT_PROFILES_FOLDER

    def get_db_file(self):
        return self._database_file

    def get_profile_name(self):
        return self._profile_name

    def set_profile_name(self, profile_name):
        self._profile_name = profile_name
        self._database_file = "%s/%s.sqlite" % (
            self._DATABASE_DIR, b64encode(self._profile_name.encode("UTF-8")).decode("UTF-8")
        )

    def set_encryption_key(self, key):
        self._encryption_key = key

    def make_encryption_key(self, salt, key_len=32):
        text = (self._profile_name + salt.decode("UTF-8")[32:])[:32]
        key = pbkdf2_hmac("sha256", text.encode("utf-8"), salt[:32], 100000)
        key = hexlify(salt + key).decode("UTF-8")
        return key[len(key)-key_len:]

    def db_error_correction(self):
        self.create_user_db()

    def create_user_db(self):
        if not path.exists(self._DATABASE_DIR):
            mkdir(self._DATABASE_DIR)

        self.open_db(file=self._database_file)
        self.execute_query("CREATE TABLE IF NOT EXISTS %s (ID, PROFILE_NAME, PASSWORD, SERVICE)" % self._DEFAULT_PROFILES_FOLDER)
        self.close_db()

    def delete_user_db(self):
        remove(self._database_file)

    def rename_user_db(self):
        pass
