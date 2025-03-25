#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import threading
from motor_control import MotorController
from haptic_feedback import HapticController
from temp_control import TemperatureController
import config

class FirehoseController:
    def __init__(self):
        # 初始化GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # 初始化各个控制器
        self.motor_controller = MotorController()
        self.haptic_controller = HapticController()
        self.temp_controller = TemperatureController()
        
        # 运行状态标志
        self.is_running = True
        
    def start(self):
        """启动所有控制系统"""
        try:
            # 创建独立线程运行各个控制系统
            motor_thread = threading.Thread(target=self.motor_controller.run)
            haptic_thread = threading.Thread(target=self.haptic_controller.run)
            temp_thread = threading.Thread(target=self.temp_controller.run)
            
            # 启动线程
            motor_thread.start()
            haptic_thread.start()
            temp_thread.start()
            
            # 主循环
            while self.is_running:
                # 监控系统状态
                print("系统运行中...")
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """停止所有系统"""
        self.is_running = False
        self.motor_controller.stop()
        self.haptic_controller.stop()
        self.temp_controller.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    controller = FirehoseController()
    controller.start() 