# Author: Mehmet B. Sefer (Technical Project Specialist II)
# Organization: NexGenPPT @ Iowa State University

version = 1.0
release_date = "12/25/2025"

import customtkinter as ctk

# ================= SPLASH SCREEN =================
class SplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback

        self.splash = ctk.CTkToplevel(root)
        self.splash.overrideredirect(True)

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_width = 600
        splash_height = 400
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

        self.create_content()
        self.splash.after(2000, self.close_splash)
    
    def create_content(self):
        bg_frame = ctk.CTkFrame(self.splash, fg_color="#3a7ebf")
        bg_frame.pack(fill="both", expand=True)

        center_frame = ctk.CTkFrame(bg_frame, fg_color="transparent")
        center_frame.pack(expand=True)

        app_name = ctk.CTkLabel(center_frame, text="Enhanced Contamination Device Controller", font=("Arial", 24, "bold"), text_color="white")
        app_name.pack(pady=10)

        loading_text = ctk.CTkLabel(center_frame, text="Loading...", font=("Open Sans", 14), text_color="white")
        loading_text.pack(pady=20)

        self.progress = ctk.CTkProgressBar(center_frame, orientation="horizontal", width=300)
        self.progress.pack(pady=10)

        self.update_progress()

    def update_progress(self, value=0):
        if value <= 100:
            self.progress.set(value / 100)
            self.splash.after(20, self.update_progress, value + 1)

    def close_splash(self):
        self.splash.destroy()
        self.callback()


import os, json, sys
from pathlib import Path
os.environ['MPLCONFIGDIR'] = str(Path.home())+"/.matplotlib/"
from frames import HealthFrame, PerformanceFrame, SettingsFrame, ControlFrame, SurfaceFrame, PIDFrame
from sync import Sync
from data import default_data_map
from diagnostics import log

def resource_path(relative_path):
    """Get absolute path to resource (dev + PyInstaller)"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        SplashScreen(self, self.show_main_app)

    def show_main_app(self):
        self.deiconify()

        log("#001", "Application", "Application has been initialized.")

        # ========== APPLICATION SETUP =======
        self.title("Enhanced Contamination Device Controller")
        self.geometry("1920x1080")
        self.bind("<1>", lambda event: event.widget.focus_set())
        self._state_before_windows_set_titlebar_color = 'zoomed'

        # ========== GLOBAL STYLING ==========
        #self.theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme.json")
        self.theme_path = resource_path("data/theme.json")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(self.theme_path)

        # ========== LOAD JSON ===============
        #self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.config_path = resource_path("data/config.json")
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
            log("#002", "Application", "Configuration file has been accessed.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = {}
            log("#003", "Application", "Configuration file cannot be accessed.")

        # ========== STATIC ==================
        
        self.data = default_data_map()

        # ========== GRID CONFIGURATION ======
        self.grid_rowconfigure(0, weight=70, uniform="Silent_Creme")
        self.grid_rowconfigure(1, weight=100, uniform="Silent_Creme")
        self.grid_rowconfigure(2, weight=80, uniform="Silent_Creme")
        self.grid_columnconfigure(0, weight=100, uniform="Silent_Creme")
        self.grid_columnconfigure(1, weight=100, uniform="Silent_Creme")
        self.grid_columnconfigure(2, weight=100, uniform="Silent_Creme")

        # ========== FRAME SETUP =============

        self.health_frame = HealthFrame(self)
        self.health_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.performance_frame = PerformanceFrame(self)
        self.performance_frame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(5, 5))

        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.control_frame = ControlFrame(self)
        self.control_frame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky="nsew", padx=(5, 5), pady=(10,5))

        initial_variables_count = sum(1 for entry in self.data.values() if entry.get("state", 0) == 1)
        self.control_frame.r12_c1.configure(text=f"{initial_variables_count} Selected")

        self.surface_frame = SurfaceFrame(self)
        self.surface_frame.grid(row=0, column=2, rowspan=2, columnspan=1, sticky="nsew", padx=(5, 10), pady=(10, 5))

        self.pid_frame = PIDFrame(self)
        self.pid_frame.grid(row=2, column=1, rowspan=1, columnspan=2, sticky="nsew", padx=(5, 10), pady=(5, 10))

        self.sync = Sync(self, frequency=int(self.config.get("sync_frequency", "1000")))

        self.variable_selection = None
        self.advanced_performance = None
        self.advanced_settings = None
        self.maintenance = None
        self.diagnostics = None
        self.firmware = None
        self.advanced_control = None
        self.PID_results = None
        self.flash_test = None
        
        self.protocol("WM_DELETE_WINDOW", self.exit)

    def exit(self):
        try:
            self.surface_frame.destroy_plot()
            self.pid_frame.destroy_plot()
            self.sync.comm.disconnect()
        except Exception:
            pass
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
