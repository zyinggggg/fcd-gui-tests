// Author: Mehmet B. Sefer (Technical Project Specialist II)
// Organization: NexGenPPT @ Iowa State University

#include <MobaTools.h>
#include <Adafruit_ADS1X15.h>
#include <ArduinoJson.h>
#include <PID_v1.h>
#include "hardware/watchdog.h"
#include <limits>

JsonDocument doc;

// System Variables
bool          comm_status                                               = true;
bool          pid_status                                                = false;

// Motors
const float   rotary_motor_in_step                                      = 0.0003125f;
const int     rotary_motor_step_rev                                     = 200;
const int     rotary_motor_microstep                                    = 8;
const int     rotary_motor_gear_ratio                                   = 10;
const int     rotary_motor_full_step_rev = rotary_motor_step_rev * rotary_motor_microstep * rotary_motor_gear_ratio;

const float   z_axis_motor_in_step                                      = 0.0003125f;
const int     z_axis_motor_step_rev                                     = 200;
const int     z_axis_motor_microstep                                    = 8;
const int     z_axis_motor_gear_ratio                                   = 1;
const int     z_axis_motor_full_step_rev = z_axis_motor_step_rev * z_axis_motor_microstep * z_axis_motor_gear_ratio;

const byte    rotary_motor_pin_step                                     = 4;
const byte    rotary_motor_pin_dir                                      = 24;
const byte    rotary_motor_pin_en                                       = 9;
MoToStepper   rotary_motor(rotary_motor_full_step_rev, STEPDIR);
float         rotary_motor_speed_step_s                                 = 0.00f;
float         rotary_motor_speed_rpm                                    = 0.00f;
long          rotary_motor_position_deg                                 = 0;
long          rotary_motor_initial_position_deg                         = 0;

const byte    right_z_axis_motor_pin_step                               = 8;
const byte    right_z_axis_motor_pin_dir                                = 15;
const byte    right_z_axis_motor_pin_en                                 = 27;
MoToStepper   right_z_axis_motor(z_axis_motor_full_step_rev, STEPDIR);
float         right_z_axis_motor_speed_step_s                           = 0.00f;
float         right_z_axis_motor_speed_rpm                              = 0.00f;
long          right_z_axis_motor_position_step                          = 0;
float         right_z_axis_motor_position_in                            = 0.00f;

const byte    left_z_axis_motor_pin_step                                = 14;
const byte    left_z_axis_motor_pin_dir                                 = 25;
const byte    left_z_axis_motor_pin_en                                  = 12;
MoToStepper   left_z_axis_motor(z_axis_motor_full_step_rev, STEPDIR);
float         left_z_axis_motor_speed_step_s                            = 0.00f;
float         left_z_axis_motor_speed_rpm                               = 0.00f;
long          left_z_axis_motor_position_step                           = 0;
float         left_z_axis_motor_position_in                             = 0.00f;

long          passive_roller_position_step                              = 0;
float         passive_roller_position_in                                = 0.00f;

float         total_revolution_rev                                      = 0.00f;

uint8_t       move_motors_by_unit                                       = 0;
float         move_rotary_motor_by_deg                                  = 0.00f;
long          move_right_z_axis_motor_by_step                           = 0;
long          move_left_z_axis_motor_by_step                            = 0;
float         move_right_z_axis_motor_by_in                             = 0.00f;
float         move_left_z_axis_motor_by_in                              = 0.00f;

uint8_t       move_motors_to_unit                                       = 0;
float         move_rotary_motor_to_deg                                  = 0.00f;
long          move_right_z_axis_motor_to_step                           = 0;
long          move_left_z_axis_motor_to_step                            = 0;
float         move_right_z_axis_motor_to_in                             = 0.00f;
float         move_left_z_axis_motor_to_in                              = 0.00f;

long          pid_loop_n                                                = 0;
float         pid_load_error_percent                                    = 0.00f;
float         pid_total_load_error_percent                              = 0.00f;
float         pid_load_error_running_avg_percent                        = 0.00f;

uint8_t       pid_rotary_motor_direction                                = 0;
float         pid_rotary_motor_speed_rpm                                = 0.00f;
double        pid_z_axis_motor_speed_rpm                                = 0.00;

long          pid_calibration_stable_start_time_ms                      = 0;
long          pid_calibration_start_time_ms                             = 0;
double        pid_overshoot_lbf                                         = 0.00;
float         pid_overshoot_percent                                     = 0.00f;
float         pid_settling_time_s                                       = 0.00f;

