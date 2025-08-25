import updated_ctk as ctk
import os
import NetConWindows

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Help(ctk.CTkToplevel):
    def __call__(self, var, master, opacity, language):

        def show_help_for_tab(tab_name):
            if tab_name == "Терминал":
                self.textbox = ctk.CTkTextbox(self.frame_1, width=100, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"))
                self.textbox.grid(row = 1, column = 1, padx = 0, pady = (0,0), sticky = "nsew")
                if self.language == "Русский":
                    self.textbox.insert("end"," \n ● «SerialTerminal»:\n  \n"
                                              " В этом разделе программы пользователь\n"
                                              " может подключаться к устройствам с по-\n"
                                              " мощью последовательного порта своего\n"
                                              " устройства, осуществлять настройку и т.д.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● «Горячие» клавиши:\n \n"
                                               " 1. «Esc» - очистить поле ввода команд.\n"
                                               " 2. «Tab, Ctrl+Tab, Shift+Tab» - навигация\n"
                                               "     между полями.\n"
                                               " 3. «Enter» - ввод команды, если курсор в\n"
                                               "     поле ввода.\n"
                                               " 4. « ↓ » - вызов выпадающего списка,\n"
                                               "     если курсор в поле выбора.\n"
                                               " 5. «Ctrl+Del» - очистка терминала.\n"
                                               " 6. «F6» - разрыв соединения.\n"
                                               " 7. «F8» - свернуть/развернуть панель\n"
                                               "     настроек терминала.\n"
                                               " 8. «F9» - вывод справки для терминала.\n"
                                               " 9. «↓/↑» - выбор команды из последних\n"
                                               "     10-ти, если курсор в поле ввода.\n"
                                               " 10. «Q/Ctrl+C» - выход/завершение прос-\n"
                                               "     мотра конфигурации и т.п.\n"
                                               " 11. «Space/Return» - следующая строка/стра-\n"
                                               "     ница при просмотре конфигурации и т.п.\n"
                                               " 12. «Ctrl+F» - открытие окна поиска.\n"
                                        )
                else:
                    self.textbox.insert("end", " \n ● «SerialTerminal»:\n  \n"
                                               " In this section of the program, the user\n"
                                               " can connect to devices using the serial\n"
                                               " port of devices, perform configuration\n"
                                               " etc.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● Hotkeys:\n \n"
                                               " 1. «Esc» - clear the command input field.\n"
                                               " 2. «Tab, Ctrl+Tab, Shift+Tab» - navigation\n"
                                               "     between fields.\n"
                                               " 3. «Enter» - enter a command if he cursor\n"
                                               "     is in the input field.\n"
                                               " 4. « ↓ » - call a drop-down list if the\n"
                                               "     cursor is in the selection field.\n"
                                               " 5. «Ctrl+Del» - clear terminal.\n"
                                               " 6. «F6» - close connection.\n"
                                               " 7. «F8» - collapse/expand the terminal\n"
                                               "     settings panel.\n"
                                               " 8. «F9» - output help for the terminal.\n"
                                               " 9. «↓/↑» - select a command from the last\n"
                                               "     10 if the cursor is in the input field.\n"
                                               " 10. «Q/Ctrl+C» - exit/finish viewing the\n"
                                               "     configuration, etc.\n"
                                               " 11. «Space/Return» - next line/page when\n"
                                               "     viewing configuration etc.\n"
                                               " 12. «Ctrl+F» - opening the search window.\n"
                                        )
                self.textbox.configure(state = "disabled")
            self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))
            self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units"))

            if tab_name == "Телнет":
                self.textbox = ctk.CTkTextbox(self.frame_1, width=100, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"))
                self.textbox.grid(row = 1, column = 1, padx = 0, pady = (0,0), sticky = "nsew")
                if self.language == "Русский":
                    self.textbox.insert("end"," \n ● «NetTerm»:\n  \n"
                                              " В этом разделе программы пользователь\n"
                                              " может подключаться к устройствам с по-\n"
                                              " мощью протоколов SSH и Telnet, осуществ-\n"
                                              " лять настройку устройств и т.д." )
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● «Горячие» клавиши:\n \n"
                                               " 1. «Esc» - очистить поле ввода команд.\n"
                                               " 2. «Tab, Ctrl+Tab, Shift+Tab» - навигация\n"
                                               "     между полями.\n"
                                               " 3. «Enter» - ввод команды, если курсор в\n"
                                               "     поле ввода.\n"
                                               " 4. «Ctrl+Del» - очистка терминала.\n"
                                               " 5. «F6» - разрыв соединения.\n"
                                               " 6. «F8» - свернуть/развернуть панель\n"
                                               "     настроек терминала.\n"
                                               " 7. «F9» - вывод справки для терминала.\n"
                                               " 8. «↓/↑» - выбор команды из последних\n"
                                               "     10-ти, если курсор в поле ввода.\n"
                                               " 9. «Q/Ctrl+C» - выход/завершение прос-\n"
                                               "     мотра конфигурации и т.п.\n"
                                               " 10. «Space/Return» - следующая строка/стра-\n"
                                               "     ница при просмотре конфигурации и т.п.\n"
                                               " 11. «Ctrl+F» - открытие окна поиска.\n"
                                        )
                else:
                    self.textbox.insert("end", " \n ● «NetTerm»:\n  \n"
                                              " In this section of the program, the user\n"
                                              " can connect to devices using the SSH and\n"
                                              " Telnet protocols, configure devices, etc.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● Hotkeys:\n \n"
                                               " 1. «Esc» - clear the command input field.\n"
                                               " 2. «Tab, Ctrl+Tab, Shift+Tab» - navigation\n"
                                               "     between fields.\n"
                                               " 3. «Enter» - enter a command if he cursor\n"
                                               "     is in the input field.\n"
                                               " 4. «Ctrl+Del» - clear terminal.\n"
                                               " 5. «F6» - close connection.\n"
                                               " 6. «F8» - collapse/expand the terminal\n"
                                               "     settings panel.\n"
                                               " 7. «F9» - output help for the terminal.\n"
                                               " 8. «↓/↑» - select a command from the last\n"
                                               "     10 if the cursor is in the input field.\n"
                                               " 9. «Q/Ctrl+C» - exit/finish viewing the\n"
                                               "     configuration, etc.\n"
                                               " 10. «Space/Return» - next line/page when\n"
                                               "     viewing configuration etc.\n"
                                               " 11. «Ctrl+F» - opening the search window.\n"
                                        )
                self.textbox.configure(state = "disabled")
            self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))
            self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units"))

            if tab_name == "Подключение":
                self.textbox = ctk.CTkTextbox(self.frame_1, width=100, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"))
                self.textbox.grid(row = 1, column = 1, padx = 0, pady = (0,0), sticky = "nsew")
                if self.language == "Русский":
                    self.textbox.insert("end"," \n ● Вкладка «Подключение»:\n  \n"
                                              " В этом разделе программы пользователь\n"
                                              " может проверять доступность устройств, а\n"
                                              " также подключаться к ним по протоколам:\n"
                                              " telnet, ssh, http и https." )
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● «Горячие» клавиши вкладки:\n \n"
                                               " 1. «F1-F4» - навигация между вкладками.\n"
                                               " 2. «Esc» - выход из окна/программы.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - навигация\n"
                                               "     между полями ввода.\n"
                                               " 4. «Enter» - выполнить, если курсор в\n"
                                               "     поле ввода.\n"
                                               " 5. « ↓ » - вызов выпадающего списка,\n"
                                               "     если курсор в поле ввода.\n"
                                               " 6. «ПКМ/Esc» - покинуть поле ввода.\n"
                                               " 7. «Del» - полная очистка поля ввода\n"
                                               "     и сброс параметров, если курсор был\n"
                                               "     внутри него.\n"
                                               " 8. «Ctrl+Del» - очистка поля вывода.\n"
                                               " 9. «F9» - вывод справки для текущей\n"
                                               "     вкладки.\n"
                                               " 10. «↓/↑» - скролл консольного вывода.\n"
                                        )
                else:
                    self.textbox.insert("end", " \n ● «Connection» tab:\n  \n"
                                               " In this section of the program, the user\n"
                                               " can check the availability of devices,\n"
                                               " as well as connect to them via proto-\n"
                                               " cols: telnet, ssh, http and https.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● Hotkeys:\n \n"
                                               " 1. «F1-F4» - navigation between tabs.\n"
                                               " 2. «Esc» - exit window/program.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - navigation\n"
                                               "     between fields.\n"
                                               " 4. «Enter» - enter a command if he cursor\n"
                                               "     is in the input field.\n"
                                               " 5. « ↓ » - call a drop-down list if the\n"
                                               "     cursor is in the selection field.\n"
                                               " 6. «RMB/Esc» - leave the input field.\n"
                                               " 7. «Del» - Completely clears the input\n"
                                               "     field and resets the parameters if\n"
                                               "     the cursor was inside it.\n"
                                               " 8. «Ctrl+Del» - clear the output field.\n"
                                               " 9. «F9» - Display help for the current\n"
                                               "     tab.\n"
                                               " 10. «↓/↑» - scroll console output.\n"
                                        )
                self.textbox.configure(state = "disabled")
            self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))
            self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units"))

            if tab_name == "Параметры сети":
                self.textbox = ctk.CTkTextbox(self.frame_1, width=100, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"))
                self.textbox.grid(row = 1, column = 1, padx = 0, pady = (0,0), sticky = "nsew")
                if self.language == "Русский":
                    self.textbox.insert("end", " \n ● Вкладка «Параметры сети»:\n  \n"
                                               " В этом разделе программы пользователь\n"
                                               " может просматривать информацию о те-\n"
                                               " кущей конфигурации сети/адаптера, а\n"
                                               " также менять сетевые настройки для\n"
                                               " выбранного адаптера.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● «Горячие» клавиши вкладки:\n \n"
                                               " 1. «F1-F4» - навигация между вкладками.\n"
                                               " 2. «Esc» - выход из окна/программы.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - навигация\n"
                                               "     между полями ввода.\n"
                                               " 4. «Enter» - выполнить, если курсор в\n"
                                               "     поле ввода.\n"
                                               " 5. « ↓ » - вызов выпадающего списка,\n"
                                               "     если курсор в поле ввода.\n"
                                               " 6. «ПКМ/Esc» - покинуть поле ввода.\n"
                                               " 7. «Del» - полная очистка поля ввода \n"
                                               "     и сброс параметров, если курсор был\n"
                                               "     внутри него.\n"
                                               " 8. «Ctrl+Del» - очистка поля вывода.\n"
                                               " 9. «F9» - вывод справки для текущей\n"
                                               "     вкладки.\n"
                                               " 10. «↓/↑» - скролл консольного вывода.\n"
                                        )
                else:
                    self.textbox.insert("end", " \n ● «Network Settings» tab:\n  \n"
                                               " n this section of the program, the\n"
                                               " user can view information about the\n"
                                               " current network/adapter configuration,\n"
                                               " as well as change the network settings\n"
                                               " for the selected adapter.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● Hotkeys:\n \n"
                                               " 1. «F1-F4» - navigation between tabs.\n"
                                               " 2. «Esc» - exit window/program.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - navigation\n"
                                               "     between fields.\n"
                                               " 4. «Enter» - enter a command if he cursor\n"
                                               "     is in the input field.\n"
                                               " 5. « ↓ » - call a drop-down list if the\n"
                                               "     cursor is in the selection field.\n"
                                               " 6. «RMB/Esc» - leave the input field.\n"
                                               " 7. «Del» - Completely clears the input\n"
                                               "     field and resets the parameters if\n"
                                               "     the cursor was inside it.\n"
                                               " 8. «Ctrl+Del» - clear the output field.\n"
                                               " 9. «F9» - Display help for the current\n"
                                               "     tab.\n"
                                               " 10. «↓/↑» - scroll console output.\n"
                                        )
                self.textbox.configure(state="disabled")

            if tab_name == "База адресов":
                self.textbox = ctk.CTkTextbox(self.frame_1, width=100, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"))
                self.textbox.grid(row = 1, column = 1, padx = 0, pady = (0,0), sticky = "nsew")
                if self.language == "Русский":
                    self.textbox.insert("end", " \n ● Вкладка «База адресов»:\n  \n"
                                               " В этом разделе программы пользователь \n"
                                               " может просматривать и редактировать \n"
                                               " базы данных с устройствами. Также пре-\n"
                                               " дусмотрен поиск в базе и возможность\n"
                                               " подключения к устройствам из БД. Для \n"
                                               " этого необходимо поключиться к БД, а\n"
                                               " затем, кликом мыши, выбрать запись\n"
                                               " для дальнейших операций над ней.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● «Горячие» клавиши вкладки:\n \n"
                                               " 1. «F1-F4» - навигация между вкладками.\n"
                                               " 2. «Esc» - выход из окна/программы.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - навигация\n"
                                               "     между полями ввода.\n"
                                               " 4. «Enter» - выполнить, если курсор в\n"
                                               "     поле ввода.\n"
                                               " 5. « ↓ » - вызов выпадающего списка,\n"
                                               "     если курсор в поле ввода.\n"
                                               " 6. «ПКМ/Esc» - покинуть поле ввода.\n"
                                               " 7. «Insert» - создание новой записи.\n"
                                               " 8. «Enter/Double-click» по записи в\n"
                                               "     режиме выбора - подключение.\n"
                                               " 9. «BackSpace/Delete» - удаление записи в\n"
                                               "     режиме выбора.\n"
                                               " 10. «СКМ/Клик за пределами поля БД» - от-\n"
                                               "     мена выбора записи, если она была\n"
                                               "     выбрана.\n"
                                               " 11. «Del» - полная очистка поля ввода,\n"
                                               "     если курсор внутри него, или уда-\n"
                                               "     ление записи в режиме выбора.\n"
                                               " 12. «F5» - обновление базы данных.\n"
                                               " 13. «F6» - разрыв соединения с БД.\n"
                                               " 14. «F7» - выбрать первую запись в БД.\n"
                                               " 15. «F8/ПКМ» - редактирование записи\n"
                                               "     в режиме выбора.\n"
                                               " 16. «F9» - вывод справки для текущей\n"
                                               "     вкладки.\n"
                                               " 17. «↓/↑» - выбор следующей/предыдущей\n"
                                               "     записи в режиме выбора.\n"
                                               " 18. «⟵/⟶» - скролл влево/вправо в ре-\n"
                                               "     жиме выбора.\n"
                                               " 19. «Ctrl+Del» - очистка поля вывода.\n"
                                        )
                else:
                    self.textbox.insert("end", " \n ● «Address Database» tab:\n  \n"
                                               " In this section of the program, the user\n"
                                               " can view and edit databases with devi-\n"
                                               " ces. It also provides a search in the\n"
                                               " database and the ability to connect to\n"
                                               " to devices from the DB. To do this, you\n"
                                               " need to connect to the DB, and then, with\n"
                                               " a mouse click, select a record for fur-\n"
                                               " ther operations on it.")
                    self.textbox.insert("end", "\n \n ──────────────────── \n")
                    self.textbox.insert("end", " \n ● Hotkeys:\n \n"
                                               " 1. «F1-F4» - navigation between tabs.\n"
                                               " 2. «Esc» - exit window/program.\n"
                                               " 3. «Tab, Ctrl+Tab, Shift+Tab» - navigation\n"
                                               "     between fields.\n"
                                               " 4. «Enter» - enter a command if he cursor\n"
                                               "     is in the input field.\n"
                                               " 5. « ↓ » - call a drop-down list if the\n"
                                               "     cursor is in the selection field.\n"
                                               " 6. «RMB/Esc» - leave the input field.\n"
                                               " 7. «Insert» - create a new record.\n"
                                               " 8. «Enter/Double-click» on the entry\n"
                                               "     in the selection mode - connection\n"
                                               " 9. «BackSpace/Delete» - delete a record\n"
                                               "      in selection mode\n"
                                               " 10. «SMB/Click outside the DB field» -\n"
                                               "     - deselects a record if it was se-\n"
                                               "     lected.\n"
                                               " 11. «Del» - Clear the input field comp-\n"
                                               "     letely if the cursor is inside it, or\n"
                                               "     delete the entry in selection mode.\n"
                                               " 12. «F5» - refresh database.\n"
                                               " 13. «F6» - close connection with DB.\n"
                                               " 14. «F7» - select the first record in DB.\n"
                                               " 15. «F8/ПКМ» - editing a record in se-\n"
                                               "     lection mode\n"
                                               " 16. «F9» - Display help for the current\n"
                                               "     tab.\n"
                                               " 17. «↓/↑» - select next/previous record\n"
                                               "     n selection mode.\n"
                                               " 18. «⟵/⟶» - scroll left/right in selection\n"
                                               "      mode.\n"
                                               " 19. «Ctrl+Del» - clear the output field.\n"
                                        )
                self.textbox.configure(state="disabled")

        def close_window():
            self.grab_release()
            self.destroy()

        tab=var
        self.language = language
        self.title("Информация")
        self.geometry("370x370")
        self.attributes("-alpha", opacity)
        self.lift()  # lift window on top
        #self.attributes("-topmost", True)  # stay on top
        self.resizable(False, False)
        self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 370
        window_height = 370
        RealSize = NetConWindows.ScreenCurrent()
        self.scaling_factor = RealSize.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.bind('<Escape>', lambda close: close_window())
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")
        self.iconbitmap(path_img + "img/sprav.ico")

        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=25, padx=25, fill="both", expand=True)
        self.frame_1.grid_columnconfigure((1), weight=1)
        self.frame_1.grid_rowconfigure((1), weight=1)

        show_help_for_tab(tab)

        self.bind("<Return>", lambda x: close_window())
        self.button_2 = ctk.CTkButton(master=self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), text="Назад", width=100, fg_color="#1F538D", border_width=0, command=lambda: close_window())
        self.button_2.grid(row=2, column=1, padx=(0, 0), pady=(10, 0), ipady = 3, sticky="nsew")

        self.master_window = master
        self.update_position()
        self.bind("<Configure>", self.update_position)

        if self.language != "Русский":
            self.title("Information")
            self.button_2.configure(text="Back")

    def update_position(self, event=None):
        master_x = self.master_window.winfo_x()
        master_y = self.master_window.winfo_y()
        master_width = self.master_window.winfo_width()
        master_height = self.master_window.winfo_height()
        search_width = self.winfo_width()
        search_height = self.winfo_height()
        x = master_x + (master_width - search_width) // 2
        y = master_y + (master_height - search_height) // 2
        self.geometry(f"+{x}+{y}")
