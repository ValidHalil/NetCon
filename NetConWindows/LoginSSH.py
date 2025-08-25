import tkinter
import updated_ctk as ctk
from NetConWindows import CTkMessagebox
import NetConWindows
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginSSH(ctk.CTkToplevel):
    def __call__(self, var, master, opacity, language):

        def close_window():
            self.grab_release()
            self.destroy()

        def right_click():
            return self.after(150, lambda: self.focus_set())

        def clicked(user_login,ip, alg):
            if user_login == "":
                if self.language == "Русский":
                    close_window()
                    CTkMessagebox(opacity = opacity, message='Поле не должно быть пустым!', title='Ошибка', icon='cancel')
                    return
                else:
                    close_window()
                    CTkMessagebox(opacity=opacity, message='The field must not be empty!', title='Error', icon='cancel')
                    return
            #close_window()
            if alg == "Auto":
                os.system("start cmd /k ssh " + user_login + "@" + ip)
            else:
                os.system(f"start cmd /k ssh -m hmac-{alg} -A " + user_login + "@" + ip)

        self.language = language
        ip_address=var
        x = tkinter.StringVar()
        self.title("Авторизация")
        self.geometry("320x270")
        self.attributes("-alpha", opacity)
        self.lift()  # lift window on top
        #self.attributes("-topmost", True)  # stay on top
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable
        self.bind("<Button-3>", lambda escape_entry: right_click())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 320
        window_height = 270
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
        self.frame_1.grid_rowconfigure((1, 3), weight=1)


        self.label_1 = ctk.CTkLabel(master=self.frame_1, text="Имя пользователя:", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.label_1.grid(row=1, column=1, columnspan=2, padx=(25, 25), pady=(15, 5), sticky="nsew")
        self.entry1 = ctk.CTkEntry(self.frame_1, textvariable=x, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="normal"), justify="c")
        self.entry1.grid(row=2, column=1,columnspan=2, padx=25, pady=(0, 0), sticky="nsew")
        self.after(150, lambda: self.entry1.focus())
        self.entry1.bind("<Return>", lambda open_ssh: clicked(self.entry1.get(),ip_address, self.combobox.get()))
        self.entry1.bind("<Down>", lambda open_var: self.combobox._clicked())
        self.label_2 = ctk.CTkLabel(master=self.frame_1, text="Алгоритм хэширования:", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.label_2.grid(row=3, column=1, columnspan=2, padx=(25, 25), pady=(10, 5), sticky="nsew")
        self.combobox = ctk.CTkComboBox(master=self.frame_1,
                                                     values=["Auto", "sha1", "sha1-96", "sha2-256", "sha2-512", "md5", "md5-96"],
                                                     state="readonly",
                                                     width=166,
                                                     justify="c")
        self.combobox.grid(row=4, column=1, columnspan=2, padx=25, pady=(0, 0), sticky="ew")
        self.combobox.set(value="Auto")
        self.combobox.bind("<Down>", lambda open_var: self.combobox._clicked())
        self.combobox.bind("<Return>", lambda open_ssh: clicked(self.entry1.get(),ip_address, self.combobox.get()))

        self.button_1 = ctk.CTkButton(master=self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), text="ОК", width=100, fg_color="#1F538D", border_width=0, command=lambda: clicked(self.entry1.get(),ip_address, self.combobox.get()))
        self.button_1.grid(row=5, column=1, padx=(25, 10), pady=(25, 25), sticky="nsew")
        self.button_2 = ctk.CTkButton(master=self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"), text="Отмена", width=100, fg_color="#de710b", border_width=0, hover_color="#ab590c", command=close_window)
        self.button_2.grid(row=5, column=2, padx=(15, 25), pady=(25, 25), sticky="nsew")
        #self.mainloop()
        self.master_window = master
        self.update_position()
        self.bind("<Configure>", self.update_position)

        if self.language != "Русский":
            self.title("Authorization")
            self.label_1.configure(text="Username:")
            self.label_2.configure(text="Hashing algorithm:")
            self.button_2.configure(text="Cancel")


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

