import updated_ctk as ctk
import os
import NetConWindows
from NetConWindows import NetConTerminal, LoginSSH, CTkMessagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SelectTerminal(ctk.CTkToplevel):
    def __call__(self, theme, var, con_type, scale, master, opacity, language):

        def close_window():
            self.master_window.after(200, lambda: [self.master_window.bind('<Escape>', lambda close: self.master_window.close_app()), self.master_window.after(50, lambda: self.master_window.bind("<Down>", lambda next: self.master_window.textbox.yview_scroll(1, "units"))), self.master_window.after(50, lambda: self.master_window.bind("<Up>", lambda next: self.master_window.textbox.yview_scroll(-1, "units")))] if self.master_window.tabview.get() == "Подключение" else print("sss"))
            self.grab_release()
            self.destroy()

        def clicked(con,ip):
            self.unbind("<Configure>")
            if con == "Windows CLI" and self.con_type == "Telnet":
                os.system("start cmd /k telnet " + ip)
            elif con == "Windows CLI" and self.con_type == "SSH":
                ssh_con = LoginSSH()
                ssh_con(str(ip), self.master_window, opacity, self.language)
            elif con == "NetTerm":
                master.iconify()
                master.bind('<Escape>', lambda close: master.close_app())
                session = NetConTerminal()
                session(self.theme,ip,self.con_type, self.scale, opacity, master, self.language)
                if self.scale != "100%":
                    self.kostil=1
            close_window()

        ip_address=var
        self.anim_hover = NetConWindows.AnimateButtonHover(self)
        self.language = language
        self.title("Выбор терминала")
        self.geometry("320x220")
        self.attributes("-alpha", opacity)
        self.lift()  # lift window on top
        #self.attributes("-topmost", True)  # stay on top
        self.resizable(False, False)
        self.grab_set()
        self.theme = theme
        self.kostil = 0
        self.con_type = con_type
        self.scale = scale
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 320
        window_height = 220
        RealSize = NetConWindows.ScreenCurrent()
        self.scaling_factor = RealSize.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")
        self.bind('<Escape>', lambda close: close_window())
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")
        self.iconbitmap(path_img + "img/connection.ico")

        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=25, padx=25, fill="both", expand=True)
        self.frame_1.grid_columnconfigure((1,2,3), weight=1)
        self.frame_1.grid_rowconfigure((1, 2, 3), weight=0)
        self.frame_1.grid_rowconfigure((1), weight=1)

        self.label_1 = ctk.CTkLabel(master=self.frame_1, text="Выбор терминала:", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.label_1.grid(row=1, column=1, columnspan=2, padx=(25, 25), pady=(10, 10), sticky="nsew")
        self.optionemenu = ctk.CTkOptionMenu(self.frame_1, values=["NetTerm", "Windows CLI"], fg_color="#1F538D", width=152)
        self.optionemenu.configure(font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), anchor="center")
        self.optionemenu.grid(row=2, column=1,columnspan=2, padx=25, pady=(0, 25), sticky="nsew")
        self.bind("<Down>", lambda open_var: self.optionemenu._clicked())
        self.bind("<Return>", lambda x: clicked(self.optionemenu.get(), ip_address))

        self.button_1 = ctk.CTkButtonSoftHover(master=self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), text="ОК", width=100, normal_color="#1F538D", fg_color="#1F538D", hover=False, border_width=0, command=lambda: clicked(self.optionemenu.get(), ip_address))
        self.button_1.grid(row=3, column=1, padx=(25, 10), pady=(0, 25), sticky="nsew")
        self.button_1.bind("<Enter>", lambda go_hover: [self.anim_hover.animate_hover(self.button_1, int("1f538d", 16), int("0f334d", 16), int("10204", 16), 10, "down")])  # print("IN")
        self.button_1._text_label.bind("<Enter>", lambda var_in: self.anim_hover.stop_leave(self.button_1))
        self.button_1._text_label.bind("<Leave>", lambda var_out: self.anim_hover.go_leave(self.button_1, "1f538d", "0f334d", "10204"))
        self.frame_1.bind("<Enter>", lambda out_of_btn: self.anim_hover.check_color(self.button_1, "1f538d", "0f334d", "10204"))
        self.anim_hover.init_hover_state(self.button_1)

        self.button_2 = ctk.CTkButtonSoftHover(master=self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), text="Отмена", width=100, normal_color="#f4740b", fg_color="#f4740b", hover=False, border_width=0, command=close_window)
        self.button_2.grid(row=3, column=2, padx=(15, 25), pady=(0, 25), sticky="nsew")
        self.button_2.bind("<Enter>", lambda go_hover: [self.anim_hover.animate_hover(self.button_2, int("f4740b", 16), int("94440B", 16), int("60300", 16), 10, "down")])
        self.button_2._text_label.bind("<Enter>", lambda var_in: self.anim_hover.stop_leave(self.button_2))
        self.button_2._text_label.bind("<Leave>", lambda var_out: self.anim_hover.go_leave(self.button_2, "f4740b", "94440B", "60300"))
        self.frame_1.bind("<Enter>", lambda out_of_btn: self.anim_hover.check_color(self.button_2, "f4740b", "94440B", "60300"))
        self.anim_hover.init_hover_state(self.button_2)

        #self.mainloop()
        self.master_window = master
        self.update_position()
        self.bind("<Configure>", self.update_position)

        if self.language != "Русский":
            self.label_1.configure(text="Select a terminal")
            self.button_2.configure(text="Cancel")
            self.title("Selecting a terminal")


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

    def get(self):
        self.master.wait_window(self)
        return self.kostil