double        pid_experiment_target_load_lbf                            = 0.00;
long          pid_experiment_start_time_ms                              = 0;
long          pid_experiment_duration_ms                                = 0;

uint8_t       pid_tuning_mode                                           = 0;

Adafruit_ADS1115 ads;
int16_t       right_loadcell_adc_16bit                                  = 0;
float         right_loadcell_volts_v                                    = 0.00f;
float         right_loadcell_load_lbf                                   = 0.00f;

int16_t       left_loadcell_adc_16bit                                   = 0;
float         left_loadcell_volts_v                                     = 0.00f;
float         left_loadcell_load_lbf                                    = 0.00f;

double        total_load_lbf                                            = 0.00;

float         thermocouple_flow_temperature_c                           = 0.00f;

// STATIC VALUES
struct Config {
  float       manual_rotary_motor_speed_rpm                             = 0.00f;
  uint16_t    manual_rotary_motor_ramplen_step                          = 0;
  float       manual_z_axis_motor_speed_rpm                             = 0.00f;
  uint16_t    manual_z_axis_motor_ramplen_step                          = 0;

  uint16_t    pid_rotary_motor_ramplen_step                             = 0;
  double      pid_z_axis_motor_max_speed_rpm                            = 0.00;
  uint16_t    pid_z_axis_motor_ramplen_step                             = 0;

  long        pid_calibration_stable_required_time_ms                   = 0;
  float       pid_calibration_load_error_percent                        = 0.00f;

  float       pid_tuning_mode_limit_percent                             = 0.00f;
  double      pid_conservative_k_p                                      = 0.00;
  double      pid_conservative_k_i                                      = 0.00;
  double      pid_conservative_k_d                                      = 0.00;
  double      pid_aggressive_k_p                                        = 0.00;
  double      pid_aggressive_k_i                                        = 0.00;
  double      pid_aggressive_k_d                                        = 0.00;
  
  long        go_home_z_axis_motors_bounce_step                         = 0;

  float       right_loadcell_zero_offset_lbf                            = 0.00f;
  float       right_loadcell_scale_factor                               = 3.0303f;
  float       right_loadcell_max_load_lbf                               = 5.00f;
  float       left_loadcell_zero_offset_lbf                             = 0.00f;
  float       left_loadcell_scale_factor                                = 3.0303f;
  float       left_loadcell_max_load_lbf                                = 5.00f;


};

Config cfg;

using Action = void(*)();
static Action     *seq_actions              = nullptr;
static uint8_t     seq_count                = 0;
static uint8_t     seq_index                = 0;
static bool        seq_active               = false;

void seq_start(Action actions[], uint8_t count) {
  seq_actions  = actions;
  seq_count    = count;
  seq_index    = 0;
  seq_active   = true;
  seq_actions[0]();
}

void tmc_enable() {
  pinMode(rotary_motor_pin_en, OUTPUT);
  digitalWrite(rotary_motor_pin_en, LOW);
  rotary_motor.attach(rotary_motor_pin_step, rotary_motor_pin_dir);

  pinMode(right_z_axis_motor_pin_en, OUTPUT);
  digitalWrite(right_z_axis_motor_pin_en, LOW);
  right_z_axis_motor.attach(right_z_axis_motor_pin_step, right_z_axis_motor_pin_dir);

  pinMode(left_z_axis_motor_pin_en, OUTPUT);
  digitalWrite(left_z_axis_motor_pin_en, LOW);
  left_z_axis_motor.attach(left_z_axis_motor_pin_step, left_z_axis_motor_pin_dir);
}

void manual_control_settings() {
  rotary_motor.setSpeed(cfg.manual_rotary_motor_speed_rpm * 10);
  rotary_motor.setRampLen(cfg.manual_rotary_motor_ramplen_step);
  right_z_axis_motor.setSpeed(cfg.manual_z_axis_motor_speed_rpm * 10);
  right_z_axis_motor.setRampLen(cfg.manual_z_axis_motor_ramplen_step);
  left_z_axis_motor.setSpeed(cfg.manual_z_axis_motor_speed_rpm * 10);
  left_z_axis_motor.setRampLen(cfg.manual_z_axis_motor_ramplen_step);
}

bool motors_moving() {
  return rotary_motor.moving() || right_z_axis_motor.moving() || left_z_axis_motor.moving();
}

