#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 系统配置参数
SYSTEM_CONFIG = {
    # 步进电机参数
    'MOTOR': {
        'MAX_SPEED': 1000,  # 最大转速(步/秒)
        'MIN_SPEED': 100,   # 最小转速(步/秒)
        'ACCELERATION': 50,  # 加速度(步/秒²)
    },
    
    # 触觉反馈参数
    'HAPTIC': {
        'MIN_FREQ': 50,     # 最小振动频率(Hz)
        'MAX_FREQ': 200,    # 最大振动频率(Hz)
        'MIN_INTENSITY': 0, # 最小振动强度(%)
        'MAX_INTENSITY': 100 # 最大振动强度(%)
    },
    
    # 温度控制参数
    'TEMP': {
        'MIN_TEMP': -10,    # 最低温度(°C)
        'MAX_TEMP': 60,     # 最高温度(°C)
        'DEFAULT_TEMP': 25, # 默认目标温度(°C)
        'TEMP_TOLERANCE': 0.5 # 温度控制精度(°C)
    },
    
    # 水压参数
    'PRESSURE': {
        'MIN_PRESSURE': 0,  # 最小水压(Bar)
        'MAX_PRESSURE': 10, # 最大水压(Bar)
        'PRESSURE_STEPS': 100 # 水压分段数
    }
} 