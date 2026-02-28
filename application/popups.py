import json
import requests
import re
from pathlib import Path
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

            if key == "pid_z_axis_motor_ramplen_step":
                label = ctk.CTkLabel(master=self.frame0, text="PID Calibration Mode:")
                label.grid(row=self.frame0_row, column=0, sticky="w", padx=10, pady=2)

                option = ctk.CTkSegmentedButton(self.frame0, values=["Time", "Count"], command=self.set_pid_calibration_mode)
                option.grid(row=self.frame0_row, column=3, sticky="e", padx=10, pady=2)
                option.set("Count")

                self.frame0_row += 1

        self.load_button = ctk.CTkButton(master=self.frame0, text="Load", command=self.load, width=121)
        self.load_button.grid(row=self.frame0_row, column=1, sticky="e", padx=0, pady=2)

        self.save_as_button = ctk.CTkButton(master=self.frame0, text="Save As", command=self.save_as, width=121)
        self.save_as_button.grid(row=self.frame0_row, column=2, sticky="e", padx=(0, 4), pady=2)

        self.configure_button = ctk.CTkButton(master=self.frame0, text="Configure", command=self.configure, width=121)
        self.configure_button.grid(row=self.frame0_row, column=3, sticky="e", padx=10, pady=2)
    
    def set_pid_calibration_mode(self, value):
        if value == "Time":
            self.pid_calibration_stable_required_count_value.configure(state="disabled")
            self.pid_calibration_stable_required_time_ms_value.configure(state="normal")
        else:
            self.pid_calibration_stable_required_time_ms_value.configure(state="disabled")
            self.pid_calibration_stable_required_count_value.configure(state="normal")

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
        self.geometry("600x450")
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

        self.r1_c1 = ctk.CTkEntry(master=self.frame0, justify="left", width=300)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=(1, 2))
        self.repo_url = "https://github.com/zyinggggg/fcd-gui-tests"
        self.r1_c1.insert(0, self.repo_url)

        self.update_status = None
        self.owner = None
        self.repo_name = None
        self.repo_version = None
        self.download_url = None
        self.auto_checked = False

        self.status_frame = ctk.CTkScrollableFrame(master=self.frame0, fg_color="#F9F9FA", height=290)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status = ctk.CTkLabel(master=self.status_frame, text="", justify="left", anchor="w")
        self.status.grid(row=0, column=0, sticky="w", padx=5, pady=0)

        self.refresh_button = ctk.CTkButton(master=self.frame0, text="↻", width=121, command=self.on_button_click)
        self.refresh_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        self.after(100, self.auto_check_for_updates)
    
    def on_button_click(self):
        if self.update_status == "update_available":
            # Open browser to the download link
            if self.download_url:
                import webbrowser
                webbrowser.open_new(self.download_url)
                self.status.configure(text="✅ Downloading...", text_color="green")
            else:
                self.status.configure(text="❌ Error: Could not determine download link.", text_color="red")
        else:
            self.check_for_updates()
    
    def auto_check_for_updates(self):
        if not self.auto_checked:
            self.auto_checked = True
            self.check_for_updates()

    def check_for_updates(self):
        if not self.check_internet_connection():
            self.status.configure(text="⚠️ No Internet Connection! Please check your internet connection and try again.", text_color="red")
            return

        self.refresh_button.configure(state="disabled")
        self.status.configure(text="⏳ Checking for updates...\n\nPlease wait...", text_color="blue")
        self.update()
        
        try:
            from main import version
            # 1. Determine Current Version
            current_version_str = str(version).strip()
            current_version_parts = [int(p) for p in current_version_str.split('.') if p.isdigit()]
            current_version = tuple(current_version_parts[:2] + [0] * (2 - len(current_version_parts)))
            
            # 2. Extract owner and repo name
            url_parts = self.r1_c1.get().rstrip("/").replace(".git", "").split("/")
            self.owner = url_parts[-2]
            self.repo_name = url_parts[-1]

            # 3. Check Remote Version in main.py
            raw_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo_name}/main/application/main.py"
            response = requests.get(raw_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                version_match = re.search(r"version\s*=\s*([\d\.]+)", content)
                release_date_match = re.search(r'release_date\s*=\s*["\']([^"\']+)["\']', content)

                if version_match:
                    repo_version_str = version_match.group(1).strip()
                    repo_version_parts = [int(p) for p in repo_version_str.split('.') if p.isdigit()]
                    self.repo_version = tuple(repo_version_parts[:2] + [0] * (2 - len(repo_version_parts)))
                    
                    repo_release_date = release_date_match.group(1) if release_date_match else "Unknown Date"

                    if self.repo_version > current_version:
                        self.update_status = "update_available"
                        self.refresh_button.configure(text="Install")
                        self.new_version_info(self.repo_version, repo_release_date)
                        self.download_url = self.downloads()
                    else:
                        self.update_status = "up_to_date"
                        self.refresh_button.configure(text="Up to Date")
                        self.status.configure(text="You are on the latest version.")
                else:
                    self.status.configure(text="❌ Error: Could not find version in repository 'main.py' file.", text_color="red")

            else:
                self.status.configure(text=f"❌ Failed to reach GitHub (Status: {response.status_code}). Please verify the Repository URL.", text_color="red")

        except Exception as e:
            self.status.configure(text=f"❌ An unexpected error occurred: {str(e)}", text_color="red")
        
        finally:
            self.refresh_button.configure(state="normal")
    
    def new_version_info(self, repo_version, repo_release_date):
        from main import resource_path

        updates_text = (f"New version v{'.'.join(map(str, repo_version))} "f"is available! ({repo_release_date})\n\n")

        version_file = resource_path("data/version.txt") 
        with open(version_file, "r", encoding="utf-8") as f:
            updates_text += f.read()

        self.status.configure(text=updates_text)

    
    def check_internet_connection(self):
        try:
            requests.head(self.r1_c1.get(), timeout=5) # Use the entry value for connection check
            return True
        except Exception:
            return False
    
    def downloads(self):
        import platform

        os_name = platform.system()

        os_keywords = {
            "Windows": ["win", "windows"],
            "Darwin": ["mac", "darwin", "osx"],
            "Linux": ["linux", "ubuntu"],
        }

        if os_name not in os_keywords:
            raise RuntimeError(f"Unsupported OS: {os_name}")
        
        tag = f"v{'.'.join(map(str, self.repo_version))}"
        api_url = f"https://api.github.com/repos/{self.owner}/{self.repo_name}/releases/tags/{tag}"

        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        release = response.json()
        assets = release.get("assets", [])

        for asset in assets:
            name = asset.get("name", "").lower()
            for kw in os_keywords[os_name]:
                if kw in name:
                    return asset["browser_download_url"]
        raise RuntimeError("No compatible installer found for your OS.")

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