void go_home_rotary_motor() {
  if (rotary_motor_position_deg >= 180 ) {
    rotary_motor.doSteps(rotary_motor_full_step_rev * (360 - rotary_motor_position_deg) / 360);
  }
  else {
    rotary_motor.doSteps(- rotary_motor_full_step_rev * (rotary_motor_position_deg) / 360);
  }
}

void go_home_z_axis_motors_1() {
  right_z_axis_motor.write(0);
  left_z_axis_motor.write(0);
}

void go_home_z_axis_motors_2() {
  right_z_axis_motor.doSteps(-cfg.go_home_z_axis_motors_bounce_step);
  left_z_axis_motor.doSteps(-cfg.go_home_z_axis_motors_bounce_step);
}

void go_home_z_axis_motors_3() {
  right_z_axis_motor.doSteps(cfg.go_home_z_axis_motors_bounce_step);
  left_z_axis_motor.doSteps(cfg.go_home_z_axis_motors_bounce_step);
}

static Action go_home_z_axis_motors[] = { go_home_z_axis_motors_1, go_home_z_axis_motors_2, go_home_z_axis_motors_3 };

static Action go_home_all_motors[] = { go_home_z_axis_motors_1, go_home_z_axis_motors_2, go_home_z_axis_motors_3, go_home_rotary_motor };

PID pid_control(&total_load_lbf, &pid_z_axis_motor_speed_rpm, &pid_experiment_target_load_lbf, cfg.pid_conservative_k_p, cfg.pid_conservative_k_i, cfg.pid_conservative_k_d, DIRECT);

void pid_control_settings() {
  rotary_motor.setSpeed(pid_rotary_motor_speed_rpm * 10);
  rotary_motor.setRampLen(cfg.pid_rotary_motor_ramplen_step);
  right_z_axis_motor.setRampLen(cfg.pid_z_axis_motor_ramplen_step);
  left_z_axis_motor.setRampLen(cfg.pid_z_axis_motor_ramplen_step);
  pid_control.SetOutputLimits(-cfg.pid_z_axis_motor_max_speed_rpm, cfg.pid_z_axis_motor_max_speed_rpm);
}

void pid_experiment_1() {
  pid_calibration_stable_start_time_ms = 0;
  pid_overshoot_lbf = 0;
  pid_overshoot_percent = 0;
  pid_load_error_running_avg_percent = 0;
  pid_settling_time_s = 0;
  pid_control_settings();
  pid_control.SetMode(AUTOMATIC);
  comm_status = true;
  Serial.write((uint8_t*)"\xCC\x20\x04\xEE", 4);
  comm_status = false;
  pid_calibration_start_time_ms = millis();
}

void pid_experiment_2() {

  pid_status = true;

  if (pid_experiment_target_load_lbf == 0) {
    seq_index++;
    return;
  }

  ads_loop();
  
  if (total_load_lbf > pid_overshoot_lbf){
    pid_overshoot_lbf = total_load_lbf;
    pid_overshoot_percent = ((pid_overshoot_lbf - pid_experiment_target_load_lbf) / pid_experiment_target_load_lbf) * 100.0f;
  }

  pid_load_error_percent = fabs((total_load_lbf - pid_experiment_target_load_lbf) * 100 / pid_experiment_target_load_lbf);

  if (pid_load_error_percent <= cfg.pid_calibration_load_error_percent) {
    if (pid_calibration_stable_start_time_ms == 0) {
      pid_calibration_stable_start_time_ms = millis();
    } 
    else {
      if ((millis() - pid_calibration_stable_start_time_ms) >= cfg.pid_calibration_stable_required_time_ms) {
        right_z_axis_motor.rotate(0);
        left_z_axis_motor.rotate(0);
        pid_settling_time_s = (millis() - pid_calibration_start_time_ms) / 1000.0f;
        pid_calibration_stable_start_time_ms = 0;
        comm_status = true;
        Serial.write((uint8_t*)"\xCC\x20\x05\xEE", 4);
        comm_status = false;
        seq_index++;
        return;
      }
    } 
  }
  else {
    pid_calibration_stable_start_time_ms = 0;
  }

  if (pid_load_error_percent < cfg.pid_tuning_mode_limit_percent) {
    pid_control.SetTunings(cfg.pid_conservative_k_p, cfg.pid_conservative_k_i, cfg.pid_conservative_k_d);
  }
  else {
    pid_control.SetTunings(cfg.pid_aggressive_k_p, cfg.pid_aggressive_k_i, cfg.pid_aggressive_k_d);
  }

  pid_control.Compute();

  right_z_axis_motor.setSpeed( fabs(pid_z_axis_motor_speed_rpm * 10) );
  left_z_axis_motor.setSpeed( fabs(pid_z_axis_motor_speed_rpm * 10) );

  if (pid_z_axis_motor_speed_rpm > 0) {
    right_z_axis_motor.rotate(-1);
    left_z_axis_motor.rotate(-1);
  }
  else if (pid_z_axis_motor_speed_rpm < 0) {
    right_z_axis_motor.rotate(1);
    left_z_axis_motor.rotate(1);
  }
  else {
    right_z_axis_motor.rotate(0);
    left_z_axis_motor.rotate(0);
  }
}

