import serial
import struct
from diagnostics import log
import json
import time
import threading

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

    def pid_experiment(self, pid_experiment_mode, pid_rotary_motor_speed_rpm, pid_target_load_lbf, pid_experiment_revolution_rev):
        try:
            if pid_experiment_mode == "CW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x00, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), float(pid_experiment_revolution_rev)))
                log("#625", "Application", "The command has been sent to the controller to initiate experiment (CW).")
            elif pid_experiment_mode == "CCW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x01, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), float(pid_experiment_revolution_rev)))
                log("#626", "Application", "The command has been sent to the controller to initiate experiment (CCW).")
            elif pid_experiment_mode == "CW+CCW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x02, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), float(pid_experiment_revolution_rev)))
                log("#627", "Application", "The command has been sent to the controller to initiate experiment (CW+CCW).")
            elif pid_experiment_mode == "CCW+CW":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x03, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), float(pid_experiment_revolution_rev)))
                log("#628", "Application", "The command has been sent to the controller to initiate experiment (CCW+CW).")
            elif pid_experiment_mode == "Swing":
                self._serial.write(struct.pack('<BBBfdL', 0xAA, 0x20, 0x04, float(pid_rotary_motor_speed_rpm), float(pid_target_load_lbf), float(pid_experiment_revolution_rev)))
                log("#629", "Application", "The command has been sent to the controller to initiate experiment (Swing).")
            else:
                pass

        except Exception:
            pass
    
    def pid_experiment_terminate(self):
        try:
            self._serial.write(struct.pack('<BB', 0xAA, 0x21))
            log("#630", "Application", "The command has been sent to the controller to terminate the experiment.")
        except Exception:
            pass

    # ==================== FLASH TEST COMMANDS ====================
    def flash_write(self, message="Hello from GUI!", callback=None):
        try:
            print("\n=== FLASH TEST DEBUG ===")
                
            # Clear any old data in buffer
            old_data = self._serial.read_all()
            if old_data:
                print(f"0. Cleared old buffer data: {old_data}")
            print("1. Serial buffer cleared")
            
            # Prepare the message
            message_bytes = message.encode('utf-8')
            msg_length = len(message_bytes)
            
            if msg_length > 255:
                print("ERROR: Message too long (max 255 bytes)")
                if callback:
                    callback("ERROR: Message too long")
                return
            
            print(f"2. Preparing to send: '{message}' ({msg_length} bytes)")
            
            # Send command 0x30 + message length + message
            self._serial.write(struct.pack('<BB', 0xAA, 0x30))  # Command header
            self._serial.write(struct.pack('B', msg_length))     # Message length
            self._serial.write(message_bytes)                    # Actual message
            
            log("#701", "Application", f"Flash write command sent with message: {message}")
            print(f"3. Sent to Arduino: Command=0x30, Length={msg_length}, Message='{message}'")

        except Exception:
            pass

    
    def flash_read(self, callback=None):
        # Wait for Arduino to process (write to flash + read back)
        try:
            print("4. Waiting 2 seconds for Arduino to write and read flash...")
            time.sleep(2.0)

            self._serial.write(struct.pack('<BB', 0xAA, 0x31))  # Command header
            # Read response from Arduino
            flash_message = ""
            lines_received = []
            timeout = time.time() + 5.0  # Increased to 5 second timeout
            flash_complete = False
            
            print("5. Reading response from Arduino...")
            print(f"   Bytes available: {self._serial.in_waiting}")
            
            while time.time() < timeout and not flash_complete:
                if self._serial.in_waiting > 0:
                    try:
                        line = self._serial.readline().decode('utf-8', errors='ignore').strip()
                        
                        # Log ALL lines for debugging
                        print(f"   Raw line: '{line}' (len={len(line)})")
                        
                        # Log all lines (even empty ones for debugging)
                        if line or True:  # Always process
                            if line and line.startswith("FLASH"):
                                print(f"   Received: {line}")
                                lines_received.append(line)
                            elif line:
                                # Non-FLASH lines (could be errors or debug from Arduino)
                                print(f"   Other: {line}")
                            
                            # Check if this is the data line
                            if line.startswith("FLASH_DATA:"):
                                flash_message = line.replace("FLASH_DATA:", "").strip()
                                log("#702", "Controller", f"Flash data received: {flash_message}")
                                print(f"   ✓ Flash returned: {flash_message}")
                            
                            # Check if we're done
                            elif line == "FLASH_END":
                                print(f"   ✓ Received FLASH_END, completing...")
                                flash_complete = True
                                break
                                
                            # Check for errors
                            elif line.startswith("FLASH_ERROR:"):
                                error_msg = line.replace("FLASH_ERROR:", "")
                                log("#703", "Controller", f"Flash error: {error_msg}")
                                flash_message = f"ERROR: {error_msg}"
                                print(f"   ✗ Error: {error_msg}")
                                flash_complete = True
                                break
                                
                    except Exception as e:
                        print(f"   ! Decode error: {e}")
                        continue
                else:
                    time.sleep(0.05)

            print(f"6. Total lines received: {len(lines_received)}")
            
            # Call callback with result
            if callback:
                callback(flash_message)
                    
            else:
                log("#704", "Application", "No flash data received.")
                print("✗ No flash data received")
                print(f"   All lines: {lines_received}")
                
                if callback:
                    callback("No response")

            print("=== FLASH TEST END ===\n")

        except Exception:
            pass 
