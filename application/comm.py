import serial
import struct
from diagnostics import log
import json
import time

class Comm:
    def __init__(self, port, baudrate, timeout, frequency):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.frequency = frequency
        
        try:
            self._serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            self._serial.reset_input_buffer()
            log("#601", "Application", "Serial has been initialized.")
            
        except:
            log("#602", "Application", "Serial cannot be initialized.")
            raise IOError()

        self._serial.write(struct.pack('<BB', 0xAA, 0x00))
        log("#603", "Application", "Connection request has been sent to the controller.")
        
        cmd = self._serial.read(4)
        if cmd == b'\xCC\x00\x00\xEE':
            log("#604", "Controller", "Connection is successful.")
        else:
            log("#605", "Application", "Connection is not successful.")
            self.close()
            raise IOError()
        
    def send_config(self, config):
        self._serial.write(struct.pack('<BB', 0xAA, 0x01) + json.dumps(config).encode("utf-8") + b'\n')
        log("#606", "Application", "Configuration file has been sent to the controller.")

        cmd = self._serial.read(4)
        if cmd == b'\xCC\x01\x00\xEE':
            log("#607", "Controller", "Configuration file has been received.")
        elif cmd == b'\xCC\x01\x01\xEE':
            log("#608", "Controller", "Configuration file cannot be read.")
        elif cmd == b'\xCC\x01\x02\xEE':
            log("#609", "Controller", "Configuration file is overflowed.")
        else:
            log("#610", "Application", "Configuration file cannot be received.")
            self.close()
            raise IOError()
        
    def disconnect(self):
        if self._serial and self._serial.is_open:
            self._serial.write(struct.pack('<BB', 0xAA, 0x02))
            log("#611", "Application", "Disconnection request has been sent to the controller.")
            self._serial.close()
            log("#612", "Controller", "Controller has ben disconnected, serial has been terminated.")

    def serial_monitor(self):
        if self._serial.in_waiting < 2:
            return None, None
        
        hdr = self._serial.read(1)
        
        exp = time.time() + self.timeout

        while time.time() < exp:
            if hdr == b'\xCC':
                feedback = self._serial.read_until(expected=b'\xEE')
                return hdr, feedback[:-1]

            elif hdr == b'\xDD':
                data = self._serial.read_until(expected=b'\xEE').decode(errors='ignore').strip().split(',')

                if len(data) != 27:
                    return None, None

                data_map = {
                    "rotary_motor_speed_step_s": float(data[0]),
                    "rotary_motor_speed_rpm": float(data[1]),
                    "rotary_motor_position_deg": float(data[2]),
                    "right_z_axis_motor_speed_step_s": float(data[3]),
                    "right_z_axis_motor_speed_rpm": float(data[4]),
                    "right_z_axis_motor_position_step": float(data[5]),
                    "right_z_axis_motor_position_in": float(data[6]),
                    "left_z_axis_motor_speed_step_s": float(data[7]),
                    "left_z_axis_motor_speed_rpm": float(data[8]),
                    "left_z_axis_motor_position_step": float(data[9]),
                    "left_z_axis_motor_position_in": float(data[10]),
                    "passive_roller_position_step": float(data[11]),
                    "passive_roller_position_in": float(data[12]),
                    "right_loadcell_adc_16bit": float(data[13]),
                    "right_loadcell_volts_v": float(data[14]),
                    "right_loadcell_load_lbf": float(data[15]),
                    "left_loadcell_adc_16bit": float(data[16]),
                    "left_loadcell_volts_v": float(data[17]),
                    "left_loadcell_load_lbf": float(data[18]),
                    "total_load_lbf": float(data[19]),
                    "total_revolution_rev": float(data[20]),
                    "pid_tuning_mode": float(data[21]),
                    "pid_overshoot_lbf": float(data[22]),
                    "pid_overshoot_percent": float(data[23]),
                    "pid_settling_time_s": float(data[24]),
                    "pid_load_error_running_avg_percent": float(data[25]),
                    "thermocouple_flow_temperature_c": float(data[26])
                }

                return hdr, data_map
            
            else:
                return None, None
        
    def halt_motors(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x10))
            log("#614", "Application", "The command has been sent to the controller to halt motors.")
        except Exception:
            pass
    
    def rotate_90deg_rotary_motor(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x11))
            log("#615", "Application", "The command has been sent to the controller to rotate Rotary Motor by 90-deg.")
        except Exception:
            pass

    def go_home_rotary_motor(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x12))
            log("#616", "Application", "The command has been sent to the controller to rotate send Rotary Motor to home.")
        except Exception:
            pass

    def go_home_z_axis_motors(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x13))
            log("#617", "Application", "The command has been sent to the controller to rotate send Z-Axis Motors to home.")
        except Exception:
            pass
    
    def move_motors_by(self, unit, rotary_motor, right_z_axis_motor, left_z_axis_motor):
        try:
            if unit == "step":
                self._serial.write(struct.pack('<BBBfii', 0xAA, 0x14, 0x00, float(rotary_motor), int(right_z_axis_motor), int(left_z_axis_motor)))
                log("#618", "Application", "The command has been sent to the controller to move motors by given distance (step).")
            elif unit == "in":
                self._serial.write(struct.pack('<BBBfff', 0xAA, 0x14, 0x01, float(rotary_motor), float(right_z_axis_motor), float(left_z_axis_motor)))
                log("#619", "Application", "The command has been sent to the controller to move motors by given distance (in).")
            else:
                pass
        except Exception:
            pass
    
    def move_motors_to(self, unit, rotary_motor, right_z_axis_motor, left_z_axis_motor):
        try:
            if unit == "step":
                self._serial.write(struct.pack('<BBBfii', 0xAA, 0x15, 0x00, float(rotary_motor), int(right_z_axis_motor), int(left_z_axis_motor)))
                log("#620", "Application", "The command has been sent to the controller to move motors to given position (step).")
            elif unit == "in":
                self._serial.write(struct.pack('<BBBfff', 0xAA, 0x15, 0x01, float(rotary_motor), float(right_z_axis_motor), float(left_z_axis_motor)))
                log("#621", "Application", "The command has been sent to the controller to move motors to given position (in).")
            else:
                pass
        except Exception:
            pass

    def set_home_rotary_motor(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x16))
            log("#622", "Application", "The command has been sent to the controller to set Rotary Motor home.")
        except Exception:
            pass
    
    def set_home_right_z_axis_motor(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x17))
            log("#623", "Application", "The command has been sent to the controller to set Right Z-Axis Motor home.")
        except Exception:
            pass
    
    def set_home_left_z_axis_motor(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x18))
            log("#624", "Application", "The command has been sent to the controller to set Left Z-Axis Motor home.")
        except Exception:
            pass

    def pid_experiment(self, pid_rotary_motor_direction, pid_rotary_motor_speed_rpm, pid_target_load_lbf, pid_experiment_duration_ms):
        try:
            if pid_rotary_motor_direction == "CW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x00, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), int(pid_experiment_duration_ms)))
                log("#625", "Application", "The command has been sent to the controller to initiate experiment (CW).")
            elif pid_rotary_motor_direction == "CCW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x01, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), int(pid_experiment_duration_ms)))
                log("#626", "Application", "The command has been sent to the controller to initiate experiment (CCW).")
            else:
                pass

        except Exception:
            pass
    
    def pid_experiment_terminate(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x21))
            log("#627", "Application", "The command has been sent to the controller to terminate the experiment.")
        except Exception:
            pass