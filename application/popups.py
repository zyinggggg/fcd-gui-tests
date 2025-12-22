import json
import customtkinter as ctk
from customtkinter import filedialog
from diagnostics import register_log, diagnostics_path

class AdvancedPerformance(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Advanced Performance")
        self.geometry("800x450")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100, uniform="Silent_Creme")
        self.grid_columnconfigure(1, weight=100, uniform="Silent_Creme")

        self.frame0_row = 0
        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)

        self.frame1_row = 0
        self.frame1 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame1.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nsew", padx=(5, 10), pady=(10, 10))

        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(1, weight=1)

        for key, entry in parent.data.items():
            excluded_keys = {"pid_tuning_mode", "pid_overshoot_lbf","pid_overshoot_percent", "pid_settling_time_s", "pid_load_error_running_avg_percent"}
            if key in excluded_keys:
                continue
            if self.frame0_row <= 12:
                label = ctk.CTkLabel(master=self.frame0, text=entry["label"])
                label.grid(row=self.frame0_row, column=0, sticky="w", padx=10, pady=2)

                value = ctk.CTkLabel(master=self.frame0, text="0.00")
                value.grid(row=self.frame0_row, column=1, sticky="e", padx=10, pady=2)

                setattr(self, f"{key}_value", value)
                self.frame0_row += 1
            
            else:
                label = ctk.CTkLabel(master=self.frame1, text=entry["label"])
                label.grid(row=self.frame1_row, column=0, sticky="w", padx=10, pady=2)

                value = ctk.CTkLabel(master=self.frame1, text="0.00")
                value.grid(row=self.frame1_row, column=1, sticky="e", padx=10, pady=2)

                setattr(self, f"{key}_value", value)
                self.frame1_row += 1

