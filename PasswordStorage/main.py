# -*- coding: utf-8 -*-

from Interface import *
from account_control import AccountControl
from profiles_db_control import ProfilesDbControl


class PasswordStorage:
    def __init__(self):
        self._ACCOUNT_CONTROL = AccountControl()
        self._ACCOUNT_CONTROL.error_correction()
        self._ACCOUNT_CONTROL.open_db()

        self._PROFILES_DB_CONTROL = ProfilesDbControl()

        self._MAIN_INTERFACE = Interface(
            self._ACCOUNT_CONTROL,
            self._PROFILES_DB_CONTROL
        )

    def start_interface(self):
        self._MAIN_INTERFACE.draw_login_in()
        self._MAIN_INTERFACE.start_interface()

    def close_db(self):
        self._ACCOUNT_CONTROL.close_db()


if __name__ == "__main__":
    main_program = PasswordStorage()
    main_program.start_interface()
    main_program.close_db()
