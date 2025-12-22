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
        self.grid_columnconfigure(1, weight=1)

        # Row 0
        self.r0_c0 = ctk.CTkLabel(self, text='Device Control', font=("Helvetica", 18, "bold"))
        self.r0_c0.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r0_c1 = ctk.CTkButton(self, text='Advanced Control', command=self.open_advanced_control)
        self.r0_c1.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        # Row 1
        self.r1_c0 = ctk.CTkLabel(self, text="Rotary Motor Direction:")
        self.r1_c0.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.r1_c1 = ctk.CTkOptionMenu(self, values=["CW", "CCW"], text_color="#FFFFFF", width=121)
        self.r1_c1.grid(row=1, column=1, sticky="e", padx=10, pady=2)

        # Row 2
        self.r2_c0 = ctk.CTkLabel(self, text=parent.data["rotary_motor_speed_rpm"]["label"]+":")
        self.r2_c0.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.r2_c1 = ctk.CTkEntry(self, justify="right", width=121)
        self.r2_c1.grid(row=2, column=1, sticky="e", padx=10, pady=2)

        # Row 3
        self.r3_c0 = ctk.CTkLabel(self, text="Apply Load:")
        self.r3_c0.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.r3_c1 = ctk.CTkSegmentedButton(self, values=["No", "Yes"], command=self.set_pid_target_load_lbf)
        self.r3_c1.grid(row=3, column=1, sticky="e", padx=10, pady=2)
        self.r3_c1.set("No")

        # Row 4
        self.r4_c0 = ctk.CTkLabel(self, text='Target Load (lbf):')
        self.r4_c0.grid(row=4, column=0, sticky="w", padx=10, pady=2)

        self.r4_c1 = ctk.CTkEntry(self, justify="right", width=121)
        self.r4_c1.grid(row=4, column=1, sticky="e", padx=10, pady=2)

        # Row 5
        self.r5_c0 = ctk.CTkLabel(self, text='Experiment Duration (hh:mm:ss):')
        self.r5_c0.grid(row=5, column=0, sticky="w", padx=10, pady=2)
        
        self.r5_c1 = ctk.CTkEntry(self, justify="right", width=121)
        self.r5_c1.grid(row=5, column=1, sticky="e", padx=10, pady=2)
        self.r5_c1.insert(0, "00:00:00")

        # Row 6
        self.r6_c0 = ctk.CTkLabel(self, text='Data Acquisition', font=("Helvetica", 18, "bold"))
        self.r6_c0.grid(row=6, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r6_c1 = ctk.CTkSegmentedButton(self, values=["Disable", "Enable"], command=self.set_data_acquisition)
        self.r6_c1.grid(row=6, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r6_c1.set("Disable")

        # Row 7
        self.r7_c0 = ctk.CTkLabel(self, text='Data Frequency (ms):')
        self.r7_c0.grid(row=7, column=0, sticky="w", padx=10, pady=2)

        self.r7_c1 = ctk.CTkEntry(self, justify="right", width=121)
        self.r7_c1.grid(row=7, column=1, sticky="e", padx=10, pady=2)

        # Row 8
        self.r8_c0 = ctk.CTkLabel(self, text='Variable Selection:')
        self.r8_c0.grid(row=8, column=0, sticky="w", padx=10, pady=2)

        self.r8_c1 = ctk.CTkButton(self, text="", command=self.open_variable_selection, width=121)
        self.r8_c1.grid(row=8, column=1, sticky="e", padx=10, pady=2)
        self.r8_c1.configure(text="0 Selected")

        # Row 9
        self.r9_c0 = ctk.CTkLabel(self, text='Experiment Name:')
        self.r9_c0.grid(row=9, column=0, sticky="w", padx=10, pady=2)

        self.r9_c1 = ctk.CTkEntry(self, justify="right", width=121)
        self.r9_c1.grid(row=9, column=1, sticky="e", padx=10, pady=2)

        # Row 10
        self.r10_c0 = ctk.CTkLabel(self, text='Save to:')
        self.r10_c0.grid(row=10, column=0, sticky="w", padx=10, pady=2)

        self.r10_c1 = ctk.CTkButton(self, text="Browse 📂", command=self.browse_experiment_directory, width=121)
        self.r10_c1.grid(row=10, column=1, sticky="e", padx=10, pady=2)

        # Row 11
        self.r11_c0 = ctk.CTkLabel(self, text='Experiment Status', font=("Helvetica", 18, "bold"))
        self.r11_c0.grid(row=11, column=0, sticky="w", padx=10, pady=(10, 5))

        self.r11_c1 = ctk.CTkSegmentedButton(self, values=["Stop", "Start"], command=self.on_pid_control)
        self.r11_c1.grid(row=11, column=1, sticky="e", padx=10, pady=(10, 5))
        self.r11_c1.set("Stop")

        # Row 12
        self.r12_c0 = ctk.CTkLabel(self, text='Run Time (hh:mm:ss):')
        self.r12_c0.grid(row=12, column=0, sticky="w", padx=10, pady=2)

        self.r12_c1 = ctk.CTkLabel(self, text="00:00:00")
        self.r12_c1.grid(row=12, column=1, sticky="e", padx=10, pady=2)

        # Row 13
        self.r13_c0 = ctk.CTkLabel(self, text='Total Rev:')
        self.r13_c0.grid(row=13, column=0, sticky="w", padx=10, pady=2)

        self.r13_c1 = ctk.CTkLabel(self, text="0.00")
        self.r13_c1.grid(row=13, column=1, sticky="e", padx=10, pady=2)

        self.set_pid_target_load_lbf("No")
        self.set_data_acquisition("Disable")

    def open_advanced_control(self):
        if self.parent.advanced_control is None or not self.parent.advanced_control.winfo_exists():
            self.parent.advanced_control = AdvancedControl(self.parent)
        else:
            self.parent.advanced_control.focus()

    def set_data_acquisition(self, value):
        state = "disabled" if value == "Disable" else "normal"
        self.r7_c1.configure(state=state)
        self.r8_c1.configure(state=state)
        self.r9_c1.configure(state=state)
        self.r10_c1.configure(state=state)

    def set_pid_target_load_lbf(self, value):
        state = "disabled" if value == "No" else "normal"
        self.r4_c1.configure(state=state)

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