import os
import pyperclip
from ui.kroma import Window, TextBox, Label, Button, MessageBox, Color, CheckBox, FileDialog, Anchor
from services.code_collector import CodeCollectorService

class Application(Window):
    def _on_construct(self):
        self.set_title("Source Code Extractor")
        self.set_size(475, 414)
        self.set_resizable(False)

        self.collector_service = CodeCollectorService(
            ignore_folders={".git", ".vs", ".vscode", "bin", "build", "dist", "node_modules", "obj", "platform"},
            ignore_relative_paths=set()
        )

        self._build_ui()

    def _build_ui(self):
        lbl_path = Label()
        lbl_path.set_text("Absolute project path:")
        lbl_path.set_position(40, 20)
        self.add_widget(lbl_path)

        self.txt_path = TextBox()
        self.txt_path.set_size(52, 1)
        self.txt_path.set_position(40, 50)
        self.txt_path.set_placeholder("E.g.: D:\\Development\\Project")
        self.add_widget(self.txt_path)

        btn_browse = Button()
        btn_browse.set_text("Browse")
        btn_browse.set_size(10, 1)
        btn_browse.set_position(365, 48)
        btn_browse.set_event(self._on_browse_click)
        self.add_widget(btn_browse)

        lbl_ext = Label()
        lbl_ext.set_text("Extensions to include in collection:")
        lbl_ext.set_position(40, 95)
        self.add_widget(lbl_ext)

        self.ext_checkboxes = {}
        extensions = [".cs", ".css", ".html", ".js", ".json", ".py", ".sql", ".ts"]
        start_x, start_y = 40, 125
        x_offset, y_offset = 80, 25
        
        for i, ext in enumerate(extensions):
            row = i // 4
            col = i % 4
            cb = CheckBox()
            cb.set_text(ext)
            cb.set_position(start_x + (col * x_offset), start_y + (row * y_offset))
            
            # Default checked extensions
            if ext in [".cs"]: 
                cb.set_checked(True)
                
            self.add_widget(cb)
            self.ext_checkboxes[ext] = cb

        lbl_adv = Label()
        lbl_adv.set_text("Advanced: Specific paths to ignore (comma-separated):")
        lbl_adv.set_position(40, 200)
        self.add_widget(lbl_adv)

        self.txt_ignored = TextBox()
        self.txt_ignored.set_size(65, 1)
        self.txt_ignored.set_position(40, 230)
        self.txt_ignored.set_placeholder("E.g.: backend/logs, backend/tests")
        self.add_widget(self.txt_ignored)

        self.lbl_status = Label()
        self.lbl_status.set_text("Ready for extraction.")
        self.lbl_status.set_foreground_color(Color.GRAY)
        self.lbl_status.set_position(40, 290)
        self.add_widget(self.lbl_status)

        btn_collect = Button()
        btn_collect.set_text("Copy")
        btn_collect.set_size(25, 1)
        btn_collect.set_anchor(Anchor.TOP)
        btn_collect.set_position(0, 350)
        btn_collect.set_event(self._on_collect_click)
        self.add_widget(btn_collect)

    def _on_browse_click(self):
        path = FileDialog.ask_directory("Select the project folder")
        if path:
            self.txt_path.set_text(os.path.normpath(path))

    def _on_collect_click(self):
        path = self.txt_path.get_text().strip()
        
        selected_exts = [ext for ext, cb in self.ext_checkboxes.items() if cb.get_checked()]
        
        ignored_raw = self.txt_ignored.get_text().strip()
        custom_ignored = [p.strip() for p in ignored_raw.split(",") if p.strip()] if ignored_raw else []

        if not path:
            MessageBox.show_warning("Please fill in the project path.")
            return

        if not selected_exts:
            MessageBox.show_warning("Please select at least one extension from the matrix.")
            return

        self.lbl_status.set_text("Reading files, please wait...")
        self.lbl_status.set_foreground_color(Color.ORANGE)
        self.get_id().update()

        try:
            combined_code = self.collector_service.collect(path, selected_exts, custom_ignored)

            if not combined_code.strip():
                self.lbl_status.set_text("No files found.")
                self.lbl_status.set_foreground_color(Color.RED)
                MessageBox.show_info("No files found with the current settings.")
                return

            pyperclip.copy(combined_code)
            
            self.lbl_status.set_text("Code successfully extracted and copied!")
            self.lbl_status.set_foreground_color(Color.GREEN)
            MessageBox.show_info("Files successfully copied to clipboard!")

        except Exception as e:
            self.lbl_status.set_text("Error during extraction.")
            self.lbl_status.set_foreground_color(Color.RED)
            MessageBox.show_error(f"Operation failed:\n{str(e)}")