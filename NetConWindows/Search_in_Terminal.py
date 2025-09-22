import updated_ctk as ctk
import re
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SearchWindow(ctk.CTkToplevel):
    def __init__(self, master, textbox, opacity, language, theme):
        super().__init__(master)
        app_name = "NetCon.py"
        path_app = (os.path.abspath(app_name))
        path_img = path_app.replace(app_name, "")

        self.theme = theme
        self.iconbitmap(path_img + "img/search_terminal.ico")
        self.up_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/up.png"), size=(15, 15))
        self.down_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/down.png"), size=(15, 15))
        self.up_active_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/up_active.png"), size=(15, 15))
        self.down_active_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/down_active.png"), size=(15, 15))
        self.up_active_light_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/up_active_light.png"), size=(15, 15))
        self.down_active_light_image = ctk.CTkImage(dark_image=Image.open(path_img + "img/down_active_light.png"), size=(15, 15))

        self.language = language
        self.master_window = master
        self.geometry("380x78")
        if self.language == "Русский":
            self.title("Поиск в терминале")
        else:
            self.title("Search in terminal")
        self.textbox = textbox
        self.results = []
        self.current_index = -1
        self.lift()
        self.resizable(False, False)
        self.grab_set()
        self.attributes("-alpha", opacity)
        #self.attributes("-topmost", True)

        # Make the window non-modal
        #self.transient(master)  # Set the main window as the parent for modality

        self.frame_1 = ctk.CTkFrame(master=self)
        self.frame_1.pack(pady=0, padx=0, fill="both", expand=True)
        self.frame_1.grid_columnconfigure((5,6), weight=1)
        self.frame_1.grid_rowconfigure((2), weight=1)

        self.search_label = ctk.CTkLabel(self.frame_1, text="Найти:", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        if self.language != "Русский":
            self.search_label.configure(text="Search:")
        self.search_label.grid(row=1, column=1, padx=(20, 10), pady=(20, 8), sticky="nsew")
        self.search_entry = ctk.CTkEntry(self.frame_1, font=ctk.CTkFont(family="Trebuchet MS", size=13, weight="bold"))
        self.search_entry.grid(row=1, column=2, padx=(0, 5), pady=(20, 8), sticky="nsew")
        self.search_entry.bind("<KeyRelease>", self.what_button)

        self.regex_toggled = False
        self.regex = ctk.CTkButton(self.frame_1, text="Cc", command=self.regex_event, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), width = 30, text_color=("gray14", "gray84"), font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.regex.grid(row=1, column=3, padx=(0, 5), pady=(20, 8), sticky="nsew")
        self.exact_match_toggled = False
        self.exact_match = ctk.CTkButton(self.frame_1, text="W", command=self.exact_match_event, fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), width = 30, text_color=("gray14", "gray84"), font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        self.exact_match.grid(row=1, column=4, padx=(0, 5), pady=(20, 8), sticky="nsew")

        self.prev_button = ctk.CTkButton(self.frame_1, text="", command=self.prev_result,fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.up_image,)
        self.prev_button.grid(row=1, column=5, padx=(0, 5), pady=(20, 8), sticky="nsew")
        self.prev_button.configure(state="disabled")
        self.next_button = ctk.CTkButton(self.frame_1, text="", command=self.next_result,fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"), image=self.down_image)
        self.next_button.grid(row=1, column=6, padx=(0, 20), pady=(20, 8), sticky="nsew")
        self.next_button.configure(state="disabled")

        self.result_label = ctk.CTkLabel(self.frame_1, text="Ожидание ввода...", font=ctk.CTkFont(family="Trebuchet MS", size=14, weight="bold"))
        if self.language != "Русский":
            self.result_label.configure(text="Waiting for input...")
        self.result_label.grid(row=2, column=1, columnspan=6, padx=(20, 20), pady=(0, 5), sticky="nsew")

        self.update_position()
        self.bind("<Configure>", self.update_position)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(150, lambda: self.search_entry.focus_set())
        self.bind("<Escape>", lambda x: self._on_closing())
        self.search_entry.bind("<Delete>", lambda del_entr: self.search_entry.delete(0, "end"))

    def what_button(self, event):
        if event.keycode == 13 or event.keycode == 40:
            self.next_result()
        elif event.keycode == 38:
            self.prev_result()
        else:
            self.search()

    def _on_closing(self):
        self.clear_highlights()
        self.grab_release()
        self.destroy()

    def update_position(self, event=None):
        master_x = self.master_window.winfo_x()
        master_y = self.master_window.winfo_y()
        master_width = self.master_window.winfo_width()
        search_width = self.winfo_width()

        x = master_x + master_width - search_width
        y = master_y

        self.geometry(f"+{x}+{y}")

    def regex_event(self):
        if self.regex_toggled:
            self.regex.configure(fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"))
            self.regex_toggled = False
        else:
            self.regex.configure(fg_color="#1F538D", hover_color="#14375e")
            self.regex_toggled = True
        self.search()

    def exact_match_event(self):
        if self.exact_match_toggled:
            self.exact_match.configure(fg_color=("#e5e5e5", "#212121"), hover_color=("white", "#333333"))
            self.exact_match_toggled = False
        else:
            self.exact_match.configure(fg_color="#1F538D", hover_color="#14375e")
            self.exact_match_toggled = True
        self.search()

    def create_word_boundary_pattern(self, search_term, ignore_case=True):
        escaped_term = re.escape(search_term)
        if ignore_case:
            pattern_string = r"(?i)\b" + escaped_term + r"\b"  # (?i) включает игнорирование регистра
        else:
            pattern_string = r"\b" + escaped_term + r"\b"

        pattern = re.compile(pattern_string)
        return pattern

    def search(self, event=None):
        search_term = self.search_entry.get()
        if not search_term:
            self.results = []
            self.clear_highlights()
            if self.language == "Русский":
                self.result_label.configure(text="Ожидание ввода...")
            else:
                self.result_label.configure(text="Waiting for input...")
            self.next_button.configure(state="disabled", image=self.down_image)
            self.prev_button.configure(state="disabled", image=self.up_image)
            return
        self.clear_highlights()
        self.results = []
        self.current_index = -1
        self.result_label.configure(text="")
        self.next_button.configure(state="disabled", image=self.down_image)
        self.prev_button.configure(state="disabled", image=self.up_image)
        text = self.textbox.get("1.0", "end")
        if self.exact_match_toggled == True and self.regex_toggled == False:
            pattern = self.create_word_boundary_pattern(search_term)
        elif self.regex_toggled == True and self.exact_match_toggled == True:
            pattern = self.create_word_boundary_pattern(search_term, ignore_case=False)
        elif self.regex_toggled and self.exact_match_toggled == False:
            pattern = re.compile(re.escape(search_term))
        else:
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        for match in pattern.finditer(text):
            start = match.start()
            end = match.end()
            start_index = self.textbox.index(f"1.0 + {start} chars")
            end_index = self.textbox.index(f"1.0 + {end} chars")
            self.results.append((start_index, end_index))
        if self.results:
            self.current_index = 0
            self.highlight_all_result()
            self.spec_clear()
            self.highlight_result()
            self.update_navigation_buttons()
            self.update_result_label()
        else:
            if self.language == "Русский":
                self.result_label.configure(text="Совпадений не найдено!")
            else:
                self.result_label.configure(text="No matches found!")


    def next_result(self):
        if self.results:
            #self.clear_highlights()
            self.current_index = (self.current_index + 1) % len(self.results)
            self.highlight_all_result()
            self.spec_clear()
            self.highlight_result()
            self.update_navigation_buttons()
            self.update_result_label()

    def prev_result(self):
        if self.results:
            #self.clear_highlights()
            self.current_index = (self.current_index - 1) % len(self.results)
            self.highlight_all_result()
            self.spec_clear()
            self.highlight_result()
            self.update_navigation_buttons()
            self.update_result_label()

    def highlight_result(self):
        if self.results:
            start_index, end_index = self.results[self.current_index]
            self.textbox.tag_add("highlight", start_index, end_index)
            self.textbox.tag_config("highlight", background="#de710b")
            self.textbox.see(start_index)

    def highlight_all_result(self):
        if self.results:
            for i in range(len(self.results)):
                start_index, end_index = self.results[i]
                self.textbox.tag_add("highlight2", start_index, end_index)
                self.textbox.tag_config("highlight2", background="#1F538D")

    def clear_highlights(self):
        self.textbox.tag_remove("highlight", "1.0", "end")
        self.textbox.tag_remove("highlight2", "1.0", "end")

    def spec_clear(self):
        start_index, end_index = self.results[self.current_index]
        self.textbox.tag_remove("highlight2", start_index, end_index)

    def update_navigation_buttons(self):
        if self.results:
            print(self.theme)
            if self.theme == "Dark" or self.theme == "Темная":
                self.next_button.configure(state="normal", image=self.down_active_image)
                self.prev_button.configure(state="normal", image=self.up_active_image)
            elif self.theme == "Light" or self.theme == "Светлая":
                self.next_button.configure(state="normal", image=self.down_active_light_image)
                self.prev_button.configure(state="normal", image=self.up_active_light_image)
        else:
            self.next_button.configure(state="disabled", image=self.down_image)
            self.prev_button.configure(state="disabled", image=self.up_image)

    def update_result_label(self):
        if self.results:
            result_number = self.current_index + 1
            total_results = len(self.results)
            if self.language == "Русский":
                self.result_label.configure(text=f"Найдено: {result_number} из {total_results}")
            else:
                self.result_label.configure(text=f"Found: {result_number} of {total_results}")

    def get(self):
        self.master.wait_window(self)
        kostil = 1
        return kostil