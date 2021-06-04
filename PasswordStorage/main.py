# -*- coding: utf-8 -*-

from Interface import *


class PasswordStorage:
    def __init__(self):
        self._MAIN_INTERFACE = Interface()

    def start_interface(self):
        self._MAIN_INTERFACE.start_interface()


if __name__ == "__main__":
    main_program = PasswordStorage()
    main_program.start_interface()
