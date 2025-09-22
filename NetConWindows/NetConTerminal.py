import re
import updated_ctk as ctk
import netmiko
import threading
import queue
import os
from PIL import Image
from NetConWindows import Help, CTkMessagebox
import NetConWindows
import ctypes
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

class NetConTerminal(ctk.CTkToplevel):
    def __call__(self, theme, ip_address, con_type, scale, opacity, master, language):
        super().__init__()
        self.old_height = 0
        self.language = language
        self.master = master
        self.entry_text = None
        self.old_name = ""
        self.new_height = 0
        self.many_input = ""
        self.current_input = ""
        self.device_ip = ip_address
        self.old_input = ""
        self.sum_line = ""
        self.show_password_flag = True
        self.old_line = "8425902375"
        self.current_name = ""
        self.flag = 1
        self.con_type = con_type
        self.special_string = ""
        self.bar_height = 0
        self.scaling_factor = 0
        self.theme = theme
        self.last_command_list = LimitedList(10)
        if self.language == "Русский":
            self.title(f"Тип подключения: {self.con_type} | Хост: {self.device_ip}")
        else:
            self.title(f"Connection type: {self.con_type} | Host: {self.device_ip}")
        self.geometry("1100x580")
        self.opacity = opacity
        self.attributes("-alpha", self.opacity)
        self.lift()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1100
        window_height = 580
        self.scaling_factor = ScreenCurrent.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.minsize(850,250)
        self.serial_port = None
        self.counter = 0
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.stop_event = threading.Event()
        self.after(150, lambda : self.create_widgets())
        if scale != "100%":
            ctk.set_widget_scaling(1)

    def create_widgets(self):
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")
        self.configure(fg_color=("#ffffff","#1a1a1a"))
        self.iconbitmap(path_img + "img/serial_title.ico")
        self.clear_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/clear_term.png"), size=(15, 20))
        self.show_pass_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/show_password.png"), size=(15, 16))
        self.hide_pass_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/hide_password.png"), size=(15, 16))
        self.cleartext_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/cleartext.png"), size=(18, 18))
        self.search_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/search_term.png"), size=(18, 18))
        self.disconnect_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial_dis1.png"), size=(20, 20))
        self.disconnect_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial_dis2.png"), size=(20, 20))
        self.connect_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial1.png"), size=(20, 20))
        self.connect_disabled_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/serial2.png"), size=(20, 20))
        self.help_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help.png"), size=(37, 18))
        self.help_eng_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/help_eng.png"), size=(37, 15))
        username_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/username.png"), size=(30, 28))
        username_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/username_light.png"), size=(30, 28))
        password_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/password.png"), size=(30, 28))
        password_light_img = ctk.CTkImage(dark_image=Image.open(path_img + "img/password_light.png"), size=(30, 28))

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan = 2)
        self.settings_frame.grid_columnconfigure((6), weight=1)
        self.settings_frame.grid_rowconfigure((0), weight=1)

        self.grid_columnconfigure(1, weight=1)

        self.bind("<Control-Delete>", lambda delete_text: self.clear_text())
        self.bind("<F9>", lambda open_help: self._show_help())
        self.bind("<F8>", lambda open_settings: self.toggle_settings_frame())
        self.bind("<F6>", lambda discon: self.disconnect())
        self.bind("<Button-3>", lambda escape_entry: self.right_click())

        self.user_label = ctk.CTkLabel(self.settings_frame, text="Имя:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.user_label.grid(row=0, column=0, padx=(57, 10), pady=(25, 5), sticky="nsew")
        if self.theme == "Темная" or self.theme == "Dark":
            self.user_label_img = ctk.CTkLabel(self.settings_frame, image=username_img, text="")
        else:
            self.user_label_img = ctk.CTkLabel(self.settings_frame, image=username_light_img, text="")
        self.user_label_img.grid(row=0, column=0, padx=(25, 0), pady=(25, 5), sticky="w")
        self.username = ctk.CTkEntry(self.settings_frame, placeholder_text="...", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), width=130)
        self.username.grid(row=0, column=1, padx=(0, 0), pady=(25, 5), sticky="nsew")
        self.clear_username = ctk.CTkButton(self.settings_frame, width=20, border_width=0, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.clear_img, text="", command=lambda: [self.username.delete(0, "end"), self.after(100, lambda: self.username.focus_set())])
        self.clear_username.grid(row=0, column=2, padx=(5, 0), pady=(25, 5), sticky="e")
        self.username.bind("<Return>", lambda next_input: self.after(50, lambda: self.password.focus_set()))
        self.username.bind("<Delete>", lambda delite_ep_tvoy_mat: [self.username.delete(0, "end"), self.after(100, lambda: self.username.focus_set())])
        self.username.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.bind('<Escape>', lambda escape_entry: self.right_click())]))
        self.username.bind("<FocusOut>", lambda focus_out: [self.bind("<Escape>", lambda x: self._on_closing())])

        self.pass_label = ctk.CTkLabel(self.settings_frame, text="Пароль:", font=ctk.CTkFont(family="Trebuchet MS", size=15, weight="bold"))
        self.pass_label.grid(row=0, column=3, padx=(57, 10), pady=(25, 5), sticky="nsew")
        if self.theme == "Темная" or self.theme == "Dark":
            self.pass_label_img = ctk.CTkLabel(self.settings_frame, image=password_img, text="")
        else:
            self.pass_label_img = ctk.CTkLabel(self.settings_frame, image=password_light_img, text="")
        self.pass_label_img.grid(row=0, column=3, padx=(25, 0), pady=(25, 5), sticky="w")
        self.password = ctk.CTkEntry(self.settings_frame, placeholder_text="...", show = "*", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), width=130)
        self.password.grid(row=0, column=4, padx=(0, 0), pady=(25, 5), sticky="nsew")
        self.clear_password = ctk.CTkButton(self.settings_frame, width=20, border_width=0, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.clear_img, text="", command=lambda: [self.password.delete(0, "end"), self.after(100, lambda: self.password.focus_set())])
        self.clear_password.grid(row=0, column=5, padx=(5, 10), pady=(25, 5), sticky="e")
        self.password.bind("<Return>", lambda con: [self.after(70, lambda: self.connect(flag=2))])
        self.password.bind("<Delete>", lambda delite_ep_tvoy_mat: [self.password.delete(0, "end"), self.after(100, lambda: self.password.focus_set())])
        self.password.bind("<FocusIn>", lambda focus_on: self.after(100, lambda: [self.bind('<Escape>', lambda escape_entry: self.right_click())]))
        self.password.bind("<FocusOut>", lambda focus_out: [self.bind("<Escape>", lambda x: self._on_closing())])

        self.show_password_btn = ctk.CTkButton(self.settings_frame, width=12, height=12, border_width=0, fg_color=("#f9f9fa", "#343638"), bg_color=("#f9f9fa", "#343638"), hover_color=("#f1f1f1", "#323232"), image=self.show_pass_img, text="", command=self.show_password)
        self.show_password_btn.grid(row=0, column=4, padx=(0, 4), pady=(25, 5), sticky="e")

        self.connect_button = ctk.CTkButton(self.settings_frame, width=50, text="", fg_color="#1F538D", command=self.connect, image=self.connect_img, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.connect_button.grid(row=0, column=7, padx=(0,0), pady=(25,5), sticky = "nse")
        self.disconnect_button = ctk.CTkButton(self.settings_frame, width=50, state="disabled", fg_color="#ab590c",command=self.disconnect, border_width=0, hover_color="#ab590c", image=self.disconnect_disabled_img, text="")
        self.disconnect_button.grid(row=0, column=8, padx=(10,0), pady=(25,5), sticky = "nsew")
        self.help_btn = ctk.CTkButton(master=self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), text_color="gray32", hover_color=("white", "#333333"), border_width=0, image=self.help_img, text="", font=ctk.CTkFont(size=11, weight="bold"), command=self._show_help)
        self.help_btn.grid(row=0, column=9, padx=(10, 0), pady=(25, 5), sticky="nsew")
        self.search_btn = ctk.CTkButton(self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.search_img, height=18, border_width=0, text="", command=self.open_search_window)
        self.search_btn.grid(row=0, column=10, padx=(10, 0), pady=(25, 5), sticky="nsew")
        self.clearbut = ctk.CTkButton(self.settings_frame, width=20, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.cleartext_img, height=18, border_width=0, text="", command=self.clear_text)
        self.clearbut.grid(row=0, column=11, padx=(10,25), pady=(25,5), sticky = "nsew")
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
        self.after(150, lambda: self.username.focus_set())
        self.bind("<KeyRelease>", self.what_button)

        self.net_connect = None
        self.output_queue = queue.Queue()
        self.running = False
        self.search_window = None

        self.base_width = 1100 * self.scaling_factor
        self.base_height = 580 * self.scaling_factor
        self.bind("<Configure>", lambda x: self.on_configure())
        self.adjust_textbox_height()

        if self.language != "Русский":
            self.user_label.configure(text="Username:")
            self.pass_label.configure(text="Password:")

    def show_password(self):
        if self.show_password_flag:
            self.password.configure(show = "")
            self.show_password_btn.configure(image=self.hide_pass_img)
            self.show_password_flag = False
        else:
            self.password.configure(show = "*")
            self.show_password_btn.configure(image=self.show_pass_img)
            self.show_password_flag = True

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
            self.search_window = NetConWindows.SearchWindow(self, self.text_area, self.opacity, self.language, self.theme)
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
            msg = CTkMessagebox(opacity=self.opacity, message='Завершить сессию?', title='Внимание', icon='warning', option_1="Отмена", option_2="Да")
        else:
            msg = CTkMessagebox(opacity=self.opacity, message='End session?', title='Attention', icon='warning', option_1="Cancel", option_2="Yes")
        msg.button_1.configure(fg_color="#de710b", hover_color="#ab590c")
        msg.focus_set()
        response = msg.get()
        if response == "Отмена" or response == "Cancel":
            return
        if response == "Да" or response == "Yes":
            self.disconnect()
            self.grab_release()
            self.destroy()
            self.master.deiconify()

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
        help_tab("Телнет", self, self.opacity, self.language)

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

    def connect(self, flag=1):
        if self.con_type == "Telnet":
            device = {
                "device_type": "cisco_ios_telnet",
                "host": f"{self.device_ip}",
                "username": f"{self.username.get()}",
                "password": f"{self.password.get()}",
                "global_delay_factor": 0.5,  # Небольшая задержка для совместимости
                "port": 23
            }
        else:
            device = {
                "device_type": "cisco_ios_ssh",
                "host": f"{self.device_ip}",
                "username": f"{self.username.get()}",
                "password": f"{self.password.get()}",
                "global_delay_factor": 0.5,  # Небольшая задержка для совместимости
                "port": 22
            }
        """
        if self.username.get() == "":
            self.username.focus_set()
            return CTkMessagebox(opacity = self.opacity, message='Введите имя пользователя!', title='Ошибка', icon='cancel')
        elif self.password.get() == "":
            self.password.focus_set()
            return CTkMessagebox(opacity = self.opacity, message='Введите пароль!', title='Ошибка', icon='cancel')
        else:
        """
        self.start_quickload()
        self.connect_thread = threading.Thread(target=self._connect_thread, args=(device,))
        self.connect_thread.daemon = True
        self.connect_thread.start()

    def _connect_thread(self, device):
        try:
            self.input_entry.configure(state="normal")
            self.clear_entry()
            self.clear_text()
            self.connect_button.configure(state="disabled", image=self.connect_disabled_img, fg_color="#14375e")
            self.disconnect_button.configure(state="normal", fg_color="#de710b", image=self.disconnect_img)
            self.username.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
            self.password.configure(state="disabled", border_color=("#8f8f8f", "#444444"), text_color=("gray50", "gray45"))
            self.input_entry.bind('<?>', lambda x: self.send_command2(f"{self.input_entry.get()}?\r"))  # при выводе справки при нажатии на "?"
            self.net_connect = netmiko.ConnectHandler(**device)
            self.running = True
            self.append_output(f"\n Connected to {device["host"]} via {self.con_type}.")
            threading.Thread(target=self.process_output_queue, daemon=True).start()
            self.after(50, lambda: [self.input_entry.focus_set(), self.stop_text_area_read_input(), self.send_command(), self.send_command()])
            self.after(250, lambda: self.back_text_area_read_input())
            self.text_area.see("end")
            self.input_entry.bind('<Tab>', lambda x: [self.stop_text_area_read_input(), self.send_command2(self.input_entry.get() + "\t", "old", tab_flag=True), self.after(30, lambda: [self.send_command2("_ _\r", tab_flag=True), self.after(30, lambda: self.send_command2("\r", tab_flag=True))]), self.after(350, lambda: self.del_fuck_after_tab())])
            self.stop_event.clear()
            self.settings_frame.grid_forget()
            self.settings_toggle_button.configure(text="▼")
            self.settings_frame_hidden = True
            self.bar_height = 50
            self.adjust_textbox_height()
            self.after(200, lambda: self.unbind("<Escape>"))
            self.after(250, lambda: self.input_entry.bind('<Escape>', lambda clear: self.clear_entry()))

        except Exception as e:
            if len(str(e)) < 200:
                self.append_output(f"\n Ошибка подключения: {e}")
            else:
                self.append_output(f"\n\n Ошибка подключения: {e}")
            self.adjust_textbox_height()
            self.net_connect = None
            self.running = False
            self.bad_connect()

        finally:
            # Stop QuickLoad after connection attempt
            self.stop_quickload()

    def right_click(self):
        self.after(150, lambda: self.focus_set())
        return

    def on_tab_pressed(self, event):
        return "break"

    def bad_connect(self):
        self.unbind("<Tab>")
        self.clear_entry()
        self.bind("<Escape>", lambda x: self._on_closing())
        self.old_name = ""
        self.after(150, lambda: self.input_label.configure(text=" >", font=("Consolas", 18, "bold")))
        self.after(100, lambda: self.input_entry.unbind("<?>"))
        self.after(100, lambda: self.input_entry.unbind("<Tab>"))
        self.net_connect = None
        self.running = False
        self.stop_event.set()  # Stop reading thread
        self.text_area.configure(state="disabled")
        self.username.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
        self.password.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
        self.connect_button.configure(state="normal", image=self.connect_img, fg_color="#1F538D")
        self.disconnect_button.configure(state="disabled", fg_color="#ab590c", image=self.disconnect_disabled_img)
        #self.after(160, lambda: [self.focus_set(), self.input_entry.insert(0, "Ожидание подключения..."), self.input_entry.configure(state="disabled")])
        if self.language == "Русский":
            self.after(160, lambda: [self.focus_set(), self.input_entry.insert(0, "Ожидание подключения..."), self.input_entry.configure(state="disabled")])
        else:
            self.after(160, lambda: [self.focus_set(), self.input_entry.insert(0, "Waiting for connection..."), self.input_entry.configure(state="disabled")])
        self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.settings_toggle_button.configure(text="▲")
        self.settings_frame_hidden = False
        self.bar_height = 108
        self.adjust_textbox_height()
        self.text_area.configure(height=self.new_height)
        self.update_idletasks()
        self.after(200, lambda: self.text_area.see("end"))

    def disconnect(self):
        if self.net_connect:
            self.unbind("<Tab>")
            self.clear_entry()
            self.bind("<Escape>", lambda x: self._on_closing())
            self.old_name=""
            self.after(150, lambda: self.input_label.configure(text=" >", font=("Consolas", 18, "bold")))
            self.after(100, lambda: self.input_entry.unbind("<?>"))
            self.after(100, lambda: self.input_entry.unbind("<Tab>"))
            self.net_connect = None
            self.running = False
            self.stop_event.set()  # Stop reading thread
            self.append_output(f"\n Disconnected from {self.device_ip}.")
            self.adjust_textbox_height()
            self.text_area.configure(state="disabled")
            self.username.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
            self.password.configure(state="normal", border_color=("#979da2", "#565b5e"), text_color=("gray14", "gray84"))
            self.connect_button.configure(state="normal", image=self.connect_img, fg_color="#1F538D")
            self.disconnect_button.configure(state="disabled", fg_color="#ab590c", image=self.disconnect_disabled_img)
            if self.language == "Русский":
                self.after(160, lambda: [self.focus_set(),self.input_entry.insert(0, "Ожидание подключения..."), self.input_entry.configure(state="disabled")])
            else:
                self.after(160, lambda: [self.focus_set(), self.input_entry.insert(0, "Waiting for connection..."), self.input_entry.configure(state="disabled")])
            #self.after(160, lambda: [self.focus_set(),self.input_entry.insert(0, "Ожидание подключения..."), self.input_entry.configure(state="disabled")])
            self.settings_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            self.settings_toggle_button.configure(text="▲")
            self.settings_frame_hidden = False
            self.bar_height = 108
            self.adjust_textbox_height()
            self.text_area.configure(height=self.new_height)
            self.update_idletasks()
            self.after(200, lambda: self.text_area.see("end"))

    def start_quickload(self):
        self.quickload = NetConWindows.QuickLoad()  # Pass self (NetConTerminal) as master
        self.quickload(self, self.opacity, self.language)
        self.quickload_thread = threading.Thread(target=self.quickload.get, daemon=True)  # Removed __call__
        self.quickload_thread.start()

    def stop_quickload(self):
        if self.quickload:
            try:
                self.quickload.destroy()
            except Exception as e:
                print(f"Error destroying QuickLoad: {e}")
                return self.stop_quickload()
            self.quickload = None
        if self.quickload_thread and self.quickload_thread.is_alive():
            self.quickload_thread.join(timeout=0.1)  # wait before destroy the window
            if self.quickload_thread.is_alive():
                print("QuickLoad thread did not terminate in time.")
    """
    def read_output(self):
        while self.running and self.net_connect:
            try:
                output = self.net_connect.read_channel()
                if output:
                    self.output_queue.put(output)
                else:
                    time.sleep(0.1) # Небольшая задержка чтобы не спамить cpu
            except Exception as e:
                self.output_queue.put(f"\n Ошибка при чтении вывода: {e}")
                self.running = False

            self.process_output_queue()
    """

    def check_previous_element_in_next(self, array):
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

    def process_output_queue(self):
        def key_q(event):
            if event.keycode == 81:  # Клавиша с буквой Й и с англ. буквой Q
                self.stop_text_area_read_input()
                self.after(10, lambda: [self.send_command2("q" + "\r"), self.send_command2("" + "\r"), self.send_command2("" + "\r")])
                self.after(300, lambda: [self.back_text_area_read_input(), self.unbind('<space>'), self.send_command2("" + "\r"), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        def key_control_c(event):
            if event.keycode == 67:  # Клавиша с буквой C и с англ. буквой C
                self.stop_text_area_read_input()
                self.after(10, lambda: [self.send_command2("q" + "\r"), self.send_command2("" + "\r"), self.send_command2("" + "\r")])
                self.after(300, lambda: [self.back_text_area_read_input(), self.unbind('<space>'), self.send_command2("" + "\r"), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        try:
            while self.running and self.net_connect:
                self.bind("<Tab>", self.on_tab_pressed)
                line = self.net_connect.read_until_pattern("\n", read_timeout=0)
                if len(line) == 1 and "\n" in line:
                    continue
                else:
                    line = self.remove_ansi_escape(line.encode())
                #print(line.encode())
                self.line = line.replace("z1x1c","")
                if "More" in line:  # Other
                    self.after(100, lambda: self.input_entry.configure(state="readonly"))  # пока подумать
                    self.after(300, lambda: self.input_entry.configure(state="readonly"))
                    if self.flag == 1:
                        self.text_area.configure(state="normal")
                        line = self.remove_more_and_surrounding(line)
                        line = line.replace("z1x1c", "")
                        if line != "\n":
                            self.text_area.insert("end", f"\n {line.replace("\n", "")}")
                        self.adjust_textbox_height()
                        self.text_area.configure(state="disabled")
                    self.after(100, lambda: [self.bind('<space>', lambda x: [self.send_command2(" " + "\r")]), self.bind('<KeyPress>', key_q), self.bind('<Control-KeyPress>', key_control_c)])
                    self.after(300, lambda: [self.bind('<space>', lambda x: [self.send_command2(" " + "\r")]), self.bind('<KeyPress>', key_q), self.bind('<Control-KeyPress>', key_control_c)])
                else:
                    self.unbind('<space>')
                    self.unbind('<KeyPress>')
                    self.unbind('<Control-KeyPress>')
                    self.input_entry.configure(state="normal")
                    if self.flag == 1:
                        self.text_area.configure(state="normal")
                        line = line.replace("z1x1c", "")
                        line_index = line.find("#")
                        line_without_name = line[line_index + 1:].replace("\n", "").rstrip().lstrip()
                        drobl_line = line_without_name.split(" ")
                        esr_input_trigger = self.check_previous_element_in_next(drobl_line)
                        if line.replace("\n", "").rstrip().lstrip() not in self.old_line.replace("\n", "").rstrip().lstrip() and self.current_input in line and self.current_input != "" and "login" not in self.line.lower() and "%" not in line and "^" not in line and "syntax error" not in self.line.lower() or ("\n" in self.current_input and esr_input_trigger):
                            if "\n" not in self.current_input:
                                self.text_area.insert("end", f"\n {self.current_name + self.current_input}")
                            else:
                                if f"\n {self.current_name + self.current_input.replace("\n", f"\n {self.current_name}")}" != self.many_input:
                                    self.many_input = f"\n {self.current_name + self.current_input.replace("\n", f"\n {self.current_name}")}"
                                    self.text_area.insert("end", self.many_input)
                                if "%" in line or "^" in line or "syntax error" in self.line.lower():
                                    self.text_area.insert("end", f"\n {line.replace("\n", "")}")
                            self.old_line = line
                            self.adjust_textbox_height()
                            self.text_area.configure(height=self.new_height)
                            self.update_idletasks()
                        else:
                            if line.replace(" ","") != "\n":
                                self.text_area.insert("end", f"\n {line.replace("\n", "")}")  # думать + думать жоска
                                self.old_line = "8425902375"
                        x = self.text_area.get("1.0", "end").count("\n")
                        if ("%" in self.text_area.get(f"{x - 1}.0", "end").lower() or "configuring" in self.text_area.get(f"{x - 1}.0", "end").lower() or "syntax error" in self.text_area.get(f"{x - 1}.0", "end").lower()) and self.old_name.strip() in self.text_area.get(f"{x}.0", "end") and self.next_after_conf:
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
                if "#" in line and len(line) < 40 and "# " not in line.rstrip() and " #" not in line:
                    index = line.find("#")
                    self.find_device_name(line[:index + 1])
                elif ">" in line and len(line) < 40 and "> " not in line.rstrip() and " >" not in line:
                    index = line.find(">")
                    self.find_device_name(line[:index + 1])
        except Exception as e:
            self.disconnect()
            self.text_area.configure(state="normal")
            if self.language == "Русский":
                self.text_area.insert("end",f"\n Ошибка при чтении вывода: {e}")
            else:
                self.text_area.insert("end", f"\n Error reading output: {e}")
            self.text_area.configure(state="disabled")
            self.running = False
            self.net_connect = None
    """
    def remove_more_and_surrounding(self, string):
        pattern = r"\n.*More.*\n"
        matches = list(re.finditer(pattern, string))  # Находим все вхождения
        if matches:
            first_occurrence = matches[0]
            string = string[:first_occurrence.start()] + string[first_occurrence.end():]
        return string
    """

    def remove_more_and_surrounding(self, string):
        pattern = r".*More.*\n"
        new_string = re.sub(pattern, "\n", string)  # re.sub заменяет все вхождения
        return new_string

    def remove_spaces_and_surrounding(self, string):
        pattern = r"\s*\n"
        new_string = re.sub(pattern, "\n", string)  # re.sub заменяет все вхождения
        return new_string

    def find_second_newline_index_enumerate(self, byte_string):
        count = 0
        for i, char in enumerate(byte_string):
            if char == ord('\n'):  # Сравниваем с числовым кодом символа новой строки
                count += 1
                if count == 2:
                    return i
        return None

    def remove_duplicate_words_ordered_loop(self, word_list):
        result = []
        seen = set()  # Множество для хранения уже встреченных слов
        for word in word_list:
            if word not in seen:
                result.append(word)
                seen.add(word)
        return result

    def del_fuck_after_tab(self):  # пока спорно, на циске работает
        result = []
        input = self.old_input
        words = input.split()
        # print(self.special_string)
        y = self.special_string.replace("_", "")
        if "Syntax error:" in y:
            y = y.replace("Syntax error:", "%")
        index = y.find("%")
        y = y[:index]
        lines = y.split()
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
        # print(result)
        final = ""
        for i in range(0, len(result)):
            final += result[i] + " "
        continue_input = {"-", "/", ":"}
        if len(final.rstrip()) > len(self.old_input.rstrip()):
            final_out = (final.replace(f"{words[len(words) - 1]} ", "").replace("z1x1c", ""))
            added_word = final_out.lower().replace(self.old_input.lower(),"")
            if final[len(final.rstrip())-1] not in continue_input:
                self.input_entry.insert("end", added_word)
            else:
                self.input_entry.insert("end", added_word.rstrip())
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

    def reload_alert(self):
        def key(event):
            if event.keycode == 89:
                self.net_connect.write_channel("y".encode())
                self.net_connect.write_channel("y".encode())
                self.net_connect.write_channel(self.nullstring.encode())
                self.input_entry.configure(state="normal")
                self.input_entry.delete(0, "end")
                self.after(140, lambda: self.input_entry.delete(0, "end"))
                self.after(150, lambda : self.input_entry.unbind("<KeyPress>"))
            elif event.keycode == 78:
                self.net_connect.write_channel("n".encode())
                self.net_connect.write_channel(self.nullstring.encode())
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
        self.net_connect.write_channel(self.nullstring.encode())
        self.after(140, lambda: self.back_text_area_read_input())

    def update_command_list(self, command):
        if command != "\r" and command.replace("\r", "") not in self.last_command_list:
            self.last_command_list.append(command.replace("\r", "").rstrip())
        if command.replace("\r", "") in self.last_command_list:
            old_index = self.last_command_list.index(command.replace("\r", ""))
            move_element = self.last_command_list.pop(old_index)
            self.last_command_list.append(move_element)

    def send_command(self):  # для элтексов вроде заебца
        self.many_input = ""
        command = self.input_entry.get() + "\r"
        if "\n" in command:
            i_n = command.count('\n')
            self.after(20, lambda: self.focus_set())
            self.after(120*i_n, lambda: self.input_entry.focus_set())
        self.sum_line = ""
        self.current_input = self.input_entry.get().lstrip().rstrip()
        self.nullstring = "\r"
        if self.net_connect:
            if ("reset " in command.lower() or "delete " in command.lower() or "boot " in command.lower() or "erase " in command.lower() or "write " in command.lower() or "reload" in command.lower() or "copy " in command.lower() or "default " in command.lower()) and not command.lower().startswith("sh") and not command.lower().startswith("disp"):  # Возможно будет дополняться
                #if "default " not in command.lower():
                self.clear_text()
                self.net_connect.write_channel(command.encode())
                self.after(150, lambda: self.reload_alert())
                self.update_command_list(command)
            else:
                self.net_connect.write_channel(command.encode())
                if command.strip() != "" and "login" not in self.line.lower() and ("#" in self.line or ">" in self.line):  # последнее условие пока не точно
                    self.update_command_list(command)
                    self.net_connect.write_channel(self.nullstring.encode())
            self.input_entry.delete(0, "end")
        self.counter = len(self.last_command_list)

    def send_command2(self, command, var=None, tab_flag=False):
        self.sum_line = ""
        # self.after(300, lambda : [self.unbind('<space>'), self.unbind('<KeyPress>'), self.unbind('<Control-KeyPress>')])
        self.current_input = self.input_entry.get().lstrip().rstrip()
        if var is not None:
            self.old_input = self.input_entry.get()
        if self.net_connect:
            self.net_connect.write_channel(command.encode())
            self.input_entry.configure(state="normal")
            if tab_flag:
                print("")
            else:
                self.input_entry.delete(0, "end")
            self.input_entry.configure(state="readonly")

    def append_output(self, text):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", text)
        self.text_area.see("end")  # Автоматическая прокрутка
        self.text_area.configure(state="disabled")
        self.adjust_textbox_height()

    def stop_text_area_read_input(self):
        self.flag = 2

    def back_text_area_read_input(self):
        self.flag = 1

    def find_device_name(self, var_line):
        if "#" in var_line and "more" not in self.line.lower() and 40 > len(var_line) > 1:
            s = var_line.replace("\n","")
            index = s.find("#")
            if var_line.replace("\n", "").replace(self.old_name.lstrip(),"") == self.old_input and self.old_input != "":
                #print("catch!")
                s = s.replace(self.old_input,"")
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
            s = var_line.replace("\n","")
            index = s.find(">")
            if var_line.replace("\n", "").replace(self.old_name.lstrip(),"") == self.old_input and self.old_input != "":
                #print("catch")
                s = s.replace(self.old_input,"")
                s = s.replace("z1x1c", "")
            if index == len(s) - 1:
                s = "  " + s[:index + 1]
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

    def remove_ansi_escape(self, data):
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

    def clear_text(self):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.configure(state="disabled")
        self.adjust_textbox_height()