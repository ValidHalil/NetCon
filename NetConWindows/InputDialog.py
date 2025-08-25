import tkinter
import updated_ctk as ctk
import keyboard
import pyautogui
from typing import Union, Tuple, Optional
import re
import os


class InputDialog(ctk.CTkToplevel):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 title: str = "CTkDialog",
                 font: Optional[Union[tuple, ctk.CTkFont]] = None,
                 text: str = "CTkDialog",
                 name_db: str = "",
                 old_ip: str = "",
                 name_device: str = "",
                 name_model: str = "",
                 name_obj: str = "",
                 master = None,
                 opacity = 1,
                 language = "Русский",
                 mode: str = "add"):

        super().__init__(fg_color=fg_color)

        # Функция которая вбивает по символу (в охуительно понтовое поле entry с точками) IP редактируемой записи
        def entry_old_ip(ip):
            point_counter = 1 # счетчик для подсчета встреч точек, нужен для правильного вывода пробелов при наборе IP, так как без него третья точка может оказаться на позиции второй и ввод произойдет неправильный (скорее всего он будет нужен а прога посчитает что нет)
            for i in range(len(ip)):
                if ip[i] == "1":
                    self._entry.insert(i,"1")
                if ip[i] == "2":
                    self._entry.insert(i,"2")
                if ip[i] == "3":
                    self._entry.insert(i,"3")
                if ip[i] == "4":
                    self._entry.insert(i,"4")
                if ip[i] == "5":
                    self._entry.insert(i,"5")
                if ip[i] == "6":
                    self._entry.insert(i,"6")
                if ip[i] == "7":
                    self._entry.insert(i,"7")
                if ip[i] == "8":
                    self._entry.insert(i,"8")
                if ip[i] == "9":
                    self._entry.insert(i,"9")
                if ip[i] == "0":
                    self._entry.insert(i,"0")
                if ip[i] == "." and (i == 3 and point_counter == 1 or i == 7 and point_counter == 2 or i == 11 and point_counter == 3):
                    point_counter += 1
                elif ip[i] == ".":
                    point_counter += 1
                    self._entry.insert(i," ")
            return self.after(50, lambda: self._entry.focus())

        def entry_mask_check(text, valid, entry):
            ip = re.findall("^\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}$", text.get())
            if len(ip) != 1:
                text.set(valid[0])
            if ip:
                valid[0] = ip[0]
                cursor_position = entry.index("insert")
                index2 = ip[0][:cursor_position - 1].rfind(u".")
                if cursor_position - index2 == 4:
                    entry.icursor(cursor_position + 1)

        # Снятие фокуса с поля ввода после нажатия правой кнопки мыши на него
        def right_click():
            self.after(150, lambda: self.focus_set())
            return

        def left_click(entry):
            if entry.get() == "...":
                pyautogui.press("left", presses=5)
            return

        def combo_focus(combo):
            self.after(50, lambda: combo.focus())
            return

        def close_window():
            self.grab_release()
            self.destroy()

        def clear_entry_ip(entry):
            self.previous_selected = None
            entry.focus_set()
            pyautogui.press("end")
            pyautogui.press("backspace", presses=15)

        def clear_entry(entry):
            self.previous_selected = None
            try:
                entry.delete(0, "end")
            except:
                entry.set("")

        def clear_dot(combo):
            if combo.get() == "...":
                combo = combo.set("")

        self._fg_color = ctk.ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ctk.ThemeManager.theme["CTkButton"]["text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ctk.ThemeManager.theme["CTkEntry"]["border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ctk.ThemeManager.theme["CTkEntry"]["text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font
        self._name_db = name_db
        self.mode = mode
        self.language = language

        self.bind("<Button-3>", lambda escape_entry: right_click())
        self.title(title)
        self.geometry("320x420")
        self.attributes("-alpha", opacity)
        self.resizable(False,False)
        self.lift()  # lift window on top
        #self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.grab_set()  # make other windows not clickable
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 320
        window_height = 410
        xlen = int((screen_width - window_width) // 2)
        ylen = int((screen_height - window_height) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.bind('<Escape>', lambda close: close_window())
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")

        if self.mode == "add":
            self.iconbitmap(path_img + "img/add_row.ico")
        elif self.mode =="change":
            self.iconbitmap(path_img + "img/ch_row.ico")

        # В зависимости от базы выводится свой список устройств
        vendors_list = []
        if self._name_db == "Коммутаторы":
            vendors_list = ["Eltex MES", "Cisco", "Avaya", "Aruba", "TP-Link", "D-Link", "Zyxel", "Allied Telesis", "Nateks", "SNR", "Qtech", "Juniper", "MikroTik", "Huawei", "Nortel"]
            vendors_list = sorted(vendors_list)
            wi_var = 144
        elif self._name_db == "Маршрутизаторы":
            vendors_list = ["Eltex ESR", "Cisco","Avaya", "Aruba", "TP-Link", "D-Link", "Zyxel", "Allied Telesis", "Nateks", "SNR", "Qtech", "Juniper", "MikroTik", "Huawei", "Nortel"]
            vendors_list = sorted(vendors_list)
            wi_var = 144
        elif self._name_db == "Мультиплексоры":
            vendors_list = ["RAD", "Оптик", "RAD MP2100", "MC04", "Nortel OME", "MOXA", "Zelax", "Eltex ToPGATE", "CRONYX", "Juniper", "ПолиКом", "Ruijie Networks", "Cisco", "Adtran", "Huawei"]
            vendors_list = sorted(vendors_list)
            wi_var = 156
        elif self._name_db == "Телефоны":
            vendors_list = ["Cisco", "Yealink", "Eltex", "Avaya", "Polycom", "Panasonic", "Grandstream", "Snom", "Fanvil", "Jabra", "TP-Link", "D-Link", "Gigaset", "Unify", "Aastra"]
            vendors_list = sorted(vendors_list)
            wi_var = 151
        elif self._name_db == "Электропитание":
            vendors_list = ["APC", "Eaton", "CyberPower", "Vertiv", "Delta Electronics", "Powerware", "Socomec", "ABB", "Штиль", "SUA", "Топаз", "V&H", "Ippon", "Enatel", "Энергия"]
            vendors_list = sorted(vendors_list)
            wi_var = 155
        else:
            vendors_list = ["Неизвестно"]
            wi_var = 153

        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=25, padx=25, fill="both", expand=True)
        self.frame_1.grid_columnconfigure((0, 1), weight=1)
        self.frame_1.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self._label = ctk.CTkLabel(master=self.frame_1,
                               width=300,
                               wraplength=300,
                               fg_color="transparent",
                               text_color=self._text_color,
                               text="IP-адрес:",
                               font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"),)
        self._label.grid(row=0, column=0, columnspan=2, padx=25, pady=(15,5), sticky="ew")
        x= tkinter.StringVar()
        self._entry = ctk.CTkEntry(master=self.frame_1,
                               width=230,
                               fg_color=self._entry_fg_color,
                               border_color=self._entry_border_color,
                               text_color=self._entry_text_color,
                               font=self._font,
                               justify = "c",
                               textvariable=x)
        self._entry.grid(row=1, column=0, columnspan=2, padx=25, pady=(0, 0), sticky="ew")
        ip_entry_string_last_valid = [u"..."]
        x.trace("w", lambda *args: entry_mask_check(x, ip_entry_string_last_valid, self._entry))
        x.set("")
        if old_ip != "":
            entry_old_ip(old_ip)

        self._label2 = ctk.CTkLabel(master=self.frame_1,
                               width=300,
                               wraplength=300,
                               fg_color="transparent",
                               text_color=self._text_color,
                               text="Имя устройства:",
                               font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"),)
        self._label2.grid(row=2, column=0, columnspan=2, padx=25, pady=(10, 5), sticky="ew")
        self._entry2 = ctk.CTkEntry(master=self.frame_1,
                               width=230,
                               fg_color=self._entry_fg_color,
                               border_color=self._entry_border_color,
                               text_color=self._entry_text_color,
                               font=self._font,
                               justify = "c")
        self._entry2.grid(row=3, column=0, columnspan=2, padx=25, pady=(0, 0), sticky="ew")
        self._entry2.insert(0,name_device)

        self._label3 = ctk.CTkLabel(master=self.frame_1,
                                width=300,
                                wraplength=300,
                                fg_color="transparent",
                                text_color=self._text_color,
                                text="Модель устройства:",
                                font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), )
        self._label3.grid(row=4, column=0, columnspan=2, padx=25, pady=(10, 5), sticky="ew")
        self._combobox1 = ctk.CTkComboBox(master=self.frame_1,
                                values=vendors_list,
                                width=wi_var,
                                justify="c",
                                command= lambda combo_var: combo_focus(self._combobox1))
        self._combobox1.grid(row=5, column=0, columnspan=2, padx=25, pady=(0, 0), sticky="ew")
        self._combobox1.set(value=name_model)

        self._label4 = ctk.CTkLabel(master=self.frame_1,
                                width=300,
                                wraplength=300,
                                fg_color="transparent",
                                text_color=self._text_color,
                                text="Принадлежность объекту:",
                                font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"), )
        self._label4.grid(row=6, column=0, columnspan=2, padx=25, pady=(10, 5), sticky="ew")
        self._combobox2 = ctk.CTkComboBox(master=self.frame_1,
                                values = ["РС_ЦиП_РЗ_ПС_","РС_ЦиП_РЗ_РПБ_","РС_ЦиП_РЗ_"],
                                width=176,
                                justify="c",
                                command= lambda combo_var: combo_focus(self._combobox2))
        self._combobox2.grid(row=7, column=0, columnspan=2, padx=25, pady=(0, 0), sticky="ew")
        self._combobox2.set(value=name_obj)

        self._cancel_button = ctk.CTkButton(master=self.frame_1,
                                        width=100,
                                        border_width=0,
                                        fg_color="#de710b",
                                        hover_color="#ab590c",
                                        text_color=self._button_text_color,
                                        text='Отмена',
                                        font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"),
                                        command=self._cancel_event)
        self._cancel_button.grid(row=8, column=1, columnspan=1, padx=(15, 25), pady=(25, 25), sticky="e")
        self._ok_button = ctk.CTkButton(master=self.frame_1,
                                    width=100,
                                    border_width=0,
                                    fg_color="#1F538D",
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='ОК',
                                    font=ctk.CTkFont(family=("Trebuchet MS"), size=14, weight="bold"),
                                    command=self._ok_event)
        self._ok_button.grid(row=8, column=0, columnspan=1, padx=(25, 10), pady=(25, 25), sticky="w")

        self._entry.bind("<Return>", self._ok_event) #Здесь вывод в функцию и наружу, короче менять тут
        self._entry.bind("<Button-1>", lambda into_entry: left_click(self._entry))
        self._entry.bind("<Delete>", lambda del_var: clear_entry_ip(self._entry))
        self._entry2.bind("<Return>", self._ok_event)  # Здесь вывод в функцию и наружу, короче менять тут
        self._entry2.bind("<Delete>", lambda del_var: clear_entry(self._entry2))
        self._combobox1.bind("<Return>", self._ok_event)
        self._combobox1.bind("<Down>", lambda open_var: self._combobox1._clicked())
        self._combobox1.bind("<Delete>", lambda del_var: clear_entry(self._combobox1))
        clear_dot(self._combobox1)
        self._combobox2.bind("<Return>", self._ok_event)
        self._combobox2.bind("<Down>", lambda open_var: self._combobox2._clicked())
        self._combobox2.bind("<Delete>", lambda del_var: clear_entry(self._combobox2))
        clear_dot(self._combobox2)
        self.after(100, lambda: self._entry.focus_set())
        self.master_window = master
        self.update_position()
        self.bind("<Configure>", self.update_position)

        if self.language != "Русский":
            self._label.configure(text="IP address:")
            self._label2.configure(text="Device name:")
            self._label3.configure(text="Device model:")
            self._label4.configure(text="Belonging to the object:")
            self._cancel_button.configure(text="Cancel")

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

    def _ok_event(self, event=None):
        if  self._entry.get() == "..." or self._entry2.get() == "": # Проверка на заполнение первых двух полей
            self._user_input = "ErrorMessage"
            self.grab_release()
            self.destroy()
            return
        else:
            ip_var = self._entry.get()
            list_ip = ip_var.split(".")
            for i in range(len(list_ip)):  # Проверка на верность формата IP
                if str(list_ip[i]) == "":
                    self._user_input = "ErrorMessage2"
                    self.grab_release()
                    self.destroy()
                    return
                elif int(list_ip[i]) > 255:
                    self._user_input = "ErrorMessage2"
                    self.grab_release()
                    self.destroy()
                    return
            x1 = self._entry.get()
            x2 = self._entry2.get()
            if self._combobox1.get() == "":
                x3 = "..."
            else:
                x3 = self._combobox1.get()
            if self._combobox2.get() == "":
                x4 = "..."
            else:
                x4 = self._combobox2.get()
            self._user_input = x1 + " " + x2 + " │ " +  x3 + " │ " + x4 # СмеклОЧКА в действии
            self.grab_release()
            self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input
