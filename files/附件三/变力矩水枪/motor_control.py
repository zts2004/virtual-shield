#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import smbus
import math

class MotorController:
    def __init__(self):
        # 步进电机引脚定义
        self.STEP_PIN = 17
        self.DIR_PIN = 18
        self.EN_PIN = 27
        
        # MPU6050地址
        self.MPU_ADDR = 0x68
        self.bus = smbus.SMBus(1)
        
        # 初始化MPU6050
        self.init_mpu6050()
        
        # 初始化步进电机引脚
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.EN_PIN, GPIO.OUT)
        
        self.is_running = True
        
    def init_mpu6050(self):
        """初始化MPU6050陀螺仪"""
        # 唤醒MPU6050
        self.bus.write_byte_data(self.MPU_ADDR, 0x6B, 0)
        
    def read_gyro_data(self):
        """读取陀螺仪数据"""
        # 读取角速度数据
        gyro_x = self.bus.read_word_data(self.MPU_ADDR, 0x43)
        gyro_y = self.bus.read_word_data(self.MPU_ADDR, 0x45)
        gyro_z = self.bus.read_word_data(self.MPU_ADDR, 0x47)
        
        # 转换为实际角速度值
        gyro_x = gyro_x / 131.0
        gyro_y = gyro_y / 131.0
        gyro_z = gyro_z / 131.0
        
        return (gyro_x, gyro_y, gyro_z)
        
    def calculate_recoil_force(self, gyro_data):
        """根据陀螺仪数据计算反作用力"""
        # 简化的反作用力计算模型
        force = math.sqrt(sum([x*x for x in gyro_data]))
        return min(100, force)  # 限制最大力为100N
        
    def control_motor(self, force):
        """控制步进电机运动"""
        # 根据力的大小调整步进电机速度
        delay = max(0.001, 0.01 - force/1000)  # 力越大,转速越快
        
        # 设置方向
        GPIO.output(self.DIR_PIN, force > 50)  # 力超过50N时改变方向
        
        # 输出一个脉冲
        GPIO.output(self.STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.STEP_PIN, GPIO.LOW)
        time.sleep(delay)
        
    def run(self):
        """运行控制循环"""
        while self.is_running:
            try:
                # 读取陀螺仪数据
                gyro_data = self.read_gyro_data()
                
                # 计算反作用力
                force = self.calculate_recoil_force(gyro_data)
                
                # 控制电机
                self.control_motor(force)
                
            except Exception as e:
                print(f"步进电机控制错误: {e}")
                time.sleep(1)
                
    def stop(self):
        """停止控制"""
        self.is_running = False
        GPIO.output(self.EN_PIN, GPIO.HIGH)  # 禁用电机 