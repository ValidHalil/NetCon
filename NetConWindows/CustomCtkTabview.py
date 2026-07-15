import updated_ctk as ctk
from typing import Union, Tuple, Dict, List, Callable, Optional, Any

class CustomCTkTabview(ctk.CTkTabview):

    def __init__(self, *args, **kwargs):
        self._display_name_dict: Dict[str, str] = {}
        super().__init__(*args, **kwargs)
        self._segmented_button.configure(command=self._segmented_button_callback)

    def _generate_unique_display_name(self, display_name: str) -> str:
        if display_name not in self._display_name_dict.values():
            return display_name
        i = 1
        while True:
            new_display_name = f"{display_name} ({i})"
            if new_display_name not in self._display_name_dict.values():
                return new_display_name
            i += 1

    def add(self, name: str, display_name: Optional[str] = None) -> ctk.CTkFrame:
        display_name = display_name if display_name is not None else name
        display_name = self._generate_unique_display_name(display_name)
        self._display_name_dict[name] = display_name
        if name not in self._tab_dict:
            if len(self._tab_dict) == 0:
                self._set_grid_segmented_button()
            tab = self._create_tab()
            self._tab_dict[name] = tab
            self._name_list.append(name)
            self._segmented_button.configure(values=list(self._display_name_dict.values()))
            if len(self._tab_dict) == 1:
                self._current_name = name
                self._segmented_button.set(display_name)
                self._grid_forget_all_tabs()
                self._set_grid_current_tab()
            return tab
        else:
             raise ValueError(f"CTkTabview already has tab named '{name}'")

    def insert(self, index: int, name: str, display_name: Optional[str] = None) -> ctk.CTkFrame:
        display_name = display_name if display_name is not None else name
        display_name = self._generate_unique_display_name(display_name)
        self._display_name_dict[name] = display_name
        if name not in self._tab_dict:
            if len(self._tab_dict) == 0:
                self._set_grid_segmented_button()
            tab = self._create_tab()
            self._tab_dict[name] = tab
            self._name_list.insert(index, name)
            self._segmented_button.configure(values=list(self._display_name_dict.values())) # Передаём список отображаемых имен
            if len(self._tab_dict) == 1:
                self._current_name = name
                self._segmented_button.set(display_name)
                self._grid_forget_all_tabs()
                self._set_grid_current_tab()
            return tab
        else:
             raise ValueError(f"CTkTabview already has tab named '{name}'")

    def rename(self, old_name: str, new_name: str, display_name: Optional[str] = None):
        is_current = self._current_name == old_name  # Запоминаем, была ли вкладка активной
        if new_name != old_name:
            if new_name in self._tab_dict:
                raise ValueError(f"new_name '{new_name}' already exists")
            else:
                tab = self._tab_dict.pop(old_name)
                self._tab_dict[new_name] = tab
                index = self._name_list.index(old_name)
                self._name_list[index] = new_name
                if is_current:
                    self._current_name = new_name
        display_name = display_name if display_name is not None else new_name
        self._display_name_dict[old_name] = display_name
        self._segmented_button.configure(values=list(self._display_name_dict.values()))
        if is_current:
            self.set(new_name)

    def delete(self, name: str):
        if name in self._tab_dict:
            self._name_list.remove(name)
            self._tab_dict[name].grid_forget()
            self._tab_dict.pop(name)
            del self._display_name_dict[name]
            values = list(self._display_name_dict.values())
            self._segmented_button.configure(values=values)
            if len(self._name_list) == 0:
                self._current_name = ""
                self._segmented_button.grid_forget()
            elif len(self._name_list) == 1:
                self._current_name = self._name_list[0]
                self.set(self._current_name)
                self._grid_forget_all_tabs()
                self._set_grid_current_tab()
            else:
                if self._current_name == name:
                    self.set(self._name_list[0])
        else:
            raise ValueError(f"CTkTabview has no tab named '{name}'")

    def set(self, name: str):
      if name in self._tab_dict:
        self._current_name = name
        self._segmented_button.set(self._display_name_dict[name])
        self._set_grid_current_tab()
        self.after(100, lambda: self._grid_forget_all_tabs(exclude_name=name))
      else:
        raise ValueError(f"CTkTabview has no tab named '{name}'")

    def _segmented_button_callback(self, selected_name):  # Corrected method name
        # Find the internal name associated with the selected display name
        for internal_name, display_name in self._display_name_dict.items():
            if display_name == selected_name:
                selected_internal_name = internal_name
                break
        else:
            print(f"Warning: Internal name not found for display name {selected_name}")
            return
        self._tab_dict[self._current_name].grid_forget()
        self._current_name = selected_internal_name
        self._set_grid_current_tab()
        if self._command is not None:
            self._command()

    def tab(self, name: str) -> ctk.CTkFrame:
      if name in self._tab_dict:
          return self._tab_dict[name]
      else:
          raise ValueError(f"CTkTabview has no tab named '{name}'")