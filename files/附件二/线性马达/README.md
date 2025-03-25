# 线性马达振动反馈控制系统

本项目用于控制树莓派上的线性震动马达，模拟无齿锯和手提链锯等工具的振动反馈。

## 功能特点
- 支持多种工具振动模式（无齿锯、手提链锯）
- 可调节振动频率和强度
- 实时响应控制
- 支持预设振动模式

## 硬件要求
- 树莓派（支持 3B+ 或更新版本）
- 线性震动马达
- L298N 电机驱动模块（用于控制马达）

## 接线说明
1. 线性震动马达连接到 L298N 驱动模块
2. L298N 模块连接到树莓派的 GPIO 引脚：
   - ENA -> GPIO18 (PWM)
   - IN1 -> GPIO23
   - IN2 -> GPIO24
   - GND -> GND

## 使用方法
1. 安装依赖：
```bash
pip install RPi.GPIO
```

2. 运行程序：
```bash
python vibration_control.py
```

## 文件结构
- `vibration_control.py`: 主程序文件
- `vibration_patterns.py`: 预设振动模式配置
- `motor_controller.py`: 马达控制类

## 注意事项
1. 使用前请确保正确连接硬件
2. 运行程序需要 root 权限
3. 请勿超过马达的额定电压和电流 