import threading
import webbrowser
import tkinter
import pyautogui
import updated_ctk as ctk
from PIL import Image
import os
import sqlite3
import re
import subprocess
import pathlib
import time
import ctypes
import sys
import psutil
from NetConWindows import *

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        #Загрузка файла конфигурации окна приложения
        def load_config():
            home_dir = pathlib.Path.home()
            netcon_dir = home_dir / "NetCon"
            config_file = netcon_dir / "config.txt"
            default_values = ["English", "None", "Dark", "100%"]  # Параметры по умолчанию
            try:
                if not os.path.exists(config_file):
                    config_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(config_file, "w") as f:
                        f.write(" ".join(default_values))
                with open(config_file, "r") as f:
                    line = f.readline().strip()
                    values = line.split()
                return values
            except Exception as e:
                return default_values

        # Заипсь в файл конфигурации окна приложения
        def save_config(param1, param2, param3, param4):
            home_dir = pathlib.Path.home()
            netcon_dir = home_dir / "NetCon"
            config_file = netcon_dir / "config.txt"
            with open(config_file, "w") as f:
                f.write(f"{param1} {param2} {param3} {param4}")

        def after_close_terminals():
            self.deiconify()
            self.listbox = CTkListbox(self.tabview.tab("База адресов"), fg_color=("white", "#333333"), border_width=0, button_color=("#e5e5e5", "#212121"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="normal"), orientation="vertical", orientation2="horizontal", width=560)
            self.listbox.grid(row=3, rowspan=6, column=2, columnspan=4, padx=(12, 20), pady=(0, 0), sticky="nsew")
            self.listbox.bind('<<ListboxSelect>>', lambda list_var: open_con_listbox())
            self.hello_button_1.grid(row=5, column=1, padx=(520, 77), pady=(10, 0), sticky="we")
            self.label_hello.grid(row=2, column=1, padx=(115, 0), pady=(0, 0), sticky="w")
            self.label_hello2.grid(row=3, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
            self.label_hello3.grid(row=4, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
            self.label_hello4.grid(row=5, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
            self.hello_line2.grid(row=6, column=1, columnspan=1, padx=(120, 120), pady=(0, 0), sticky="nsew")
            self.hello_button_1.grid(row=5, column=1, padx=(530, 115), pady=(10, 0), sticky="we")
            self.hello_button_2.grid(row=7, column=1, padx=(115, 115), pady=(5, 120), sticky="ew", ipady=5)
            self.label_line2.grid(row=3, column=1, columnspan=9, padx=24, pady=(10, 10))
            if self.combobox_4.get() != "":
                refresh_db_after_scale(name_db, self.listbox)

        # Подключение telnet/web
        def clicked2(radio):
            s_radio = radio.get()
            if s_radio == 3:
                self.after(150, lambda: self.focus_set())
                if self.scaling_optionemenu.get() != "100%":
                    self.scaling_optionemenu.set(value="100%")
                    ctk.set_widget_scaling(1)
                self.iconify()
                serial_con = SerialTerminal()
                serial_con(self.appearance_mode_optionemenu.get(), self.opacity, self.language)
                clear_entry_telnet(self.entry3, self.radio_var)
                if serial_con.get() == 1:
                    self.bind('<Escape>', lambda close: close_app())
                    self.scaling_optionemenu.set(value="100%")
                    after_close_terminals()
            elif str(x3.get()) == "...":
                self.entry3.focus_set()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Поле не должно быть пустым!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity = self.opacity, message='The field must not be empty!', title='Error', icon='cancel')
            else:
                ip_var = str(x3.get())
                list_ip = ip_var.split(".")
                for i in range(len(list_ip)):  # Проверка на верность формата IP
                    if str(list_ip[i]) == "":
                        self.entry3.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP-address format!', title='Error', icon='cancel')
                    elif int(list_ip[i]) > 255:
                        self.entry3.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP-address format!', title='Error', icon='cancel')
                if s_radio == 1:
                    self.after(150, lambda: self.focus_set())
                    select_terminal = SelectTerminal()
                    select_terminal(self.appearance_mode_optionemenu.get(),str(x3.get()),"Telnet", self.scaling_optionemenu.get(),self, self.opacity, self.language)
                    if select_terminal.get() == 1:
                        self.bind('<Escape>', lambda close: close_app())
                        self.scaling_optionemenu.set(value="100%")
                        after_close_terminals()
                elif s_radio == 2:
                    self.after(150, lambda: self.focus_set())
                    select_terminal = SelectTerminal()
                    select_terminal(self.appearance_mode_optionemenu.get(), str(x3.get()), "SSH", self.scaling_optionemenu.get(),self, self.opacity, self.language)
                    if select_terminal.get() == 1:
                        self.bind('<Escape>', lambda close: close_app())
                        self.scaling_optionemenu.set(value="100%")
                        after_close_terminals()
                elif s_radio == 4:
                    self.after(150, lambda: self.focus_set())
                    web_con = SelectWeb()
                    web_con(str(x3.get()),self, self.opacity, self.language)
                    if web_con.get() == 1:
                        self.bind('<Escape>', lambda close: close_app())

        # Ping (это БАЗАААААА)
        def execute_cmd(ip, type_con, entry):
            if ip == "...":
                entry.focus_set()
                if self.language == "Русский":
                    return CTkMessagebox(opacity=self.opacity, message='Поле не должно быть пустым!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='The field must not be empty!', title='Error', icon='cancel')
            else:
                ip_var = ip
                list_ip = ip_var.split(".")
                for i in range(len(list_ip)):  # Проверка на верность формата IP
                    if str(list_ip[i]) == "":
                        entry.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP-address format!', title='Error', icon='cancel')
                    if int(list_ip[i]) > 255:
                        entry.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP-address format!', title='Error', icon='cancel')
                right_click()
                self.after(200, lambda: self.unbind('<Escape>'))
                message5 = Loading()
                message5(ip, self.textbox, type_con, self, self.opacity, self.language)
                #if "win" not in self.combobox_ping.get() and "win" not in self.combobox_tracert.get():
                self.entry1.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
                self.entry_tracert.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
                self.combobox_ping.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                self.combobox_tracert.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                self.main_button_1.configure(state="disabled", fg_color="#14375e")
                self.main_button_2.configure(state="disabled", fg_color="#14375e")
                self.clear_btn_ip.configure(state="disabled", fg_color="#ab590c", image=clear_disabled_img)
                self.clear_btn_tracert.configure(state="disabled", fg_color="#ab590c", image=clear_disabled_img)
                # костыль для того чтобы после остановки пинга на esc бинд на эту же клавишу в основной проге не возвращался сразу(хуй знает как но это работает)
                if message5.get() == 1:
                    self.textbox.configure(state="disabled")
                    self.bind('<Escape>', lambda close: close_app())
                    self.entry1.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                    self.entry_tracert.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                    self.combobox_ping.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
                    self.combobox_tracert.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
                    self.main_button_1.configure(state="normal", fg_color="#1F538D")
                    self.main_button_2.configure(state="normal", fg_color="#1F538D")
                    self.clear_btn_ip.configure(state="normal", fg_color="#de710b", image=clear_img)
                    self.clear_btn_tracert.configure(state="normal", fg_color="#de710b", image=clear_img)
                    return right_click()

        # IPconfig (Пригодится)
        def execute_cmd2(command):
            try:
                if command == "ipconfig Выберите из списка или введите...":
                    command = "ipconfig"
                if command == "ipconfig Select from the list or enter...":
                    command = "ipconfig"
                cmd_output2 = subprocess.check_output(command, shell=True).decode('cp866')
                self.textbox2.configure(state='normal')
                self.textbox2.insert('end', " \n")
                self.textbox2.insert('end', "    〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
                self.textbox2.insert('end', " \n")
                if self.language == "Русский":
                    self.textbox2.insert('end', "                                             Текущая конфигурация сети:\n")
                else:
                    self.textbox2.insert('end', "                                             Current network configuration:\n")
                self.textbox2.insert('end', " \n")
                self.textbox2.insert('end', "    〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
                self.textbox2.insert('end', cmd_output2)
                self.textbox2.insert('end', " \n")
                self.textbox2.insert('end', "    〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
                self.textbox2.see('end')
                self.textbox2.configure(state='disabled')
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Готово! Смотрите "Console log"', title='Успех', icon='check'), right_click()
                else:
                    return CTkMessagebox(opacity = self.opacity, message='Ready! See the "Console log"', title='Success', icon='check'), right_click()
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Повторите ввод атрибута!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity = self.opacity, message='Re-enter the attribute!', title='Error', icon='cancel')


        # Адаптер (вывод его имени тупа тока)
        def execute_cmd3(command):
            try:
                if str(x4.get()) == "" and self.language == "Русский" or str(x4.get()) == "Выберите из списка или введите...":
                    self.combobox_2.focus_set()
                    return CTkMessagebox(opacity = self.opacity, message='Поле не должно быть пустым!', title='Ошибка', icon='cancel')
                elif str(x4.get()) == ""  and self.language == "English" or str(x4.get()) == "Select from the list or enter...":
                    self.combobox_2.focus_set()
                    return CTkMessagebox(opacity = self.opacity, message='The field must not be empty!', title='Error', icon='cancel')
                else:
                    cmd_output3 = subprocess.check_output(command, shell=True).decode('cp866')
                    self.textbox2.configure(state='normal')
                    self.textbox2.insert('end', cmd_output3)
                    self.textbox2.insert('end', "    〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
                    self.textbox2.see('end')
                    self.textbox2.configure(state='disabled')
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Готово! Смотрите "Console log"', title='Успех', icon='check'), right_click()
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='Ready! See the "Console log"', title='Success', icon='check'), right_click()
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Повторите ввод имени!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Re-enter the name!', title='Error', icon='cancel')

        # Применение новых настроек адаптера
        def execute_cmd3_1(command, dhcp_flag = False):
            message = Loading_adapter()
            message(command, self.textbox2, self.combobox_3, dhcp_flag, self, self.opacity, self.language)
            return right_click()

        # Параметры адаптера
        def execute_cmd4(command):
            if str(x8.get()) == "" or str(x5.get()) == "..." or str(x6.get()) == "..." or str(x7.get()) == "...":
                self.combobox_3.focus_set()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Все поля должны быть заполнены!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='All fields must be filled in!', title='Error', icon='cancel')
            else:
                ip_var = str(x5.get())
                mask_var = str(x6.get())
                gate_var = str(x7.get())
                list_ip = ip_var.split(".")
                list_mask = mask_var.split(".")
                list_gate = gate_var.split(".")
                for i in range(len(list_ip)):  # Проверка на верность формата IP
                    if str(list_ip[i]) == "":
                        self.entry6.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP address format!', title='Error', icon='cancel')
                    elif int(list_ip[i]) > 255:
                        self.entry6.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect IP address format!', title='Error', icon='cancel')
                    if str(list_mask[i]) == "":
                        self.entry7.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Неверный формат Маски!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect Mask format!', title='Error', icon='cancel')
                    elif int(list_mask[i]) > 255:
                        self.entry7.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат Маски!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect Mask format!', title='Error', icon='cancel')
                    if str(list_gate[i]) == "":
                        self.entry8.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат Шлюза!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect Gateway format!', title='Error', icon='cancel')
                    if int(list_gate[i]) > 255:
                        self.entry8.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity=self.opacity, message='Неверный формат Шлюза!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Incorrect Gateway format!', title='Error', icon='cancel')
                #os.system('start cmd /c ' + command)
                subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                execute_cmd3_1(str(x8.get()))  # САМ ПОНЯЛ КАКОЕ ГОВНО НАПИСАЛ?
                return right_click()

        # Включение DHCP (нахуй с пляжа)
        def execute_cmd5(command):
            if str(x8.get()) == "":
                self.combobox_3.focus_set()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Поле «Имя» не должно быть пустым!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='The "Name" field should not be empty!', title='Ошибка', icon='cancel')
            else:
                if self.language == "Русский":
                    msg = CTkMessagebox(opacity = self.opacity, message='Вы уверены?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да")
                else:
                    msg = CTkMessagebox(opacity=self.opacity, message='Are you sure?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes")
                msg.focus_set()
                msg.button_1.configure(fg_color="#de710b", hover_color="#ab590c")
                response = msg.get()
                if response == "Отмена" or response == "Cancel":
                    return
                elif response == "Да" or response == "Yes":
                    try:
                        #os.system('start cmd /c ' + command)
                        subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        execute_cmd3_1(str(x8.get()), dhcp_flag=True)
                        return right_click()
                    except:
                        self.combobox_3.focus_set()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Повторите ввод имени!', title='Ошибка', icon='cancel')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='Re-enter the name!', title='Error', icon='cancel')

        # Очистка "console log" (понял вычеркиваем)
        def clear_text(textbox):
            self.focus_set()
            if self.tabview.get() == "База адресов" and textbox.get(0) != None:
                lock_states_and_binds_during_refresh()
                self.listbox.deactivate(0)
                self.unbind("<Double-Button-1>")
                self.bind("<Button-3>", lambda escape_entry: right_click())
                self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
                self.unbind("<BackSpace>")
                self.unbind("<Down>")
                self.unbind("<Up>")
                self.unbind("<Left>")
                self.unbind("<Right>")
                self.unbind("<Return>")
                self.unbind("<F8>")
                textbox.delete(0.0, 'end')
                return back_states_and_binds_after_refresh()
            else:
                textbox.configure(state="normal")
                textbox.delete(0.0, 'end')
                textbox.configure(state="disabled")

        # Очистка поля счета элементов в базе при нажатии кнопки очистки listbox (ты че брэдман)
        def clear_count():
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            self.textbox3.configure(state="disabled")

        # Очистка "Entry" с IP-адресами (не только) (заебись костыль, чисто выкрутился из ситуации неприятной)
        def clear_entry(entry):  # Замазка для комбобокса базы данных (всякие костылики хрумки нямки )
            self.previous_selected = None
            try:
                for i in range(0, len(entry.get())):
                    entry.delete(i)
                for i in range(0, len(entry.get())):
                    entry.delete(i)
                return entry.icursor(0), entry.xview(0)
            except:
                entry.set("")
                if not entry.is_focused:
                    entry.set_placeholder()


        # Очистка "Entry" с IP PING и атрибутом (бля ну ты жук внатуре, выкрутился х2)
        def clear_entry_ip(entry, combo):
            if combo.get() == " None " or combo.get() == "/d" or combo.get() == "/j":
                combo.set(value=" None ")
            else:
                combo.set(value="None")
            for i in range(0, len(entry.get())):
                entry.delete(i)
            for i in range(0, len(entry.get())):
                entry.delete(i)
            return entry.icursor(0), entry.xview(0)

        # Очистка "Entry" с IP TELNET и сбросом типа подключения (не надоело?)
        def clear_entry_telnet(entry, radio):
            radio.set(value=1)
            self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
            for i in range(0, len(entry.get())):
                entry.delete(i)
            for i in range(0, len(entry.get())):
                entry.delete(i)
            return entry.icursor(0), entry.xview(0)

        # Функция дисконнекта (пришлось разделить с обычной очисткой)
        def clear_entry_baza(entry):
            if self.tabview.get() == "База адресов" and entry.get() != "":
                if self.listbox.curselection() != None:
                    self.listbox.deactivate(0)
                self.previous_selected = None
                entry.set("")
                clear_count()
                clear_entry(self.combobox_4)
                entry.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                self.clear_btn3.configure(command=None)
                self.help_btn_tab3.configure(command=None)
                self.con_button.configure(state="disabled", fg_color="#14375e")
                self.search_button.configure(state="disabled", fg_color="#14375e")
                self.del_button.configure(state="disabled", fg_color="#ab590c")
                self.update_row_button.configure(state="disabled", fg_color="#14375e")
                self.add_button.configure(state="disabled", fg_color="#14375e")
                self.update_button.configure(state="disabled", fg_color="#14375e")
                self.textbox3.configure(state="disabled", border_color=("#8f8f8f", "#444444"))
                if self.language == "Русский":
                    self.combobox_5.configure(placeholder_text="Требуется подключение к БД...")
                else:
                    self.combobox_5.configure(placeholder_text="A database connection is required...")
                clear_entry(self.combobox_5)
                self.combobox_5.set_placeholder()
                self.combobox_5.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                self.clear_btn_baza.configure(state="disabled", fg_color="#ab590c", image=disconnect_disabled_img)
                self.clear_btn_search.configure(state="disabled", fg_color="#ab590c", image=clear_disabled_img)
                self.combobox_4.bind("<Delete>", lambda del_var: clear_entry(self.combobox_4))
                self.unbind("<Down>")
                self.unbind("<Up>")
                self.unbind("<Left>")
                self.unbind("<Right>")
                self.unbind("<Return>")
                self.unbind("<F6>")
                self.unbind("<F9>")
                self.unbind("<F5>")  # тута неточна
                #self.unbind("<Control-Delete>")
                self.unbind("<Insert>")
                self.unbind("<KeyPress-Control_L>")
                self.unbind("<KeyRelease-Control_L>")
                self.listbox.delete(0.0, 'end')
                entry.configure(state="normal", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"), command=lambda combo_var: combo_focus(entry, flag=1))
                entry.bind("<Return>", lambda combobox_4_var: show_db(name_db, self.listbox))
                self.main_button_6.configure(state="normal", fg_color="#1F538D")
                self.help_btn_tab3.configure(command=lambda: help(self.tabview.get()))
                self.clear_btn3.configure(command=lambda: [clear_text(self.listbox), clear_count()])
                if self.language == "Русский":
                    CTkMessagebox(opacity=self.opacity, message='Подключение закрыто!', title='Успех', icon='check')
                else:
                    CTkMessagebox(opacity=self.opacity, message='Connection is closed!', title='Success', icon='check')
                return self.after(100, lambda: [self.focus_set(), self.bind("<F9>", lambda open_help: help(self.tabview.get()))])
            else:
                return

        # Формат IP-аддреса для поля "Entry" (нереальная дрочка и попаболь)
        def entry_mask_check(text, valid, entry):
            ip = re.findall("^\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}$", text.get())
            if len(ip) != 1:
                text.set(valid[0])
            if ip:
                valid[0] = ip[0]
                # прыжок на некст 3 цифры
                cursor_position = entry.index("insert")
                index2 = ip[0][:cursor_position - 1].rfind(u".")
                if cursor_position - index2 == 4:
                    entry.icursor(cursor_position + 1)

        # Функция подключения к БД и вывода из нее информации в listbox, также подсчет элементов в ней (ща мы бля выведем твою так называемую БАЗУУУ)
        def show_db(name, listbox):
            check_db_eng_name(name)
            self.combobox_4.configure(state="readonly")
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.unbind("<Insert>")
            self.unbind("<KeyPress-Control_L>")
            self.unbind("<KeyRelease-Control_L>")
            self.unbind("<F5>")
            self.unbind("<F9>")
            #self.unbind("<Control-Delete>")
            self.combobox_4.unbind("<Delete>")
            self.combobox_4.unbind("<Return>")
            self.textbox3.delete(0.0, "end")
            #listbox.delete(0.0, "end")
            try:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
            except:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), 1000)
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address,name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                    cursor.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor.fetchone()[0]
                    self.textbox3.configure(state="normal", border_color=("#979da2", "#565b5e"))
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    self.con_button.configure(state="normal", fg_color="#1F538D")
                    self.search_button.configure(state="normal", fg_color="#1F538D")
                    self.del_button.configure(state="normal", fg_color="#de710b")
                    self.update_row_button.configure(state="normal", fg_color="#1F538D")
                    self.add_button.configure(state="normal", fg_color="#1F538D")
                    self.update_button.configure(state="normal", fg_color="#1F538D")
                    if self.language == "Русский":
                        self.combobox_5.configure(state="normal", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"), placeholder_text="Выберите из списка или введите...")
                    else:
                        self.combobox_5.configure(state="normal", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"), placeholder_text="Select from the list or enter...")
                    self.clear_btn_baza.configure(state="normal", fg_color="#de710b", image=disconnect_img)
                    self.clear_btn_search.configure(state="normal", fg_color="#de710b", image=clear_img)
                    self.combobox_4.configure(state="readonly", command=lambda combo_var: combo_focus(self.combobox_4, flag=2))
                    self.main_button_6.configure(state="disabled", fg_color="#14375e")
                    if self.tabview.get() != "База адресов":
                        nav_tab4()
                        self.unbind("<F5>")
                        self.unbind("<Insert>")
                        self.unbind("<KeyPress-Control_L>")
                        self.unbind("<KeyRelease-Control_L>")
                        #self.unbind("<Control-Delete>")
                    if self.language == "Русский":
                        CTkMessagebox(opacity=self.opacity, message=f'Подключение к БД: «{self.name}»\nпрошло успешно!', title='Успех', icon='check')
                    else:
                        CTkMessagebox(opacity=self.opacity, message=f'Connection to DB: «{self.eng_name}»\nwas successful!', title='Success', icon='check')
                    return self.after(100, lambda: self.focus_set()), self.after(120, lambda: [self.bind("<F6>", lambda del_var: clear_entry_baza(self.combobox_4)), self.bind("<Insert>", lambda insert_var: add_item(name_db, self.listbox)), self.bind("<KeyPress-Control_L>", on_ctrl_press), self.bind("<KeyRelease-Control_L>", on_ctrl_release), self.bind("<F5>", lambda refresh_var: refresh_db(name_db, self.listbox)), self.bind("<F9>", lambda open_help: help(self.tabview.get()))])
            except:
                self.combobox_4.configure(state="normal")
                self.after(150, lambda: [self.combobox_4.focus_set(), self.combobox_4.bind("<Return>", lambda combobox_4_var: show_db(name_db, self.listbox)), self.combobox_4.bind("<Delete>", lambda del_var: clear_entry(self.combobox_4))])
                if self.language == "Русский":
                    return CTkMessagebox(opacity=self.opacity, message='Такой БД не существует!\nПовторите ввод или выберите БД из списка.', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='This database does not exist!\nPlease re-enter or select a database from the list.', title='Error', icon='cancel')

        def lock_states_and_binds_during_refresh():
            antibug()  # Пока в тесте
            self.combobox_4.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
            self.clear_btn3.configure(command=None)
            self.help_btn_tab3.configure(command=None)
            self.update_button.configure(state="disabled", fg_color="#14375e")
            self.add_button.configure(state="disabled", fg_color="#14375e")
            self.update_row_button.configure(state="disabled", fg_color="#14375e")
            self.del_button.configure(state="disabled", fg_color="#ab590c")
            self.combobox_5.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
            self.search_button.configure(state="disabled", fg_color="#14375e")
            self.con_button.configure(state="disabled", fg_color="#14375e")
            self.after(50, lambda: self.clear_btn_baza.configure(state="disabled", fg_color="#ab590c", image=disconnect_disabled_img))
            self.after(150, lambda: self.clear_btn_search.configure(state="disabled", fg_color="#ab590c", image=clear_disabled_img))
            self.combobox_5.unbind("<Down>")
            self.combobox_5.unbind("<Return>")
            self.combobox_4.unbind("<Down>")
            self.unbind("<Insert>")
            self.unbind("<KeyPress-Control_L>")
            self.unbind("<KeyRelease-Control_L>")
            self.unbind("<F5>")
            self.unbind("<F6>")
            self.unbind("<F9>")
            #self.unbind("<Control-Delete>")
            # self.unbind("<F1>")
            # self.unbind("<F2>")
            # self.unbind("<F3>")
            # elf.unbind("<F4>")
            return self.after(180, lambda: [app.update(), app.update_idletasks()])  # пока спорно (профит был ток на интеле)

        def back_states_and_binds_after_refresh():
            self.combobox_4.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
            self.clear_btn3.configure(command=lambda: [clear_text(self.listbox), clear_count()])
            self.help_btn_tab3.configure(command=lambda: help(self.tabview.get()))
            self.con_button.configure(state="normal", fg_color="#1F538D")
            self.update_button.configure(state="normal", fg_color="#1F538D")
            self.add_button.configure(state="normal", fg_color="#1F538D")
            self.update_row_button.configure(state="normal", fg_color="#1F538D")
            self.del_button.configure(state="normal", fg_color="#de710b")
            self.combobox_5.configure(state="normal", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
            self.search_button.configure(state="normal", fg_color="#1F538D")
            self.after(50, lambda: self.clear_btn_baza.configure(state="normal", fg_color="#de710b", image=disconnect_img))
            self.after(150, lambda: self.clear_btn_search.configure(state="normal", fg_color="#de710b", image=clear_img))
            self.after(100, lambda: [self.combobox_4.bind("<Down>", lambda open_var: self.combobox_4._clicked()), self.bind("<F5>", lambda refresh_var: refresh_db(name_db, self.listbox)), self.bind("<F9>", lambda open_help: help(self.tabview.get()))])
            self.after(101, lambda: [self.bind("<Insert>", lambda insert_var: add_item(name_db, self.listbox)), self.bind("<KeyPress-Control_L>", on_ctrl_press), self.bind("<KeyRelease-Control_L>", on_ctrl_release)])
            self.after(102, lambda: [self.combobox_5.bind("<Down>", lambda open_var: self.combobox_5._clicked()), self.combobox_5.bind("<Return>", lambda combobox_5_var: search_item(name_db, self.listbox, self.combobox_5.get()))])
            self.after(103, lambda: [self.bind("<F6>", lambda del_var: clear_entry_baza(self.combobox_4))])
            # self.after(104, lambda: [self.bind("<F1>", lambda open_tab_var: nav_tab1()), self.bind("<F2>", lambda open_tab_var: nav_tab2()), self.bind("<F3>", lambda open_tab_var: nav_tab3()), self.bind("<F4>", lambda open_tab_var: nav_tab4())])
            if self.tabview.get() != "База адресов":
                nav_tab4()
                self.unbind("<F5>")
                self.unbind("<Insert>")
                self.unbind("<KeyPress-Control_L>")
                self.unbind("<KeyRelease-Control_L>")
                #self.unbind("<Control-Delete>")
            return self.after(180, lambda: [app.update(), app.update_idletasks()])  # пока спорно

        #Оптимизация удаления (для более быстрой работы с базой, заебала эта красота, слишком медленно было)
        def delete_items_in_batches(listbox, indices, batch_size):
            """Удаляет элементы из Listbox партиями."""
            for i in range(0, len(indices), batch_size):
                batch = indices[i:i + batch_size]
                for index in sorted(batch, reverse=True):  # Удаляем в обратном порядке, чтобы избежать смещения индексов
                    listbox.delete(index)
            self.listbox._parent_canvas.yview("moveto", 0)

        # Функция обновления БД (по сути повторный её вывод, но с другим уведомлением лол) (приколист)))))
        def refresh_db(name, listbox):
            check_db_eng_name(name)
            if self.listbox.curselection() != None:
                self.listbox.deactivate(0)
            lock_states_and_binds_during_refresh()
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            #listbox.delete(0.0, "end")
            try:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
            except:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), 1000)
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                    cursor.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor.fetchone()[0]
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Данные обновлены!', title='Успех', icon='check')
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='Data refreshed!', title='Success', icon='check')
            except:
                if self.language == "Русский":
                    CTkMessagebox(opacity=self.opacity, message='Требуется подключение к БД!', title='Ошибка', icon='cancel')
                else:
                    CTkMessagebox(opacity=self.opacity, message='A database connection is required!', title='Error', icon='cancel')
                return self.after(100, lambda: [self.combobox_4.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e")), self.combobox_4.bind("<Down>", lambda open_var: self.combobox_4._clicked())]), self.bind("<F5>", lambda refresh_var: refresh_db(name_db, self.listbox)), self.after(100, lambda: [self.bind("<Insert>", lambda insert_var: add_item(name_db, self.listbox)), self.bind("<KeyPress-Control_L>", on_ctrl_press), self.bind("<KeyRelease-Control_L>", on_ctrl_release)]), self.after(100, lambda: [self.combobox_5.bind("<Down>", lambda open_var: self.combobox_5._clicked()), self.combobox_5.bind("<Return>", lambda combobox_5_var: search_item(name_db, self.listbox, self.combobox_5.get()))]), self.after(100, lambda: [self.bind("<F6>", lambda del_var: clear_entry_baza(self.combobox_4))])

        # Обновление без хуйни (почти) для поиска
        def refresh_db_after_search(name, listbox):
            check_db_eng_name(name)
            if self.listbox.curselection() != None:
                self.listbox.deactivate(0)
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подсТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                    cursor.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor.fetchone()[0]
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    if self.language == "Русский":
                        CTkMessagebox(opacity=self.opacity, message='Ничего не найдено!\nПовторите поиск.', title='Ошибка', icon='cancel')
                    else:
                        CTkMessagebox(opacity=self.opacity, message='Nothing was found!\nRepeat the search.', title='Error', icon='cancel')
                    return self.after(195, lambda: self.combobox_5.focus_set())
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity=self.opacity, message='Требуется подключение к БД!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='A database connection is required!', title='Error', icon='cancel')

        # Обновление без хуйни (почти), используется при выборе базы уже после подключения к первой
        def refresh_db_after_reconnect(name, listbox):
            check_db_eng_name(name)
            if self.listbox.curselection() != None:
                self.listbox.deactivate(0)
            lock_states_and_binds_during_refresh()
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            #listbox.delete(0.0, "end")
            try:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
            except:
                delete_items_in_batches(self.listbox, list(range(self.listbox.size())), 1000)
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                    cursor.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor.fetchone()[0]
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message=f'Вы успешно переподключились к\nБД: «{self.name}»!', title='Успех', icon='check')
                    else:
                        return CTkMessagebox(opacity=self.opacity, message=f'You have successfully reconnected \nto the DB: «{self.eng_name}»!', title='Success', icon='check')
            except:
                return

        def check_db_eng_name(name):
            self.name = name.get()
            self.eng_name = name.get()
            if name.get() == "Switches":
                self.name = "Коммутаторы"
            elif name.get() == "Routers":
                self.name = "Маршрутизаторы"
            elif name.get() == "Multiplexers":
                self.name = "Мультиплексоры"
            elif name.get() == "Power supply":
                self.name = "Электропитание"
            elif name.get() == "Phones":
                self.name = "Телефоны"
            elif name.get() == "Other":
                self.name = "Другое"

        # Обновление внатуре без хуйни (отвечаю) для скалинг ивента (после того как заново отрисовали листбоксы поске изм-я скейла)
        def refresh_db_after_scale(name, listbox):
            check_db_eng_name(name)
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            #listbox.delete(0.0, "end")
            delete_items_in_batches(self.listbox, list(range(self.listbox.size())), 1000)
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                    cursor.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor.fetchone()[0]
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
            except:
                return

        # Функция выбора элемента в списке lisbox (содержащем БД) и последующего подключения (ультаа)
        def selected_item():
            self.unbind("<Double-Button-1>")
            try:
                member = self.listbox.curselection()
                list_member = self.listbox.get(member)
                s = " "
                s2 = (s.join(list_member))
                head, sep, tail = s2.partition(s)
                con_type_window = SelectCon()
                con_type_window(head, self.appearance_mode_optionemenu.get(), self.scaling_optionemenu.get(), self, self.opacity, self.language)
                if con_type_window.get() == 1:
                    self.bind('<Escape>', lambda close: close_app())
                    self.scaling_optionemenu.set(value="100%")
                    after_close_terminals()
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Выберите элемент для подключения!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Select an item to connect!', title='Error', icon='cancel')

        # Функция удания элемента из БД (вывод обновленной базы после удаления) (осторожнее шевели ручками)
        def delete_item(name, listbox):
            check_db_eng_name(name)
            self.unbind("<Double-Button-1>")
            self.previous_selected = None
            try:
                member = self.listbox.curselection()
                list_member = self.listbox.get(member)
                s = " "
                s2 = (s.join(list_member))
                head, sep, tail = s2.partition(s)
                sql_string = ('"' + head + '"')
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Выберите элемент для удаления!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Select the item to delete!', title='Error', icon='cancel')

            if self.language == "Русский":
                msg = CTkMessagebox(opacity = self.opacity, message='Вы уверены?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да")
            else:
                msg = CTkMessagebox(opacity=self.opacity, message='Are you sure?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes")
            msg.focus_set()
            msg.button_1.configure(fg_color="#de710b", hover_color="#ab590c")
            response = msg.get()
            # msg.option_text_1 = "Да"
            if response == "Отмена" or response == "Cancel":
                return simulate_ctrl_release()
            if response == "Да" or response == "Yes":
                try:
                    with sqlite3.connect("db/" + self.name + ".db") as db:
                        lock_states_and_binds_during_refresh()
                        cursor = db.cursor()
                        query = 'DELETE FROM net WHERE ip_address =' + sql_string
                        cursor.execute(query)
                        db.commit()
                        cursor.close()
                        cursor2 = db.cursor()
                        cursor2.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                        self.textbox3.configure(state="normal")
                        self.textbox3.delete(0.0, "end")
                        #listbox.delete(0.0, "end")
                        delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        list2 = cursor2.fetchall()
                        for member in list2:
                            listbox.insert("END", member)
                        cursor2.execute('SELECT COUNT(*) FROM net')
                        self.total_users = cursor2.fetchone()[0]
                        self.textbox3.insert('end', self.total_users)
                        self.textbox3.configure(state="disabled")
                        cursor2.close()
                        back_states_and_binds_after_refresh()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Данные успешно удалены!', title='Успех', icon='check')
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='The data has been successfully deleted!', title='Success', icon='check')
                except:
                    self.previous_selected = None
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='База данных пуста!', title='Ошибка', icon='cancel')
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='The database is empty!', title='Error', icon='cancel')

        # Массовое удаление выделения на кантроул (геноцид.)
        def delete_items(name, listbox):
            check_db_eng_name(name)
            self.unbind("<Double-Button-1>")
            self.previous_selected = None
            members = self.listbox.curselection()
            count = len(members)
            if self.language == "Русский":
                if count == 0:
                    simulate_ctrl_release()
                    return CTkMessagebox(opacity=self.opacity, message='Выберите элементы для удаления!', title='Ошибка', icon='cancel', multiselection_on=True)
            else:
                if count == 0:
                    simulate_ctrl_release()
                    return CTkMessagebox(opacity=self.opacity, message='Select any items to delete!', title='Error', icon='cancel', multiselection_on=True)
            if self.language == "Русский":
                msg = CTkMessagebox(opacity=self.opacity, message=f'Вы уверены что хотите\nудалить {count} выбранных элементов?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да", multiselection_on=True)
            else:
                msg = CTkMessagebox(opacity=self.opacity, message=f'Are you sure you want\nto delete {count} selected items?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes", multiselection_on=True)
            msg.focus_set()
            msg.button_1.configure(fg_color="#de710b", hover_color="#ab590c")
            response = msg.get()
            if response == "Отмена" or response == "Cancel":
                return simulate_ctrl_release()
            if response == "Да" or response == "Yes":
                simulate_ctrl_release()
                sql_strings = []
                for index in members:
                    list_member = self.listbox.get(index)
                    s = " "
                    s2 = (s.join(list_member))
                    head, sep, tail = s2.partition(s)
                    sql_string = ('"' + head + '"')
                    sql_strings.append(sql_string)
                try:
                    with sqlite3.connect("db/" + self.name + ".db") as db:
                        lock_states_and_binds_during_refresh()
                        for sql_string in sql_strings:
                            cursor = db.cursor()
                            query = 'DELETE FROM net WHERE ip_address =' + sql_string
                            cursor.execute(query)
                            db.commit()
                            cursor.close()
                        cursor2 = db.cursor()
                        cursor2.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                        self.textbox3.configure(state="normal")
                        self.textbox3.delete(0.0, "end")
                        #listbox.delete(0.0, "end")
                        delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        list2 = cursor2.fetchall()
                        for member in list2:
                            listbox.insert("END", member)
                        cursor2.execute('SELECT COUNT(*) FROM net')
                        self.total_users = cursor2.fetchone()[0]
                        self.textbox3.insert('end', self.total_users)
                        self.textbox3.configure(state="disabled")
                        cursor2.close()
                        back_states_and_binds_after_refresh()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Данные успешно удалены!', title='Успех', icon='check', multiselection_on=True)
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='The data has been successfully deleted!', title='Success', icon='check', multiselection_on=True)
                except:
                    self.previous_selected = None
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='База данных пуста!', title='Ошибка', icon='cancel', multiselection_on=True)
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='The database is empty!', title='Error', icon='cancel', multiselection_on=True)




        # Функция добавления нового значения в БД (проверка на повторный ввод IP и фокус на дубликате в базе если есть,
        # обновление базы и фокус на только что добавленном элементе) (ну и брээээд)
        def add_item(name, listbox):
            check_db_eng_name(name)
            self.previous_selected = None
            if self.language == "Русский":
                dialog = InputDialog(title="Создание записи", name_db=self.name,master = self, opacity = self.opacity, language=self.language)
            else:
                dialog = InputDialog(title="Create record", name_db=self.name, master=self, opacity=self.opacity, language=self.language)
            s = " "
            s2 = dialog.get_input()
            head, sep, tail = s2.partition(s)
            if s2 == "ErrorMessage":
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='«IP-адрес» и «Имя устройства» обязательны для заполнения!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='"IP address" and "Device name" are required!', title='Error', icon='cancel')
            elif s2 == "ErrorMessage2":
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Incorrect IP address format!', title='Error', icon='cancel')
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            try:
                with (sqlite3.connect("db/" + self.name + ".db") as db):
                    lock_states_and_binds_during_refresh()
                    cursor = db.cursor()
                    cursor2 = db.cursor()
                    cursor3 = db.cursor()
                    cursor3.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    #listbox.delete(0.0, "end")
                    delete_items_in_batches(self.listbox, list(range(self.listbox.size())), 1000)
                    list2 = cursor3.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                        string = "".join(member)
                        ip_check, seps, name_check = string.partition(s)
                        if head == ip_check:
                            m_index = list2.index(member)
                            try:
                                listbox.move_up(m_index)
                                listbox.activate(0)
                            except:
                                listbox.activate(0)
                            back_states_and_binds_after_refresh()
                            self.textbox3.configure(state="disabled")
                            if self.language == "Русский":
                                return CTkMessagebox(opacity = self.opacity, message='Устройство с таким IP-адресом уже есть в базе!', title='Ошибка', icon='cancel'), self.after(115, lambda: listbox.select(0))
                            else:
                                return CTkMessagebox(opacity = self.opacity, message='The device with this IP address is already in the database!', title='Error', icon='cancel'), self.after(115, lambda: listbox.select(0))
                        listbox.delete(0.0, "end")
                        #delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                    cursor3.close()
                    query = 'INSERT INTO net (name,ip_address) VALUES (' + '" ' + tail + ' "' + "," + '"' + head + '"' + ")"
                    cursor.execute(query)
                    db.commit()
                    cursor2.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor2.fetchall()
                    for member in list2:
                        listbox.insert("END", member)
                        string = "".join(member)
                        if s2 in string:
                            m_index = list2.index(member)
                            try:
                                listbox.move_up(m_index)
                                listbox.activate(0)
                            except:
                                listbox.activate(0)
                    cursor2.execute('SELECT COUNT(*) FROM net')
                    self.total_users = cursor2.fetchone()[0]
                    self.textbox3.insert('end', self.total_users)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    cursor2.close()
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Данные успешно добавлены!', title='Успех', icon='check'), self.after(115, lambda: listbox.select(0))
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='The data has been added successfully!', title='Success', icon='check'), self.after(115, lambda: listbox.select(0))
            except:
                back_states_and_binds_after_refresh()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Требуется подключение к БД!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='A database connection is required!', title='Error', icon='cancel')

        # Функция изменения данных в базе (пиздец полный, почти как добавление, есть проверка на возникший дубликат при изменении IP,
        # из него следует исключение, что при попытке изменить ТОЛЬКО ИМЯ (айпи вводится старый) проверка на дубликат выполняться не будет! => изменится только имя!)
        # ты че ваще долбоеб???
        def update_item(name, listbox):
            if self.is_ctrl_pressed:
                return
            check_db_eng_name(name)
            self.unbind("<Double-Button-1>")
            self.previous_selected = None
            try:
                member = self.listbox.curselection()
                list_member = self.listbox.get(member)
                s = " "
                s2 = (s.join(list_member))
                head, sep, tail = s2.partition(s)
            except:
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Выберите элемент для изменения!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Select an item to change!', title='Error', icon='cancel')
            dev, sepx, modobj = tail.partition(" │ ")  # Деление поля name из базы на составные части для ввода в энтри значений изменяемого поля (как дефолтные)
            mod, sepx, obj = modobj.partition(" │ ")
            if self.language == "Русский":
                dialog = InputDialog(title="Изменение записи", name_db=self.name, name_device=dev[1:], old_ip=head, name_model=mod, name_obj=obj[:len(obj) - 1], mode="change", master = self, opacity = self.opacity, language=self.language)  # изпользую срезы на концевых строках, чтобы не плодить лишние пробелы (так как пробелы добавляются при инсерте)
            else:
                dialog = InputDialog(title="Edit record", name_db=self.name, name_device=dev[1:], old_ip=head, name_model=mod, name_obj=obj[:len(obj) - 1], mode="change", master = self, opacity = self.opacity, language=self.language)  # изпользую срезы на концевых строках, чтобы не плодить лишние пробелы (так как пробелы добавляются при инсерте)
            ss2 = dialog.get_input()
            head2, sep2, tail2 = ss2.partition(s)
            if ss2 == "ErrorMessage":
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='«IP-адрес» и «Имя устройства» обязательны для заполнения!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='«"IP address" and "Device name" are required!', title='Error', icon='cancel')
            elif ss2 == "ErrorMessage2":
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Неверный формат IP-адреса!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='Incorrect IP address format!', title='Error', icon='cancel')
            if head2 == head:
                # refresh_db_after_scale(name_db, self.listbox)
                self.textbox3.configure(state="normal")
                self.textbox3.delete(0.0, "end")
                try:
                    with (sqlite3.connect("db/" + self.name + ".db") as db):
                        lock_states_and_binds_during_refresh()
                        self.textbox3.delete(0.0, "end")
                        #listbox.delete(0.0, "end")
                        delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        cursor = db.cursor()
                        cursor2 = db.cursor()
                        query = 'UPDATE net SET name = " ' + tail2 + ' ", ip_address = "' + head2 + '" WHERE ip_address = "' + head + '"'
                        listbox.delete(0.0, "end")
                        #delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        cursor.execute(query)
                        db.commit()
                        cursor.close()
                        cursor2.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                        list2 = cursor2.fetchall()
                        for member in list2:
                            listbox.insert("END", member)
                            string = "".join(member)
                            if ss2 in string:
                                m_index = list2.index(member)
                                try:
                                    listbox.move_up(m_index)
                                    listbox.select(0)
                                except:
                                    listbox.select(0)
                        cursor2.execute('SELECT COUNT(*) FROM net')
                        self.total_users = cursor2.fetchone()[0]
                        self.textbox3.insert('end', self.total_users)
                        self.textbox3.configure(state="disabled")
                        db.commit()
                        cursor2.close()
                        back_states_and_binds_after_refresh()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Данные успешно изменены!', title='Успех', icon='check'), self.after(115, lambda: listbox.select(0))
                        else:
                            return CTkMessagebox(opacity=self.opacity, message='The data has been successfully changed!', title='Success', icon='check'), self.after(115, lambda: listbox.select(0))
                except:
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Требуется подключение к БД!', title='Ошибка', icon='cancel')
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='A database connection is required!', title='Error', icon='cancel')
            else:
                try:
                    with (sqlite3.connect("db/" + self.name + ".db") as db):
                        lock_states_and_binds_during_refresh()
                        self.textbox3.configure(state="normal")
                        self.textbox3.delete(0.0, "end")
                        #listbox.delete(0.0, "end")
                        delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        cursor = db.cursor()
                        cursor2 = db.cursor()
                        cursor3 = db.cursor()
                        cursor3.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                        list2 = cursor3.fetchall()
                        for member in list2:
                            listbox.insert("END", member)
                            string = " ".join(member)
                            ip_check, seps, name_check = string.partition(s)
                            if head2 == ip_check and head2 != head:
                                m_index = list2.index(member)
                                try:
                                    listbox.move_up(m_index)
                                    listbox.select(0)
                                except:
                                    listbox.select(0)
                                back_states_and_binds_after_refresh()
                                self.textbox3.configure(state="disabled")
                                if self.language == "Русский":
                                    return CTkMessagebox(opacity = self.opacity, message='Устройство с таким IP-адресом уже есть в базе!', title='Ошибка', icon='cancel'), self.after(115, lambda: listbox.select(0))
                                else:
                                    return CTkMessagebox(opacity = self.opacity, message='The device with this IP address is already in the database!', title='Error', icon='cancel'), self.after(115, lambda: listbox.select(0))
                            listbox.delete(0.0, "end")
                            #delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                        cursor3.close()
                        query = 'UPDATE net SET name = " ' + tail2 + ' ", ip_address = "' + head2 + '" WHERE ip_address = "' + head + '"'
                        cursor.execute(query)
                        db.commit()
                        cursor.close()
                        cursor2.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                        list2 = cursor2.fetchall()
                        for member in list2:
                            listbox.insert("END", member)
                            string = "".join(member)
                            if ss2 in string:
                                m_index = list2.index(member)
                                try:
                                    listbox.move_up(m_index)
                                    listbox.select(0)
                                except:
                                    listbox.select(0)
                        cursor2.execute('SELECT COUNT(*) FROM net')
                        self.total_users = cursor2.fetchone()[0]
                        self.textbox3.insert('end', self.total_users)
                        self.textbox3.configure(state="disabled")
                        db.commit()
                        cursor2.close()
                        back_states_and_binds_after_refresh()
                        if self.language == "Русский":
                            return CTkMessagebox(opacity = self.opacity, message='Данные успешно изменены!', title='Успех', icon='check'), self.after(115, lambda: listbox.select(0))
                        else:
                            return CTkMessagebox(opacity = self.opacity, message='The data has been successfully changed!', title='Success', icon='check'), self.after(115, lambda: listbox.select(0))
                except:
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Требуется подключение к БД!', title='Ошибка', icon='cancel')
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='A database connection is required!', title='Error', icon='cancel')

        # Функция поиска в БД (нюхач в деле)
        def search_item(name, listbox, item):
            check_db_eng_name(name)
            if self.listbox.curselection() != None:
                self.listbox.deactivate(0)
            if item == "Выберите из списка или введите...":
                item = ""
            lock_states_and_binds_during_refresh()
            self.unbind("<Double-Button-1>")
            self.previous_selected = None
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            if item == "":
                self.after(150, lambda: self.combobox_5.focus_set())
                back_states_and_binds_after_refresh()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='Поле не должно быть пустым!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='The field must not be empty!', title='Error', icon='cancel')
            try:
                mamba = self.listbox.get(0)
            except:
                self.after(150, lambda: self.focus_set())
                back_states_and_binds_after_refresh()
                if self.language == "Русский":
                    return CTkMessagebox(opacity = self.opacity, message='«Содержимое БД» - не должно быть пустым. Подключитесь/Обновите БД!', title='Ошибка', icon='cancel')
                else:
                    return CTkMessagebox(opacity=self.opacity, message='"DB contents" should not be empty. Connect/Update the database!', title='Error', icon='cancel')
            self.textbox3.configure(state="normal")
            self.textbox3.delete(0.0, "end")
            try:
                with sqlite3.connect("db/" + self.name + ".db") as db:
                    cursor = db.cursor()
                    cursor.execute("""SELECT ip_address, name FROM net ORDER BY ip_address""")
                    list2 = cursor.fetchall()
                    list3 = []
                    for member in list2:
                        string = " ".join(member)
                        if item.lower() in string.lower():  # Регистр вышел нахуй
                            list3.append(member)
                    #listbox.delete(0.0, "end")
                    delete_items_in_batches(self.listbox, list(range(self.listbox.size())), self.listbox.size())
                    for member in list3:
                        listbox.insert("END", member)
                    # На замену комменту ниже  пока не точно
                    if listbox.get(0) == None:
                        return refresh_db_after_search(name_db, self.listbox), back_states_and_binds_after_refresh()
                    # listbox.select(0)  # спорный момент, если ничо не найдено то выделить нечего -> порождает ошибку, которая вызывает рефреш дб
                    count = len(list3)
                    self.textbox3.insert('end', count)
                    self.textbox3.configure(state="disabled")
                    db.commit()
                    cursor.close()
                    back_states_and_binds_after_refresh()
                    if self.language == "Русский":
                        return CTkMessagebox(opacity = self.opacity, message='Поиск завершен, найдено: ' + str(count) + ' записей.', title='Успех', icon='check'), self.after(130, lambda: listbox.select(0))  # Спорный момент, нужно больше тестов (было 115!)
                    else:
                        return CTkMessagebox(opacity=self.opacity, message='Search completed, found:' + str(count) + ' records.', title='Success', icon='check'), self.after(130, lambda: listbox.select(0))
            except:
                return refresh_db_after_search(name_db, self.listbox), back_states_and_binds_after_refresh()

        # Кнопка телеграма на приветственном экране (всем похуй + поебать)
        def get_contact():
            webbrowser.open_new_tab("https://t.me/ValidHalil")
            return

        # Кнопка на приветственном экране (поогнали нахууй)
        def open_tab1():
            self.tabview.set("Подключение")
            self.tabview._segmented_button_callback("Подключение")
            return

        # Снятие фокуса с поля ввода после нажатия правой кнопки мыши на него (долбоеб?)
        def right_click():
            self.after(150, lambda: self.focus_set())
            return

        # Функция для перевода курсора на начало строки (для entry с маской для ip-адреса) (Суходрочка)
        def left_click(entry):
            if entry.get() == "...":
                time.sleep(0.1)
                pyautogui.press("left", presses=5)
            return

        # Функкция перемещения вниз пол листбоксу при нажатии на стрелку вниз (я еблан я еблан да я долбоеб тупой)
        def next_item_listbox():
            if self.is_ctrl_pressed:
                #self.unbind("<Delete>")
                indexes = self.listbox.curselection()
                next_index = indexes[len(indexes)-1] + 1
                if next_index == self.listbox.size():
                    self.listbox._parent_canvas.yview("scroll", int(100 / 3) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    self.last_arrow = "Down"
                    return
                if self.scaling_optionemenu.get() == "100%":
                    self.listbox.activate(next_index)
                    if self.last_arrow == "Up":
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    else:
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3), "units")
                elif self.scaling_optionemenu.get() == "95%":
                    self.listbox.activate(next_index)
                    if self.last_arrow == "Up":
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3.1) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    else:
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3.1), "units")
                elif self.scaling_optionemenu.get() == "105%":
                    self.listbox.activate(next_index)
                    if self.last_arrow == "Up":
                        self.listbox._parent_canvas.yview("scroll", int(100 / 2.9) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    else:
                        self.listbox._parent_canvas.yview("scroll", int(100 / 2.9), "units")
                self.last_arrow = "Down"
            else:
                if self.listbox.curselection() == self.listbox.size() - 1:
                    self.listbox.activate(0)
                    self.listbox._parent_canvas.yview("moveto", 0)
                else:
                    if self.scaling_optionemenu.get() == "100%":
                        self.listbox.activate(self.listbox.curselection() + 1)
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3), "units")
                    elif self.scaling_optionemenu.get() == "95%":
                        self.listbox.activate(self.listbox.curselection() + 1)
                        self.listbox._parent_canvas.yview("scroll", int(100 / 3.1), "units")
                    elif self.scaling_optionemenu.get() == "105%":
                        self.listbox.activate(self.listbox.curselection() + 1)
                        self.listbox._parent_canvas.yview("scroll", int(100 / 2.9), "units")

        # Функкция перемещения вверх пол листбоксу при нажатии на стрелку вниз
        def prev_item_listbox():
            if self.is_ctrl_pressed:
                #self.unbind("<Delete>")
                indexes = self.listbox.curselection()
                prev_index = indexes[0] - 1
                if prev_index == -1:
                    if self.listbox.size() > 8:
                        self.listbox._parent_canvas.yview("scroll", -int(100 / 3.1) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    elif self.listbox.size() > 7 and self.scaling_optionemenu.get() != "95%":
                        self.listbox._parent_canvas.yview("scroll", -int(100 / 3) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                    self.last_arrow = "Up"
                    return
                if self.scaling_optionemenu.get() == "100%":
                    if self.listbox.size() > 7:
                        self.listbox.activate(prev_index)
                        if self.last_arrow == "Down":
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                        else:
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3), "units")
                    else:
                        self.listbox.activate(prev_index)
                elif self.scaling_optionemenu.get() == "95%":
                    if self.listbox.size() > 8:
                        self.listbox.activate(prev_index)
                        if self.last_arrow == "Down":
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3.1) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                        else:
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3.1), "units")
                    else:
                        self.listbox.activate(prev_index)
                elif self.scaling_optionemenu.get() == "105%":
                    if self.listbox.size() > 7:
                        self.listbox.activate(prev_index)
                        if self.last_arrow == "Down":
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 2.9) * (indexes[len(indexes) - 1] - indexes[0]), "units")
                        else:
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 2.9), "units")
                    else:
                        self.listbox.activate(prev_index)
                self.last_arrow = "Up"
            else:
                if self.listbox.curselection() == 0:
                    self.listbox.activate(self.listbox.size() - 1)
                    self.listbox._parent_canvas.yview("moveto", self.listbox.size() - 1)
                else:
                    if self.scaling_optionemenu.get() == "100%":
                        if self.listbox.size() > 7:
                            self.listbox.activate(self.listbox.curselection() - 1)
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3), "units")
                        else:
                            self.listbox.activate(self.listbox.curselection() - 1)
                    elif self.scaling_optionemenu.get() == "95%":
                        if self.listbox.size() > 8:
                            self.listbox.activate(self.listbox.curselection() - 1)
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 3.1), "units")
                        else:
                            self.listbox.activate(self.listbox.curselection() - 1)
                    elif self.scaling_optionemenu.get() == "105%":
                        if self.listbox.size() > 7:
                            self.listbox.activate(self.listbox.curselection() - 1)
                            self.listbox._parent_canvas.yview("scroll", -int(100 / 2.9), "units")
                        else:
                            self.listbox.activate(self.listbox.curselection() - 1)

        # Функкция скролла листбокса влево на стрелку
        def left_scroll_listbox():
            self.listbox._parent_canvas.xview("scroll", -12, "units")

        # Функкция скролла листбокса вправо на стрелку
        def right_scroll_listbox():
            self.listbox._parent_canvas.xview("scroll", 12, "units")

        # Бинды для выбранного элемента listbox (Ваще делать нехуй??? там же кнопки есть, ну яНЕтупой да я да хочу жать клавиши)
        def open_con_listbox():
            if self.is_ctrl_pressed:
                self.bind("<Delete>", lambda x3: delete_items(name_db, self.listbox))
                self.bind("<BackSpace>", lambda x4: delete_items(name_db, self.listbox))
            else:
                self.bind("<Delete>", lambda x7: delete_item(name_db, self.listbox))
                self.bind("<BackSpace>", lambda x6: delete_item(name_db, self.listbox))
                self.bind("<Return>", lambda x1: selected_item())
                self.bind("<Double-Button-1>", lambda x1: selected_item())
                self.bind("<Button-3>", lambda x2: update_item(name_db, self.listbox))
                self.bind("<F8>", lambda x5: update_item(name_db, self.listbox))
            self.bind("<Down>", lambda next: next_item_listbox())
            self.bind("<Up>", lambda prev: prev_item_listbox())
            self.bind("<Left>", lambda left: left_scroll_listbox())
            self.bind("<Right>", lambda right: right_scroll_listbox())
            self.focus_set()
            return

        def key_control_a(event):
            if event.keycode == 65:  # Клавиша с буквой Ф и с англ. буквой A
                start_time = time.time()
                self.listbox.deactivate("all")
                self.listbox.activate("all")
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # В миллисекундах
                print(f"Все элементы выделены за {duration:.2f} мс.")
            return

        # Запечатан
        def on_ctrl_press(event):
            if event.keysym == "Control_L":
                prev_index = self.listbox.curselection()
                antibug()
                self.bind("<Delete>", lambda x3: [delete_items(name_db, self.listbox)])
                self.bind("<BackSpace>", lambda x4: [delete_items(name_db, self.listbox)])
                self.bind('<Control-KeyPress>', key_control_a)
                self.unbind('<ButtonPress-1>')
                self.unbind('<Button-2>')
                if not self.is_ctrl_pressed:
                    self.del_button.configure(command=lambda: delete_items(name_db, self.listbox))
                    self.combobox_4.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                    self.clear_btn3.configure(command=None)
                    self.help_btn_tab3.configure(command=None)
                    self.con_button.configure(state="disabled", fg_color="#14375e")
                    self.update_button.configure(state="disabled", fg_color="#14375e")
                    self.add_button.configure(state="disabled", fg_color="#14375e")
                    self.update_row_button.configure(state="disabled", fg_color="#14375e")
                    self.combobox_5.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
                    self.search_button.configure(state="disabled", fg_color="#14375e")
                    self.after(50, lambda: self.clear_btn_baza.configure(state="disabled", fg_color="#ab590c", image=disconnect_disabled_img))
                    self.after(150, lambda: self.clear_btn_search.configure(state="disabled", fg_color="#ab590c", image=clear_disabled_img))
                    self.combobox_5.unbind("<Down>")
                    self.combobox_5.unbind("<Return>")
                    self.combobox_4.unbind("<Down>")
                    self.bind("<Left>", lambda left: left_scroll_listbox())
                    self.bind("<Right>", lambda right: right_scroll_listbox())
                    self.unbind("<Insert>")
                    self.unbind("<F5>")
                    self.unbind("<F6>")
                    self.unbind("<F8>")
                    self.unbind("<F9>")
                self.is_ctrl_pressed = True
                self.listbox.configure(multiple_selection=True)
                self.listbox.activate(prev_index)
                self.bind("<Down>", lambda next: next_item_listbox())
                self.bind("<Up>", lambda prev: prev_item_listbox())

        # Колдун был отпущен и все грехи прощены
        def on_ctrl_release(event):
            if event.keysym == "Control_L":
                self.is_ctrl_pressed = False
                deactivating_indexes = self.listbox.curselection()
                for i in range (0,len(deactivating_indexes)):
                    self.listbox.deactivate(deactivating_indexes[i])
                self.listbox.configure(multiple_selection=False)
                self.del_button.configure(command=lambda: delete_item(name_db, self.listbox))
                self.combobox_4.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
                self.clear_btn3.configure(command=lambda: [clear_text(self.listbox), clear_count()])
                self.help_btn_tab3.configure(command=lambda: help(self.tabview.get()))
                self.con_button.configure(state="normal", fg_color="#1F538D")
                self.update_button.configure(state="normal", fg_color="#1F538D")
                self.add_button.configure(state="normal", fg_color="#1F538D")
                self.update_row_button.configure(state="normal", fg_color="#1F538D")
                self.combobox_5.configure(state="normal", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
                self.search_button.configure(state="normal", fg_color="#1F538D")
                self.combobox_5.bind("<Down>", lambda open_var: self.combobox_5._clicked())
                self.combobox_5.bind("<Return>", lambda combobox_5_var: search_item(name_db, self.listbox, self.combobox_5.get()))
                self.combobox_4.bind("<Down>", lambda open_var: self.combobox_4._clicked())
                self.after(50, lambda: self.clear_btn_baza.configure(state="normal", fg_color="#de710b", image=disconnect_img))
                self.after(150, lambda: self.clear_btn_search.configure(state="normal", fg_color="#de710b", image=clear_img))
                self.unbind("<KeyPress>")
                self.unbind('<Control-KeyPress>')
                self.bind("<Insert>", lambda insert_var: add_item(name_db, self.listbox))
                self.bind("<F5>", lambda refresh_var: refresh_db(name_db, self.listbox))
                self.bind("<F6>", lambda del_var: clear_entry_baza(self.combobox_4))
                self.bind("<F8>", lambda x2: update_item(name_db, self.listbox))
                self.bind("<F9>", lambda open_help: help(self.tabview.get()))
                self.bind('<ButtonPress-1>', self.deselect_item)
                self.bind('<Button-2>', self.deselect_item)

        # Кантрал атпусти быстро блять гандоун
        def simulate_ctrl_release():
            class MockEvent:
                def __init__(self, keysym):
                    self.keysym = keysym
            mock_event = MockEvent("Control_L")
            on_ctrl_release(mock_event)

        # Бинд инсерта на добавление значения в базу (работает только для вкладки "База адресов") (Срал мочой короче) (UPD: Функция превратилась в полный пиздец)
        def bind_add_item_to_insert():
            self.after(150, lambda: self.focus_set())
            if self.tabview.get() == "База адресов":
                self.unbind("<Down>")
                self.unbind("<Up>")
                self.unbind("<Return>")
                self.bind("<F9>", lambda open_help: help(self.tabview.get()))
                if self.main_button_6._state == "disabled":
                    self.bind("<Insert>", lambda insert_var: add_item(name_db, self.listbox))
                    self.bind("<KeyPress-Control_L>", on_ctrl_press)
                    self.bind("<KeyRelease-Control_L>", on_ctrl_release)
                    self.bind("<F5>", lambda refresh_var: refresh_db(name_db, self.listbox))
                    #self.bind("<Control-Delete>", lambda delete_text: [clear_text(self.listbox), clear_count()])  # НАД ЭТИМ И ИНСЕРТОМ ЩЕ ПОДУМАТЬ, ОСТАЮТСЯ ВО ВРЕМЯ ОБНОВЛЕНИЯ ЕСЛИ ВЫЙТИ С 4 ВКЛАДКИ И САМОМУ ЗАЙТИ ОБРАТНО НА НЕЕ, ПОЧЕМУ СБРАСЫВАЕТСЯ
                else:
                    self.unbind("<Insert>")
                    self.unbind("<F5>")
                    self.unbind("<KeyPress-Control_L>")
                    self.unbind("<KeyRelease-Control_L>")
                    #self.unbind("<Control-Delete>")
                self.bind("<F7>", lambda focus_lisbox_var: [self.listbox.activate(0), self.listbox._parent_canvas.yview("moveto", 0)])
            elif self.tabview.get() == "Начальное окно":
                self.unbind("<Down>")
                self.unbind("<Up>")
                self.unbind("<Double-Button-1>")
                #self.unbind("<Control-Delete>")
                self.unbind("<Insert>")
                self.unbind("<KeyPress-Control_L>")
                self.unbind("<KeyRelease-Control_L>")
                self.unbind("<F5>")
                self.unbind("<F9>")
                self.unbind("<F7>")
                self.after(50, lambda: self.bind("<Return>", lambda go: nav_tab2()))
                try:
                    simulate_ctrl_release()
                    self.listbox.deactivate(0)
                    self.previous_selected = None
                except:
                    return
            elif self.tabview.get() == "Подключение":
                self.after(100, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units")))  # НОВАЯ
                self.after(100, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))  # НОВАЯ
                self.unbind("<Double-Button-1>")
                #self.unbind("<Control-Delete>")
                self.unbind("<Insert>")
                self.unbind("<KeyPress-Control_L>")
                self.unbind("<KeyRelease-Control_L>")
                self.unbind("<Return>")
                self.unbind("<F5>")
                self.unbind("<F7>")
                self.bind("<F9>", lambda open_help: help(self.tabview.get()))
                #self.bind("<Control-Delete>", lambda delete_text: clear_text(self.textbox))
                try:
                    simulate_ctrl_release()
                    self.listbox.deactivate(0)
                    self.previous_selected = None
                except:
                    return
            else:
                self.after(100, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))) #НОВАЯ
                self.after(100, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units"))) #НОВАЯ
                #self.unbind("<Control-Delete>")
                self.unbind("<Double-Button-1>")
                self.unbind("<Insert>")
                self.unbind("<KeyPress-Control_L>")
                self.unbind("<KeyRelease-Control_L>")
                self.unbind("<Return>")
                self.unbind("<F5>")
                self.unbind("<F8>")
                self.unbind("<F7>")
                self.bind("<F9>", lambda open_help: help(self.tabview.get()))
                #self.bind("<Control-Delete>", lambda delete_text: clear_text(self.textbox2))
                try:
                    simulate_ctrl_release()
                    self.listbox.deactivate(0)
                    self.previous_selected = None
                except:
                    return

        # Навигация между вкладками на F1-F4 (какой-то мужик)
        def nav_tab1():
            self.tabview.set("Начальное окно")
            self.tabview._segmented_button_callback("Начальное окно")
            bind_add_item_to_insert()
            return antibug()

        def nav_tab2():
            self.tabview.set("Подключение")
            self.tabview._segmented_button_callback("Подключение")
            bind_add_item_to_insert()
            return antibug()

        def nav_tab3():
            self.tabview.set("Параметры сети")
            self.tabview._segmented_button_callback("Параметры сети")
            bind_add_item_to_insert()
            return antibug()

        def nav_tab4():
            self.tabview.set("База адресов")
            self.tabview._segmented_button_callback("База адресов")
            bind_add_item_to_insert()
            return antibug()

        # Вывод справки в зависимости от активной вкладки
        def help(tab):
            help_tab = Help()
            help_tab(tab, self, self.opacity, self.language)

        # Антибаг при использовании хоткеев (и кнопок) на вкладке "База адресов" (ну насрал багооов, мдааа)
        def antibug():
            if self.listbox.curselection() != None and not self.listbox.multiple:
                self.listbox.deactivate(0)
            #self.unbind("<Down>") #Возможно придется вернуть, сбрасывало новые бинды (скролл текстбоксов на стрелки) при переключении на фки между вкладками
            #self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
            self.unbind("<Double-Button-1>")
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            # self.combobox_4.unbind("<Delete>") #??? Нахуя я это добавил

        # Функция фокуса курсора на конец комбобокса при выборе элемента выпадающего списка (ну типа шобы редактировать приятнее было)
        # Теперь еще для приколов с выбором вэлью, когда уже подключен к базе (ну шобы при не было уведомлений о подключении ЧИСТО обновляем базу)
        def combo_focus(combo, flag=1):
            if self.tabview.get() == "База адресов" and combo.get() != "" and flag == 2:
                refresh_db_after_reconnect(name_db, self.listbox)  # Чистое обновление
                self.after(50, lambda: self.focus_set())
            else:
                self.after(50, lambda: combo.focus())
            return

        # Костыль для закрытия проги на энтер (смари функцию ниже дээээб)
        def full_close():
            self.destroy()
            self.grab_release()
            quit(self)

        # Закрытие приложения на ESC (нахуя если есть крестик???)
        def close_app():
            if self.language == "Русский":
                msg = CTkMessagebox(opacity = self.opacity, message='Выйти из программы?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да")
            else:
                msg = CTkMessagebox(opacity=self.opacity, message='Exit the program?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes")
            msg.bind("<Return>", lambda close_var: full_close())

            msg.button_1.configure(fg_color="#de710b",hover_color="#ab590c")
            msg.focus_set()
            response = msg.get()
            if response == "Отмена" or response == "Cancel":
                return
            if response == "Да" or response == "Yes":
                self.destroy()
                self.grab_release()
                quit(self) # Я папысал нимножкааа и паслал тибя нахооой и сказал атсаси у миня крошкаааааа

        # Вызов тем
        # WhitePower
        def Light():
            self.hello_line2.configure(text_color="#a5a5a5")
            self.label_line.configure(text_color="#a5a5a5")
            self.label_line2.configure(text_color="#a5a5a5")
            self.label_line3.configure(text_color="#a5a5a5")
            self.ping_label_img.configure(image=ping_light_img)
            self.tracert_label_img.configure(image=tracert_light_img)
            self.tel_label_img.configure(image=telnet_light_img)
            self.ipconfig_label_img.configure(image=ipconfig_light_img)
            self.adapter_label_img.configure(image=adapter_light_img)
            self.settings_label_img.configure(image=settings_light_img)
            self.baza_label_img.configure(image=baza_light_img)
            self.search_label_img.configure(image=search_light_img)
            ctk.set_appearance_mode("Light")

        #Чорни властилин
        def Dark():
            self.hello_line2.configure(text_color="gray32")
            self.label_line.configure(text_color="gray32")
            self.label_line2.configure(text_color="gray32")
            self.label_line3.configure(text_color="gray32")
            self.ping_label_img.configure(image=ping_img)
            self.tracert_label_img.configure(image=tracert_img)
            self.tel_label_img.configure(image=telnet_img)
            self.ipconfig_label_img.configure(image=ipconfig_img)
            self.adapter_label_img.configure(image=adapter_img)
            self.settings_label_img.configure(image=settings_img)
            self.baza_label_img.configure(image=baza_img)
            self.search_label_img.configure(image=search_img)
            ctk.set_appearance_mode("Dark")

        # Перемещение на бинд между радиокнопками стрэлка вныз
        def next_radio(radio):
            if radio.get() == 1:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(2)
            elif radio.get() == 2:
                self.entry3.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
                radio.set(3)
            elif radio.get() == 3:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(4)
            else:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(1)

        # Перемещение на бинд между радиокнопками стрэлка ввэрх
        def prev_radio(radio):
            if radio.get() == 4:
                self.entry3.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
                radio.set(3)
            elif radio.get() == 3:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(2)
            elif radio.get() == 2:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(1)
            else:
                self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
                radio.set(4)

        # Скалинг эвент переехал короче, теперь при выборе скейла заново отрисовываем листобк (были проблемы с размером кнопок изза правок в классах CTkListBox и CTkScrollableFrame)
        def change_scaling_event(new_scaling):
            if new_scaling == "95%":
                self.listbox = CTkListbox(self.tabview.tab("База адресов"), fg_color=("white", "#333333"), border_width=0, button_color=("#e5e5e5", "#212121"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="normal"), orientation="vertical", orientation2="horizontal", width=620)
                self.listbox.grid(row=3, rowspan=6, column=2, columnspan=4, padx=(12, 20), pady=(0, 0), sticky="nsew")
                self.listbox.bind('<<ListboxSelect>>', lambda list_var: open_con_listbox())
                self.label_hello.grid(row=2, column=1, padx=(145, 0), pady=(0, 0), sticky="w")
                self.label_hello2.grid(row=3, column=1, padx=(145, 0), pady=(10, 0), sticky="w")
                self.label_hello3.grid(row=4, column=1, padx=(145, 0), pady=(10, 0), sticky="w")
                self.label_hello4.grid(row=5, column=1, padx=(145, 0), pady=(10, 0), sticky="w")
                self.hello_line2.grid(row=6, column=1, columnspan=1, padx=(150, 150), pady=(0, 0), sticky="nsew")
                self.hello_button_1.grid(row=5, column=1, padx=(560, 145), pady=(10, 0), sticky="we")
                self.hello_button_2.grid(row=7, column=1, padx=(145, 145), pady=(5, 120), sticky="ew", ipady=5)
                self.label_line2.grid(row=3, column=1, columnspan=9, padx=24, pady=(10, 10))
                if self.combobox_4.get() != "":
                    refresh_db_after_scale(name_db, self.listbox)
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                ctk.set_widget_scaling(new_scaling_float)
                update_config_params("scale","95%")
            elif new_scaling == "105%":
                self.listbox = CTkListbox(self.tabview.tab("База адресов"), fg_color=("white", "#333333"), border_width=0, button_color=("#e5e5e5", "#212121"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="normal"), orientation="vertical", orientation2="horizontal", width=515)
                self.listbox.grid(row=3, rowspan=6, column=2, columnspan=4, padx=(12, 20), pady=(0, 0), sticky="nsew")
                self.listbox.bind('<<ListboxSelect>>', lambda list_var: open_con_listbox())
                self.label_hello.grid(row=2, column=1, padx=(95, 0), pady=(0, 0), sticky="w")
                self.label_hello2.grid(row=3, column=1, padx=(95, 0), pady=(10, 0), sticky="w")
                self.label_hello3.grid(row=4, column=1, padx=(95, 0), pady=(10, 0), sticky="w")
                self.label_hello4.grid(row=5, column=1, padx=(95, 0), pady=(10, 0), sticky="w")
                self.hello_line2.grid(row=6, column=1, columnspan=1, padx=(100, 100), pady=(10, 10), sticky="nsew")
                self.hello_button_1.grid(row=5, column=1, padx=(500, 95), pady=(10, 0), sticky="we")
                self.hello_button_2.grid(row=7, column=1, padx=(95, 95), pady=(5, 120), sticky="ew", ipady=5)
                self.label_line2.grid(row=3, column=1, columnspan=9, padx=24, pady=(0, 0))
                if self.combobox_4.get() != "":
                    refresh_db_after_scale(name_db, self.listbox)
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                ctk.set_widget_scaling(new_scaling_float)
                update_config_params("scale","105%")
            else:
                self.listbox = CTkListbox(self.tabview.tab("База адресов"), fg_color=("white", "#333333"), border_width=0, button_color=("#e5e5e5", "#212121"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="normal"), orientation="vertical", orientation2="horizontal", width=560)
                self.listbox.grid(row=3, rowspan=6, column=2, columnspan=4, padx=(12, 20), pady=(0, 0), sticky="nsew")
                self.listbox.bind('<<ListboxSelect>>', lambda list_var: open_con_listbox())
                self.hello_button_1.grid(row=5, column=1, padx=(520, 77), pady=(10, 0), sticky="we")
                self.label_hello.grid(row=2, column=1, padx=(115, 0), pady=(0, 0), sticky="w")
                self.label_hello2.grid(row=3, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
                self.label_hello3.grid(row=4, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
                self.label_hello4.grid(row=5, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
                self.hello_line2.grid(row=6, column=1, columnspan=1, padx=(120, 120), pady=(0, 0), sticky="nsew")
                self.hello_button_1.grid(row=5, column=1, padx=(530, 115), pady=(10, 0), sticky="we")
                self.hello_button_2.grid(row=7, column=1, padx=(115, 115), pady=(5, 120), sticky="ew", ipady=5)
                self.label_line2.grid(row=3, column=1, columnspan=9, padx=24, pady=(10, 10))
                if self.combobox_4.get() != "":
                    refresh_db_after_scale(name_db, self.listbox)
                new_scaling = "95%"
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                ctk.set_widget_scaling(new_scaling_float)
                new_scaling = "100%"
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                ctk.set_widget_scaling(new_scaling_float)
                update_config_params("scale","100%")

        # Обновление параметров, при изменении их пользователем, перед сохранением файла конфигурации окна приложения
        def update_config_params(param, new_value):
            if param == "scale":
                load_params = load_config()
                language, opacity, theme, scale = load_params
                scale = new_value
                save_config(language, opacity, theme, scale)
            elif param == "opacity":
                load_params = load_config()
                language, opacity, theme, scale = load_params
                opacity = new_value
                save_config(language, opacity, theme, scale)
            elif param == "language":
                load_params = load_config()
                language, opacity, theme, scale = load_params
                language = new_value
                save_config(language, opacity, theme, scale)
            elif param == "theme":
                load_params = load_config()
                language, opacity, theme, scale = load_params
                theme = new_value
                save_config(language, opacity, theme, scale)

        def change_appearance_mode(value):
            if value == "Светлая" or value == "Light":
                Light()
                update_config_params("theme", value)
            elif value == "Темная" or value == "Dark":
                Dark()
                update_config_params("theme", value)

        def change_language(value, theme_var, opacity_var):
            if value == "Английский" or value == "English":
                self.help_btn_tab1.configure(image=help_eng_img)
                self.help_btn_tab2.configure(image=help_eng_img)
                self.help_btn_tab3.configure(image=help_eng_img)
                self.label_con3.configure(image=show_bd_eng_img)

                self.label_hello.configure(text="Hello!")
                self.label_hello2.configure(text='Thank  you  for  using  the  NetCon 2.0  application.')
                self.label_hello3.configure(text='This application is under development, so please use my')
                self.label_hello4.configure(text='Telegram  for  any questions  you  have:')
                self.hello_button_2.configure(text='Start')

                self.language = "English"
                self.language_list = ["Russian", "English"]
                self.language_optionemenu.configure(values=self.language_list)
                self.language_optionemenu.set(value=self.language)
                update_config_params("language","English")

                self.transparancy_mode_label.configure(text = "Opacity:")
                self.scaling_label.configure(text = "Scale:")
                self.appearance_mode_label.configure(text = "Theme:")
                self.language_label.configure(text = "Language:")

                self.theme_list = ["Dark", "Light"]
                self.appearance_mode_optionemenu.configure(values=self.theme_list)
                if theme_var == "Светлая":
                    theme_var = "Light"
                elif theme_var == "Темная":
                    theme_var = "Dark"
                self.appearance_mode_optionemenu.set(value=theme_var)
                update_config_params("theme", theme_var)

                self.transparent_list = ["None", "25%", "50%", "75%", "100%"]
                self.transparancy_mode_optionemenu.configure(values=self.transparent_list)
                if opacity_var == "Отсутствует":
                    opacity_var = "None"
                self.transparancy_mode_optionemenu.set(value=opacity_var)
                update_config_params("opacity", opacity_var)

                self.tabview.rename("Начальное окно", "Начальное окно", display_name="Start window")
                self.tabview.rename("Подключение", "Подключение", display_name="Connection")
                self.tabview.rename("Параметры сети", "Параметры сети", display_name="Network settings")
                self.tabview.rename("База адресов", "База адресов", display_name="Address database")

                self.main_button_1.configure(text = "Start")
                self.main_button_2.configure(text="Start")
                self.label3.configure(text="Connection:")
                self.main_button_3.configure(text="Open")

                self.label_ipconfig.configure(text="Show IpConfig:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
                combo = self.combobox_ipconfig.get()
                self.combobox_ipconfig.configure(placeholder_text="Select from the list or enter...")
                if combo != "Выберите из списка или введите...":
                    self.combobox_ipconfig.set(combo)
                self.button_ipconfig.configure(text="Show")
                self.label4.configure(text="Adapter name:")

                combo = self.combobox_2.get()
                self.combobox_2.configure(placeholder_text="Select from the list or enter...")
                if combo != "Выберите из списка или введите...":
                    self.combobox_2.set(combo)

                self.main_button_4.configure(text="Show")
                self.label5_1.configure(text="Adapter settings:")
                self.label5.configure(text="Name:")
                self.label6.configure(text="IP-add:")
                self.label7.configure(text="Mask:")
                self.label8_1.configure(text="Gate:")
                self.main_button_5.configure(text="Apply")
                self.main_button_55.configure(text='Enable "DHCP"')

                self.label8.configure(text="Name of DB:")
                combo = self.combobox_4.get()
                self.devices = ["Switches", "Routers", "Multiplexers", "Power supply", "Phones", "Other"]
                self.combobox_4.configure(placeholder_text="Select from the list or enter...", values=self.devices)
                if self.scaling_optionemenu.get() == "105%":
                    if self.scaling_factor != 1:
                        self.textbox3.configure(width=69*0.95+1.5)
                    else:
                        self.textbox3.configure(width=69*0.95)
                elif self.scaling_optionemenu.get() == "95%":
                    if self.scaling_factor != 1:
                        self.textbox3.configure(width=67)
                    else:
                        self.textbox3.configure(width=66)
                else:
                    if self.scaling_factor != 1:
                        self.textbox3.configure(width=66)
                    else:
                        self.textbox3.configure(width=69)
                self.after(100, lambda: self.textbox3.configure(state="disabled"))
                if combo != "Выберите из списка или введите...":
                    self.combobox_4.set(combo)
                if self.combobox_4.get() == "Коммутаторы":
                    self.combobox_4.set("Switches")
                if self.combobox_4.get() == "Маршрутизаторы":
                    self.combobox_4.set("Routers")
                if self.combobox_4.get() == "Мультиплексоры":
                    self.combobox_4.set("Multiplexers")
                if self.combobox_4.get() == "Электропитание":
                    self.combobox_4.set("Power supply")
                if self.combobox_4.get() == "Телефоны":
                    self.combobox_4.set("Phones")
                if self.combobox_4.get() == "Другое":
                    self.combobox_4.set("Other")
                self.main_button_6.configure(text="Connect")
                self.label9.configure(text="Records:")
                self.con_button.configure(text="Open")
                self.update_button.configure(text="Refresh")
                self.add_button.configure(text="Add")
                self.update_row_button.configure(text="Change")
                self.del_button.configure(text="Delete")
                self.label10.configure(text="Find in DB:")
                combo = self.combobox_5.get()
                self.combobox_5.configure(placeholder_text="Select from the list or enter...")
                if combo == "Требуется подключение к БД...":
                    self.combobox_5.configure(state="normal", placeholder_text="A database connection is required...")
                    self.combobox_5.configure(state="disabled")
                if combo != "Выберите из списка или введите..." and combo != "Требуется подключение к БД...":
                    self.combobox_5.set(combo)
                self.search_button.configure(text="Find")

            elif value == "Русский" or value == "Russian":
                self.help_btn_tab1.configure(image=help_img)
                self.help_btn_tab2.configure(image=help_img)
                self.help_btn_tab3.configure(image=help_img)
                self.label_con3.configure(image=show_bd_img)

                self.label_hello.configure(text="Привет!")
                self.label_hello2.configure(text='Спасибо, что пользуетесь приложением "NetCon 2.0".')
                self.label_hello3.configure(text='Приложение находится на стадии разработки, так что')
                self.label_hello4.configure(text='вот мой Telegram для обратной связи:')
                self.hello_button_2.configure(text='Начать')

                self.language = "Русский"
                self.language_list = ["Русский", "Английский"]
                self.language_optionemenu.configure(values=self.language_list)
                self.language_optionemenu.set(value=self.language)
                update_config_params("language","Русский")

                self.transparancy_mode_label.configure(text="Прозрачность:")
                self.scaling_label.configure(text="Масштаб:")
                self.appearance_mode_label.configure(text="Тема:")
                self.language_label.configure(text="Язык:")
                self.theme_list = ["Темная", "Светлая"]
                self.appearance_mode_optionemenu.configure(values=self.theme_list)
                if theme_var == "Light":
                    theme_var = "Светлая"
                elif theme_var == "Dark":
                    theme_var = "Темная"
                self.appearance_mode_optionemenu.set(value=theme_var)
                update_config_params("theme", theme_var)

                self.transparent_list = ["Отсутствует", "25%", "50%", "75%", "100%"]
                self.transparancy_mode_optionemenu.configure(values=self.transparent_list)
                if opacity_var == "None":
                    opacity_var = "Отсутствует"
                self.transparancy_mode_optionemenu.set(value=opacity_var)
                update_config_params("opacity", opacity_var)

                self.tabview.rename("Начальное окно", "Начальное окно", display_name="Начальное окно")
                self.tabview.rename("Подключение", "Подключение", display_name="Подключение")
                self.tabview.rename("Параметры сети", "Параметры сети", display_name="Параметры сети")
                self.tabview.rename("База адресов", "База адресов", display_name="База адресов")

                self.main_button_1.configure(text="Начать")
                self.main_button_2.configure(text="Начать")
                self.label3.configure(text="Подключение:")
                self.main_button_3.configure(text="Открыть")

                self.label_ipconfig.configure(text="Вывод IpConfig:", font=ctk.CTkFont(family="Trebuchet MS", size=19, weight="bold"))
                combo = self.combobox_ipconfig.get()
                self.combobox_ipconfig.configure(placeholder_text="Выберите из списка или введите...")
                if combo != "Select from the list or enter...":
                    self.combobox_ipconfig.set(combo)
                self.button_ipconfig.configure(text="Показать")
                self.label4.configure(text="Имя адаптера:")
                combo = self.combobox_2.get()
                self.combobox_2.configure(placeholder_text="Выберите из списка или введите...")
                if combo != "Select from the list or enter...":
                    self.combobox_2.set(combo)
                self.main_button_4.configure(text="Показать")
                self.label5_1.configure(text="Настройки адаптера:")
                self.label5.configure(text="Имя:")
                self.label6.configure(text="IP-адр:")
                self.label7.configure(text="Маска:")
                self.label8_1.configure(text="Шлюз:")
                self.main_button_5.configure(text="Применить")
                self.main_button_55.configure(text='Включить "DHCP"')

                self.label8.configure(text="Название БД:")
                self.textbox3.configure(width=50)
                self.after(100, lambda: self.textbox3.configure(state="disabled"))
                combo = self.combobox_4.get()
                self.devices = ["Коммутаторы", "Маршрутизаторы", "Мультиплексоры", "Электропитание", "Телефоны", "Другое"]
                self.combobox_4.configure(placeholder_text="Выберите из списка или введите...", values=self.devices)
                if combo != "Select from the list or enter...":
                    self.combobox_4.set(combo)
                if self.combobox_4.get() == "Switches":
                    self.combobox_4.set("Коммутаторы")
                if self.combobox_4.get() == "Routers":
                    self.combobox_4.set("Маршрутизаторы")
                if self.combobox_4.get() == "Multiplexers":
                    self.combobox_4.set("Мультиплексоры")
                if self.combobox_4.get() == "Power supply":
                    self.combobox_4.set("Электропитание")
                if self.combobox_4.get() == "Phones":
                    self.combobox_4.set("Телефоны")
                if self.combobox_4.get() == "Other":
                    self.combobox_4.set("Другое")
                self.main_button_6.configure(text="Соединить")
                self.label9.configure(text="Записей:")
                self.con_button.configure(text="Открыть")
                self.update_button.configure(text="Обновить")
                self.add_button.configure(text="Добавить")
                self.update_row_button.configure(text="Изменить")
                self.del_button.configure(text="Удалить")
                self.label10.configure(text="Поиск в БД:")

                combo = self.combobox_5.get()
                self.combobox_5.configure(placeholder_text="Выберите из списка или введите...")
                if combo == "A database connection is required...":
                    self.combobox_5.configure(state="normal", placeholder_text="Требуется подключение к БД...")
                    self.combobox_5.configure(state="disabled")
                if combo != "Select from the list or enter..." and combo != "A database connection is required...":
                    self.combobox_5.set(combo)

                self.search_button.configure(text="Найти")

        # Прозрачность окна (экспереметальная функция, мб доработаю когда-нибудь) //Нахуя и зачем? Апогей шизофрении одним словом
        def change_transparency_mode(value):
            if value == "25%":
                self.attributes("-alpha", 0.97)
                self.opacity = 0.97
                update_config_params("opacity","25%")
            elif value == "50%":
                self.attributes("-alpha", 0.95)
                self.opacity = 0.95
                update_config_params("opacity","50%")
            elif value == "75%":
                self.attributes("-alpha", 0.93)
                self.opacity = 0.93
                update_config_params("opacity","75%")
            elif value == "100%":
                self.attributes("-alpha", 0.9)
                self.opacity = 0.9
                update_config_params("opacity","100%")
            elif value == "Отсутствует":
                self.attributes("-alpha", 1)
                self.opacity = 1
                update_config_params("opacity","Отсутствует")
            elif value == "None":
                self.attributes("-alpha", 1)
                self.opacity = 1
                update_config_params("opacity", "None")

        # Функция позволяюща юзать вставку и копирование на русской раскладке
        def _onKeyRelease(event):
            ctrl = (event.state & 0x4) != 0
            if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
                event.widget.event_generate("<<Cut>>")
            if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
                event.widget.event_generate("<<Paste>>")
            if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
                event.widget.event_generate("<<Copy>>")
            if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
                event.widget.event_generate("<<SelectAll>>")

        # Получение списка адаптеров (теперь реалтайм)
        # При вызове выпадающего списка на стрелку вниз
        def get_adapters_list(combo):
            adapterskeys = psutil.net_if_addrs()
            adapter = list(adapterskeys.keys())
            combo.configure(values=adapter)
            combo._clicked()

        # При вызове выпадающего списка кликом
        def get_adapters_list_click(combo):
            adapterskeys = psutil.net_if_addrs()
            adapter = list(adapterskeys.keys())
            combo.configure(values=adapter)

        # Параметры окна + всякие плюшки
        # Получение директории скрипта для пути картинок
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")
        self.path_img = path_img

        self.bind_all("<Key>", _onKeyRelease, "+")
        self.title("NetCon 2.0")
        self.geometry("1100x580")
        self.resizable(False, False)
        self.lift() #Пока не точно
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1100
        window_height = 580
        self.scaling_factor = ScreenCurrent.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.attributes("-alpha", 1)  # Ситцевые трусики ммм нямка сладуля
        self.opacity = 1
        self.language = ""
        self.last_arrow = ""
        self.total_users = 0
        self.is_ctrl_pressed = False
        self.protocol("WM_DELETE_WINDOW", lambda: close_app())
        params = load_config()
        language, opacity, theme, scale = params

        ping_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/s_ping.png"), size=(30, 28))
        ping_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/s_ping_light.png"), size=(30, 28))
        tracert_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/tracert.png"), size=(30, 28))
        tracert_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/tracert_light.png"), size=(30, 28))
        telnet_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/telnet.png"), size=(28, 28))
        telnet_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/telnet_light.png"), size=(28, 28))
        ipconfig_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/config.png"), size=(30, 28))
        ipconfig_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/config_light.png"), size=(30, 28))
        adapter_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/card.png"), size=(30, 28))
        adapter_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/card_light.png"), size=(30, 28))
        settings_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/settings.png"), size=(30, 28))
        settings_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/settings_light.png"), size=(30, 28))
        baza_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/subd.png"), size=(30, 28))
        baza_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/subd_light.png"), size=(30, 28))
        search_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/search.png"), size=(30, 28))
        search_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/search_light.png"), size=(30, 28))

        # Создание вкладок

        self.tabview = CustomCTkTabview(self, width=250, command=bind_add_item_to_insert, segmented_button_selected_color="#1F538D")
        self.tabview.grid(row=0, rowspan=8, column=1, columnspan=3, padx=(25, 25), pady=(5, 25), sticky="nsew")
        self.tabview._segmented_button.configure(font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))

        self.tabview.add("Начальное окно")
        self.tabview.tab("Начальное окно").grid_columnconfigure((1), weight=1)
        self.tabview.tab("Начальное окно").grid_rowconfigure((5), weight=1)

        self.tabview.add("Подключение")
        self.tabview.tab("Подключение").grid_columnconfigure((1), weight=0)
        self.tabview.tab("Подключение").grid_columnconfigure((2), weight=1)
        self.tabview.tab("Подключение").grid_rowconfigure((5), weight=1)

        self.tabview.add("Параметры сети")
        self.tabview.tab("Параметры сети").grid_columnconfigure((1, 7), weight=0)
        self.tabview.tab("Параметры сети").grid_columnconfigure((2), weight=1)
        self.tabview.tab("Параметры сети").grid_rowconfigure((5), weight=0)

        self.tabview.add("База адресов")
        self.tabview.tab("База адресов").grid_columnconfigure((1), weight=0)
        self.tabview.tab("База адресов").grid_columnconfigure((2), weight=1)
        self.tabview.tab("База адресов").grid_rowconfigure((5), weight=1)

        self.tabview.set("Начальное окно")
        self.tabview._segmented_button_callback("Начальное окно")

        # Бинды

        self.bind("<F1>", lambda open_tab_var: nav_tab1())
        self.bind("<F2>", lambda open_tab_var: nav_tab2())
        self.bind("<F3>", lambda open_tab_var: nav_tab3())
        self.bind("<F4>", lambda open_tab_var: nav_tab4())
        self.bind('<Escape>', lambda close: close_app())
        self.bind("<Button-3>", lambda escape_entry: right_click())

        # Настройка общей(?) сетки

        self.grid_columnconfigure((1), weight=0)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((5), weight=1)

        # Создание боковой панели
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")

        self.sidebar_frame.grid_columnconfigure((1), weight=0)
        self.sidebar_frame.grid_columnconfigure((2), weight=1)
        self.sidebar_frame.grid_rowconfigure((1, 2, 3, 4), weight=0)
        self.sidebar_frame.grid_rowconfigure((3), weight=1)

        # Логотип

        self.iconbitmap(path_img + "img/mainpic.ico")
        logo_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/logo.png"), size=(86, 40))
        self.logo_label_img = ctk.CTkLabel(self.sidebar_frame, image=logo_img, text="")
        self.logo_label_img.grid(row=0, column=0, padx=(25, 128), pady=(25, 0), sticky="w")
        logo2_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/logo2.png"), size=(20, 20))
        self.logo_label_img2 = ctk.CTkLabel(self.sidebar_frame, image=logo2_img, text="")
        self.logo_label_img2.grid(row=0, column=0, padx=(0, 26), pady=(44, 0), sticky="e")
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NetCon 2.0", font=ctk.CTkFont(family="Unispace", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(74, 0), pady=(25, 0), sticky="w")
        logo3_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/logo3.png"), size=(54, 38))
        self.logo_label_img3 = ctk.CTkLabel(self.sidebar_frame, image=logo3_img, text="")
        self.logo_label_img3.grid(row=1, column=0, padx=(0, 26), pady=(5, 0), sticky="e")
        self.name_label = ctk.CTkLabel(self.sidebar_frame, text="● by Valid Halil ", font=ctk.CTkFont(family="Unispace", size=11, weight="bold"))
        self.name_label.grid(row=1, column=0, padx=(0, 37), pady=(6, 0), sticky="e")

        self.language_list = ["Русский", "Английский"]
        self.theme_list = ["Темная", "Светлая"]
        self.transparent_list = ["Отсутствует", "25%", "50%", "75%", "100%"]
        self.scaling_list = ["95%", "100%", "105%"]

        self.transparancy_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Прозрачность:", anchor="w", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.transparancy_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.transparancy_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, fg_color="#1F538D", values=self.transparent_list, command=lambda trans_var: change_transparency_mode(self.transparancy_mode_optionemenu.get()))
        self.transparancy_mode_optionemenu.configure(font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.transparancy_mode_optionemenu.set(value=opacity)
        self.transparancy_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(5, 0))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="Масштаб:", anchor="w", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.scaling_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=self.scaling_list, command=lambda ch_sc: change_scaling_event(self.scaling_optionemenu.get()), fg_color="#1F538D")
        self.scaling_optionemenu.set(value=scale)
        self.scaling_optionemenu.configure(font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.scaling_optionemenu.grid(row=7, column=0, padx=20, pady=(5, 0))

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Тема:", anchor="w", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=self.theme_list, command=lambda theme_var: change_appearance_mode(self.appearance_mode_optionemenu.get()), fg_color="#1F538D")
        self.appearance_mode_optionemenu.configure(font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.appearance_mode_optionemenu.set(value=theme)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(5, 0))

        self.language_label = ctk.CTkLabel(self.sidebar_frame, text="Язык:", anchor="w", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.language_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.language_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, fg_color="#1F538D", values=self.language_list, command=lambda lang_var: [self.after(50, lambda: change_language(self.language_optionemenu.get(), self.appearance_mode_optionemenu.get(), self.transparancy_mode_optionemenu.get()))])
        self.language_optionemenu.configure(font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.language_optionemenu.set(value=language)
        self.language_optionemenu.grid(row=11, column=0, padx=20, pady=(5, 30))

        # --------------------------------------------TAB Начало--------------------------------------------

        self.tabview.tab("Начальное окно").grid_columnconfigure((1), weight=1)
        self.tabview.tab("Начальное окно").grid_columnconfigure((2), weight=1)
        self.tabview.tab("Начальное окно").grid_rowconfigure((1, 6), weight=1)
        self.tabview.tab("Начальное окно").grid_rowconfigure((2, 3, 4, 5), weight=0)

        hello1_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/hello1.png"), size=(110, 110))
        self.hello1_label_img = ctk.CTkLabel(self.tabview.tab("Начальное окно"), image=hello1_img, text="")
        self.hello1_label_img.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="ne")

        self.label_hello = ctk.CTkLabel(self.tabview.tab("Начальное окно"), text="Привет!", font=ctk.CTkFont(family="Corbel", size=48, weight="bold"))
        self.label_hello.grid(row=2, column=1, padx=(115, 0), pady=(0, 0), sticky="w")
        self.label_hello2 = ctk.CTkLabel(self.tabview.tab("Начальное окно"), text='Спасибо, что пользуетесь приложением "NetCon 2.0".', font=ctk.CTkFont(family="Corbel", size=24, weight="normal"))
        self.label_hello2.grid(row=3, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
        self.label_hello3 = ctk.CTkLabel(self.tabview.tab("Начальное окно"), text='Приложение находится на стадии разработки, так что', font=ctk.CTkFont(family="Corbel", size=24, weight="normal"))
        self.label_hello3.grid(row=4, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
        self.label_hello4 = ctk.CTkLabel(self.tabview.tab("Начальное окно"), text='вот мой Telegram для обратной связи:', font=ctk.CTkFont(family="Corbel", size=24, weight="normal"))
        self.label_hello4.grid(row=5, column=1, padx=(115, 0), pady=(10, 0), sticky="w")
        self.hello_button_1 = ctk.CTkButton(master=self.tabview.tab("Начальное окно"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Corbel"), size=20, weight="normal"), text="t.me/ValidHalil", command=get_contact)
        self.hello_button_1.grid(row=5, column=1, padx=(530, 115), pady=(10, 0), sticky="we")
        self.hello_line2 = ctk.CTkLabel(self.tabview.tab("Начальное окно"), text="──────────────────────────────────", text_color="gray32", font=ctk.CTkFont(size=30, weight="normal"))
        self.hello_line2.grid(row=6, column=1, columnspan=1, padx=(120, 120), pady=(0, 0), sticky="nsew")

        hello2_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/hello2.png"), size=(130, 130))
        self.hello2_label_img = ctk.CTkLabel(self.tabview.tab("Начальное окно"), image=hello2_img, text="")
        self.hello2_label_img.grid(row=7, column=1, padx=(0, 0), pady=(0, 0), sticky="sw")

        self.hello_button_2 = ctk.CTkButton(master=self.tabview.tab("Начальное окно"), fg_color="#de710b", border_width=0, hover_color="#ab590c", text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Corbel"), size=30, weight="bold"), text="Начать", command=open_tab1)
        self.hello_button_2.grid(row=7, column=1, padx=(115, 115), pady=(5, 120), sticky="ew", ipady=5)

        # --------------------------------------------TAB 1--------------------------------------------

        self.tabview.tab("Подключение").grid_columnconfigure((1), weight=0)
        self.tabview.tab("Подключение").grid_columnconfigure((2), weight=1)
        self.tabview.tab("Подключение").grid_rowconfigure((5), weight=1)

        x = tkinter.StringVar()
        x_tr = tkinter.StringVar()
        x3 = tkinter.StringVar()

        clear_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/clear.png"), size=(20, 20))
        cleartext_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/cleartext.png"), size=(18, 18))
        help_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help.png"), size=(37, 18))
        help_eng_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help_eng.png"), size=(37, 15))
        consolelog_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/consolelog.png"), size=(75, 18))
        show_bd_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/show_bd.png"), size=(110, 18))
        show_bd_eng_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/show_bd_eng.png"), size=(80, 16))

        self.label1 = ctk.CTkLabel(self.tabview.tab("Подключение"), text="Do Ping:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label1.grid(row=1, column=1, padx=(50, 0), pady=(30, 5), sticky="w")
        self.ping_label_img = ctk.CTkLabel(self.tabview.tab("Подключение"), image=ping_img, text="")
        self.ping_label_img.grid(row=1, column=1, padx=(18, 0), pady=(30, 5), sticky="w")
        self.entry1 = ctk.CTkEntry(self.tabview.tab("Подключение"), textvariable=x, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry1.grid(row=1, column=1, columnspan=5, padx=(145, 89), pady=(30, 5), sticky="nsew")
        self.entry1.bind("<Return>", lambda entry1_var: execute_cmd(str(x.get()), self.combobox_ping.get(), self.entry1))
        self.entry1.bind("<Button-1>", lambda into_entry: left_click(self.entry1))
        self.entry1.bind("<Down>", lambda open_var: [self.combobox_ping._clicked(), self.after(50, lambda: self.entry1.focus_set())])
        self.entry1.bind("<Delete>", lambda del_var: clear_entry_ip(self.entry1, self.combobox_ping))
        self.entry1.bind("<FocusIn>", lambda focus_on: self.after(70, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.entry1.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))] if self.tabview.get() == "Подключение" else print("sss"))

        self.combobox_ping = ctk.CTkComboBox(self.tabview.tab("Подключение"), values=["None", "/t", "/a", "win", "/t win", "/a win"], width=80, justify="c", state="readonly", font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.combobox_ping.grid(row=1, column=5, columnspan=1, padx=(0, 0), pady=(30, 5), sticky="nsew")
        self.combobox_ping.set(value="None")
        self.combobox_ping.bind("<Down>", lambda open_var: self.combobox_ping._clicked())
        self.combobox_ping.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_ping.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))] if self.tabview.get() == "Подключение" else print("sss"))
        self.combobox_ping.bind("<Return>", lambda entry1_var: execute_cmd(str(x.get()), self.combobox_ping.get(), self.entry1))
        self.main_button_1 = ctk.CTkButton(master=self.tabview.tab("Подключение"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Начать", command=lambda: execute_cmd(str(x.get()), self.combobox_ping.get(), self.entry1))
        self.main_button_1.grid(row=1, column=6, padx=(20, 0), pady=(30, 5), sticky="nsew")
        self.clear_btn_ip = ctk.CTkButton(master=self.tabview.tab("Подключение"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry_ip(self.entry1, self.combobox_ping))
        self.clear_btn_ip.grid(row=1, column=7, padx=(10, 20), pady=(30, 5), sticky="e")
        ip_entry_string_last_valid = [u"..."]
        x.trace("w", lambda *args: entry_mask_check(x, ip_entry_string_last_valid, self.entry1))
        x.set("")

        self.label2 = ctk.CTkLabel(self.tabview.tab("Подключение"), text="Tracert:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label2.grid(row=2, column=1, padx=(50, 0), pady=(10, 20), sticky="w")
        self.tracert_label_img = ctk.CTkLabel(self.tabview.tab("Подключение"), image=tracert_img, text="")
        self.tracert_label_img.grid(row=2, column=1, padx=(18, 0), pady=(10, 20), sticky="w")
        self.entry_tracert = ctk.CTkEntry(self.tabview.tab("Подключение"), textvariable=x_tr, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry_tracert.grid(row=2, column=1, columnspan=5, padx=(145, 89), pady=(10, 20), sticky="nsew")
        self.entry_tracert.bind("<Return>", lambda entry_tracert_var: execute_cmd(str(x_tr.get()), self.combobox_tracert.get(), self.entry_tracert))
        self.entry_tracert.bind("<Button-1>", lambda into_entry: left_click(self.entry_tracert))
        self.entry_tracert.bind("<Down>", lambda open_var: [self.combobox_tracert._clicked(), self.after(50, lambda: self.entry_tracert.focus_set())])
        self.entry_tracert.bind("<Delete>", lambda del_var: clear_entry_ip(self.entry_tracert, self.combobox_tracert))
        self.entry_tracert.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.entry_tracert.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))] if self.tabview.get() == "Подключение" else print("sss"))

        self.combobox_tracert = ctk.CTkComboBox(self.tabview.tab("Подключение"), values=[" None ", "/d", "/j", " win ", "/d win", "/j win"], width=80, justify="c", state="readonly", font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.combobox_tracert.grid(row=2, column=5, padx=(0, 0), pady=(10, 20), sticky="nsew")
        self.combobox_tracert.set(value=" None ")
        self.combobox_tracert.bind("<Down>", lambda open_var: self.combobox_tracert._clicked())
        self.combobox_tracert.bind("<FocusIn>", lambda focus_on: self.after(70, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_tracert.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))] if self.tabview.get() == "Подключение" else print("sss"))
        self.combobox_tracert.bind("<Return>", lambda entry_tracert_var: execute_cmd(str(x_tr.get()), self.combobox_tracert.get(), self.entry_tracert))
        self.main_button_2 = ctk.CTkButton(master=self.tabview.tab("Подключение"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Начать", command=lambda: execute_cmd(str(x_tr.get()), self.combobox_tracert.get(), self.entry_tracert))
        self.main_button_2.grid(row=2, column=6, padx=(20, 0), pady=(10, 20), sticky="nsew")
        self.clear_btn_tracert = ctk.CTkButton(master=self.tabview.tab("Подключение"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry_ip(self.entry_tracert, self.combobox_tracert))
        self.clear_btn_tracert.grid(row=2, column=7, padx=(10, 20), pady=(10, 20), sticky="e")
        ip_entry_string_last_valid_trace = [u"..."]
        x_tr.trace("w", lambda *args: entry_mask_check(x_tr, ip_entry_string_last_valid_trace, self.entry_tracert))
        x_tr.set("")

        self.label_con = ctk.CTkLabel(self.tabview.tab("Подключение"), text="", image=consolelog_img, font=ctk.CTkFont(size=11, weight="bold"))
        self.label_con.grid(row=3, column=1, padx=20, pady=(0, 4), sticky="w")
        self.help_btn_tab1 = ctk.CTkButton(master=self.tabview.tab("Подключение"), width=20, fg_color=("#e5e5e5", "#212121"), text_color="gray32", hover_color=("white", "#333333"), border_width=0, image=help_img, text="", font=ctk.CTkFont(size=11, weight="bold"), command=lambda: help(self.tabview.get()))
        self.help_btn_tab1.grid(row=3, column=6, padx=(0, 0), pady=(0, 5), sticky="e")
        self.clear_btn = ctk.CTkButton(master=self.tabview.tab("Подключение"), width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), text="", image=cleartext_img, border_width=0, command=lambda: clear_text(self.textbox))
        self.clear_btn.grid(row=3, column=7, padx=(0, 20), pady=(0, 5), sticky="e")
        self.textbox = ctk.CTkTextbox(self.tabview.tab("Подключение"), width=250, state="disabled")
        self.textbox.grid(row=4, rowspan=2, column=1, columnspan=7, padx=(20, 20), pady=(0, 13), sticky="nsew")

        self.label_line = ctk.CTkLabel(self.tabview.tab("Подключение"), text="────────────────────────────────────────────────────────────────────────────", text_color="gray32", font=ctk.CTkFont(size=22, weight="normal"))
        self.label_line.grid(row=6, column=1, columnspan=7, padx=24, pady=(0, 11))

        self.label3 = ctk.CTkLabel(self.tabview.tab("Подключение"), text="Подключение:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label3.grid(row=7, column=1, padx=(50, 0), pady=(15, 30), sticky="w")
        self.tel_label_img = ctk.CTkLabel(self.tabview.tab("Подключение"), image=telnet_img, text="")
        self.tel_label_img.grid(row=7, column=1, padx=(18, 0), pady=(15, 30), sticky="w")
        self.entry3 = ctk.CTkEntry(self.tabview.tab("Подключение"), textvariable=x3, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry3.grid(row=7, column=2, columnspan=3, padx=(18, 92), pady=(15, 30), sticky="ew")
        self.entry3.bind("<Return>", lambda entry3_var: clicked2(self.radio_var))
        self.entry3.bind("<Button-1>", lambda into_entry: left_click(self.entry3))
        self.entry3.bind("<Delete>", lambda del_var: clear_entry_telnet(self.entry3, self.radio_var))
        self.entry3.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())] if self.tabview.get() == "Подключение" else print("sss")))
        self.entry3.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox.yview_scroll(-1, "units")))] if self.tabview.get() == "Подключение" else print("sss"))
        ip_entry_string_last_valid2 = [u"..."]
        x3.trace("w", lambda *args: entry_mask_check(x3, ip_entry_string_last_valid2, self.entry3))
        x3.set("")

        self.radio_var = tkinter.IntVar(value=1)
        self.radio_button_1 = ctk.CTkRadioButton(master=self.tabview.tab("Подключение"), text="Telnet", variable=self.radio_var, value=1, width=5, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"), command = lambda: self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84")))
        self.radio_button_1.grid(row=7, column=4, pady=(4, 0), padx=(0, 0), sticky="new")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.tabview.tab("Подключение"), text="SSH", variable=self.radio_var, value=2, width=5, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"), command = lambda: self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84")))
        self.radio_button_3.grid(row=7, column=5, pady=(4, 0), padx=(20, 0), sticky="new")
        self.radio_button_4 = ctk.CTkRadioButton(master=self.tabview.tab("Подключение"), text="Serial", variable=self.radio_var, value=3, width=5, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"), command = lambda: self.entry3.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45")))
        self.radio_button_4.grid(row=7, column=4, pady=(0, 19), padx=(0, 0), sticky="sew")
        self.radio_button_2 = ctk.CTkRadioButton(master=self.tabview.tab("Подключение"), text="Web", variable=self.radio_var, value=4, width=5, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"), command = lambda: self.entry3.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84")))
        self.radio_button_2.grid(row=7, column=5, pady=(0, 19), padx=(20, 0), sticky="sew")
        self.entry3.bind('<Down>', lambda sex: next_radio(self.radio_var))
        self.entry3.bind('<Up>', lambda sex: prev_radio(self.radio_var))

        self.main_button_3 = ctk.CTkButton(master=self.tabview.tab("Подключение"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Открыть", command=lambda: clicked2(self.radio_var))
        self.main_button_3.grid(row=7, column=6, padx=(20, 0), pady=(15, 30), sticky="ew")
        self.clear_btn_telnet = ctk.CTkButton(master=self.tabview.tab("Подключение"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry_telnet(self.entry3, self.radio_var))
        self.clear_btn_telnet.grid(row=7, column=7, padx=(10, 20), pady=(15, 30), sticky="e")

        # --------------------------------------------TAB 2--------------------------------------------

        x2 = tkinter.StringVar()
        x4 = tkinter.StringVar()
        x5 = tkinter.StringVar()
        x6 = tkinter.StringVar()
        x7 = tkinter.StringVar()
        x8 = tkinter.StringVar()

        self.tabview.tab("Параметры сети").grid_columnconfigure((1, 2, 3), weight=0)
        self.tabview.tab("Параметры сети").grid_columnconfigure((5, 7, 4, 6), weight=1)
        self.tabview.tab("Параметры сети").grid_rowconfigure((3, 11), weight=1)
        self.tabview.tab("Параметры сети").grid_rowconfigure((8), weight=0)

        self.label_ipconfig = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Вывод IpConfig:", font=ctk.CTkFont(family="Trebuchet MS", size=19, weight="bold"))
        self.label_ipconfig.grid(row=1, column=1, padx=(50, 0), pady=(30, 5), sticky="w")
        self.ipconfig_label_img = ctk.CTkLabel(self.tabview.tab("Параметры сети"), image=ipconfig_img, text="")
        self.ipconfig_label_img.grid(row=1, column=1, padx=(18, 0), pady=(30, 5), sticky="w")
        self.combobox_ipconfig = PlaceholderComboBox(self.tabview.tab("Параметры сети"), values=["/all", "/displaydns", "/showclassid *"], width=155, variable=x2, command=lambda combo_var: combo_focus(self.combobox_ipconfig), placeholder_text="Выберите из списка или введите...")
        self.combobox_ipconfig.grid(row=1, column=1, columnspan=7, padx=(210, 0), pady=(30, 5), sticky="nsew")
        self.combobox_ipconfig.bind("<Return>", lambda combobox_ipconfig: execute_cmd2("ipconfig " + str(x2.get())))
        self.combobox_ipconfig.bind("<Down>", lambda open_var: self.combobox_ipconfig._clicked())
        self.combobox_ipconfig.bind("<Delete>", lambda del_var: clear_entry(self.combobox_ipconfig))
        self.combobox_ipconfig.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_ipconfig.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.button_ipconfig = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Показать", command=lambda: execute_cmd2("ipconfig " + str(x2.get())))
        self.button_ipconfig.grid(row=1, column=8, padx=(20, 10), pady=(30, 5), sticky="nsew")
        self.clear_btn_ipconfig = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.combobox_ipconfig))
        self.clear_btn_ipconfig.grid(row=1, column=9, padx=(0, 20), pady=(30, 5), sticky="e")

        self.label4 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Имя адаптера:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label4.grid(row=2, column=1, padx=(50, 0), pady=(10, 10), sticky="w")
        self.adapter_label_img = ctk.CTkLabel(self.tabview.tab("Параметры сети"), image=adapter_img, text="")
        self.adapter_label_img.grid(row=2, column=1, padx=(18, 0), pady=(10, 10), sticky="w")
        self.combobox_2 = PlaceholderComboBox(self.tabview.tab("Параметры сети"), variable=x4, width=285, command=lambda combo_var: combo_focus(self.combobox_2), placeholder_text="Выберите из списка или введите...")
        self.combobox_2.grid(row=2, column=1, columnspan=7, padx=(210, 0), pady=(10, 10), sticky="nsew")
        self.combobox_2.bind("<Return>", lambda combobox_2_var: execute_cmd3('netsh interface ipv4 show config name="' + str(x4.get()) + '"'))
        self.combobox_2.bind("<Down>", lambda open_var: get_adapters_list(self.combobox_2))
        self.combobox_2.bind("<Delete>", lambda del_var: clear_entry(self.combobox_2))
        self.combobox_2._canvas.bind("<Enter>", lambda ada: get_adapters_list_click(self.combobox_2)) # Для обновления списка именно перед кликом (грязно-грязно)
        self.combobox_2.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_2.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.main_button_4 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Показать", command=lambda: execute_cmd3('netsh interface ipv4 show config name="' + str(x4.get()) + '"'))
        self.main_button_4.grid(row=2, column=8, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.clear_btn_adapter = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.combobox_2))
        self.clear_btn_adapter.grid(row=2, column=9, padx=(0, 20), pady=(10, 10), sticky="e")

        self.label_line2 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="────────────────────────────────────────────────────────────────────────────", text_color="gray32", font=ctk.CTkFont(size=22, weight="normal"))
        self.label_line2.grid(row=3, column=1, columnspan=9, padx=24, pady=(10, 10))

        self.label_con2 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="", image=consolelog_img, height=19)
        self.label_con2.grid(row=4, column=3, padx=(0, 0), pady=(0, 3), sticky="sw")
        self.help_btn_tab2 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color=("#e5e5e5", "#212121"), text_color="gray32", hover_color=("white", "#333333"), height=18, border_width=0, image=help_img, text="", font=ctk.CTkFont(size=11, weight="bold"), command=lambda: help(self.tabview.get()))
        self.help_btn_tab2.grid(row=4, column=8, padx=(0, 0), pady=(20, 0), sticky="e")
        self.clear_btn2 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=cleartext_img, height=18, border_width=0, text="", command=lambda: clear_text(self.textbox2))
        self.clear_btn2.grid(row=4, column=9, padx=(0, 20), pady=(20, 0), sticky="se")
        self.textbox2 = ctk.CTkTextbox(self.tabview.tab("Параметры сети"), width=1100, state="disabled")
        self.textbox2.grid(row=4, rowspan=8, column=3, columnspan=8, padx=(0, 20), pady=(55, 19), sticky="nsew")

        self.label5_1 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Настройки адаптера:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label5_1.grid(row=4, column=1, columnspan=4, padx=(50, 15), pady=(0, 0), sticky="w")
        self.settings_label_img = ctk.CTkLabel(self.tabview.tab("Параметры сети"), image=settings_img, text="")
        self.settings_label_img.grid(row=4, column=1, padx=(18, 0), pady=(0, 0), sticky="w")

        self.label5 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Имя:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.label5.grid(row=5, column=1, padx=(20, 10), pady=(10, 20), sticky="w")
        self.combobox_3 = ctk.CTkComboBox(self.tabview.tab("Параметры сети"), width=137, variable=x8, command=lambda combo_var: combo_focus(self.combobox_3))
        self.combobox_3.grid(row=5, column=1, padx=(80, 0), pady=(10, 20), sticky="nsew")
        self.combobox_3.bind("<Down>", lambda open_var: get_adapters_list(self.combobox_3))
        self.combobox_3.bind("<Return>", lambda entry7_var: execute_cmd4('netsh interface ipv4 set address name="' + str(x8.get()) + '"' + " static " + str(x5.get()) + " " + str(x6.get()) + " " + str(x7.get())))
        self.combobox_3.bind("<Delete>", lambda del_var: clear_entry(self.combobox_3))
        self.combobox_3._canvas.bind("<Enter>", lambda ada: get_adapters_list_click(self.combobox_3)) # Для обновления списка именно перед кликом (грязно-грязно)
        self.combobox_3.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_3.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.clear_btn_adapter2 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.combobox_3))
        self.clear_btn_adapter2.grid(row=5, column=2, padx=(10, 20), pady=(10, 20), sticky="w")

        self.label6 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="IP-адр:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.label6.grid(row=6, column=1, padx=(20, 10), pady=(0, 20), sticky="w")
        self.entry6 = ctk.CTkEntry(self.tabview.tab("Параметры сети"), textvariable=x5, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry6.grid(row=6, column=1, padx=(80, 0), pady=(0, 20), sticky="nsew")
        self.entry6.bind("<Return>", lambda entry6_var: execute_cmd4('netsh interface ipv4 set address name="' + str(x8.get()) + '"' + " static " + str(x5.get()) + " " + str(x6.get()) + " " + str(x7.get())))
        self.entry6.bind("<Button-1>", lambda into_entry: left_click(self.entry6))
        self.entry6.bind("<Delete>", lambda del_var: clear_entry(self.entry6))
        self.entry6.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.entry6.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.clear_btn_ips = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.entry6))
        self.clear_btn_ips.grid(row=6, column=2, padx=(10, 20), pady=(0, 20), sticky="w")
        ip_entry_string_last_valid3 = [u"..."]
        x5.trace("w", lambda *args: entry_mask_check(x5, ip_entry_string_last_valid3, self.entry6))
        x5.set("")

        self.label7 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Маска:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.label7.grid(row=7, column=1, padx=(20, 10), pady=(0, 20), sticky="w")
        self.entry7 = ctk.CTkEntry(self.tabview.tab("Параметры сети"), textvariable=x6, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry7.grid(row=7, column=1, padx=(80, 0), pady=(0, 20), sticky="nsew")
        self.entry7.bind("<Return>", lambda entry7_var: execute_cmd4('netsh interface ipv4 set address name="' + str(x8.get()) + '"' + " static " + str(x5.get()) + " " + str(x6.get()) + " " + str(x7.get())))
        self.entry7.bind("<Button-1>", lambda into_entry: left_click(self.entry7))
        self.entry7.bind("<Delete>", lambda del_var: clear_entry(self.entry7))
        self.entry7.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.entry7.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.clear_btn_mask = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.entry7))
        self.clear_btn_mask.grid(row=7, column=2, padx=(10, 20), pady=(0, 20), sticky="w")
        ip_entry_string_last_valid4 = [u"..."]
        x6.trace("w", lambda *args: entry_mask_check(x6, ip_entry_string_last_valid4, self.entry7))
        x6.set("")

        self.label8_1 = ctk.CTkLabel(self.tabview.tab("Параметры сети"), text="Шлюз:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.label8_1.grid(row=8, column=1, padx=(20, 0), pady=(0, 20), sticky="w")
        self.entry8 = ctk.CTkEntry(self.tabview.tab("Параметры сети"), textvariable=x7, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.entry8.grid(row=8, column=1, padx=(80, 0), pady=(0, 20), sticky="nsew")
        self.entry8.bind("<Return>", lambda entry8_var: execute_cmd4('netsh interface ipv4 set address name="' + str(x8.get()) + '"' + " static " + str(x5.get()) + " " + str(x6.get()) + " " + str(x7.get())))
        self.entry8.bind("<Button-1>", lambda into_entry: left_click(self.entry8))
        self.entry8.bind("<Delete>", lambda del_var: clear_entry(self.entry8))
        self.entry8.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.unbind("<Down>"), self.unbind("<Up>"), self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.entry8.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.after(50, lambda: self.bind("<Down>", lambda next: self.textbox2.yview_scroll(1, "units"))), self.after(50, lambda: self.bind("<Up>", lambda next: self.textbox2.yview_scroll(-1, "units")))] if self.tabview.get() == "Параметры сети" else print("sss"))
        self.clear_btn_gate = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), width=20, fg_color="#de710b", border_width=0, hover_color="#ab590c", image=clear_img, text="", command=lambda: clear_entry(self.entry8))
        self.clear_btn_gate.grid(row=8, column=2, padx=(10, 20), pady=(0, 20), sticky="w")
        ip_entry_string_last_valid5 = [u"..."]
        x7.trace("w", lambda *args: entry_mask_check(x7, ip_entry_string_last_valid5, self.entry8))
        x7.set("")

        self.main_button_5 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Применить", command=lambda: execute_cmd4('netsh interface ipv4 set address name="' + str(x8.get()) + '"' + " static " + str(x5.get()) + " " + str(x6.get()) + " " + str(x7.get())))
        self.main_button_5.grid(row=9, column=1, columnspan=2, padx=(20, 20), pady=(0, 15), ipady=4, sticky="nsew")

        self.main_button_55 = ctk.CTkButton(master=self.tabview.tab("Параметры сети"), fg_color="#de710b", border_width=0, hover_color="#ab590c", text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text='Включить "DHCP"', command=lambda: execute_cmd5('netsh interface ip set address name = "' + str(x8.get()) + '" dhcp'))
        self.main_button_55.grid(row=10, column=1, columnspan=2, padx=(20, 20), pady=(0, 20), ipady=4, sticky="nsew")

        # --------------------------------------------TAB 3--------------------------------------------

        name_db = tkinter.StringVar()

        self.tabview.tab("База адресов").grid_columnconfigure((1), weight=0)
        self.tabview.tab("База адресов").grid_columnconfigure((2), weight=1)
        self.tabview.tab("База адресов").grid_rowconfigure((3, 4, 6, 7, 8), weight=1)

        disconnect_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/discon.png"), size=(20, 20))
        disconnect_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/discon_dis.png"), size=(20, 20))
        self.baza_label_img = ctk.CTkLabel(self.tabview.tab("База адресов"), image=baza_img, text="")
        self.baza_label_img.grid(row=1, column=1, padx=(18, 0), pady=(30, 20), sticky="w")
        self.label8 = ctk.CTkLabel(self.tabview.tab("База адресов"), text="Название БД:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label8.grid(row=1, column=1, padx=(50, 0), pady=(30, 20), sticky="w")
        self.devices = ["Коммутаторы", "Маршрутизаторы", "Мультиплексоры", "Электропитание", "Телефоны", "Другое"]
        self.combobox_4 = PlaceholderComboBox(self.tabview.tab("База адресов"), values=self.devices, variable=name_db, width=175, command=lambda combo_var: combo_focus(self.combobox_4, flag=1), placeholder_text="Выберите из списка или введите...")
        self.combobox_4.grid(row=1, column=2, columnspan=2, padx=(12, 0), pady=(30, 20), sticky="nsew")
        self.combobox_4.bind("<Return>", lambda combobox_4_var: show_db(name_db, self.listbox))
        self.combobox_4.bind("<Down>", lambda open_var: self.combobox_4._clicked())
        self.combobox_4.bind("<Delete>", lambda del_var: clear_entry(self.combobox_4))
        self.combobox_4.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.bind('<Escape>', lambda escape_entry: right_click())]))
        self.combobox_4.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app())])

        self.main_button_6 = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Соединить", command=lambda: show_db(name_db, self.listbox))
        self.main_button_6.grid(row=1, column=4, padx=(20, 10), pady=(30, 20), sticky="nsew")
        self.clear_btn_baza = ctk.CTkButton(master=self.tabview.tab("База адресов"), width=20, state="disabled", fg_color="#ab590c", border_width=0, hover_color="#ab590c", image=disconnect_disabled_img, text="", command=lambda: clear_entry_baza(self.combobox_4))
        self.clear_btn_baza.grid(row=1, column=5, padx=(0, 20), pady=(30, 20), sticky="e")

        self.label_con3 = ctk.CTkLabel(self.tabview.tab("База адресов"), text="", image=show_bd_img)
        self.label_con3.grid(row=2, column=2, padx=(12, 0), pady=(0, 5), sticky="w")
        self.help_btn_tab3 = ctk.CTkButton(master=self.tabview.tab("База адресов"), width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), border_width=0, image=help_img, text="", command=lambda: help(self.tabview.get()))
        self.help_btn_tab3.grid(row=2, column=4, padx=(0, 10), pady=(0, 5), sticky="e")
        self.clear_btn3 = ctk.CTkButton(master=self.tabview.tab("База адресов"), width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=cleartext_img, border_width=0, text="", command=lambda: [clear_text(self.listbox), clear_count()])
        self.clear_btn3.grid(row=2, column=5, padx=(0, 20), pady=(0, 5), sticky="e")

        self.previous_selected = None
        self.listbox = CTkListbox(self.tabview.tab("База адресов"), fg_color=("white", "#333333"), border_width=0, button_color=("#e5e5e5", "#212121"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="normal"), orientation="vertical", orientation2="horizontal", width=560)
        self.listbox.grid(row=3, rowspan=6, column=2, columnspan=4, padx=(12, 20), pady=(0, 0), sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', lambda list_var: open_con_listbox())
        self.bind('<ButtonPress-1>', self.deselect_item)
        self.bind('<Button-2>', self.deselect_item)  # Возможно стоит убрать нахуй потом

        self.textbox3 = ctk.CTkTextbox(self.tabview.tab("База адресов"), width=50, height=20, border_width=2, font=ctk.CTkFont(family=("Trebuchet MS"), size=11, weight="bold"), state="disabled", border_color=("#8f8f8f", "#444444"))
        self.textbox3.grid(row=3, column=1, padx=(95, 19), pady=(0, 0), sticky="ew")
        self.label9 = ctk.CTkLabel(self.tabview.tab("База адресов"), text="Записей:", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.label9.grid(row=3, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.con_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Открыть", command=selected_item)
        self.con_button.grid(row=4, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.update_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Обновить", command=lambda: [refresh_db(name_db, self.listbox)])
        self.update_button.grid(row=5, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.add_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Добавить", command=lambda: [add_item(name_db, self.listbox)])
        self.add_button.grid(row=6, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.update_row_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Изменить", command=lambda: [update_item(name_db, self.listbox)])
        self.update_row_button.grid(row=7, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.del_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#de710b", hover_color="#ab590c", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Удалить", command=lambda: delete_item(name_db, self.listbox))
        self.del_button.grid(row=8, column=1, padx=(23, 0), pady=(0, 0), sticky="w")
        self.label_line3 = ctk.CTkLabel(self.tabview.tab("База адресов"), text="────────────────────────────────────────────────────────────────────────────", text_color="gray32", font=ctk.CTkFont(size=22, weight="normal"))
        self.label_line3.grid(row=9, column=1, columnspan=5, padx=24, pady=(15, 15))

        search_var = tkinter.StringVar()
        #combo5_values = ["РС_ЦиП_РЗ_ПС", "РС_ЦиП_РЗ_РПБ", "Eltex", "Cisco", "MikroTik", "Nortel", "10.62.", "SWMP", "SWLU", "SWOD", "SWOC", "SWOQ", "RMPP", "RMP"]
        combo5_values = ["192.168.", "172.16.", "10.", "Cisco", "MikroTik", "Nortel", "Eltex", "Yealink", "Huawei", "TP-Link", "D-Link", "Zyxel", "Juniper"] # Для продакшна

        self.label10 = ctk.CTkLabel(self.tabview.tab("База адресов"), text="Поиск в БД:", font=ctk.CTkFont(family="Trebuchet MS", size=20, weight="bold"))
        self.label10.grid(row=10, column=1, padx=(50, 0), pady=(0, 20), sticky="w")
        self.combobox_5 = PlaceholderComboBox(self.tabview.tab("База адресов"), values=combo5_values, variable=search_var, width=138, command=lambda combo_var: combo_focus(self.combobox_5), placeholder_text="Требуется подключение к БД...") #width = 138/175
        self.combobox_5.grid(row=10, column=2, columnspan=2, padx=(12, 0), pady=(0, 20), sticky="ew")
        self.combobox_5.bind("<Return>", lambda combobox_5_var: [search_item(name_db, self.listbox, self.combobox_5.get())])
        self.combobox_5.bind("<Down>", lambda open_var: self.combobox_5._clicked())
        self.combobox_5.bind("<Delete>", lambda del_var: clear_entry(self.combobox_5))
        self.combobox_5.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.bind('<Escape>', lambda escape_entry: right_click()), self.unbind("<KeyPress-Control_L>")]))
        self.combobox_5.bind("<FocusOut>", lambda focus_out: [self.bind('<Escape>', lambda close: close_app()), self.bind("<KeyPress-Control_L>", on_ctrl_press)])

        clear_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/clear_dis.png"), size=(20, 20))
        self.search_button = ctk.CTkButton(master=self.tabview.tab("База адресов"), fg_color="#1F538D", border_width=0, text_color=("white", "#DCE4EE"), font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), text="Найти", command=lambda: search_item(name_db, self.listbox, self.combobox_5.get()))
        self.search_button.grid(row=10, column=4, padx=(20, 10), pady=(0, 20), sticky="ew")
        self.clear_btn_search = ctk.CTkButton(master=self.tabview.tab("База адресов"), state="disabled", fg_color="#ab590c", width=20, border_width=0, hover_color="#ab590c", image=clear_disabled_img, text="", command=lambda: clear_entry(self.combobox_5))
        self.clear_btn_search.grid(row=10, column=5, padx=(0, 20), pady=(0, 20), sticky="e")
        self.search_label_img = ctk.CTkLabel(self.tabview.tab("База адресов"), image=search_img, text="")
        self.search_label_img.grid(row=10, column=1, padx=(18, 0), pady=(0, 22), sticky="w")

        self.con_button.configure(state="disabled", fg_color="#14375e")
        self.search_button.configure(state="disabled", fg_color="#14375e")
        self.del_button.configure(state="disabled", fg_color="#ab590c")
        self.update_row_button.configure(state="disabled", fg_color="#14375e")
        self.add_button.configure(state="disabled", fg_color="#14375e")
        self.update_button.configure(state="disabled", fg_color="#14375e")
        self.combobox_5.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))

        # Секция от остаточных багов после выбора эл-та листбокс (ебейший антибаг в деле (ЕБАНЫЕ ХОТКЕИИИИИ))

        self.tabview.tab("База адресов").bind('<Button-1>', lambda antibag: antibug())
        self.combobox_5.bind('<FocusIn>', lambda antibag: antibug())
        self.combobox_4.bind('<FocusIn>', lambda antibag: antibug())
        self.clear_btn_baza.bind('<Button-1>', lambda antibag: antibug())
        self.clear_btn_search.bind('<Button-1>', lambda antibag: antibug())
        self.label10.bind('<Button-1>', lambda antibag: antibug())
        self.label9.bind('<Button-1>', lambda antibag: antibug())
        self.label8.bind('<Button-1>', lambda antibag: antibug())
        self.clear_btn3.bind('<Button-1>', lambda antibag77: antibug())
        self.scaling_optionemenu.bind('<Button-1>', lambda antibag228: antibug())
        # self.search_button.bind('<Button-1>', lambda antibag: antibug()) # Ну тут пока спорно, могут быть баги но это не точно!

        change_language(self.language_optionemenu.get(), theme, opacity)
        change_transparency_mode(self.transparancy_mode_optionemenu.get())
        change_appearance_mode(self.appearance_mode_optionemenu.get())
        change_scaling_event(self.scaling_optionemenu.get())

        threading.Thread(target=self.run_update_open_ssh, daemon=True).start()

    # Все приколы теперь в батнике (UPD: теперь есть обработка ошибки отсутствия файла настройки, запускается не батник а ярлык на него (для свернутого отображения))
    def run_update_open_ssh(self):
        try:
            os.startfile(self.path_img + "tools/RunUpdate.lnk")
            self.after(5000, lambda: self.create_ssh_config())  # Запуск создания файла конфигурации SSH с задержкой, чтобы успела создаться папка .ssh в сабпроцессе (если вдруг ее еще нет)
        except:
            if self.language == "Русский":
                CTkMessagebox(opacity = self.opacity, message='Отсутсвует файл авто-настройки OpenSSH!', title='Внимание', icon='warning')
            else:
                CTkMessagebox(opacity=self.opacity, message='There is no OpenSSH auto-configuration file!', title='Attention', icon='warning')

    # Создание config в $HOME\.ssh с заготовками (надо бы в отдельный файл потом в exe и вызывать в том же батнике в конце (возможно))
    def create_ssh_config(self):
        home_path = (os.path.expanduser('~'))
        home_path_ssh = home_path + r"\.ssh\config"
        with open(home_path_ssh, 'w') as the_file:
            the_file.write("# Config for use specific key for github\n")
            the_file.write("Host github.com\n")
            the_file.write("  HostName github.com\n")
            the_file.write("  User git\n")
            the_file.write("  IdentityFile ~/.ssh/id_ed25519_github\n")
            the_file.write("  IdentitiesOnly yes\n")
            the_file.write("\n")
            the_file.write("# For server 172.x.x.x\n")
            the_file.write("Host 172.x.x.x\n")
            the_file.write("  User user\n")
            the_file.write("  Port 2121\n")
            the_file.write("  IdentityFile ~/.ssh/id_ed25519\n")
            the_file.write("  IdentitiesOnly yes\n")
            the_file.write("\n")
            the_file.write("# For all other servers\n")
            the_file.write("Host *\n")
            the_file.write("    HostkeyAlgorithms +ssh-rsa\n")
            # the_file.write("    PubkeyAcceptedAlgorithms +ssh-rsa\n")

    # Снятие селекта с поля listbox при нажатии за границы поля
    def deselect_item(self, event):
        def right_click():  # ну да павторкааа ну и штоооооо (похуй+поебать+ссать сидя)
            self.after(150, lambda: self.focus_set())
            return
        if self.listbox.curselection() == self.previous_selected:
            try:
                self.listbox.deactivate(0)
                print("Заебок чилок")
            except:
                print("Подключитесь к базе уебки")
            self.listbox.configure(multiple_selection=False)
            self.bind("<Button-3>", lambda escape_entry: right_click())
            self.unbind("<Delete>")  # аналогичная подСТРАХовОЧКА для функции удаления
            self.unbind("<BackSpace>")
            self.unbind("<Down>")
            self.unbind("<Up>")
            self.unbind("<Left>")
            self.unbind("<Right>")
            self.unbind("<Return>")
            self.unbind("<F8>")
        self.previous_selected = self.listbox.curselection()

"""
if __name__ == "__main__":
    app = App()
    app.mainloop()
"""

if ctypes.windll.shell32.IsUserAnAdmin():
    if __name__ == "__main__":
        app = App()
        app.mainloop()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)