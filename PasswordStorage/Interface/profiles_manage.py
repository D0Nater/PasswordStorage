# -*- coding: utf-8 -*-

from tkinter import *

from .my_scrollbar import Scrollable
from .my_entry_binder import MyEntryBinder


class Profile:
    def __init__(self, profiles_db_control, scrollable_body,
                 profile_id, login, password, service, folder):

        self._PROFILES_DB_CONTROL = profiles_db_control
        self._scrollable_body = scrollable_body

        self._profile_id = profile_id
        self._login = login
        self._password = password
        self._service = service
        self._folder = folder

        self.bg_color = "grey80"

    def draw_profile(self, profile_num, delete_func):
        canvas = Canvas(self._scrollable_body, height=30, bg=self.bg_color)

        service_text = Text(width=6, height=1, bd=1, wrap=NONE, font="Verdana 12", cursor="arrow", bg=self.bg_color)
        login_text = Text(width=6, height=1, bd=1, wrap=NONE, font="Verdana 12", cursor="arrow", bg=self.bg_color)
        password_text = Text(width=6, height=1, bd=1, wrap=NONE, font="Verdana 12", cursor="arrow", bg=self.bg_color)
        delete_button = Button(text="Удалить", command=lambda: delete_func(profile_id=self._profile_id, folder=self._folder))

        service_text.insert(END, self._service)
        service_text.config(state=DISABLED)

        login_text.insert(END, self._login)
        login_text.config(state=DISABLED)

        password_text.insert(END, self._password)
        password_text.config(state=DISABLED)

        service_text_draw = canvas.create_window(5, 17, anchor=W, window=service_text)
        login_text_draw = canvas.create_window(canvas.bbox(service_text_draw)[2]+5, 17, anchor=W, window=login_text)
        password_text_draw = canvas.create_window(canvas.bbox(login_text_draw)[2]+5, 17, anchor=W, window=password_text)
        delete_button = canvas.create_window(canvas.bbox(password_text_draw)[2]+5, 17, anchor=W, window=delete_button)

        canvas.pack(fill="both", expand=True)


class ProfilesManage:
    def draw_head(self):
        def exit_click():
            self._PROFILES_DB_CONTROL.close_db()
            self.draw_login_in()

        self.clear_frame(self._HEAD_FRAME)

        self._HEAD_FRAME.config(bg="grey92")

        user_name = self._PROFILES_DB_CONTROL.get_profile_name()

        draw_user_name = Label(self._HEAD_FRAME, text=user_name, justify=LEFT, font="Arial 14", bg="grey92")
        exit_button = Button(self._HEAD_FRAME, text="Выйти", bd=1, relief=RIDGE, font="13", command=exit_click)

        draw_user_name.place(relx=0.76, rely=0.25, anchor=N)
        exit_button.place(relx=0.9, rely=0.25, anchor=N)

    def draw_profiles(self):
        def delete_profile(profile_id, folder):
            self._PROFILES_DB_CONTROL.delete_profile(profile_id=profile_id, folder=folder)
            self.draw_profiles()

        self._PROFILES_FRAME.destroy()

        self._PROFILES_FRAME = Frame(self._ROOT)
        scrollable_body = Scrollable(self._PROFILES_FRAME, bg="grey85")

        profiles_list = self._PROFILES_DB_CONTROL.get_profiles()

        profile_num = 0
        for profile in profiles_list:
            Profile(
                profiles_db_control=self._PROFILES_DB_CONTROL,
                scrollable_body=scrollable_body,
                profile_id=profile[0],
                login=profile[1],
                password=profile[2],
                service=profile[3],
                folder=self.folder_name_now
            ).draw_profile(
                profile_num=profile_num,
                delete_func=delete_profile
            )

            profile_num += 1

        self._PROFILES_FRAME.place(x=0, y=84, relwidth=.6, relheight=0.70, anchor=NW)

    def draw_filter(self):
        pass

    def draw_main_interface(self):
        self.clear_frame(self._MAIN_FRAME)

        self.folder_name_now = self._PROFILES_DB_CONTROL.get_default_folder()

        self.draw_head()
        self.draw_profiles()
        self.draw_filter()

        Label(self._MAIN_FRAME, text=self.folder_name_now,
              justify=RIGHT, font="Arial 14"
        ).place(x=17, y=0, anchor=NW)

        Button(self._MAIN_FRAME, text="Добавить аккаунт",
               bd=1, relief=RIDGE, font="13",
               command=self.draw_add_profile
        ).place(x=17, rely=0.9, anchor=NW)

    def draw_add_profile(self):
        def add_profile():
            login = login_var.get()
            password = password_var.get()
            service = service_var.get()

            self._PROFILES_DB_CONTROL.add_profile(
                profile_name=login,
                password=password,
                service=service,
                folder=self.folder_name_now
            )

            self.draw_main_interface()

        self.clear_frame(self._MAIN_FRAME)
        self._PROFILES_FRAME.destroy()

        login_var = StringVar()
        password_var = StringVar()
        service_var = StringVar()

        login_entry = Entry(self._MAIN_FRAME, textvariable=login_var, width=18, font="Verdana 11")
        password_entry = Entry(self._MAIN_FRAME, textvariable=password_var, width=18, font="Verdana 11")
        service_entry = Entry(self._MAIN_FRAME, textvariable=service_var, width=18, font="Verdana 11")
        add_profile_button = Button(self._MAIN_FRAME, text="Добавить аккаунт", bd=1, relief=RIDGE, font="13", command=add_profile)
        back_button = Button(self._MAIN_FRAME, text="Назад", bd=1, relief=RIDGE, font="13", command=self.draw_main_interface)

        MyEntryBinder.bind_entry(entry=login_entry, text="Логин")
        MyEntryBinder.bind_entry(entry=password_entry, text="Пароль", show="*")
        MyEntryBinder.bind_entry(entry=service_entry, text="Сервис")

        login_entry.place(relx=0.5, rely=0.2, anchor=CENTER)
        password_entry.place(relx=0.5, rely=0.29, anchor=CENTER)
        service_entry.place(relx=0.5, rely=0.38, anchor=CENTER)
        add_profile_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        back_button.place(x=10, y=10, anchor=NW)