void pid_experiment_3() {
  pid_experiment_start_time_ms = millis();
  comm_status = true;
  Serial.write((uint8_t*)"\xCC\x20\x06\xEE", 4);
  comm_status = false;
  rotary_motor_initial_position_deg = rotary_motor.read();
  if (pid_rotary_motor_direction == 0x01) {
    rotary_motor.rotate(-1);
  }
  else {
    rotary_motor.rotate(1);
  }
  pid_loop_n = 0;
  pid_load_error_running_avg_percent = 0;
  pid_total_load_error_percent = 0;
  seq_index++;
}

void pid_experiment_4() {

  if (millis() - pid_experiment_start_time_ms >= pid_experiment_duration_ms) {
    seq_index++;
    return;
  }

  if (pid_experiment_target_load_lbf == 0) {
    return;
  }

  ads_loop();

  pid_load_error_percent = fabs((total_load_lbf - pid_experiment_target_load_lbf) * 100 / pid_experiment_target_load_lbf);
  pid_total_load_error_percent += pid_load_error_percent;
  pid_load_error_running_avg_percent = pid_total_load_error_percent / pid_loop_n++;
  
  if (pid_load_error_percent < cfg.pid_tuning_mode_limit_percent) {
    pid_control.SetTunings(cfg.pid_conservative_k_p, cfg.pid_conservative_k_i, cfg.pid_conservative_k_d);
  }
  else {
    pid_control.SetTunings(cfg.pid_aggressive_k_p, cfg.pid_aggressive_k_i, cfg.pid_aggressive_k_d);
  }

  pid_control.Compute();

  right_z_axis_motor.setSpeed( fabs(pid_z_axis_motor_speed_rpm * 10) );
  left_z_axis_motor.setSpeed( fabs(pid_z_axis_motor_speed_rpm * 10) );

  if (pid_z_axis_motor_speed_rpm > 0) {
    right_z_axis_motor.rotate(-1);
    left_z_axis_motor.rotate(-1);
  }
  else if (pid_z_axis_motor_speed_rpm < 0) {
    right_z_axis_motor.rotate(1);
    left_z_axis_motor.rotate(1);
  }
  else {
    right_z_axis_motor.rotate(0);
    left_z_axis_motor.rotate(0);
  }
}

void pid_experiment_5() {
  halt_motors();
  comm_status = true;
  Serial.write((uint8_t*)"\xCC\x20\x07\xEE", 4);
  comm_status = false;
  seq_start(go_home_all_motors, sizeof(go_home_all_motors)/sizeof(go_home_all_motors[0]));
}

static Action pid_experiment[] = { go_home_z_axis_motors_1, go_home_z_axis_motors_2, go_home_z_axis_motors_3, go_home_rotary_motor, pid_experiment_1, pid_experiment_2, pid_experiment_3, pid_experiment_4, pid_experiment_5 };

void halt_motors() {
  pid_control.SetMode(MANUAL);
  pid_status = false;

  seq_active = false;
  seq_index = 0;
  
  rotary_motor.rotate(0);
  right_z_axis_motor.rotate(0);
  left_z_axis_motor.rotate(0);
  manual_control_settings();
}

