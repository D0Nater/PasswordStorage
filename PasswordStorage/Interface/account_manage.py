# -*- coding: utf-8 -*-

from tkinter import *

from .my_entry_binder import MyEntryBinder


class AccountManage:
    def draw_login_in(self):
        def draw_error_icon(name, password):
            pass

        def login_in():
            login = profile_name_var.get()
            password = profile_pass_var.get()

            is_correct_login = False if self._ACCOUNT_CONTROL.check_valid_text(login) is None else True
            is_correct_password = False if self._ACCOUNT_CONTROL.check_valid_text(password) is None else True

            if not is_correct_login or not is_correct_password:
                draw_error_icon(is_correct_login, is_correct_password)
                print("not correct text")
                return "not correct text"

            if not self._ACCOUNT_CONTROL.check_password(login, password):
                print("bad password")
                return "bad password"

            self._PROFILES_DB_CONTROL.set_profile_name(login)

            encryption_key = self._PROFILES_DB_CONTROL.make_encryption_key(
                salt=self._ACCOUNT_CONTROL.get_profile_password(login, is_encode=True)
            )
            self._PROFILES_DB_CONTROL.set_encryption_key(encryption_key)

            self._PROFILES_DB_CONTROL.db_error_correction()
            self._PROFILES_DB_CONTROL.open_db(file=self._PROFILES_DB_CONTROL.get_db_file())

            self.draw_main_interface()

        self.clear_frame(self._HEAD_FRAME)
        self.clear_frame(self._MAIN_FRAME)
        self._PROFILES_FRAME.destroy()

        self._HEAD_FRAME.config(bg="grey94")

        profile_name_var = StringVar()
        profile_pass_var = StringVar()

        profile_name_entry = Entry(self._MAIN_FRAME, textvariable=profile_name_var, width=18, font="Verdana 11")
        profile_pass_entry = Entry(self._MAIN_FRAME, textvariable=profile_pass_var, width=18, font="Verdana 11")

        login_in_button = Button(self._MAIN_FRAME, text="Войти", bd=1, relief=RIDGE, font="13", command=login_in)
        create_profile_button = Button(self._MAIN_FRAME, text="Создать профиль", bd=1, relief=RIDGE, font="13", command=self.draw_create_profile)

        MyEntryBinder.bind_entry(entry=profile_name_entry, text="Логин")
        MyEntryBinder.bind_entry(entry=profile_pass_entry, text="Пароль", show="*")

        profile_name_entry.place(relx=0.5, rely=0.2, anchor=CENTER)
        profile_pass_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

        login_in_button.place(relx=0.5, rely=0.4, anchor=CENTER)
        create_profile_button.place(relx=0.5, rely=0.55, anchor=CENTER)

    def draw_create_profile(self):
        def draw_error_icon(name, password1, password2):
            pass

        def create_profile():
            login = profile_name_var.get()
            password1 = profile_pass_var1.get()
            password2 = profile_pass_var2.get()

            is_correct_login = False if self._ACCOUNT_CONTROL.check_valid_text(login) is None else True
            is_correct_password1 = False if self._ACCOUNT_CONTROL.check_valid_text(password1) is None else True
            is_correct_password2 = False if self._ACCOUNT_CONTROL.check_valid_text(password2) is None else True

            if password1 != password2:
                print("password1 != password2")
                return "password1 != password2"

            if not is_correct_login or not is_correct_password1 or not is_correct_password2:
                draw_error_icon(is_correct_login, is_correct_password1, is_correct_password2)
                print("not correct text")
                return "not correct text"

            if self._ACCOUNT_CONTROL.check_profile(login):
                print("login error")
                return "login error"

            self._ACCOUNT_CONTROL.create_profile(login, password1)

            self._PROFILES_DB_CONTROL.set_profile_name(login)
            self._PROFILES_DB_CONTROL.create_user_db()

            encryption_key = self._PROFILES_DB_CONTROL.make_encryption_key(
                salt=self._ACCOUNT_CONTROL.get_profile_password(login, is_encode=True)
            )
            self._PROFILES_DB_CONTROL.set_encryption_key(encryption_key)

            self._PROFILES_DB_CONTROL.open_db(file=self._PROFILES_DB_CONTROL.get_db_file())

            self.draw_main_interface()

        self.clear_frame(self._HEAD_FRAME)
        self.clear_frame(self._MAIN_FRAME)

        profile_name_var = StringVar()
        profile_pass_var1 = StringVar()
        profile_pass_var2 = StringVar()

        profile_name_entry = Entry(self._MAIN_FRAME, textvariable=profile_name_var, width=18, font="Verdana 11")
        profile_pass_entry1 = Entry(self._MAIN_FRAME, textvariable=profile_pass_var1, width=18, font="Verdana 11")
        profile_pass_entry2 = Entry(self._MAIN_FRAME, textvariable=profile_pass_var2, width=18, font="Verdana 11")

        create_profile_button = Button(self._MAIN_FRAME, text="Создать профиль", bd=1, relief=RIDGE, font="13", command=create_profile)
        login_in_button = Button(self._MAIN_FRAME, text="Войти", bd=1, relief=RIDGE, font="13", command=self.draw_login_in)

        MyEntryBinder.bind_entry(entry=profile_name_entry, text="Логин")
        MyEntryBinder.bind_entry(entry=profile_pass_entry1, text="Пароль", show="*")
        MyEntryBinder.bind_entry(entry=profile_pass_entry2, text="Повторите пароль", show="*")

        profile_name_entry.place(relx=0.5, rely=0.2, anchor=CENTER)
        profile_pass_entry1.place(relx=0.5, rely=0.3, anchor=CENTER)
        profile_pass_entry2.place(relx=0.5, rely=0.38, anchor=CENTER)

        create_profile_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        login_in_button.place(relx=0.5, rely=0.65, anchor=CENTER)
