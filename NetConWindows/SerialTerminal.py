import re
import updated_ctk as ctk
import serial
import serial.tools.list_ports
import threading
import pyautogui
import os
from PIL import Image
from NetConWindows import Help, CTkMessagebox
import ctypes
import NetConWindows
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScreenCurrent():
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_display_scaling():
        try:
            if sys.platform == "win32":
                if ctypes.windll.shcore.SetProcessDpiAwareness(2) != 0:
                    pass
                else:
                    ctypes.windll.user32.SetProcessDPIAware()
            hwnd = 0
            hdc = ctypes.windll.user32.GetDC(hwnd)
            dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            ctypes.windll.user32.ReleaseDC(hwnd, hdc)
            scaling = dpi_x / 96.0
            return scaling
        except Exception as e:
            print(f"Error getting display scaling: {e}")
            return 1.0

class LimitedList(list):

    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def append(self, item):
        super().append(item)
        while len(self) > self.max_size:
            self.pop(0)

class SerialTerminal(ctk.CTkToplevel):

    def __call__(self, theme, opacity, language):
        super().__init__()
        self.old_height = 0
        self.entry_text = None
        self.language = language
        self.line = ""
        self.old_name = ""
        self.new_height = 0
        self.old_input = ""
        self.flag = 1
        self.old_line = "8425902375"
        self.special_string = ""
        self.many_input = ""
        self.current_input = ""
        self.current_name = ""
        self.bar_height = 0
        self.scaling_factor = 0
        self.next_after_conf = False
        self.theme = theme
        self.last_command_list = LimitedList(10)
        self.title("SerialTerminal")
        self.geometry("1100x580")
        self.opacity = opacity
        self.attributes("-alpha", self.opacity)
        self.lift()
        #self.resizable(False, False)
        #self.attributes("-topmost", True)
        #self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1100
        window_height = 580
        self.scaling_factor = ScreenCurrent.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.minsize(850, 250)
        self.serial_port = None
        self.search_window = None
        self.counter = 0
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.stop_event = threading.Event()
        self.after(150, lambda : self.create_widgets())
        #ctk.set_widget_scaling(1)

    def create_widgets(self):

        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")
        self.configure(fg_color=("#ffffff","#1a1a1a"))
        self.iconbitmap(path_img + "img/serial_title.ico")
        self.search_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/search_term.png"), size=(18, 18))
        self.cleartext_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/cleartext.png"), size=(18, 18))
        self.disconnect_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial_dis1.png"), size=(20, 20))
        self.disconnect_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial_dis2.png"), size=(20, 20))
        self.connect_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial1.png"), size=(20, 20))
        self.connect_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial2.png"), size=(20, 20))
        self.help_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help.png"), size=(37, 18))
        self.help_eng_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help_eng.png"), size=(37, 15))
        port_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/port.png"), size=(30, 28))
        port_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/port_light.png"), size=(30, 28))
        speed_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/speed.png"), size=(30, 28))
        speed_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/speed_light.png"), size=(30, 28))

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan = 2)
        self.settings_frame.grid_columnconfigure((4), weight=1)
        self.settings_frame.grid_rowconfigure((0), weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.bind("<F6>", lambda discon: self.disconnect_serial())
        self.bind("<Control-Delete>", lambda delete_text: self.clear_text())
        self.bind("<F9>", lambda open_help: self._show_help())
        self.bind("<F8>", lambda open_settings: self.toggle_settings_frame())

        if self.language == "Русский":
            speed = "Скорость:"
            port = "Порт:"
        else:
            speed = "Baudrate:"
            port = "Port:"

        self.portlabel = ctk.CTkLabel(self.settings_frame, text=port, font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.portlabel.grid(row=0, column=0, padx=(57,10), pady=(25,5), sticky="nsew")
        if self.theme == "Темная" or self.theme == "Dark":
            self.portlabel_img = ctk.CTkLabel(self.settings_frame, image=port_img, text="")
        else:
            self.portlabel_img = ctk.CTkLabel(self.settings_frame, image=port_light_img, text="")
        self.portlabel_img.grid(row=0, column=0, padx=(25, 0), pady=(25, 5), sticky="w")
        self.port_combobox = ctk.CTkComboBox(self.settings_frame, values=self.get_available_ports(), font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), width=130, state="readonly")
        self.port_combobox.grid(row=0, column=1, padx=(0,0), pady=(25,5), sticky="nsew")
        self.port_combobox.set(self.get_available_ports()[0])
        self.port_combobox.bind("<Return>", lambda con: self.connect_serial(flag=2))
        self.port_combobox.bind("<Down>", lambda open_var: self.auto_refresh_ports())#, self.refresh_ports()])
        self.port_combobox._canvas.bind("<Enter>", lambda ada: self.refresh_ports())

        self.baud = ctk.CTkLabel(self.settings_frame, text=speed, font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.baud.grid(row=0, column=2, padx=(57,10), pady=(25,5), sticky="nsew")
        if self.theme == "Темная" or self.theme == "Dark":
            self.baud_img = ctk.CTkLabel(self.settings_frame, image=speed_img, text="")
        else:
            self.baud_img = ctk.CTkLabel(self.settings_frame, image=speed_light_img, text="")
        self.baud_img.grid(row=0, column=2, padx=(25, 0), pady=(25, 5), sticky="w")
        self.baudrate_combobox = ctk.CTkComboBox(self.settings_frame, values=["9600", "19200", "38400", "57600", "115200"], font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), width=130, state="readonly")
        self.baudrate_combobox.grid(row=0, column=3, padx=(0,10), pady=(25,5), sticky="nsew")
        self.baudrate_combobox.bind("<Return>", lambda con: self.connect_serial(flag=2))
        self.baudrate_combobox.bind("<Down>", lambda open_var: self.baudrate_combobox._clicked())
        self.baudrate_combobox.set("9600")

        self.connect_button = ctk.CTkButton(self.settings_frame, width=50, text="", fg_color="#1F538D", command=self.connect_serial, image=self.connect_img, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.connect_button.grid(row=0, column=5, padx=(0,0), pady=(25,5), sticky = "nse")
        self.disconnect_button = ctk.CTkButton(self.settings_frame, width=50, state="disabled", fg_color="#ab590c", border_width=0, hover_color="#ab590c", image=self.disconnect_disabled_img, text="", command=self.disconnect_serial)
        self.disconnect_button.grid(row=0, column=6, padx=(10,0), pady=(25,5), sticky = "nsew")
        self.help_btn = ctk.CTkButton(master=self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), text_color="gray32", hover_color=("white", "#333333"), border_width=0, image=self.help_img, text="", font=ctk.CTkFont(size=11, weight="bold"), command=self._show_help)
        self.help_btn.grid(row=0, column=7, padx=(10, 0), pady=(25, 5), sticky="nsew")
        self.search_btn = ctk.CTkButton(self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.search_img, height=18, border_width=0, text="", command=self.open_search_window)
        self.search_btn.grid(row=0, column=8, padx=(10, 0), pady=(25, 5), sticky="nsew")
        self.clearbut = ctk.CTkButton(self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.cleartext_img, height=18, border_width=0, text="", command=self.clear_text)
        self.clearbut.grid(row=0, column=9, padx=(10,25), pady=(25,5), sticky = "nsew")
        self.after(20, lambda : self.focus_set())

        self.settings_toggle_button = ctk.CTkButton(self, text="▲", width=20, height=20, command=self.toggle_settings_frame, corner_radius=0, fg_color=("#e5e5e5","#212121"), text_color=("#212121","#d6d6d6"), hover_color=("#d5d5d5","#313131"), font=("Consolas", 13, "bold"))
        self.settings_toggle_button.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.settings_frame_hidden = False

        self.text_area = ctk.CTkTextbox(self, font=("Consolas", 14), corner_radius=0, state = "disabled", bg_color=("#ffffff","#1a1a1a"), fg_color=("#ffffff","#1a1a1a"), wrap="word", height=0) #text_color="#05f71d"
        self.text_area.grid(row=2, column=0, rowspan=1, sticky="nsew", columnspan = 2, padx=(3,0))
        self.text_area._border_spacing=0

        self.input_label = ctk.CTkLabel(self, fg_color=("#ffffff","#1a1a1a"), width=20, bg_color=("#ffffff","#1a1a1a"), text=" >", font=("Consolas", 18, "bold"), height=0)
        self.input_label.grid(row=3, column=0, rowspan=1, sticky="ew", padx=0)
        self.input_entry = ctk.CTkEntry(self, state="normal", placeholder_text="...", font=("Consolas", 14), corner_radius=0, border_width=0, fg_color=("#ffffff","#1a1a1a"), bg_color=("#ffffff","#1a1a1a"), height=0)
        self.input_entry.grid(row=3, column=1, rowspan=1, sticky="ew", padx = (0,0))
        if self.language == "Русский":
            self.input_entry.insert(0,"Ожидание подключения...")
            self.help_btn.configure(image=self.help_img)
        else:
            self.input_entry.insert(0, "Waiting for connection...")
            self.help_btn.configure(image=self.help_eng_img)
        self.input_entry.configure(state="disabled")
        self.input_entry.bind('<Return>', lambda x: self.send_command())
        self.input_entry.bind('<Down>', lambda prev: self.previous_command())
        self.input_entry.bind('<Up>', lambda prev: self.next_command())
        self.input_entry.bind('<Escape>', lambda clear: self.clear_entry())
        self.bind("<Escape>", lambda x: self._on_closing())
        self.bind("<KeyRelease>", self.what_button)
        self.base_width = 1100 * self.scaling_factor
        self.base_height = 580 * self.scaling_factor
        self.bind("<Configure>", lambda x: self.on_configure())
        self.adjust_textbox_height()

    def on_configure(self):
        if self.base_width != self.winfo_width() or self.base_height != self.winfo_height():
            #print(f"W Do: {self.base_width}, Posle: {self.winfo_width()}")
            #print(f"H Do: {self.base_height}, Posle: {self.winfo_height()}")
            self.adjust_textbox_height()
            self.text_area.see("end")
            self.base_width = self.winfo_width()
            self.base_height = self.winfo_height()

    def what_button(self, event):
        #print(event.keycode)
        ctrl = (event.state & 0x4) != 0
        if event.keycode == 70 and ctrl :
            self.open_search_window()

    def open_search_window(self):
        if self.search_window is None or not self.search_window.winfo_exists():
            self.search_window = NetConWindows.SearchWindow(self, self.text_area, self.opacity, self.language)
        self.search_window.focus()

    def adjust_textbox_height(self):
        text_lines = self.text_area.get("1.0", "end").splitlines()
        content_height = len(text_lines) * 17
        max_height = self.winfo_height()//self.scaling_factor - self.bar_height
        new_height = min(content_height, max_height)
        self.new_height = new_height
        new_rows = round(self.new_height/17)
        if self.new_height != max_height or self.winfo_height() != self.old_height:
            self.text_area.configure(height=self.new_height)
            self.update_idletasks()
            self.input_label.grid_forget()
            self.input_label.grid(row= new_rows + 1, column=0, padx=0, pady=(0, 0), sticky="ew") # изменяем row
            self.input_entry.grid_forget()
            self.input_entry.grid(row= new_rows + 1, column=1, padx=0, pady=(0, 0), sticky="ew") # изменяем row
            self.old_height = self.winfo_height()

    def _on_closing(self):
        if self.language == "Русский":
            msg = CTkMessagebox(opacity = self.opacity, message='Завершить сессию?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да")
        else:
            msg = CTkMessagebox(opacity=self.opacity, message='End session?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes")
        msg.button_1.configure(fg_color="#de710b", hover_color="#ab590c")
        msg.focus_set()
        response = msg.get()
        if response == "Отмена" or response == "Cancel":
            return
        if response == "Да" or response == "Yes":
            self.disconnect_serial()
            self.destroy()

    def toggle_settings_frame(self):
        #size = self.text_area.get("1.0", "end").count("\n")
        if self.settings_frame_hidden:
            self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            self.settings_toggle_button.configure(text="▲")
            self.settings_frame_hidden = False
            self.bar_height=108
            self.adjust_textbox_height()
            self.text_area.configure(height=self.new_height)
            self.update_idletasks()
            self.after(100, lambda: self.text_area.see("end"))
        else:
            self.settings_frame.grid_forget()
            self.settings_toggle_button.configure(text="▼")
            self.settings_frame_hidden = True
            #self.after(100, lambda: self.text_area.yview_scroll(-1, "units"))
            self.bar_height = 50
            self.adjust_textbox_height()
            self.text_area.configure(height=self.new_height)
            self.update_idletasks()
            #self.after(200, lambda: self.text_area.see(f"{size - 1}.0"))

    def _show_help(self):
        help_tab = Help()
        help_tab("Терминал", self, self.opacity, self.language)

    def auto_refresh_ports(self):
        self.refresh_ports()
        self.port_combobox._clicked()

    def clear_entry(self):
        self.input_entry.delete(0, "end")
        self.counter = len(self.last_command_list)

    def previous_command(self):
        self.counter +=1
        if self.counter > len(self.last_command_list)-1:
            self.counter = 0
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, self.last_command_list[self.counter])
        return self.counter

    def next_command(self):
        self.counter -=1
        if self.counter < 0:
            self.counter = len(self.last_command_list) - 1
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, self.last_command_list[self.counter])
        return self.counter

    def get_available_ports(self):
        try:
            ports = [port.device for port in serial.tools.list_ports.comports()]
            if not ports:
                if self.language == "Русский":
                    ports = ["Не найдено!"]
                else:
                    ports = ["Not found!"]
                return ports
            else:
                return ports
        except:
            ports = [""]
            if self.language == "Русский":
                return ports, CTkMessagebox(opacity = self.opacity, message='COM-порты отсутствуют!', title='Ошибка', icon='cancel')
            else:
                return ports, CTkMessagebox(opacity=self.opacity, message='COM ports are missing!', title='Error', icon='cancel')

    def refresh_ports(self):
        self.port_combobox.configure(values=self.get_available_ports())

    def connect_serial(self, flag=1):
        port = self.port_combobox.get()
        baudrate = int(self.baudrate_combobox.get())
        self.clear_text()
        try:
            self.serial_port = serial.Serial(port, baudrate)
            self.text_area.configure(state = "normal")
            self.text_area.insert("end", f"\n Connected to {port} at {baudrate}")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")
            self.input_entry.configure(state="normal")
            self.clear_entry()
            self.old_name = ""
            self.port_combobox.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
            self.baudrate_combobox.configure(state="disabled", border_color=("#8f8f8f", "#444444"), button_color=("#8f8f8f", "#444444"))
            self.connect_button.configure(state="disabled", image=self.connect_disabled_img, fg_color="#14375e")
            self.disconnect_button.configure(state="normal", fg_color="#de710b", image=self.disconnect_img)
            self.start_reading()
            self.stop_text_area_read_input()
            if flag == 1:
                self.send_command()
            self.send_command()
            self.text_area.see("end")
            self.after(200, lambda: self.back_text_area_read_input())
        except serial.SerialException as e:
            self.disconnect_serial()
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"\n Error connecting to port {port}: {e}")
            self.text_area.see("end")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")
            self.input_entry.configure(state="disabled")

    def disconnect_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.unbind("<Tab>")
            self.clear_entry()
            self.bind("<Escape>", lambda x: self._on_closing())
            self.after(150, lambda: self.input_label.configure(text=" >", font=("Consolas", 18, "bold")))
            self.after(100, lambda: self.input_entry.unbind("<?>"))
            self.after(100, lambda: self.input_entry.unbind("<Tab>"))
            self.stop_event.set()  # Stop reading thread
            self.serial_port.close()
            self.text_area.configure(state="normal")
            self.text_area.insert("end", "\n Disconnected from serial port.")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")
            self.port_combobox.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
            self.baudrate_combobox.configure(state="readonly", border_color=("#979da2", "#565b5e"), button_color=("#979da2", "#565b5e"))
            self.connect_button.configure(state="normal", image=self.connect_img, fg_color="#1F538D")
            self.disconnect_button.configure(state="disabled", fg_color="#ab590c", image=self.disconnect_disabled_img)
            if self.language == "Русский":
                self.after(160, lambda: [self.focus_set(),self.input_entry.insert(0, "Ожидание подключения..."), self.input_entry.configure(state="disabled")])
            else:
                self.after(160, lambda: [self.focus_set(), self.input_entry.insert(0, "Waiting for connection..."), self.input_entry.configure(state="disabled")])
            self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            self.settings_toggle_button.configure(text="▲")
            self.settings_frame_hidden = False
            self.bar_height = 108
            self.adjust_textbox_height()
            self.text_area.configure(height=self.new_height)
            self.old_name=""
            self.update_idletasks()
            self.after(200, lambda: self.text_area.see("end"))

    def reload_alert(self):
        def key(event):
            if event.keycode == 89:
                self.serial_port.write("y".encode())
                self.serial_port.write("y".encode())
                self.serial_port.write("\r".encode())
                self.input_entry.configure(state="normal")
                self.input_entry.delete(0, "end")
                self.after(140, lambda: self.input_entry.delete(0, "end"))
                self.after(150, lambda : self.input_entry.unbind("<KeyPress>"))
            elif event.keycode == 78:
                self.serial_port.write("n".encode())
                self.serial_port.write("\r".encode())
                self.input_entry.configure(state="normal")
                self.after(140, lambda: self.input_entry.delete(0,"end"))
                self.after(150, lambda : self.input_entry.unbind("<KeyPress>"))
            else:
                self.input_entry.delete(0, "end")
                self.after(140, lambda: self.input_entry.delete(0, "end"))
                self.after(150, lambda : self.input_entry.unbind("<KeyPress>"))
        x = self.text_area.get("1.0", "end").count("\n")
        y = self.text_area.get(f"{x-4}.0", "end")
        if "%" in y:
            self.serial_port.write("\r".encode())
        else:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", "\n\n ┌───────────────────────────┐\n │ Are you sure?[Y/N/RETURN] │\n └───────────────────────────┘ \n")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")
            #size = self.text_area.get("1.0", "end").count("\n")
            self.text_area.see("end")
            self.input_entry.bind('<KeyPress>', key)

    def hide_write(self):
        self.stop_text_area_read_input()
        self.serial_port.write(self.nullstring.encode())
        self.after(100, lambda: self.back_text_area_read_input())

    def update_command_list(self, command):
        if command != "\r" and command.replace("\r", "") not in self.last_command_list:
            self.last_command_list.append(command.replace("\r", "").rstrip())
        if command.replace("\r", "") in self.last_command_list:
            old_index = self.last_command_list.index(command.replace("\r", ""))
            move_element = self.last_command_list.pop(old_index)
            self.last_command_list.append(move_element)

    def send_command(self): #для элтексов вроде заебца
        self.many_input = ""
        command = self.input_entry.get() + "\r"
        if "\n" in command:
            i_n = command.count('\n')
            self.after(20, lambda: self.focus_set())
            self.after(120*i_n, lambda: self.input_entry.focus_set())
        self.current_input = self.input_entry.get().lstrip().rstrip()
        self.nullstring = "\r"
        if self.serial_port and self.serial_port.is_open:
            try:
                if ("reset " in command.lower() or "delete " in command.lower() or "boot " in command.lower() or "erase " in command.lower() or "write " in command.lower() or "reload" in command.lower() or "copy " in command.lower() or "default " in command.lower()) and "show" not in command.lower(): #Возможно будет дополняться
                    #if "default " not in command.lower():
                    self.clear_text()
                    self.serial_port.write(command.encode())
                    self.after(150, lambda: self.reload_alert())
                    self.update_command_list(command)
                else:
                    self.serial_port.write(command.encode())
                    if command.strip() != "" and "login" not in self.line.lower() and ("#" in self.line or ">" in self.line): #последнее условие пока не точно
                        #self.serial_port.write(self.nullstring.encode())
                        self.update_command_list(command)
                        self.serial_port.write(self.nullstring.encode())
                self.input_entry.delete(0, "end")
                #if self.old_name == "Password:":
                    #self.old_name = ""
                    #pyautogui.press("Enter")
            except serial.SerialException as e:
                self.disconnect_serial()
                self.input_entry.configure(state="normal")
                self.after(30, lambda: self.input_entry.focus_set())
                self.text_area.configure(state="normal")
                self.text_area.insert("end", f"\n Error sending command: {e}")
                self.adjust_textbox_height()
                self.text_area.see("end")
                self.text_area.configure(state="disabled")
        self.counter = len(self.last_command_list)

    def send_command2(self,command,var = None, tab_flag=False):
        #self.after(300, lambda : [self.unbind('<space>'), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        self.current_input = self.input_entry.get().lstrip().rstrip()
        if var is not None:
            self.old_input = self.input_entry.get()
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(command.encode())
                self.input_entry.configure(state="normal")
                if tab_flag:
                    print("")
                else:
                    self.input_entry.delete(0, "end")
                self.input_entry.configure(state="readonly")
            except serial.SerialException as e:
                self.disconnect_serial()
                self.input_entry.configure(state="normal")
                self.after(30, lambda: self.input_entry.focus_set())
                self.text_area.configure(state="normal")
                self.text_area.insert("end", f"\n Error sending command: {e}")
                self.adjust_textbox_height()
                self.text_area.see("end")
                self.text_area.configure(state="disabled")

    def del_fuck_after_tab(self):  # пока спорно, на циске работает
        result = []
        input = self.old_input
        words = input.split()
        # print(self.special_string)
        y = self.special_string.replace("_", "")
        if "Syntax error:" in y:
            y = y.replace("Syntax error:","%")
        index = y.find("%")
        y = y[:index]
        lines = y.split()
        #print(lines)
        if "#" in self.old_name:
            for word in words:
                for i in range(0, len(lines)):
                    if word.lower() in lines[i].lower():
                        index = lines[i].find("#")
                        x = lines[i][index + 1:]
                        result.append(x)
            result = self.remove_duplicate_words_ordered_loop(result)
            # print(result)
            for word in words:
                for i in range(0, len(result) - 1):
                    if word in result[i] and word != result[i]:
                        result[i] = ""
            if len(result) == 1:
                index = result[0].find("#")
                result[0] = result[0][index + 1:]
            result = list(filter(lambda word: word not in [""], result))
        elif ">" in self.old_name:
            for word in words:
                for i in range(0, len(lines)):
                    if word.lower() in lines[i].lower():
                        index = lines[i].find(">")
                        x = lines[i][index + 1:]
                        result.append(x)
            result = self.remove_duplicate_words_ordered_loop(result)
            # print(result)
            for word in words:
                for i in range(0, len(result) - 1):
                    if word in result[i] and word != result[i]:
                        result[i] = ""
            if len(result) == 1:
                index = result[0].find(">")
                result[0] = result[0][index + 1:]
            result = list(filter(lambda word: word not in [""], result))
        #print(result)
        final = ""
        for i in range(0, len(result)):
            final += result[i] + " "
        continue_input = {"-","/",":"}
        if len(final.rstrip()) > len(self.old_input.rstrip()):
            final_out = (final.replace(f"{words[len(words)-1]} ","").replace("z1x1c", ""))
            added_word = final_out.lower().replace(self.old_input.lower(),"")
            if final[len(final.rstrip())-1] not in continue_input:
                self.input_entry.insert("end", added_word.replace("z1x1c", ""))
            else:
                self.input_entry.insert("end", added_word.rstrip().replace("z1x1c", ""))
        """
        else:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"\n % Command not found!")
            self.adjust_textbox_height()
            self.text_area.see("end")
            self.text_area.configure(state="disabled")
        """
        self.back_text_area_read_input()
        self.special_string = ""

    def remove_duplicate_words_ordered_loop(self, word_list):
        result = []
        seen = set()  # Множество для хранения уже встреченных слов
        for word in word_list:
            if word not in seen:
                result.append(word)
                seen.add(word)
        return result

    def stop_text_area_read_input(self):
        self.flag = 2

    def back_text_area_read_input(self):
        self.flag = 1

    def find_device_name(self, var_line):
        if "#" in var_line and "more" not in self.line.lower() and 40 > len(var_line) > 1:
            s = var_line
            index = s.find("#")
            if index == len(s)-1:
                s = "  " + s[:index + 1]
                s = s.replace("z1x1c", "")
                self.current_name = s.strip()
                if self.old_name !=s:
                    self.input_label.configure(text=s, font=("Consolas", 14))
                    x = self.text_area.get("1.0", "end").count("\n")
                    if ">" in self.text_area.get(f"{x}.0", "end") or "#" in self.text_area.get(f"{x}.0", "end"):
                        self.text_area.configure(state="normal")
                        self.text_area.delete(f"{x}.0", "end")
                        self.text_area.configure(state="disabled")
                        self.adjust_textbox_height()
                        self.text_area.see("end")
                self.old_name = s
        elif ">" in var_line and "more" not in self.line.lower() and 40 > len(var_line) > 1:
            s = var_line
            index = s.find(">")
            if index == len(s) - 1:
                s = "  " + s[:index + 1]
                s = s.replace("z1x1c", "")
                self.current_name = s.strip()
                if self.old_name != s:
                    self.input_label.configure(text=s, font=("Consolas", 14))
                    x = self.text_area.get("1.0", "end").count("\n")
                    if ">" in self.text_area.get(f"{x}.0", "end") or "#" in self.text_area.get(f"{x}.0", "end"):
                        self.text_area.configure(state="normal")
                        self.text_area.delete(f"{x}.0", "end")
                        self.text_area.configure(state="disabled")
                        self.adjust_textbox_height()
                        self.text_area.see("end")
                self.old_name = s

    def start_reading(self):
        self.stop_event.clear()
        self.input_entry.bind('<?>', lambda x: self.send_command2(f"{self.input_entry.get()}?\r")) #при выводе справки при нажатии на "?"
        self.input_entry.bind('<Tab>', lambda x: [self.stop_text_area_read_input(),self.send_command2(self.input_entry.get() + "\t","old", tab_flag=True), self.send_command2("_ _\r", tab_flag=True), self.send_command2("\r", tab_flag=True), self.after(300, lambda: self.del_fuck_after_tab())])
        threading.Thread(target=self.read_from_port, daemon=True).start()
        self.after(100, lambda: self.input_entry.focus_set())
        self.unbind("<Escape>")
        self.settings_frame.grid_forget()
        self.settings_toggle_button.configure(text="▼")
        self.settings_frame_hidden = True
        self.bar_height = 50
        self.adjust_textbox_height()

    def remove_ansi_escape(self,data):
        # 0. Удаляем Control Sequence Introducer CSI codes
        data = re.sub(b'\x1b\[D', b'\n\n', data)

        data = re.sub(b'\x1b\[74D\x1b\[2K', b'z1x1c', data)
        data = re.sub(b'\x1b\[[0-9;]*m', b'', data)  # Цвета, стили
        data = re.sub(b'\x1b\[[0-9;]*H', b'', data)  # Перемещение курсора
        data = re.sub(b'\x1b\[[0-9;]*J', b'', data)  # Очистка экрана
        data = re.sub(b'\x1b\[[0-9;]*K', b'', data)  # Очистка строки
        data = re.sub(b'\x1b\[\?25[hl]', b'', data)  # Скрыть/показать курсор

        # 1. Cursor control:  Более общие, чем в примере, но полезные
        data = re.sub(b'\x1b\[\d*A', b'', data)  # Cursor Up
        data = re.sub(b'\x1b\[\d*B', b'', data)  # Cursor Down
        data = re.sub(b'\x1b\[\d*C', b'', data)  # Cursor Forward
        data = re.sub(b'\x1b\[\d*D', b'', data)  # Cursor Backward
        data = re.sub(b'\x1b\[\d*E', b'', data)  # Cursor Next Line
        data = re.sub(b'\x1b\[\d*F', b'', data)  # Cursor Previous Line
        data = re.sub(b'\x1b\[\d*G', b'', data)  # Cursor Horizontal Absolute
        data = re.sub(b'\x1b\[\d*\d*H', b'', data)  # Cursor Position (CUP)
        data = re.sub(b'\x1b\[\d*\d*f', b'', data)  # Horizontal & Vertical Position

        # 2. Specific escape-последовательности, упомянутые в примере.  Делаем их более общими, если нужно.
        data = re.sub(b'\x1b\[\d*D', b'', data)  # Cursor Backward (CB) -  уже есть выше, но можно сделать специфичнее, если нужно
        data = re.sub(b'\x1b\[\d*C', b'', data)  # Cursor Forward (CF) -  уже есть выше
        data = re.sub(b'\x1b\[\d*J', b'', data)  # Erase in Display (ED) -  уже есть выше

        # 3. Другие распространенные escape-последовательности
        data = re.sub(b'\x1b\[0m', b'', data)  # Reset all attributes
        data = re.sub(b'\x1b\[[1-9]m', b'', data)  # Удаление атрибутов текста (bold, underline, etc)

        # 4. Прочие символы
        data = re.sub(b'\x08\s*\x08', b'z1x1c', data)
        data = re.sub(b'\x08', b'', data)  # Backspace
        data = re.sub(b'\x07', b'', data)

        if len(data.decode("utf-8", errors="replace")) < 500:
            data = re.sub(b'\r\s*\r', b'z1x1c', data)  # Carriage return
        else:
            data = re.sub(b'\r\s*\r', b'\n\n', data)

        # 5. Удаляем последовательность (ESC CR пробелы CR) которая в каждой строке
        data = re.sub(b'\x1b\r\s+\r', b'', data)
        # 6. Удаляем лишние CR LF
        data = re.sub(b'(\r\n)+', b'\r\n', data)
        # 7.  Удаляем одиночные CR
        data = re.sub(b'\r', b'', data)
        # 8. Удаляем Control Sequence Introducer CSI codes - самое важное
        data = re.sub(b'\x1b\[K', b'', data)
        data = re.sub(b'\x1b', b'', data)

        # 9. Удаляем последовательности пробелов, за которыми следуют backspace
        data = re.sub(b' +(\x08+)', b'', data)  # Удаляет пробелы с backspace
        # 10. Удаляем лишние CUU (курсор вверх)
        data = re.sub(b"\x1b\[<n>A", b"", data)
        # 11. Удаляем лишние CUD (курсор вниз)
        data = re.sub(b"\x1b\[<n>B", b"", data)
        # 12. Удаляем лишние CUB (курсор назад)
        data = re.sub(b"\x1b\[<n>D", b"", data)
        # 13. Удаляем лишние CUF (курсор вперед)
        data = re.sub(b"\x1b\[<n>C", b"", data)

        data = re.sub(b'(\n\n)+', b'\n', data)

        data = re.sub(b'(\ns*\n)+', b'\n', data)
        # 11. Удаляем пробелы в начале строки с помощью регулярного выражения
        # data = re.sub(b'^\s+', b'', data)
        data = data.decode("utf-8", errors="replace")
        return data


    def del_dublicate_after_quit(self): #пока спорно UPD: больше ничо не удаляет, только вставляет пустую строку
        x = self.text_area.get("1.0", "end").count("\n")
        self.text_area.configure(state="normal")
        self.text_area.insert(f"{x}.0", "\n")
        self.adjust_textbox_height()
        self.text_area.configure(state="disabled")

    def on_tab_pressed(self, event):
        return "break"

    def check_previous_element_in_next(self,array):
        result = []
        previous_element = None
        for current_element in array:
            if previous_element is None:
                result.append(False)  # For the first element
            else:
                if current_element == "":
                    continue
                is_contained = str(previous_element) in str(current_element)
                if is_contained:
                    return True
            previous_element = current_element


    def read_from_port(self):
        def key_q(event):
            if event.keycode == 81:  # Клавиша с буквой C и с англ. буквой C
                self.stop_text_area_read_input()
                self.after(10, lambda: [self.send_command2("q" + "\r"), self.send_command2("" + "\r"), self.send_command2("" + "\r")])
                #self.after(250, lambda: self.del_dublicate_after_quit())
                self.after(300, lambda: [self.back_text_area_read_input(), self.unbind('<space>'), self.send_command2("" + "\r"), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        def key_control_c(event):
            if event.keycode == 67:  # Клавиша с буквой C и с англ. буквой C
                self.stop_text_area_read_input()
                self.after(10, lambda: [self.send_command2("q" + "\r"), self.send_command2("" + "\r"), self.send_command2("" + "\r")])
                #self.after(250, lambda:  self.del_dublicate_after_quit())
                self.after(300, lambda: [self.back_text_area_read_input(), self.unbind('<space>'), self.send_command2("" + "\r"), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        while self.serial_port and self.serial_port.is_open and not self.stop_event.is_set():
            try:
                if self.serial_port.in_waiting:
                    self.bind("<Tab>", self.on_tab_pressed)
                    line = self.serial_port.readline()
                    line = self.remove_ansi_escape(line)
                    self.line = line.replace("z1x1c","")
                    if "    " in line and "#" in line: #for mes2424p (end of run config)
                        line = line.lstrip()
                    if "More" in line:  # Other
                        self.after(100, lambda: self.input_entry.configure(state="readonly"))  # пока подумать
                        if self.flag == 1:
                            self.text_area.configure(state="normal")
                            line = self.remove_more_and_surrounding(line)
                            line = line.replace("z1x1c","")
                            self.text_area.insert("end", f"\n {line.replace("\n","")}")
                            self.adjust_textbox_height()
                            self.text_area.configure(state="disabled")
                        self.after(100, lambda: [self.bind('<space>', lambda x: [self.send_command2(" " + "\r")]), self.bind('<KeyPress>', key_q), self.bind('<Control-KeyPress>', key_control_c)])
                    else:
                        self.unbind('<space>')
                        self.unbind('<KeyPress>')
                        self.unbind('<Control-KeyPress>')
                        self.input_entry.configure(state="normal")
                        if self.flag == 1:
                            self.text_area.configure(state="normal")
                            line = line.replace("z1x1c", "")

                            line_index = line.find("#")
                            line_without_name = line[line_index+1:].replace("\n","").rstrip().lstrip()
                            drobl_line=line_without_name.split(" ")
                            esr_input_trigger = self.check_previous_element_in_next(drobl_line)
                            #rint(drobl_line, " | ", esr_input_trigger)

                            if line.replace("\n", "").rstrip().lstrip() not in self.old_line.replace("\n", "").rstrip().lstrip() and self.current_input in line and self.current_input != "" and "login" not in self.line.lower() and "%" not in line and "^" not in line  and "syntax error" not in self.line.lower() or ("\n" in self.current_input and esr_input_trigger):
                                if "\n" not in self.current_input:
                                    self.text_area.insert("end", f"\n {self.current_name + self.current_input}")
                                else:
                                    if f"\n {self.current_name + self.current_input.replace("\n",f"\n {self.current_name}")}" != self.many_input:
                                        self.many_input = f"\n {self.current_name + self.current_input.replace("\n",f"\n {self.current_name}")}"
                                        self.text_area.insert("end", self.many_input)
                                    if "%" in line or "^" in line or "syntax error" in self.line.lower():
                                        self.text_area.insert("end", f"\n {line.replace("\n", "")}")
                                self.old_line = line
                                self.adjust_textbox_height()
                                self.text_area.configure(height=self.new_height)
                                self.update_idletasks()
                            else:
                                if line.replace(" ", "") != "\n":
                                    self.text_area.insert("end", f"\n {line.replace("\n", "")}")  # думать + думать жоска
                                    self.old_line = "8425902375"
                            x = self.text_area.get("1.0", "end").count("\n")
                            y = self.text_area.get(f"{x-1}.0", "end").lower()
                            if ("%" in y or "configuring" in y or "syntax error" in y) and self.old_name.strip() in self.text_area.get(f"{x}.0", "end") and self.next_after_conf:
                                self.text_area.configure(state="normal")
                                self.text_area.delete(f"{x}.0", "end")
                                self.text_area.configure(state="disabled")
                                self.adjust_textbox_height()
                                self.text_area.see("end")
                                self.next_after_conf = False
                                self.after(50, lambda: self.hide_write())
                            else:
                                self.next_after_conf = True

                            self.adjust_textbox_height()
                            self.text_area.configure(state="disabled")
                        else:
                            self.special_string += line
                    self.text_area.see("end")
                    x = self.text_area.get("1.0", "end").count("\n")
                    last_string = self.text_area.get(f"{x}.0", "end")
                    if self.old_name == "Password:":
                        self.input_label.configure(self, fg_color=("#ffffff", "#1a1a1a"), width=20, bg_color=("#ffffff", "#1a1a1a"), text=" >", font=("Consolas", 18, "bold"), height=0)
                    if ("login" in self.line.lower() or "User Name:" in self.line or "retry authentication" in last_string.lower()) and self.old_name != "Login:":
                        self.input_label.configure(text="  Login:", font=("Consolas", 14))
                        self.old_name = "Login:"
                        continue
                    if self.old_name == "Login:" and "password" not in self.line.lower() or self.old_input in last_string and self.old_name == "Login:":
                        self.input_label.configure(text="  Password:", font=("Consolas", 14))
                        self.old_name = "Password:"
                    if "#" in line and len(line) < 40 and "# " not in line.rstrip() and " #" not in line:
                        index = line.find("#")
                        self.find_device_name(line[:index+1])
                    elif ">" in line and len(line) < 40 and "> " not in line.rstrip() and " >" not in line:
                        index = line.find(">")
                        self.find_device_name(line[:index+1])
            except serial.SerialException as e:
                self.disconnect_serial()
                self.input_entry.configure(state="normal")
                self.after(30, lambda: self.input_entry.focus_set())
                self.text_area.configure(state="normal")
                self.text_area.insert("end", f"\n Error reading from port: {e}")
                self.adjust_textbox_height()
                self.text_area.see("end")
                self.text_area.configure(state="disabled")
                break
        if self.serial_port and not self.serial_port.is_open:
            self.input_entry.configure(state="normal")
            self.after(30, lambda: self.input_entry.focus_set())
            self.text_area.configure(state="normal")
            self.text_area.insert("end", "\n Reading thread stopped due to disconnect.")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")

    def remove_more_and_surrounding(self, string):
        pattern = r".*More.*?(?=z1x1c)"
        new_string = re.sub(pattern, "\n", string)  # re.sub заменяет все вхождения
        return new_string

    def remove_spaces_and_surrounding(self, string):
        pattern = r"\s*"
        new_string = re.sub(pattern, "\n", string)  # re.sub заменяет все вхождения
        return new_string

    def clear_text(self):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.configure(state="disabled")
        self.adjust_textbox_height()

    def get(self):
        self.master.wait_window(self)
        kostil = 1
        return kostil