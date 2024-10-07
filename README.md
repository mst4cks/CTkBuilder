# 🏗️ CTkBuilder: A JSON-Driven CustomTkinter GUI Builder

## 📜 Description
CTkBuilder is a customizable framework built on top of CustomTkinter, allowing users to define widgets and layouts using JSON files. The builder automates the process of window configuration, widget creation, layout management, and applying specific settings for different operating systems like Windows.

## ⭐ Features
- Widget layout and properties are defined using JSON.
- Automatically binds commands and event handlers to widgets.
- Supports multiple widget types like buttons, labels, frames, sliders, etc.
- Flexible layout with both grid and absolute positioning.
- Easy to extend with new widgets or custom commands.
- Update theme for all widgets dynamically.
- Themes profiles can be defined using JSON

## 🛠 Installation
- Clone the repository:
```bash
   git clone https://github.com/mst4cks/CTkBuilder.git
   cd ctkbuilder
   pip install -r requirements.txt
   ```

- Install with pip:
``` bash
   pip install ctkbuilder
   ```   

## 📦 Usage

- Widgets json configuration example (for example `widgets.json`):
```json
   {
     "widgets": [
       {
         "type": "button",
         "name": "submit_button",
         "text": "Submit",
         "row": 0,
         "column": 1,
         "command": "submit_form"
       },
       {
         "type": "label",
         "name": "welcome_label",
         "text": "Welcome to CTkBuilder",
         "row": 0,
         "column": 0
       }
     ]
   }
   ```

- Main App json configuration example :
```json
   {
     "geometry": "800x600",
     "title": "My Application",
     "resize_width": true,
     "resize_height": true,
     "opacity": 0.8
   }
```

- Themes json configuration example:
```json
 {
    "themes": [
        {
            "name": "light_theme",
            "bg_color": "#ffffff",
            "fg_color": "#000000",
            "hover_color": "#cccccc",
            "text_color": "#333333"
        },
        {
            "name": "dark_theme",
            "bg_color": "#333333",
            "fg_color": "#ffffff",
            "hover_color": "#555555",
            "text_color": "#cccccc"
        },
        {
            "name": "blue_theme",
            "bg_color": "#e0f7fa",
            "fg_color": "#00796b",
            "hover_color": "#80deea",
            "text_color": "#004d40"
        }
    ]
}
   
```
- App example:
 ```python
   from ctkbuilder import CTkBuilder
   import customtkinter as ctk

   def test_command():
       print("Button pressed!")

   app = ctk.CTk()
   builder = CTkBuilder(app, 'config.json')
   builder.build_widgets()
   builder.apply_theme('dark', 'themes.json') # set a custom global theme
   app.mainloop()
   ```

## 🪟 Advanced Configuration for Windows

- **minimize_status**: Control the minimize button's behavior.
- **maximize_status**: Control the maximize button's behavior.
- **opacity**: Set window opacity (0 to 1).
- **bar_color**: Set the color of the title bar.
- **border_color**: Set the color of the window border.
- **title_style**: Customize the title text style.


## 🛠️ Key Methods for Application Development

The following methods are essential for creating and customizing applications using the `CTkBuilder` class:

1. **`build_widgets(self)`**  
   This method creates all the widgets defined in the JSON file and adds them to the graphical interface. It is fundamental for building the UI.

2. **`create_widget(self, widget_info)`**  
   Creates an individual widget based on the details provided in the JSON (widget type, positioning, and configuration options). It is used by `build_widgets` to handle each widget.

3. **`toggle_widget_state(self, widget_name, state)`**  
   Changes the state of widgets (e.g., enabled or disabled). This is useful for dynamically controlling the interface based on user interaction or application state.

4. **`preconfig_app(self, json_config)`**  
   Pre-configures the application settings, such as window size, title, and resizing options, using a JSON file. This is useful for initial window setup.

5. **`apply_theme(self, theme_name, theme_file)`**  
   Applies a custom theme to the interface. This allows dynamic changes to the UI styles (colors, text styles, etc.) from a JSON file that defines the themes.

6. **`save_state(self)`**  
   Saves the current states of the widgets, such as text in `Entry` fields or the state of `CheckBox` and `Switch` widgets. Useful for applications that need to preserve user input between sessions.

7. **`load_state(self)`**  
   Loads the saved states of widgets, allowing the restoration of the interface to a previously saved state. This can restore form inputs, selections, and other widget data.


## 🐛 Issues

If you encounter any problems while using the project, please report them on the [Issues](https://github.com/mst4cks/CTkBuilder/issues) page of this repository.


## 💬 Contributions

If you'd like to contribute to the project, please fork the repository, create a feature branch, and submit a pull request with your improvements.

## 🌀 Other
The project is still under development!

## ⚖️ License

This project is licensed under the MIT License.
