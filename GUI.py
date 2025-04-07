import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from pathlib import Path
from executor import TestExecutor
from logger import HTMLReportGenerator
from utils import load_translation_table, generate_code_from_testcase
from config.settings import DEFAULT_TESTCASE_PATH, TRANSLATION_TABLE_PATH
import os  # Import the os module

class TestCaseGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("BugZero - Selenium Test Automation")
        self.root.geometry("900x700")

        # Set BugZero theme colors
        self.primary_color = "#2C3E50"  # Dark blue
        self.secondary_color = "#E74C3C"  # Red
        self.accent_color = "#3498DB"  # Light blue
        self.bg_color = "#ECF0F1"  # Light gray

        self.root.configure(bg=self.bg_color)

        # Initialize components
        self.test_cases = []
        self.test_case_file = None
        self.translation_table = load_translation_table(TRANSLATION_TABLE_PATH)

        # Create header frame
        self._create_header()

        # UI Elements
        self._create_widgets()

        # Add version info
        self._create_footer()

    def _create_header(self):
        """Create the header with BugZero branding"""
        header_frame = tk.Frame(self.root, bg=self.primary_color)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        # BugZero logo (text-based)
        logo_label = tk.Label(
            header_frame,
            text="BugZero",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg=self.primary_color
        )
        logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Tagline
        tagline_label = tk.Label(
            header_frame,
            text="Selenium Test Automation Framework",
            font=("Helvetica", 10),
            fg="white",
            bg=self.primary_color
        )
        tagline_label.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_footer(self):
        """Create footer with version info"""
        footer_frame = tk.Frame(self.root, bg=self.primary_color)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        version_label = tk.Label(
            footer_frame,
            text="BugZero v1.0 | © 2023 BugZero All Rights Reserved",
            font=("Helvetica", 8),
            fg="white",
            bg=self.primary_color
        )
        version_label.pack(pady=3)

    def _create_widgets(self):
        """Create and arrange all GUI widgets"""
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Test Case Name
        name_frame = tk.Frame(main_frame, bg=self.bg_color)
        name_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            name_frame,
            text="Test Case Name:",
            bg=self.bg_color,
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)

        self.test_case_name_entry = tk.Entry(
            name_frame,
            width=60,
            font=("Helvetica", 10)
        )
        self.test_case_name_entry.pack(side=tk.LEFT, padx=5)

        # Command Selection
        command_frame = tk.Frame(main_frame, bg=self.bg_color)
        command_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            command_frame,
            text="Command:",
            bg=self.bg_color,
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)

        self.command_var = tk.StringVar()
        self.command_dropdown = ttk.Combobox(
            command_frame,
            textvariable=self.command_var,
            values=sorted(self.translation_table.keys()),
            state="readonly",
            width=25,
            font=("Helvetica", 10)
        )
        self.command_dropdown.pack(side=tk.LEFT, padx=5)
        self.command_var.trace('w', self._update_input_fields)

        # Dynamic Fields Frame
        self.fields_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.fields_frame.pack(fill=tk.X, pady=10)

        # Steps Listbox with Scrollbar
        list_container = tk.Frame(main_frame, bg=self.bg_color)
        list_container.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(
            list_container,
            text="Test Steps:",
            bg=self.bg_color,
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W)

        list_inner_frame = tk.Frame(list_container, bg=self.bg_color)
        list_inner_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_inner_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.steps_listbox = tk.Listbox(
            list_inner_frame,
            yscrollcommand=scrollbar.set,
            width=100,
            height=15,
            selectbackground=self.accent_color,
            selectforeground="white",
            font=("Courier", 9),
            bg="white",
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.steps_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.steps_listbox.yview)

        # Buttons Frame
        self.button_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.button_frame.pack(fill=tk.X, pady=10)

        button_style = {
            'bg': self.primary_color,
            'fg': 'white',
            'activebackground': self.accent_color,
            'activeforeground': 'white',
            'font': ("Helvetica", 10),
            'relief': tk.RAISED,
            'borderwidth': 2
        }

        buttons = [
            ("Add Step", self._add_step),
            ("Remove Selected", self._remove_step),
            ("Generate Test Case", self._generate_test_case),
            ("Import Test Cases", self._import_test_cases),
            ("Execute Test", self._execute_test)
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.button_frame,
                text=text,
                command=command,
                **button_style
            )
            btn.pack(side=tk.LEFT, padx=5, ipadx=5, ipady=3)

            if text == "Execute Test":
                self.execute_button = btn
                btn.config(state=tk.DISABLED)

    def _update_input_fields(self, *args):
        """Update input fields based on selected command"""
        # Clear previous fields
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        command = self.command_var.get()
        template = self.translation_table.get(command, "")

        # Add fields based on template placeholders
        if '{locator}' in template:
            tk.Label(self.fields_frame, text="Locator:", bg=self.bg_color, font=("Helvetica", 10)).pack(side=tk.LEFT)
            self.locator_entry = tk.Entry(self.fields_frame, width=40, font=("Helvetica", 10))
            self.locator_entry.pack(side=tk.LEFT, padx=5)

        if '{value}' in template or '{url}' in template:
            label_text = "URL:" if command == "OpenURL" else "Value:"
            tk.Label(self.fields_frame, text=label_text, bg=self.bg_color, font=("Helvetica", 10)).pack(side=tk.LEFT)
            self.value_entry = tk.Entry(self.fields_frame, width=30, font=("Helvetica", 10))
            self.value_entry.pack(side=tk.LEFT, padx=5)

    def _add_step(self):
        """Add a new test step from the input fields"""
        command = self.command_var.get()
        if not command:
            messagebox.showwarning("Input Error", "Please select a command")
            return

        template = self.translation_table.get(command)
        locator = ""
        value = ""

        # Get locator if needed
        if '{locator}' in template:
            locator = getattr(self, 'locator_entry', tk.Entry()).get()
            if not locator:
                messagebox.showwarning("Input Error", "Locator is required for this command")
                return

        # Get value if needed
        if '{value}' in template or '{url}' in template:
            value = getattr(self, 'value_entry', tk.Entry()).get()
            if not value and command != "Click":  # Click can have empty value
                messagebox.showwarning("Input Error", "Value is required for this command")
                return

        # Add to steps list
        step_desc = f"{command}: {locator} {value}".strip()
        self.test_cases.append({
            'Command': command,
            'Locator': locator,
            'Value': value
        })
        self.steps_listbox.insert(tk.END, step_desc)

        # Clear inputs
        if hasattr(self, 'locator_entry'):
            self.locator_entry.delete(0, tk.END)
        if hasattr(self, 'value_entry'):
            self.value_entry.delete(0, tk.END)

    def _remove_step(self):
        """Remove selected step from the list"""
        selection = self.steps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a step to remove")
            return

        index = selection[0]
        self.steps_listbox.delete(index)
        del self.test_cases[index]

    def _generate_test_case(self):
        """Generate Excel test case file from current steps"""
        if not self.test_cases:
            messagebox.showwarning("Input Error", "No steps to generate test case")
            return

        test_case_name = self.test_case_name_entry.get()
        if not test_case_name:
            messagebox.showwarning("Input Error", "Please enter a test case name")
            return

        # Create DataFrame with steps
        df = pd.DataFrame([
            {'Step': idx+1, **step}
            for idx, step in enumerate(self.test_cases)
        ])

        # Save to Excel
        self.test_case_file = Path(f"{test_case_name}.xlsx")
        df.to_excel(self.test_case_file, index=False)

        messagebox.showinfo(
            "Success",
            f"Test case saved to {self.test_case_file}"
        )
        self.execute_button.config(state=tk.NORMAL)

    def _import_test_cases(self):
        """Import test cases from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Test Case File",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            self.test_cases = df.to_dict('records')

            # Update UI
            self.steps_listbox.delete(0, tk.END)
            for step in self.test_cases:
                step_desc = f"{step['Command']}: {step.get('Locator', '')} {step.get('Value', '')}".strip()
                self.steps_listbox.insert(tk.END, step_desc)

            self.test_case_file = Path(file_path)
            self.test_case_name_entry.delete(0, tk.END)
            self.test_case_name_entry.insert(0, self.test_case_file.stem)
            self.execute_button.config(state=tk.NORMAL)

            messagebox.showinfo("Success", "Test cases imported successfully")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import test cases: {str(e)}")

    def _execute_test(self):
        """Execute the current test case"""
        if not self.test_case_file:
            messagebox.showwarning("Execution Error", "No test case file loaded")
            return

        try:
            # Create test executor
            executor = TestExecutor()

            # Generate and execute script
            df = pd.DataFrame(self.test_cases)
            script_lines = generate_code_from_testcase(df, self.translation_table)
            results = executor.execute_script(script_lines)

            # Generate report
            HTMLReportGenerator.generate_report(script_lines, results)
            messagebox.showinfo("Execution Complete", "Test execution finished. Report generated.")

        except Exception as e:
            messagebox.showerror("Execution Error", f"Test execution failed: {str(e)}")
        finally:
            if hasattr(executor, 'close') and callable(executor.close):
                executor.close()

if __name__ == "__main__":
    root = tk.Tk()

    # Set window icon (replace with actual BugZero icon if available)
    try:
        # Construct the path to the icon file in the parent directory
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(parent_dir, "Bugzero.ico")
        root.iconbitmap(icon_path)
    except tk.TclError:
        pass  # Use default icon if custom icon not available

    app = TestCaseGenerator(root)

    # Center the window on screen
    window_width = 900
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.mainloop()