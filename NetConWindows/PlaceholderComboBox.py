import updated_ctk as ctk

class PlaceholderComboBox(ctk.CTkComboBox):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(master, **kwargs)
        self._variable = None
        self.placeholder_text = placeholder_text
        self.is_placeholder = True
        self.is_focused = False
        #self.configure(values=[placeholder_text] + values)
        self.set(placeholder_text)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.configure(text_color = ("gray52", "gray62"))

    def on_focus_in(self, event):
        self.is_focused = True
        if self.is_placeholder:
            self.set("")
            self.configure(text_color = ("gray14", "gray84"))
            self.is_placeholder = False

    def on_focus_out(self, event):
        self.is_focused = False
        if self.get() == "":
            self.configure(text_color = ("gray52", "gray62"))
            self.set(self.placeholder_text)
            self.is_placeholder = True

    def set_placeholder(self):
        self.configure(text_color=("gray52", "gray62"))
        self.set(self.placeholder_text)
        self.is_placeholder = True
        
    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            self._create_grid()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
            require_redraw = True

        if "button_color" in kwargs:
            self._button_color = self._check_color_type(kwargs.pop("button_color"))
            require_redraw = True

        if "button_hover_color" in kwargs:
            self._button_hover_color = self._check_color_type(kwargs.pop("button_hover_color"))
            require_redraw = True

        if "dropdown_fg_color" in kwargs:
            self._dropdown_menu.configure(fg_color=kwargs.pop("dropdown_fg_color"))

        if "dropdown_hover_color" in kwargs:
            self._dropdown_menu.configure(hover_color=kwargs.pop("dropdown_hover_color"))

        if "dropdown_text_color" in kwargs:
            self._dropdown_menu.configure(text_color=kwargs.pop("dropdown_text_color"))

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True

        if "text_color_disabled" in kwargs:
            self._text_color_disabled = self._check_color_type(kwargs.pop("text_color_disabled"))
            require_redraw = True

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "dropdown_font" in kwargs:
            self._dropdown_menu.configure(font=kwargs.pop("dropdown_font"))

        if "values" in kwargs:
            self._values = kwargs.pop("values")
            self._dropdown_menu.configure(values=self._values)

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._entry.configure(state=self._state)
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "variable" in kwargs:
            self._variable = kwargs.pop("variable")
            self._entry.configure(textvariable=self._variable)

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "justify" in kwargs:
            self._entry.configure(justify=kwargs.pop("justify"))

        if "placeholder_text" in kwargs:
            self.placeholder_text = kwargs.pop("placeholder_text")
            self.set(self.placeholder_text)


        super().configure(require_redraw=require_redraw, **kwargs)