void ads_loop() {
  right_loadcell_adc_16bit = ads.readADC_SingleEnded(1);
  left_loadcell_adc_16bit = ads.readADC_SingleEnded(1);

  right_loadcell_volts_v = ads.computeVolts(right_loadcell_adc_16bit);
  left_loadcell_volts_v = ads.computeVolts(left_loadcell_adc_16bit);

  right_loadcell_load_lbf = right_loadcell_volts_v * cfg.right_loadcell_scale_factor - cfg.right_loadcell_zero_offset_lbf;
  left_loadcell_load_lbf = left_loadcell_volts_v * cfg.left_loadcell_scale_factor - cfg.left_loadcell_zero_offset_lbf;
  total_load_lbf = right_loadcell_load_lbf + left_loadcell_load_lbf;

  if ((right_loadcell_load_lbf + cfg.right_loadcell_zero_offset_lbf) >= cfg.right_loadcell_max_load_lbf 
      || (left_loadcell_load_lbf + cfg.left_loadcell_zero_offset_lbf) >= cfg.left_loadcell_max_load_lbf){
    halt_motors();
    comm_status = true;
    Serial.write((uint8_t*)"\xCC\x99\x00\xEE", 4);
    comm_status = false;
  }
}

void setup() {
  Serial.begin(115200);
  tmc_enable();
  ads.begin();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
}

