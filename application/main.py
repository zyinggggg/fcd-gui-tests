# Author: Mehmet B. Sefer (Technical Project Specialist II)
# Organization: NexGenPPT @ Iowa State University

version = 1.0
release_date = "12/20/2025"

import os, json
import customtkinter as ctk
from frames import HealthFrame, PerformanceFrame, SettingsFrame, ControlFrame, SurfaceFrame, PIDFrame
from sync import Sync
from data import default_data_map
from diagnostics import log

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        log("#001", "Application", "Application has been initialized.")

        # ========== APPLICATION SETUP =======
        self.title("Enhanced Contamination Device Controller")
        self.geometry("1920x1080")
        self.bind("<1>", lambda event: event.widget.focus_set())
        self._state_before_windows_set_titlebar_color = 'zoomed'

        # ========== GLOBAL STYLING ==========
        self.theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme.json")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(self.theme_path)

        # ========== LOAD JSON ===============
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
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
        self.control_frame.r8_c1.configure(text=f"{initial_variables_count} Selected")

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