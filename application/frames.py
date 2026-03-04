import re
import customtkinter as ctk
from customtkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plots import create_surface_plot, update_surface_plot, create_pid_plot, update_pid_plot
from popups import VariableSelection, AdvancedPerformance, AdvancedSettings, Maintenance, Diagnostics, Firmware, AdvancedControl, PIDResults

class HealthFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Row 0
        self.r0_c0 = ctk.CTkLabel(self, text='Device Health', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))

        self.r0_c1 = ctk.CTkLabel(self, text="Not Connected ⬤")
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10,5))

        # Row 1
        self.r1_c0 = ctk.CTkLabel(self, text='Rotary Motor Status')
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkLabel(self, text="Inactive ⬤")
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        # Row 2
        self.r2_c0 = ctk.CTkLabel(self, text='Right Z-Axis Motor Status')
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkLabel(self, text="Inactive ⬤")
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        # Row 3
        self.r3_c0 = ctk.CTkLabel(self, text='Left Z-Axis Motor Status')
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkLabel(self, text="Inactive ⬤")
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)

        # Row 4
        self.r4_c0 = ctk.CTkLabel(self, text='Right Load Cell Status')
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkLabel(self, text="Inactive ⬤")
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)

        # Row 5
        self.r5_c0 = ctk.CTkLabel(self, text='Left Load Cell Status')
        self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        self.r5_c1 = ctk.CTkLabel(self, text="Inactive ⬤")
        self.r5_c1.grid(row=5, column=1, sticky="e", padx=10, pady=2)

class PerformanceFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.parent = parent
        self.advanced_performance = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.r0_c0 = ctk.CTkLabel(self, text='Real-Time Performance', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r0_c1 = ctk.CTkButton(self, text='Advanced Perfomance', command=self.open_advanced_performance)
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        self.r1_c0 = ctk.CTkLabel(self, text=parent.data["rotary_motor_speed_rpm"]["label"]+":")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkLabel(self, text='0.00')
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        self.r2_c0 = ctk.CTkLabel(self, text=parent.data["rotary_motor_position_deg"]["label"]+":")
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkLabel(self, text='0.00')
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        self.r3_c0 = ctk.CTkLabel(self, text=parent.data["passive_roller_position_in"]["label"]+":")
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkLabel(self, text='0.00')
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)

        self.r4_c0 = ctk.CTkLabel(self, text=parent.data["right_loadcell_load_lbf"]["label"]+":")
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkLabel(self, text='0.00')
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)

        self.r5_c0 = ctk.CTkLabel(self, text=parent.data["left_loadcell_load_lbf"]["label"]+":")
        self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        self.r5_c1 = ctk.CTkLabel(self, text='0.00')
        self.r5_c1.grid(row=5, column=1, sticky="e", padx=10, pady=2)

        self.r6_c0 = ctk.CTkLabel(self, text=parent.data["total_load_lbf"]["label"]+":")
        self.r6_c0.grid(row=6, column=0, sticky="w", padx=10, pady=2)

        self.r6_c1 = ctk.CTkLabel(self, text='0.00')
        self.r6_c1.grid(row=6, column=1, sticky="e", padx=10, pady=2)

        self.r7_c0 = ctk.CTkLabel(self, text=parent.data["thermocouple_flow_temperature_c"]["label"]+":")
        self.r7_c0.grid(row=7, column=0, sticky="w", padx=10, pady=2)

        self.r7_c1 = ctk.CTkLabel(self, text='0.00')
        self.r7_c1.grid(row=7, column=1, sticky="e", padx=10, pady=2)

    def open_advanced_performance(self):
        if self.parent.advanced_performance is None or not self.parent.advanced_performance.winfo_exists():
            self.parent.advanced_performance = AdvancedPerformance(self.parent)
        else:
            self.parent.advanced_performance.focus()

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.parent = parent
        self.advanced_settings = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Row 1
        self.r0_c0 = ctk.CTkLabel(self, text='Settings', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r0_c1 = ctk.CTkButton(self, text='Advanced Settings', command=self.open_advanced_settings)
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        self.r1_c0 = ctk.CTkLabel(self, text='Select Device Port:')
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkOptionMenu(self, values=[""], text_color="#FFFFFF", width=121)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        self.r2_c0 = ctk.CTkLabel(self, text='Connection:')
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkButton(self, text="Connect", command= lambda: self.parent.sync.connection(), width=121)
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        self.r3_c0 = ctk.CTkLabel(self, text='Maintenance:')
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkButton(self, text="Launch", width=121, command=self.open_maintenance)
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)

        self.r4_c0 = ctk.CTkLabel(self, text='Diagnostics:')
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkButton(self, text="Launch", command=self.open_diagnostics, width=121)
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)

        self.r5_c0 = ctk.CTkLabel(self, text='Firmware:')
        self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        self.r5_c1 = ctk.CTkButton(self, text="Check", command=self.open_firmware, width=121)
        self.r5_c1.grid(row=5, column=1, stick="e", padx=10, pady=2)

    def open_advanced_settings(self):
        if self.parent.advanced_settings is None or not self.parent.advanced_settings.winfo_exists():
            self.parent.advanced_settings = AdvancedSettings(self.parent)
        else:
            self.parent.advanced_settings.focus()

    def open_maintenance(self):
        if self.parent.maintenance is None or not self.parent.maintenance.winfo_exists():
            self.parent.maintenance = Maintenance(self.parent)
        else:
            self.parent.maintenance.focus()

    def open_diagnostics(self):
        if self.parent.diagnostics is None or not self.parent.diagnostics.winfo_exists():
            self.parent.diagnostics = Diagnostics(self.parent)
        else:
            self.parent.diagnostics.focus()
    
    def open_firmware(self):
        if self.parent.firmware is None or not self.parent.firmware.winfo_exists():
            self.parent.firmware = Firmware(self.parent)
        else:
            self.parent.firmware.focus()

class ControlFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.parent = parent
        self.variable_selection = None
        self.advanced_control = None
        self.experiment_directory = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame0 = ctk.CTkScrollableFrame(self, width = 350, fg_color="#FFFFFF")
        self.frame0.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=0)

        # Row 0
        self.r0_c0 = ctk.CTkLabel(self.frame0, text='Device Control', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r0_c1 = ctk.CTkButton(self.frame0, text='Advanced Control', command=self.open_advanced_control)
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        # Row 1
        self.r1_c0 = ctk.CTkLabel(self.frame0, text="Experiment Mode:")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkOptionMenu(self.frame0, values=["CW", "CCW", "CW+CCW", "CCW+CW", "Swing"], text_color="#FFFFFF", width=121, command=self.on_experiment_mode_change)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        # Row 2
        self.r2_c0 = ctk.CTkLabel(self.frame0, text=parent.data["rotary_motor_speed_rpm"]["label"]+":")
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)
        self.r2_c1.bind("<KeyRelease>", lambda e: self.calculate_run_limit())

        # Row 3
        self.r3_c0 = ctk.CTkLabel(self.frame0, text="Apply Load:")
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkSegmentedButton(self.frame0, values=["No", "Yes"], command=self.set_pid_target_load_lbf)
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)
        self.r3_c1.set("No")

        # Row 4
        self.r4_c0 = ctk.CTkLabel(self.frame0, text='Target Load (lbf):')
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)

        # Row 5
        self.r5_c0 = ctk.CTkLabel(self.frame0, text='Rev Per Cycle:')

        self.r5_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)

        # Row 6
        self.r6_c0 = ctk.CTkLabel(self.frame0, text='Run Limit Type:')
        self.r6_c0.grid(row=6, column=0, sticky="w", padx=10, pady=2)
        
        self.r6_c1 = ctk.CTkOptionMenu(self.frame0, values=["Time", "Revolution"], text_color="#FFFFFF", width=121, command=self.on_run_limit_type_change)
        self.r6_c1.grid(row=6, column=1, sticky="e", padx=10, pady=2)

        # Row 7
        self.r7_c0 = ctk.CTkLabel(self.frame0, text='Duration (hh:mm:ss):')
        self.r7_c0.grid(row=7, column=0, sticky="w", padx=10, pady=2)
        
        self.r7_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)
        self.r7_c1.grid(row=7, column=1, sticky="e", padx=10, pady=2)
        self.r7_c1.insert(0, "00:00:00")
        self.r7_c1.bind("<KeyRelease>", lambda e: self.calculate_run_limit())

        # Row 8
        self.r8_c0 = ctk.CTkLabel(self.frame0, text='Total Rev:')
        self.r8_c0.grid(row=8, column=0, sticky="w", padx=10, pady=2)
        
        self.r8_c1 = ctk.CTkLabel(self.frame0, text='0')
        self.r8_c1.grid(row=8, column=1, sticky="e", padx=10, pady=(2, 0))

        # Row 9
        self.r9_c1 = ctk.CTkLabel(self.frame0, text='(CW: 0   CCW: 0)', font=("Helvetica", 10, "italic"))
        self.r9_c1.grid(row=9, column=1, sticky="e", padx=10, pady=0)

        # Row 10
        self.r10_c0 = ctk.CTkLabel(self.frame0, text='Data Acquisition', font=("Helvetica", 18, "bold"))
        self.r10_c0.grid(row=10, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r10_c1 = ctk.CTkSegmentedButton(self.frame0, values=["Disable", "Enable"], command=self.set_data_acquisition)
        self.r10_c1.grid(row=10, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r10_c1.set("Disable")

        # Row 11
        self.r11_c0 = ctk.CTkLabel(self.frame0, text='Data Frequency (ms):')
        self.r11_c0.grid(row=11, column=0, sticky="w", padx=10, pady=2)

        self.r11_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)
        self.r11_c1.grid(row=11, column=1, sticky="e", padx=10, pady=2)

        # Row 12
        self.r12_c0 = ctk.CTkLabel(self.frame0, text='Variable Selection:')
        self.r12_c0.grid(row=12, column=0, sticky="w", padx=10, pady=2)

        self.r12_c1 = ctk.CTkButton(self.frame0, text="", command=self.open_variable_selection, width=121)
        self.r12_c1.grid(row=12, column=1, sticky="e", padx=10, pady=2)
        self.r12_c1.configure(text="0 Selected")

        # Row 13
        self.r13_c0 = ctk.CTkLabel(self.frame0, text='Experiment Name:')
        self.r13_c0.grid(row=13, column=0, sticky="w", padx=10, pady=2)

        self.r13_c1 = ctk.CTkEntry(self.frame0, justify="right", width=121)
        self.r13_c1.grid(row=13, column=1, sticky="e", padx=10, pady=2)

        # Row 14
        self.r14_c0 = ctk.CTkLabel(self.frame0, text='Save to:')
        self.r14_c0.grid(row=14, column=0, sticky="w", padx=10, pady=2)

        self.r14_c1 = ctk.CTkButton(self.frame0, text="Browse 📂", command=self.browse_experiment_directory, width=121)
        self.r14_c1.grid(row=14, column=1, sticky="e", padx=10, pady=2)

        # Row 15
        self.r15_c0 = ctk.CTkLabel(self.frame0, text='Experiment Status', font=("Helvetica", 18, "bold"))
        self.r15_c0.grid(row=15, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r15_c1 = ctk.CTkSegmentedButton(self.frame0, values=["Stop", "Start"], command=self.on_pid_control)
        self.r15_c1.grid(row=15, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r15_c1.set("Stop")

        # Row 16
        self.r16_c0 = ctk.CTkLabel(self.frame0, text='Run Time (hh:mm:ss):')
        self.r16_c0.grid(row=16, column=0, sticky="w", padx=10, pady=2)

        self.r16_c1 = ctk.CTkLabel(self.frame0, text="00:00:00")
        self.r16_c1.grid(row=16, column=1, sticky="e", padx=10, pady=2)

        # Row 17
        self.r17_c0 = ctk.CTkLabel(self.frame0, text='Total Running Rev:')
        self.r17_c0.grid(row=17, column=0, sticky="w", padx=10, pady=2)

        self.r17_c1 = ctk.CTkLabel(self.frame0, text="0.00")
        self.r17_c1.grid(row=17, column=1, sticky="e", padx=10, pady=2)

        self.set_pid_target_load_lbf("No")
        self.set_data_acquisition("Disable")

    def open_advanced_control(self):
        if self.parent.advanced_control is None or not self.parent.advanced_control.winfo_exists():
            self.parent.advanced_control = AdvancedControl(self.parent)
        else:
            self.parent.advanced_control.focus()

    def set_pid_target_load_lbf(self, value):
        state = "disabled" if value == "No" else "normal"
        self.r4_c1.configure(state=state)

    def on_experiment_mode_change(self, experiment_mode):
        if experiment_mode == "Swing":
            self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=2)
            self.r5_c1.grid(row=5, column=1, sticky="e", padx=10, pady=2)
        else:
            self.r5_c0.grid_remove()
            self.r5_c1.grid_remove()
        
        self.calculate_run_limit()

    def on_run_limit_type_change(self, run_limit_type):
        self.r7_c1.delete(0, "end")
        if run_limit_type == "Time":
            self.r7_c0.configure(text="Duration (hh:mm:ss):")
            self.r7_c1.insert(0, "00:00:00")
            self.r8_c0.configure(text="Total Rev:")
            self.r8_c1.configure(text="0")

        elif run_limit_type == "Revolution":
            self.r7_c0.configure(text="Total Rev:")
            self.r7_c1.insert(0, "0")
            self.r8_c0.configure(text="Duration (hh:mm:ss):")
            self.r8_c1.configure(text="00:00:00")
    
    def calculate_run_limit(self):
        try:
            rotary_motor_speed_rpm = float(self.r2_c1.get())
            if rotary_motor_speed_rpm <= 0:
                return

            run_limit_type = self.r6_c1.get()
            experiment_mode = self.r1_c1.get()

            if run_limit_type == "Revolution":
                total_rev = float(self.r7_c1.get())
                total_duration_s = int((total_rev/rotary_motor_speed_rpm) * 60)
                hh = total_duration_s // 3600
                mm = (total_duration_s % 3600) // 60
                ss = total_duration_s % 60
                self.r8_c1.configure(text=f"{hh:02d}:{mm:02d}:{ss:02d}")
            else:
                hh, mm, ss = map(int, self.r7_c1.get().split(':'))
                duration_s = (hh * 3600) + (mm * 60) + ss
                total_rev = (duration_s / 60.0) * rotary_motor_speed_rpm
                self.r8_c1.configure(text=f"{total_rev:.2f}")
            
            import math
            total_rev = float(total_rev)

            if experiment_mode == "CW":
                cw = total_rev
                ccw = 0.0
            elif experiment_mode == "CCW":
                cw = 0.0
                ccw = total_rev
            elif experiment_mode == "CW+CCW":
                ccw = math.floor(total_rev / 2)
                cw = total_rev - ccw
            elif experiment_mode == "CCW+CW":
                cw = math.floor(total_rev / 2)
                ccw = total_rev - cw
            elif experiment_mode == "Swing":
                ccw = math.floor(total_rev / 2)
                cw  = total_rev - ccw
            else:
                cw, ccw = 0.0, 0.0
            
            self.r9_c1.configure(text=f"(CW: {cw}   CCW: {ccw})")
            
        except Exception:
            pass

    def set_data_acquisition(self, value):
        state = "disabled" if value == "Disable" else "normal"
        self.r11_c1.configure(state=state)
        self.r12_c1.configure(state=state)
        self.r13_c1.configure(state=state)
        self.r14_c1.configure(state=state)

    def open_variable_selection(self):
        if self.parent.variable_selection is None or not self.parent.variable_selection.winfo_exists():
            self.parent.variable_selection = VariableSelection(self.parent)
        else:
            self.parent.variable_selection.focus()

    def browse_experiment_directory(self):
        experiment_directory = filedialog.askdirectory()
        self.experiment_directory = experiment_directory

    def on_pid_control(self, control):
        if control == "Start":
            self.parent.sync.pid_experiment()
        elif control == "Stop":
            self.parent.sync.pid_experiment_terminate()

class SurfaceFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.r0_c0 = ctk.CTkLabel(self, text='2D Surface Profile', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        self.fig, self.ax = create_surface_plot()
        self.canvas_surface = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_surface.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))

    def destroy_plot(self):
        try:
            self.canvas_surface.get_tk_widget().destroy()
            plt.close(self.fig)
        except:
            pass

class PIDFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")

        self.parent = parent
        self.PID_results = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Row 1
        self.r0_c0 = ctk.CTkLabel(self, text='Step Response (PID)', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(25,0), pady=(10, 0))

        self.r0_c1 = ctk.CTkButton(self, text='PID Results', command=self.open_PID_results)
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        self.fig, self.ax = create_pid_plot()
        self.canvas_pid = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_pid.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0,0), pady=(0,5))

    def destroy_plot(self):
        try:
            self.canvas_pid.get_tk_widget().destroy()
            plt.close(self.fig)
        except:
            pass
    
    def open_PID_results(self):
        if self.parent.PID_results is None or not self.parent.PID_results.winfo_exists():
            self.parent.PID_results = PIDResults(self.parent)
        else:
            self.parent.PID_results.focus()