class AdvancedSettings(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Advanced Settings")
        self.geometry("800x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0_row = 0
        self.frame0 = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=100, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(1, weight=45, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(2, weight=45, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(3, weight=45, uniform="Silent_Creme")

        for key, entry in parent.config.items():
            label = ctk.CTkLabel(master=self.frame0, text=key)
            label.grid(row=self.frame0_row, column=0, sticky="w", padx=10, pady=2)

            value = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
            value.grid(row=self.frame0_row, column=3, sticky="e", padx=10, pady=2)
            value.insert(0, entry)

            setattr(self, f"{key}_value", value)
            self.frame0_row += 1

        self.load_button = ctk.CTkButton(master=self.frame0, text="Load", command=self.load, width=121)
        self.load_button.grid(row=self.frame0_row, column=1, sticky="e", padx=0, pady=2)

        self.save_as_button = ctk.CTkButton(master=self.frame0, text="Save As", command=self.save_as, width=121)
        self.save_as_button.grid(row=self.frame0_row, column=2, sticky="e", padx=(0, 4), pady=2)

        self.configure_button = ctk.CTkButton(master=self.frame0, text="Configure", command=self.configure, width=121)
        self.configure_button.grid(row=self.frame0_row, column=3, sticky="e", padx=10, pady=2)
    
    def configure(self):
        config = self.parent.config
        for key in list(config.keys()):
            value = getattr(self, f"{key}_value").get().strip()
            if value:
                config[key] = value

        with open(self.parent.config_path, "w") as f:
            json.dump(self.parent.config, f, indent=4)

        self.destroy()
    
    def save_as(self):
        config_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON File", "*.json"), ("All Files", "*.*")],
            title="Save As:"
        )

        if config_path:
            with open(config_path, 'w') as f:
                json.dump(self.parent.config, f, indent=4)

    def load(self):
        config_path = filedialog.askopenfilename(
            title="Select a JSON File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )

        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                for key, value in loaded_config.items():
                    widget_name = f"{key}_value"
                    if hasattr(self, widget_name):
                        entry_widget = getattr(self, widget_name)
                        entry_widget.delete(0, "end")
                        entry_widget.insert(0, str(value))

            except (FileNotFoundError, json.JSONDecodeError):
                pass

class Maintenance(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Maintenance")
        self.geometry("400x100")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)
    
        self.r0_c0 = ctk.CTkLabel(master=self.frame0, text="Total Run Time (hh:mm:ss):")
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r0_c1 = ctk.CTkLabel(master=self.frame0, text="00:00:00")
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        self.r1_c0 = ctk.CTkLabel(master=self.frame0, text="Totel Rev:")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkLabel(master=self.frame0, text="0.00")
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

class Diagnostics(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Diagnostics")
        self.geometry("800x350")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0_row = 1
        self.frame0 = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=50, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(1, weight=30, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(2, weight=30, uniform="Silent_Creme")
        self.frame0.grid_columnconfigure(3, weight=100, uniform="Silent_Creme")

        self.datetime_label = ctk.CTkLabel(master=self.frame0, text="Date/Time")
        self.datetime_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.id_label = ctk.CTkLabel(master=self.frame0, text="ID")
        self.id_label.grid(row=0, column=1, sticky="w", padx=10, pady=2)

        self.source_label = ctk.CTkLabel(master=self.frame0, text="Source")
        self.source_label.grid(row=0, column=2, sticky="w", padx=10, pady=2)

        self.log_label = ctk.CTkLabel(master=self.frame0, text="Message")
        self.log_label.grid(row=0, column=3, sticky="w", padx=10, pady=2)

        register_log(self.add_log)
        self.load_existing_logs() # Load existing log entries from the file

    def add_log(self, datetime, id, source, msg):

        log_datetime_label = ctk.CTkLabel(self.frame0, text=datetime)
        log_datetime_label.grid(row=self.frame0_row, column=0, sticky="w", padx=10, pady=2)

        log_id_label = ctk.CTkLabel(self.frame0, text=id)
        log_id_label.grid(row=self.frame0_row, column=1, sticky="w", padx=10, pady=2)
        
        log_source_label = ctk.CTkLabel(self.frame0, text=source)
        log_source_label.grid(row=self.frame0_row, column=2, sticky="w", padx=10, pady=2)

        log_msg_label = ctk.CTkLabel(self.frame0, text=msg)
        log_msg_label.grid(row=self.frame0_row, column=3, sticky="w", padx=10, pady=2)

        self.frame0_row += 1

    def load_existing_logs(self):
        try:
            with open(diagnostics_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): #Check if the line becomes empty
                        continue # Skip empty lines/spaces
                    entry = json.loads(line.strip()) #Only call json.loads if line has actual content
                    self.add_log(entry["datetime"], entry["id"], entry["source"], entry["msg"])
        except (FileNotFoundError, json.JSONDecodeError):
            pass

class Firmware(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Firmware")
        self.geometry("600x350")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)
    
        self.r0_c0 = ctk.CTkLabel(master=self.frame0, text="Firmware Version:")
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        from main import version, release_date
        self.r0_c1 = ctk.CTkLabel(master=self.frame0, text=f"v{version} ({release_date})")
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=2)

        self.r1_c0 = ctk.CTkLabel(master=self.frame0, text="Repository URL:")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=300)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        self.r2_c0 = ctk.CTkLabel(master=self.frame0, text="Check for Updates:")
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkButton(master=self.frame0, text="↻", width=121)
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        self.r2_c1.bind("<Enter>", self.on_enter)
        self.r2_c1.bind("<Leave>", self.on_leave)

        self.check_for_updates()

    def on_enter(self, event):
        if self.r2_c1.cget("text") == "↻":
            self.r2_c1.configure(text="Up to Date")
        
    def on_leave(self, event):
        if self.r2_c1.cget("text") == "Up to Date":
            self.r2_c1.configure(text="↻")


class AdvancedControl(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Advanced Control")
        self.geometry("400x695")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)

        self.r0_c0 = ctk.CTkLabel(master=self.frame0, text="Main Commands", font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r1_c0 = ctk.CTkLabel(master=self.frame0, text='Halt Motors:')
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkButton(master=self.frame0, text="Halt", command=self.parent.sync.halt_motors, width=121)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        self.r2_c0 = ctk.CTkLabel(master=self.frame0, text='Rotate Rotary Motor:')
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkButton(master=self.frame0, text="↻ 90-deg", command=self.parent.sync.rotate_90deg_rotary_motor, width=121)
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        self.r3_c0 = ctk.CTkLabel(master=self.frame0, text='Return Rotary Motor to Home:')
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkButton(master=self.frame0, text="Go Home", command=self.parent.sync.go_home_rotary_motor, width=121)
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)

        self.r4_c0 = ctk.CTkLabel(master=self.frame0, text='Return Z-Axis Motors to Home:')
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkButton(master=self.frame0, text="Go Home", command=self.parent.sync.go_home_z_axis_motors, width=121)
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)
        
        self.r5_c0 = ctk.CTkLabel(master=self.frame0, text="Move Motors By", font=("Helvetica", 18, "bold"))
        self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r5_c1 = ctk.CTkSegmentedButton(master=self.frame0, values=["step", "in"], command=None)
        self.r5_c1.grid(row=5, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r5_c1.set("step")

        self.r6_c0 = ctk.CTkLabel(master=self.frame0, text="Rotary Motor (deg):")
        self.r6_c0.grid(row=6, column=0, sticky="w", padx=10, pady=2)

        self.r6_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r6_c1.grid(row=6, column=1, sticky="e", padx=10, pady=2)

        self.r7_c0 = ctk.CTkLabel(master=self.frame0, text="Right Z-Axis Motor:")
        self.r7_c0.grid(row=7, column=0, sticky="w", padx=10, pady=2)

        self.r7_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r7_c1.grid(row=7, column=1, sticky="e", padx=10, pady=2)

        self.r8_c0 = ctk.CTkLabel(master=self.frame0, text="Left Z-Axis Motor:")
        self.r8_c0.grid(row=8, column=0, sticky="w", padx=10, pady=2)

        self.r8_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r8_c1.grid(row=8, column=1, sticky="e", padx=10, pady=2)

        self.r9_c1 = ctk.CTkButton(master=self.frame0, text="Run", command=self.parent.sync.move_motors_by, width=121)
        self.r9_c1.grid(row=9, column=1, sticky="e", padx=10, pady=2)

        self.r10_c0 = ctk.CTkLabel(master=self.frame0, text="Move Motors To", font=("Helvetica", 18, "bold"))
        self.r10_c0.grid(row=10, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r10_c1 = ctk.CTkSegmentedButton(master=self.frame0, values=["step", "in"], command=None)
        self.r10_c1.grid(row=10, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r10_c1.set("step")

        self.r11_c0 = ctk.CTkLabel(master=self.frame0, text="Rotary Motor (deg):")
        self.r11_c0.grid(row=11, column=0, sticky="w", padx=10, pady=2)

        self.r11_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r11_c1.grid(row=11, column=1, sticky="e", padx=10, pady=2)

        self.r12_c0 = ctk.CTkLabel(master=self.frame0, text="Right Z-Axis Motor:")
        self.r12_c0.grid(row=12, column=0, sticky="w", padx=10, pady=2)

        self.r12_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r12_c1.grid(row=12, column=1, sticky="e", padx=10, pady=2)

        self.r13_c0 = ctk.CTkLabel(master=self.frame0, text="Left Z-Axis Motor:")
        self.r13_c0.grid(row=13, column=0, sticky="w", padx=10, pady=2)

        self.r13_c1 = ctk.CTkEntry(master=self.frame0, justify="right", width=121)
        self.r13_c1.grid(row=13, column=1, sticky="e", padx=10, pady=2)

        self.r14_c1 = ctk.CTkButton(master=self.frame0, text="Run", command=self.parent.sync.move_motors_to, width=121)
        self.r14_c1.grid(row=14, column=1, sticky="e", padx=10, pady=2)

        self.r15_c0 = ctk.CTkLabel(master=self.frame0, text="Set Motors Home", font=("Helvetica", 18, "bold"))
        self.r15_c0.grid(row=15, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r16_c0 = ctk.CTkLabel(master=self.frame0, text="Rotary Motor:")
        self.r16_c0.grid(row=16, column=0, sticky="w", padx=10, pady=2)

        self.r16_c1 = ctk.CTkButton(master=self.frame0, text="Set Home", command=self.parent.sync.set_home_rotary_motor, width=121)
        self.r16_c1.grid(row=16, column=1, sticky="e", padx=10, pady=2)

        self.r17_c0 = ctk.CTkLabel(master=self.frame0, text="Right Z-Axis Motor:")
        self.r17_c0.grid(row=17, column=0, sticky="w", padx=10, pady=2)

        self.r17_c1 = ctk.CTkButton(master=self.frame0, text="Set Home", command=self.parent.sync.set_home_right_z_axis_motor, width=121)
        self.r17_c1.grid(row=17, column=1, sticky="e", padx=10, pady=2)

        self.r18_c0 = ctk.CTkLabel(master=self.frame0, text="Left Z-Axis Motor:")
        self.r18_c0.grid(row=18, column=0, sticky="w", padx=10, pady=2)

        self.r18_c1 = ctk.CTkButton(master=self.frame0, text="Set Home", command=self.parent.sync.set_home_left_z_axis_motor, width=121)
        self.r18_c1.grid(row=18, column=1, sticky="e", padx=10, pady=2)

class VariableSelection(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("Variable Selection")
        self.geometry("800x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100, uniform="Silent_Creme")
        self.grid_columnconfigure(1, weight=100, uniform="Silent_Creme")

        self.frame0_row = 0
        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame1_row = 0
        self.frame1 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame1.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nsew", padx=(5, 10), pady=(10, 10))

        for key, entry in parent.data.items():
            if self.frame0_row <= 12:
                switch = ctk.CTkSwitch(master=self.frame0, text=entry["label"], command=lambda k=key: self.update_variable_selection(k))
                switch.grid(row=self.frame0_row, column=0, sticky="w", padx=10, pady=2)

                setattr(self, f"{key}_switch", switch)
                self.frame0_row += 1
            
            else:
                switch = ctk.CTkSwitch(master=self.frame1, text=entry["label"], command=lambda k=key: self.update_variable_selection(k))
                switch.grid(row=self.frame1_row, column=0, sticky="w", padx=10, pady=2)

                setattr(self, f"{key}_switch", switch)
                self.frame1_row += 1

            if entry.get("state", 0) == 1:
                    switch.select()
            else:
                switch.deselect()


    def update_variable_selection(self, k):
        entry = self.parent.data[k]
        entry["state"] = 1 if getattr(self, f"{k}_switch").get() else 0

        variables_count = sum(1 for entry in self.parent.data.values() if entry.get("state", 0) == 1)
        self.parent.control_frame.r8_c1.configure(text=f"{variables_count} Selected")

class PIDResults(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#EBEBEB")
        self.parent = parent

        self.title("PID Results")
        self.geometry("400x150")
        self.resizable(False, False)
        self.transient(parent)
        self.focus()

        self.grid_rowconfigure(0, weight=100)
        self.grid_columnconfigure(0, weight=100)

        self.frame0 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 10))

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)

        # Row 0
        self.r0_c0 = ctk.CTkLabel(self.frame0, text=self.parent.data["pid_overshoot_lbf"]["label"]+":")
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.r0_c1 = ctk.CTkLabel(self.frame0, text="0.00")
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=2)

        # Row 1
        self.r1_c0 = ctk.CTkLabel(self.frame0, text=self.parent.data["pid_overshoot_percent"]["label"]+":")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkLabel(self.frame0, text="0.00")
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        # Row 2
        self.r2_c0 = ctk.CTkLabel(self.frame0, text=self.parent.data["pid_settling_time_s"]["label"]+":")
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkLabel(self.frame0, text="0.00")
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        # Row 3
        self.r3_c0 = ctk.CTkLabel(self.frame0, text=self.parent.data["pid_load_error_running_avg_percent"]["label"]+":")
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkLabel(self.frame0, text="0.00")
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)