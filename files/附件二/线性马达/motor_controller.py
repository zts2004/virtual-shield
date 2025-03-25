import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, ena_pin=18, in1_pin=23, in2_pin=24):
        """
        初始化马达控制器
        :param ena_pin: PWM控制引脚
        :param in1_pin: 方向控制引脚1
        :param in2_pin: 方向控制引脚2
        """
        # 设置GPIO模式为BCM
        GPIO.setmode(GPIO.BCM)
        
        # 保存引脚配置
        self.ena_pin = ena_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        
        # 设置引脚为输出模式
        GPIO.setup(self.ena_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        
        # 创建PWM对象，频率设置为1000Hz
        self.pwm = GPIO.PWM(self.ena_pin, 1000)
        self.pwm.start(0)
        
        # 初始化停止状态
        self.stop()
    
    def set_vibration(self, frequency, duty_cycle):
        """
        设置振动频率和强度
        :param frequency: 振动频率（Hz）
        :param duty_cycle: PWM占空比（0-100）
        """
        # 更新PWM频率
        self.pwm.ChangeFrequency(frequency)
        # 设置占空比（控制振动强度）
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        # 设置正向旋转
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
    
    def stop(self):
        """
        停止马达
        """
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
    
    def cleanup(self):
        """
        清理GPIO设置
        """
        self.stop()
        self.pwm.stop()
        GPIO.cleanup()
    
    def simulate_tool(self, tool_type, power_level):
        """
        模拟特定工具的振动
        :param tool_type: 工具类型（'saw' 或 'chainsaw'）
        :param power_level: 功率级别（0-100）
        """
        if tool_type == 'saw':
            # 无齿锯的振动参数（频率范围：80-120Hz）
            base_frequency = 80
            frequency = base_frequency + (power_level * 0.4)  # 最大120Hz
            duty_cycle = min(power_level * 0.8, 100)  # 控制振动强度
        
        elif tool_type == 'chainsaw':
            # 手提链锯的振动参数（频率范围：100-150Hz）
            base_frequency = 100
            frequency = base_frequency + (power_level * 0.5)  # 最大150Hz
            duty_cycle = min(power_level * 0.9, 100)  # 控制振动强度
        
        else:
            raise ValueError("不支持的工具类型")
        
        self.set_vibration(frequency, duty_cycle) 