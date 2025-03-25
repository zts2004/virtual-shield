#!/usr/bin/env python3
import time
import signal
import sys
from motor_controller import MotorController
from vibration_patterns import get_pattern

class VibrationControl:
    def __init__(self):
        """
        初始化振动控制系统
        """
        # 创建马达控制器实例
        self.motor = MotorController()
        self.running = True
        
        # 注册信号处理函数
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """
        处理退出信号
        """
        print("\n正在停止振动控制系统...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """
        清理资源
        """
        if hasattr(self, 'motor'):
            self.motor.cleanup()
    
    def run_tool(self, tool_type, intensity='normal'):
        """
        运行指定工具的振动模式
        :param tool_type: 工具类型（'saw' 或 'chainsaw'）
        :param intensity: 强度级别（'idle', 'normal', 或 'heavy'）
        """
        try:
            pattern = get_pattern(tool_type, intensity)
            print(f"正在模拟 {tool_type} 的振动，强度级别：{intensity}")
            print(f"频率：{pattern['frequency']}Hz，功率：{pattern['power_level']}%")
            
            self.motor.simulate_tool(tool_type, pattern['power_level'])
            
        except ValueError as e:
            print(f"错误：{str(e)}")
            self.cleanup()
            sys.exit(1)

def main():
    """
    主程序入口
    """
    control = VibrationControl()
    
    print("振动控制系统已启动")
    print("可用工具：saw（无齿锯）, chainsaw（手提链锯）")
    print("强度级别：idle（怠速）, normal（正常）, heavy（重负载）")
    
    try:
        while control.running:
            tool = input("\n请选择工具类型 (saw/chainsaw): ").lower()
            if tool not in ['saw', 'chainsaw']:
                print("无效的工具类型，请重试")
                continue
            
            intensity = input("请选择强度级别 (idle/normal/heavy): ").lower()
            if intensity not in ['idle', 'normal', 'heavy']:
                print("无效的强度级别，请重试")
                continue
            
            control.run_tool(tool, intensity)
            
            # 运行5秒后询问是否继续
            time.sleep(5)
            response = input("\n是否继续？(y/n): ").lower()
            if response != 'y':
                break
    
    except KeyboardInterrupt:
        pass
    finally:
        control.cleanup()
        print("\n振动控制系统已停止")

if __name__ == "__main__":
    main() 