#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
import struct
import statistics
import argparse
from datetime import datetime

def receive_packets(host, port, num_packets=100):
    """
    接收UDP数据包并计算延时
    :param host: 监听主机IP
    :param port: 监听端口
    :param num_packets: 预期接收数据包数量
    """
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 绑定地址和端口
    sock.bind((host, port))
    print(f"开始监听 {host}:{port}")
    
    # 存储延时数据
    latencies = []
    received_count = 0
    
    try:
        while received_count < num_packets:
            # 接收数据包
            data, addr = sock.recvfrom(1024)
            
            # 获取接收时间戳（微秒级精度）
            receive_time = int(time.time() * 1000000)
            
            # 解析发送时间戳
            send_time = struct.unpack('!Q', data)[0]
            
            # 计算延时（微秒）
            latency = receive_time - send_time
            
            # 记录延时数据
            latencies.append(latency)
            received_count += 1
            
            print(f"接收第 {received_count} 个数据包，延时: {latency} 微秒")
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        sock.close()
    
    # 计算统计信息
    if latencies:
        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
        packet_loss = ((num_packets - received_count) / num_packets) * 100
        
        print("\n统计信息:")
        print(f"总发送包数: {num_packets}")
        print(f"成功接收包数: {received_count}")
        print(f"丢包率: {packet_loss:.2f}%")
        print(f"平均延时: {avg_latency:.2f} 微秒")
        print(f"最大延时: {max_latency:.2f} 微秒")
        print(f"最小延时: {min_latency:.2f} 微秒")
        print(f"标准差: {std_dev:.2f} 微秒")
        
        # 保存结果到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"latency_test_{timestamp}.txt"
        with open(filename, 'w') as f:
            f.write(f"测试时间: {datetime.now()}\n")
            f.write(f"总发送包数: {num_packets}\n")
            f.write(f"成功接收包数: {received_count}\n")
            f.write(f"丢包率: {packet_loss:.2f}%\n")
            f.write(f"平均延时: {avg_latency:.2f} 微秒\n")
            f.write(f"最大延时: {max_latency:.2f} 微秒\n")
            f.write(f"最小延时: {min_latency:.2f} 微秒\n")
            f.write(f"标准差: {std_dev:.2f} 微秒\n")
            f.write("\n详细延时数据:\n")
            for i, latency in enumerate(latencies, 1):
                f.write(f"包 {i}: {latency} 微秒\n")
        
        print(f"\n详细结果已保存到文件: {filename}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='UDP延时测试接收端')
    parser.add_argument('--host', default='0.0.0.0', help='监听主机IP地址')
    parser.add_argument('--port', type=int, default=5000, help='监听端口号')
    parser.add_argument('--num', type=int, default=100, help='预期接收数据包数量')
    
    args = parser.parse_args()
    
    # 接收数据包
    receive_packets(args.host, args.port, args.num)

if __name__ == '__main__':
    main() 