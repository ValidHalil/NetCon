
class AnimateButtonHover:
    def __init__(self, root):
        self.root = root

    # Инициализация локальных переменных состояния
    def init_hover_state(self, widget):
        widget.stop_flag = False
        widget.last_mode = ""
        widget.counter = 0

    # Анимация медленного изменения цвета кнопок
    def animate_hover(self, widget, start, end, step, delay, mode, upper=False):
        if widget.counter < 1:
            widget.last_mode = mode
        value = start
        stop_animation = False
        if not upper:
            if value > end and mode == "down" and  widget.cget("state") != "disabled":
                value -= step
                widget.counter += 1
            elif value < end and mode == "up" and not widget.stop_flag and widget.cget("state") != "disabled":
                value += step
            else:
                stop_animation = True
        else:
            if value > end and mode == "down" and not widget.stop_flag and widget.cget("state") != "disabled":
                value -= step
            elif value < end and mode == "up" and widget.cget("state") != "disabled":
                value += step
                widget.counter += 1
            else:
                stop_animation = True
        if not stop_animation:
            widget.configure(fg_color=f"#{value:06x}")
            if not upper:
                self.root.after(delay, lambda: self.animate_hover(widget, value, end, step, delay, mode))
            else:
                self.root.after(delay, lambda: self.animate_hover(widget, value, end, step, delay, mode, upper=True))
        else:
            widget.counter = 0

    # Для фикса срабатывания биндов текст лейбла внутри кнопки
    def stop_leave(self, widget):
        widget.stop_flag = True

    # Для фикса срабатывания биндов текст лейбла внутри кнопки
    def go_leave(self, widget, current_color, hover_color, step, upper=False):
        widget.stop_flag = False
        if not upper:
            widget.last_mode = "down"
            widget.unbind("<Enter>")
            self.root.after(200, lambda: widget.bind("<Enter>", lambda e: self.animate_hover(widget, int(current_color, 16), int(hover_color, 16), int(step, 16), 10, "down")))
        else:
            widget.last_mode = "up"
            widget.unbind("<Enter>")
            self.root.after(200,lambda: widget.bind("<Enter>", lambda e: self.animate_hover(widget, int(current_color, 16), int(hover_color, 16), int(step, 16), 10, "up", upper=True)))

    # От залипания хувера на слабых пк
    def check_color(self, widget, normal_color, hover_color, step, modal=False, upper=False):
        current = int(widget.cget("fg_color").replace("#", ""), 16)
        normal = int(normal_color, 16)
        if not upper:
            if current < normal and widget.last_mode == "down":
                if modal: delay = 0
                else: delay = 50
                self.root.after(delay, lambda: self.animate_hover(widget, int(hover_color, 16), int(normal_color, 16), int(step, 16), 10, "up"))
                widget.last_mode = "up"
        else:
            if current > normal and widget.last_mode == "up":
                if modal: delay = 0
                else: delay = 50
                self.root.after(delay, lambda: self.animate_hover(widget, int(hover_color, 16), int(normal_color, 16), int(step, 16), 10, "down", upper=True))
                widget.last_mode = "down"
