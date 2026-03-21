import updated_ctk as ctk
import NetConWindows

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuickLoad(ctk.CTkToplevel):
    def __call__(self, master, opacity, language):

        def kill_proc(proc):
            proc.terminate()

        def close_window():
            self.grab_release()
            self.destroy()

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

        self.configure(fg_color=("#ffffff","#1a1a1a"))
        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=25, padx=25, fill="both", expand=True)
        self.frame_1.grid_rowconfigure((1, 2, 3), weight=1)
        self.frame_1.grid_rowconfigure((1,2), weight=0)
        self.label_1 = ctk.CTkLabel(master=self.frame_1, text="Подождите...", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        if self.language != "Русский":
            self.label_1.configure(text="Wait...")
        self.label_1.grid(row=1, column=1, columnspan=1, padx=(25, 25), pady=(10, 10), sticky="nsew")
        self.progressbar_1 = ctk.CTkProgressBar(self.frame_1)
        self.progressbar_1.grid(row=2, column=1, padx=(25, 25), pady=(0, 10), sticky="nsew")
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
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