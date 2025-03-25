#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import os
import glob

class TemperatureController:
    def __init__(self):
        # TEC控制引脚
        self.TEC_PIN = 20  # PWM控制引脚
        self.TEC_EN_PIN = 21  # 使能引脚
        
        # 温度传感器设置
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.TEMP_SENSOR_PATH = '/sys/bus/w1/devices/28-*'
        self.device_file = glob.glob(self.TEMP_SENSOR_PATH)[0] + '/w1_slave'
        
        # 初始化GPIO
        GPIO.setup(self.TEC_PIN, GPIO.OUT)
        GPIO.setup(self.TEC_EN_PIN, GPIO.OUT)
        
        # 初始化PWM控制
        self.pwm = GPIO.PWM(self.TEC_PIN, 100)  # 100Hz PWM频率
        self.pwm.start(0)
        
        # PID控制参数
        self.Kp = 5.0
        self.Ki = 0.2
        self.Kd = 1.0
        self.last_error = 0
        self.integral = 0
        
        self.is_running = True
        
    def read_temp(self):
        """读取温度传感器数据"""
        try:
            with open(self.device_file, 'r') as f:
                lines = f.readlines()
            if lines[0].strip()[-3:] == 'YES':
                temp_pos = lines[1].find('t=')
                if temp_pos != -1:
                    temp_str = lines[1][temp_pos+2:]
                    temp = float(temp_str) / 1000.0  # 转换为摄氏度
                    return temp
        except Exception as e:
            print(f"温度读取错误: {e}")
        return 25.0  # 错误时返回默认值
        
    def pid_control(self, current_temp, target_temp):
        """PID温度控制算法"""
        error = target_temp - current_temp
        self.integral += error
        derivative = error - self.last_error
        
        # 计算PID输出
        output = (self.Kp * error + 
                 self.Ki * self.integral + 
                 self.Kd * derivative)
        
        # 限制输出范围在0-100之间
        output = max(0, min(100, output))
        
        self.last_error = error
        return output
        
    def set_temperature(self, temp, power):
        """设置TEC工作状态"""
        # 根据目标温度决定制冷或加热模式
        GPIO.output(self.TEC_EN_PIN, GPIO.HIGH if power > 0 else GPIO.LOW)
        self.pwm.ChangeDutyCycle(abs(power))
        
    def run(self):
        """运行温度控制循环"""
        while self.is_running:
            try:
                # 读取当前温度
                current_temp = self.read_temp()
                
                # 根据水压和环境条件计算目标温度(示例)
                target_temp = 25  # 这里可以根据实际需求动态调整
                
                # 计算控制输出
                power = self.pid_control(current_temp, target_temp)
                
                # 控制TEC
                self.set_temperature(target_temp, power)
                
                # 打印状态信息
                print(f"当前温度: {current_temp:.1f}°C, 目标温度: {target_temp}°C, 输出功率: {power:.1f}%")
                
                time.sleep(0.5)  # 控制更新频率
                
            except Exception as e:
                print(f"温度控制错误: {e}")
                time.sleep(1)
                
    def stop(self):
        """停止温度控制"""
        self.is_running = False
        self.pwm.stop()
        GPIO.output(self.TEC_EN_PIN, GPIO.LOW) 