import updated_ctk as ctk
import subprocess
import keyboard
import datetime
from NetConWindows import CTkMessagebox
import NetConWindows

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Loading(ctk.CTkToplevel):
    def __call__(self,ipa,textbox,type,master,opacity,language):

        def kill_proc(proc):
            proc.terminate()

        def close_window():
            self.grab_release()
            self.destroy()

        def ping(ip,textbox,type_var):
            self.withdraw()
            if type_var == " None ":
                command = "tracert " + ip
            elif type_var == "/d":
                command = "tracert /d " + ip
            elif type_var == "/j":
                command = "tracert /j " + ip
            elif type_var == "/t":
                command = "ping /t /a " + ip
            elif type_var == "/a":
                command = "ping -a " + ip
            else:
                command = "ping " + ip
            textbox.configure(state='normal')
            textbox.insert('end', " \n")
            textbox.insert('end'," 〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
            textbox.insert('end', " \n")
            if self.language == "Русский":
                textbox.insert('end',"                                                                                   Для остановки нажмите «ESCAPE»!\n")
            else:
                textbox.insert('end',"                                                                                       To stop, press «ESCAPE»!\n")
            textbox.insert('end', " \n")
            textbox.insert('end'," 〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉〉\n")
            popen = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW)
            keyboard.on_press_key("esc", lambda x: kill_proc(popen))
            lines_iterator = iter(popen.stdout.readline, b"")
            while popen.poll() is None:
                for line in lines_iterator:
                    now = datetime.datetime.now()
                    textbox.configure(state='normal')
                    nline = line.rstrip()
                    if "Reply from" in nline.decode("cp866") or "Ответ от" in nline.decode("cp866") or "Interval exceeded" in nline.decode("cp866") or "Превышен интервал" in nline.decode("cp866") or " мс " in nline.decode("cp866") or " ms " in nline.decode("cp866"):
                        if self.language == "Русский":
                            textbox.insert('end',"      " + nline.decode("cp866") + " │ Сообщение получено в: " + now.strftime('%X') + "\r\n")
                        else:
                            textbox.insert('end', "      " + nline.decode("cp866") + " │ Message received at: " + now.strftime('%X') + "\r\n")
                    else:
                        textbox.insert('end', "      " + nline.decode("cp866") + "\r\n")
                    textbox.see('end')
                    textbox.update()
            close_window()
            if self.language == "Русский":
                return CTkMessagebox(opacity = opacity, message='Операция завершена!', title='Успех', icon='check')
            else:
                return CTkMessagebox(opacity=opacity, message='Operation completed!', title='Success', icon='check')

        ping_type=type
        textbox_out = textbox
        self.language = language
        self.geometry("300x120")
        self.lift()
        self.grab_set()
        #self.attributes("-topmost", True)
        self.resizable(False, False)
        self.overrideredirect(1)
        self.attributes("-alpha", opacity)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 300
        window_height = 120
        RealSize = NetConWindows.ScreenCurrent()
        self.scaling_factor = RealSize.get_display_scaling()
        xlen = int((screen_width - window_width * self.scaling_factor) // 2)
        ylen = int((screen_height - window_height * self.scaling_factor) // 2)
        self.geometry(f"+{xlen}+{ylen}")

        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=25, padx=25, fill="both", expand=True)
        self.frame_1.grid_rowconfigure((1, 2, 3), weight=1)
        self.frame_1.grid_rowconfigure((1,2), weight=0)
        self.label_1 = ctk.CTkLabel(master=self.frame_1, text="Подождите...", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.label_1.grid(row=1, column=1, columnspan=1, padx=(25, 25), pady=(10, 10), sticky="nsew")
        if self.language != "Русский":
            self.label_1.configure(text = "Wait...")
        self.progressbar_1 = ctk.CTkProgressBar(self.frame_1)
        self.progressbar_1.grid(row=2, column=1, padx=(25, 25), pady=(0, 10), sticky="nsew")
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()

        self.after(2000, lambda: ping(ipa,textbox_out,ping_type))

        self.master_window = master
        self.update_position()
        self.bind("<Configure>", self.update_position)

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
        kostil = 1
        return kostil