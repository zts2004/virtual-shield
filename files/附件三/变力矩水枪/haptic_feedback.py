#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import numpy as np

class HapticController:
    def __init__(self):
        # LRA马达PWM引脚定义
        self.LRA_PINS = [12, 13, 19, 26]  # 4个LRA马达的控制引脚
        self.PWM_FREQ = 200  # PWM基础频率
        
        # 初始化PWM控制器
        self.pwm_controllers = []
        for pin in self.LRA_PINS:
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, self.PWM_FREQ)
            pwm.start(0)
            self.pwm_controllers.append(pwm)
            
        self.is_running = True
        
    def set_vibration(self, motor_id, intensity, frequency):
        """设置指定马达的振动强度和频率"""
        if 0 <= motor_id < len(self.pwm_controllers):
            # 更新PWM频率
            self.pwm_controllers[motor_id].ChangeFrequency(frequency)
            # 更新占空比(强度)
            self.pwm_controllers[motor_id].ChangeDutyCycle(intensity)
            
    def generate_vibration_pattern(self, water_pressure):
        """根据水压生成振动模式"""
        # 水压范围假定为0-100
        base_intensity = water_pressure * 0.8  # 基础强度
        base_frequency = 50 + water_pressure  # 基础频率
        
        # 为每个马达生成略微不同的参数
        patterns = []
        for i in range(len(self.LRA_PINS)):
            # 添加随机变化使振动更自然
            intensity = min(100, base_intensity * (0.8 + 0.4 * np.random.random()))
            frequency = base_frequency * (0.9 + 0.2 * np.random.random())
            patterns.append((intensity, frequency))
            
        return patterns
        
    def run(self):
        """运行振动控制循环"""
        while self.is_running:
            try:
                # 模拟水压变化(实际应从传感器获取)
                water_pressure = 50 + 30 * np.sin(time.time() * 0.5)
                
                # 生成振动模式
                patterns = self.generate_vibration_pattern(water_pressure)
                
                # 应用振动模式
                for i, (intensity, frequency) in enumerate(patterns):
                    self.set_vibration(i, intensity, frequency)
                    
                time.sleep(0.05)  # 控制更新频率
                
            except Exception as e:
                print(f"触觉反馈控制错误: {e}")
                time.sleep(1)
                
    def stop(self):
        """停止所有振动"""
        self.is_running = False
        for pwm in self.pwm_controllers:
            pwm.stop() 