void comm() {
  if (Serial.available() >= 2 && Serial.read() == 0xAA) {
    comm_status = true;
    uint8_t cmd = Serial.read();
    switch(cmd) {
      case 0x00: {//Connect
        Serial.write((uint8_t*)"\xCC\x00\x00\xEE", 4);
        delay(100);
        break;
      }
      case 0x01: {//Receive System Configurations
        String line = Serial.readStringUntil('\n');
        DeserializationError err = deserializeJson(doc, line);

        if (err) {
          Serial.write((uint8_t*)"\xCC\x01\x01\xEE", 4);
          return;
        }

        if (doc.overflowed()) {
          Serial.write((uint8_t*)"\xCC\x01\x02\xEE", 4);
          return;
        }

        JsonObject obj = doc.as<JsonObject>();

        cfg.manual_rotary_motor_speed_rpm = obj["manual_rotary_motor_speed_rpm"].as<float>();
        cfg.manual_rotary_motor_ramplen_step = obj["manual_rotary_motor_ramplen_step"].as<float>();
        cfg.manual_z_axis_motor_speed_rpm = obj["manual_z_axis_motor_speed_rpm"].as<float>();
        cfg.manual_z_axis_motor_ramplen_step = obj["manual_z_axis_motor_ramplen_step"].as<float>();
        
        cfg.pid_rotary_motor_ramplen_step = obj["pid_rotary_motor_ramplen_step"].as<float>();
        cfg.pid_z_axis_motor_max_speed_rpm = obj["pid_z_axis_motor_max_speed_rpm"].as<float>();
        cfg.pid_z_axis_motor_ramplen_step = obj["pid_z_axis_motor_ramplen_step"].as<float>();

        cfg.pid_calibration_stable_required_time_ms = obj["pid_calibration_stable_required_time_ms"].as<float>();
        cfg.pid_calibration_load_error_percent = obj["pid_calibration_load_error_percent"].as<float>();
        
        cfg.pid_tuning_mode_limit_percent = obj["pid_tuning_mode_limit_percent"].as<float>();
        cfg.pid_conservative_k_p = obj["pid_conservative_k_p"].as<float>();
        cfg.pid_conservative_k_i = obj["pid_conservative_k_i"].as<float>();
        cfg.pid_conservative_k_d = obj["pid_conservative_k_d"].as<float>();
        cfg.pid_aggressive_k_p = obj["pid_aggressive_k_p"].as<float>();
        cfg.pid_aggressive_k_i = obj["pid_aggressive_k_i"].as<float>();
        cfg.pid_aggressive_k_d = obj["pid_aggressive_k_d"].as<float>();
    
        cfg.go_home_z_axis_motors_bounce_step = obj["go_home_z_axis_motors_bounce_step"].as<float>();

        cfg.right_loadcell_zero_offset_lbf = obj["right_loadcell_zero_offset_lbf"].as<float>();
        cfg.right_loadcell_scale_factor = obj["right_loadcell_scale_factor"].as<float>();
        cfg.right_loadcell_max_load_lbf = obj["right_loadcell_max_load_lbf"].as<float>();
        cfg.left_loadcell_zero_offset_lbf = obj["left_loadcell_zero_offset_lbf"].as<float>();
        cfg.left_loadcell_scale_factor = obj["left_loadcell_scale_factor"].as<float>();
        cfg.left_loadcell_max_load_lbf = obj["left_loadcell_max_load_lbf"].as<float>();
        
        Serial.write((uint8_t*)"\xCC\x01\x00\xEE", 4);  
        delay(100);

        manual_control_settings();

        comm_status = false;
        break;
      }
      case 0x02: {//Disconnect
        // seq_start(go_home_all_motors, sizeof(go_home_all_motors)/sizeof(go_home_all_motors[0]));
        comm_status = false;
        break;
      }
      case 0x10: //halt_motors
        halt_motors();
        Serial.write((uint8_t*)"\xCC\x10\x00\xEE", 4);
        comm_status = false;
        break;
      case 0x11: //rotate_90deg_rotary_motor
        if (!motors_moving()) {
          manual_control_settings();
          rotary_motor.doSteps(rotary_motor_full_step_rev * 90 / 360);
          Serial.write((uint8_t*)"\xCC\x11\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x12: //go_home_rotary_motor
        if (!motors_moving()) {
          manual_control_settings();
          go_home_rotary_motor();
          Serial.write((uint8_t*)"\xCC\x12\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x13: //go_home_z_axis_motors
        if (!motors_moving()) {
          manual_control_settings();
          seq_start(go_home_z_axis_motors, sizeof(go_home_z_axis_motors)/sizeof(go_home_z_axis_motors[0]));
          Serial.write((uint8_t*)"\xCC\x13\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x14: //move_motors_by
        if (!motors_moving()) {
          manual_control_settings();

          move_motors_by_unit = Serial.read();

          if (Serial.readBytes((uint8_t*)&move_rotary_motor_by_deg, sizeof(move_rotary_motor_by_deg)) != sizeof(move_rotary_motor_by_deg)) {
            Serial.write((uint8_t*)"\xCC\x14\x01\xEE", 4);
            comm_status = false;
            return;
          }
          
          if (move_motors_by_unit == 0x00) {

            if (Serial.readBytes((uint8_t*)&move_right_z_axis_motor_by_step, sizeof(move_right_z_axis_motor_by_step)) != sizeof(move_right_z_axis_motor_by_step)) {
              Serial.write((uint8_t*)"\xCC\x14\x02\xEE", 4);
              comm_status = false;
            return;
            }

            if (Serial.readBytes((uint8_t*)&move_left_z_axis_motor_by_step, sizeof(move_left_z_axis_motor_by_step)) != sizeof(move_left_z_axis_motor_by_step)) {
              Serial.write((uint8_t*)"\xCC\x14\x03\xEE", 4);
              comm_status = false;
              return;
            }

            rotary_motor.doSteps(rotary_motor_full_step_rev * move_rotary_motor_by_deg / 360);
            right_z_axis_motor.doSteps(-move_right_z_axis_motor_by_step);
            left_z_axis_motor.doSteps(-move_left_z_axis_motor_by_step);
          }
          else if (move_motors_by_unit == 0x01) {

            if (Serial.readBytes((uint8_t*)&move_right_z_axis_motor_by_in, sizeof(move_right_z_axis_motor_by_in)) != sizeof(move_right_z_axis_motor_by_in)) {
              Serial.write((uint8_t*)"\xCC\x14\x04\xEE", 4);
              comm_status = false;
              return;
            }

            if (Serial.readBytes((uint8_t*)&move_left_z_axis_motor_by_in, sizeof(move_left_z_axis_motor_by_in)) != sizeof(move_left_z_axis_motor_by_in)) {
              Serial.write((uint8_t*)"\xCC\x14\x05\xEE", 4);
              comm_status = false;
              return;
            }

            rotary_motor.doSteps(rotary_motor_full_step_rev * move_rotary_motor_by_deg / 360);
            right_z_axis_motor.doSteps(-move_right_z_axis_motor_by_in * z_axis_motor_microstep / z_axis_motor_in_step);
            left_z_axis_motor.doSteps(-move_left_z_axis_motor_by_in * z_axis_motor_microstep / z_axis_motor_in_step);
          }
          else {
            Serial.write((uint8_t*)"\xCC\x14\x06\xEE", 4);
            comm_status = false;
            return;
          }
          Serial.write((uint8_t*)"\xCC\x14\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x15: //move_motors_to
        if (!motors_moving()) {
          manual_control_settings();

          move_motors_to_unit = Serial.read();

          if (Serial.readBytes((uint8_t*)&move_rotary_motor_to_deg, sizeof(move_rotary_motor_to_deg)) != sizeof(move_rotary_motor_to_deg)) {
            Serial.write((uint8_t*)"\xCC\x15\x01\xEE", 4);
            comm_status = false;
            return;
          }
          
          if (move_motors_to_unit == 0x00) {

            if (Serial.readBytes((uint8_t*)&move_right_z_axis_motor_to_step, sizeof(move_right_z_axis_motor_to_step)) != sizeof(move_right_z_axis_motor_to_step)) {
              Serial.write((uint8_t*)"\xCC\x15\x02\xEE", 4);
              comm_status = false;
              return;
            }

            if (Serial.readBytes((uint8_t*)&move_left_z_axis_motor_to_step, sizeof(move_left_z_axis_motor_to_step)) != sizeof(move_left_z_axis_motor_to_step)) {
              Serial.write((uint8_t*)"\xCC\x15\x03\xEE", 4);
              comm_status = false;
              return;
            }

            rotary_motor.writeSteps(rotary_motor_full_step_rev * move_rotary_motor_to_deg / 360);
            right_z_axis_motor.writeSteps(-move_right_z_axis_motor_to_step);
            left_z_axis_motor.writeSteps(-move_left_z_axis_motor_to_step);
          }
          else if (move_motors_to_unit == 0x01) {

            if (Serial.readBytes((uint8_t*)&move_right_z_axis_motor_to_in, sizeof(move_right_z_axis_motor_to_in)) != sizeof(move_right_z_axis_motor_to_in)) {
              Serial.write((uint8_t*)"\xCC\x15\x04\xEE", 4);
              comm_status = false;
              return;
            }

            if (Serial.readBytes((uint8_t*)&move_left_z_axis_motor_to_in, sizeof(move_left_z_axis_motor_to_in)) != sizeof(move_left_z_axis_motor_to_in)) {
              Serial.write((uint8_t*)"\xCC\x15\x05\xEE", 4);
              comm_status = false;
              return;
            }

            rotary_motor.writeSteps(rotary_motor_full_step_rev * move_rotary_motor_to_deg / 360);
            right_z_axis_motor.writeSteps(-move_right_z_axis_motor_to_in * z_axis_motor_microstep / z_axis_motor_in_step);
            left_z_axis_motor.writeSteps(-move_left_z_axis_motor_to_in * z_axis_motor_microstep / z_axis_motor_in_step);
          }
          else{
            Serial.write((uint8_t*)"\xCC\x15\x06\xEE", 4);
            comm_status = false;
            break;
          }
          Serial.write((uint8_t*)"\xCC\x15\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x16: //set_home_rotary_motor
        if (!motors_moving()) {
          rotary_motor.setZero();
          Serial.write((uint8_t*)"\xCC\x16\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x17: //set_home_right_z_axis_motor
        if (!motors_moving()) {
          right_z_axis_motor.setZero();
          Serial.write((uint8_t*)"\xCC\x17\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x18: //set_home_left_z_axis_motor
        if (!motors_moving()) {
          left_z_axis_motor.setZero();
          Serial.write((uint8_t*)"\xCC\x18\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x20: //pid_experiment
        if (!motors_moving()) {
          
          pid_rotary_motor_direction = Serial.read();

          if (Serial.readBytes((uint8_t*)&pid_rotary_motor_speed_rpm, sizeof(pid_rotary_motor_speed_rpm)) != sizeof(pid_rotary_motor_speed_rpm)) {
            Serial.write((uint8_t*)"\xCC\x20\x01\xEE", 4);
            comm_status = false;
            return;
          }

          if (Serial.readBytes((uint8_t*)&pid_experiment_target_load_lbf, sizeof(pid_experiment_target_load_lbf)) != sizeof(pid_experiment_target_load_lbf)) {
            Serial.write((uint8_t*)"\xCC\x20\x02\xEE", 4);
            comm_status = false;
            return;
          }

          if (Serial.readBytes((uint8_t*)&pid_experiment_duration_ms, sizeof(pid_experiment_duration_ms)) != sizeof(pid_experiment_duration_ms)) {
            Serial.write((uint8_t*)"\xCC\x20\x03\xEE", 4);
            comm_status = false;
            return;
          }
          seq_start(pid_experiment, sizeof(pid_experiment)/sizeof(pid_experiment[0]));
          Serial.write((uint8_t*)"\xCC\x20\x00\xEE", 4);
        }
        comm_status = false;
        break;
      case 0x21: //pid_experiment_terminate
        manual_control_settings();
        halt_motors();
        seq_start(go_home_all_motors, sizeof(go_home_all_motors)/sizeof(go_home_all_motors[0]));
        Serial.write((uint8_t*)"\xCC\x21\x00\xEE", 4);
        comm_status = false;
        break;
      default:
        break;
    }
  }
}

void send_data() {

  String data;

  data += char(0xDD);

  rotary_motor_speed_step_s = rotary_motor.getSpeedSteps() / 10.00f;
  data += String(rotary_motor_speed_step_s);
  data += ",";

  rotary_motor_speed_rpm = rotary_motor_speed_step_s * 60.00f / rotary_motor_full_step_rev;
  data += String(rotary_motor_speed_rpm);
  data += ",";

  rotary_motor_position_deg = ((rotary_motor.read() % 360) + 360) % 360;
  data += String(rotary_motor_position_deg);
  data += ",";

  right_z_axis_motor_speed_step_s = -right_z_axis_motor.getSpeedSteps() / 10.00f;
  data += String(right_z_axis_motor_speed_step_s);
  data += ",";

  right_z_axis_motor_speed_rpm = right_z_axis_motor_speed_step_s * 60.00f / z_axis_motor_full_step_rev;
  data += String(right_z_axis_motor_speed_rpm);
  data += ",";

  right_z_axis_motor_position_step = -right_z_axis_motor.readSteps();
  data += String(right_z_axis_motor_position_step);
  data += ",";

  right_z_axis_motor_position_in = right_z_axis_motor_position_step * z_axis_motor_in_step / z_axis_motor_microstep;
  data += String(right_z_axis_motor_position_in);
  data += ",";

  left_z_axis_motor_speed_step_s = -left_z_axis_motor.getSpeedSteps() / 10.00f;
  data += String(left_z_axis_motor_speed_step_s);
  data += ",";

  left_z_axis_motor_speed_rpm = left_z_axis_motor_speed_step_s * 60.00f / z_axis_motor_full_step_rev;
  data += String(left_z_axis_motor_speed_rpm);
  data += ",";

  left_z_axis_motor_position_step = -left_z_axis_motor.readSteps();
  data += String(left_z_axis_motor_position_step);
  data += ","; 

  left_z_axis_motor_position_in = left_z_axis_motor_position_step * z_axis_motor_in_step / z_axis_motor_microstep;
  data += String(left_z_axis_motor_position_in);
  data += ",";

  passive_roller_position_step = (right_z_axis_motor_position_step + left_z_axis_motor_position_step) / 2;
  data += String(passive_roller_position_step);
  data += ",";

  passive_roller_position_in = (right_z_axis_motor_position_in + left_z_axis_motor_position_in) / 2.00f;
  data += String(passive_roller_position_in);
  data += ",";

  data += String(right_loadcell_adc_16bit);
  data += ",";

  data += String(right_loadcell_volts_v);
  data += ",";

  data += String(right_loadcell_load_lbf);
  data += ",";

  data += String(left_loadcell_adc_16bit);
  data += ",";

  data += String(left_loadcell_volts_v);
  data += ",";

  data += String(left_loadcell_load_lbf);
  data += ",";

  data += String(total_load_lbf);
  data += ",";

  //total_revolution_rev = fabs((rotary_motor.readSteps() - rotary_motor_initial_position_step) / rotary_motor_full_step_rev);
  total_revolution_rev = fabs((rotary_motor.read() - rotary_motor_initial_position_deg) / 360.00f);
  data += String(total_revolution_rev);
  data += ",";

  if (pid_control.GetKp() == cfg.pid_conservative_k_p){
    pid_tuning_mode = 0;
  } else {
    pid_tuning_mode = 1;
  }

  data += String(pid_tuning_mode);
  data += ",";

  data += String(pid_overshoot_lbf);
  data += ",";

  data += String(pid_overshoot_percent);
  data += ",";

  data += String(pid_settling_time_s);
  data += ",";

  data += String(pid_load_error_running_avg_percent);
  data += ",";

  data += String(thermocouple_flow_temperature_c);
  
  data += char(0xEE);

  Serial.write((const uint8_t*)data.c_str(), data.length());

  delay(100);
}

void loop() {

  comm();
  ads_loop();
  if (!comm_status) send_data();
  yield();

  if (!seq_active) return;

  if (pid_status) {
    seq_actions[seq_index]();
  }
  else {
    if (!motors_moving()) {
      seq_index++;
      if (seq_index < seq_count) {
        seq_actions[seq_index]();
      } else {
        seq_active = false;
        seq_index   = 0;
      }
    }
  }
}
