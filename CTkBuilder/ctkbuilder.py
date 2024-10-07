import customtkinter as ctk
import json
import sys
if sys.platform.startswith("win"):
    try:
        import hPyT  
    except ImportError:
        print("hPyT module not found. Please ensure it's installed.")
        hPyT = None  
else:
    print(f"Your system {sys.platform} is not supported for this module.")
    hPyT = None 

        



class CTkBuilder:
    def __init__(self, master, json_file):
        self.json_file = json_file
        self.master = master
        self.styles = hPyT
        self.widgets = []
        self.widget_dict = {}
        self.widget_states = {}
        self.flexible_layouts = {}
        
        # widgets type dictionary
        self.widgets_map = {
            "frame": ctk.CTkFrame,
            "scrollableframe": ctk.CTkScrollableFrame,
            "button": ctk.CTkButton,
            "checkbox": ctk.CTkCheckBox,
            "entry": ctk.CTkEntry,
            "label": ctk.CTkLabel,
            "scrollbar": ctk.CTkScrollbar,
            "switch": ctk.CTkSwitch,
            "slider": ctk.CTkSlider,
            "combobox":ctk.CTkComboBox,
            "textbox": ctk.CTkTextbox,
            "tabview": ctk.CTkTabview,
            "inputdialog": ctk.CTkInputDialog,
            "optionmenu": ctk.CTkOptionMenu,
            "segmentedbutton": ctk.CTkSegmentedButton,
            "canvas": ctk.CTkCanvas
        }
        # load json file
        with open(json_file, 'r') as file:
            self.json_data = json.load(file)
            
    # configure complex layout for frames       
    def configure_flexible_layout(self, widget_info):
        rows = widget_info.get("rows", {})
        columns = widget_info.get("columns", {})
        
        for row, weight in rows.items():
            self.master.grid_rowconfigure(row, weight=weight)

        for column, weight in columns.items():
            self.master.grid_columnconfigure(column, weight=weight)
     
    
    def build_widgets(self):
        for key, value in self.json_data.items():
            if isinstance(value, list):
                self.build_from_options(value)
            else:
                print((f"Unknown json structure: {key} -> {value}"))
    
    def build_from_options(self, widget_list):
        for widget_info in widget_list:
            widget_type = widget_info.get("type", "").lower()
            if widget_type in self.widgets_map:
                widget = self.create_widget(widget_info)
                self.auto_bind(widget, widget_info)
    
   
        
        
    # create widget /widgets from options
    def create_widget(self, widget_info):
        widget_type = widget_info["type"].lower()
        widget_class = self.widgets_map[widget_type]

        # Placement variables
        row = widget_info.pop("row", None)
        column = widget_info.pop("column", None)
        padx = widget_info.pop("padx", None)
        pady = widget_info.pop("pady", None)
        sticky = widget_info.pop("sticky", None)
        x = widget_info.pop("x", None)
        y = widget_info.pop("y", None)
        
        all_options = {key: value for key, value in widget_info.items() if key not in ["type", "name", "master"]}
        widget_root = self.widget_dict.get(widget_info.get("master")) if widget_info.get("master") else self.master
        widget = widget_class(widget_root, **all_options)
        
        # for advanced grid layout
        if "rows" in widget_info or "columns" in widget_info:
            self.configure_flexible_layout(widget_info)
            
            
        # Place widgets
        if row is not None and column is not None:
            widget.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        elif x is not None and y is not None:
            widget.place(x=x, y=y)
        else:
            widget.pack()

        # format command string and call function
        if "command" in widget_info:
            command_name = widget_info.pop("command")
            if hasattr(widget_root, command_name):
                widget.configure(command=getattr(widget_root, command_name))
            elif hasattr(self.master, command_name):
                widget.configure(command=getattr(self.master, command_name))
            else:
                print(f"Warning: Command '{command_name}' is not defined in {widget_root}")

        # save all widgets in dictionary
        name = widget_info.get("name", None)
        if name:
            self.widget_dict[name] = widget
        self.widgets.append(widget)

        return widget


    # use binds from json file
    def auto_bind(self, widget, widget_info):
        binds = widget_info.get("binds", None)
        if binds:
            for event, command_name in binds.items():
                if hasattr(self, command_name):
                    widget.bind(event, getattr(self, command_name))
    
    # create binds for widgets manually             
    def create_bind(self, name, event, command):
        if name in self.widget_dict:
            widget = self.widget_dict[name]
            widget.bind(event, lambda e: command())
    
    # set the state of your widgets
    def toggle_widget_state(self, widget_name, state):
        if widget_name in self.widget_dict:
            self.widget_dict[widget_name].configure(state=state)
    
    
    def save_state(self):
        self.widget_states = {}
        for widget_name, widget in self.widget_dict.items():
            if isinstance(widget, ctk.CTkEntry):
                self.widget_states[widget_name] = widget.get()# Save the text from entry
            elif isinstance(widget, ctk.CTkCheckBox):
                self.widget_states[widget_name] = widget.get()  # Save the checkbox state
            elif isinstance(widget, ctk.CTkSwitch):
                self.widget_states[widget_name] = widget.get()
    
              
    def load_state(self):
        if not self.widget_states:
            print("No saved state found in memory")
            return

        for widget_name, value in self.widget_states.items():
            if widget_name in self.widget_dict:
                widget = self.widget_dict[widget_name]
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, 'end')  # Clear existing text
                    widget.insert(0, value)  # Restore saved text
                elif isinstance(widget, ctk.CTkCheckBox):
                    widget.select() if value else widget.deselect()
                elif isinstance(widget, ctk.CTkSwitch):
                    widget.select() if value else widget.deselect()      
    
    
    def preconfig_app(self, json_config):
        
        with open(json_config, 'r') as config:
            config_data = json.load(config)
            
        # settings which work with all os    
        geometry = config_data.get("geometry")  
        self.master.geometry(geometry)
        title = config_data.get("title")
        self.master.title(title)
        overrideredirect_status = config_data.get("overriderredirect")
        self.master.overrideredirect(overrideredirect_status)
        resize_width = config_data.get("resize_width")
        resize_height = config_data.get("resize_height")
        self.master.resizable(resize_width, resize_height)
        
        
        
        #settings which are only for windows
        if sys.platform.startswith("win"):
            
            minimize_status = config_data.get("minimize_status", False)
            if minimize_status:
                self.styles.minimize_button.disable(self.master)
            
            maximize_status = config_data.get("maximize_status")
            if maximize_status:
                self.styles.maximize_button.disable(self.master)
            
            hide_resize_btn = config_data.get("min_max_status")
            if hide_resize_btn:
                self.styles.maximize_minimize_button.hide(self.master)
            
            hide_all = config_data.get("hide_all", False)
            if hide_all:
                self.styles.all_stuffs.hide(self.master)
            
            rainbow_bar = config_data.get("rainbow_bar")
            if rainbow_bar:
                self.styles.rainbow_title_bar.start(self.master, rainbow_bar)
            
            rainbow_border = config_data.get("rainbow_border")
            if rainbow_border:
                self.styles.rainbow_border.start(self.master, rainbow_border)
                
            opacity = config_data.get("opacity")
            if opacity is not None:
                self.styles.opacity.set(self.master, opacity)  
            
            bar_color = config_data.get("bar_color")
            if bar_color:
                self.styles.title_bar_color.set(self.master)
        
            border_color = config_data.get("border_color")
            if border_color:
                self.styles.border_color.set(border_color)
            
            title_style = config_data.get("title_style")
            if title_style:
                self.styles.title_text.stylize(self.master, style=title_style)
                
            centered_app = config_data.get("centered")
            if centered_app:
                self.styles.window_frame.center(self.master)
        
        
        else:
            print(f"Your system {sys.platform} don't allow those arguments")
            self.master.destroy()
        
    # Change dynamic all widgets
    def apply_theme(self, theme_name, theme_file):
        
        with open(theme_file, 'r') as file:
            themes_data = json.load(file)
            
        selected_theme = None
        for theme in themes_data.get("themes", []):
            if theme["name"].lower() == theme_name.lower():
                selected_theme = theme
                break
        
        if not selected_theme:
            print(f"Theme '{theme_name}' was not found in the file {theme_file}")
            return
        
        
        for widget_name, widget in self.widget_dict.items():
            # Update for CTkButton
            if isinstance(widget, ctk.CTkButton):
                widget.configure(
                    bg_color=selected_theme.get("bg_color", None),
                    fg_color=selected_theme.get("fg_color", None),
                    hover_color=selected_theme.get("hover_color", None),
                    text_color=selected_theme.get("text_color", None)
                )
            # Update for CTkLabel
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(
                    bg_color=selected_theme.get("bg_color", None),
                    text_color=selected_theme.get("text_color", None)
                )
            # Update for CTkEntry
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(
                    bg_color=selected_theme.get("bg_color", None),
                    text_color=selected_theme.get("text_color", None)
                )
            # Update for CTkCheckBox
            elif isinstance(widget, ctk.CTkCheckBox):
                widget.configure(
                    fg_color=selected_theme.get("fg_color", None),
                    text_color=selected_theme.get("text_color", None)
                )
            # Update for CTkSwitch
            elif isinstance(widget, ctk.CTkSwitch):
                widget.configure(
                    fg_color=selected_theme.get("fg_color", None),
                    text_color=selected_theme.get("text_color", None)
                )
            # Update for CTkSlider
            elif isinstance(widget, ctk.CTkSlider):
                widget.configure(
                    fg_color=selected_theme.get("fg_color", None)
                )
            # Update for other widget types as needed
            elif isinstance(widget, ctk.CTkComboBox):
                widget.configure(
                    fg_color=selected_theme.get("fg_color", None)
            
                 )
              
        