#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
import struct
import sys
import argparse

def send_packets(host, port, num_packets=100):
    """
    发送UDP数据包并记录时间戳
    :param host: 目标主机IP
    :param port: 目标端口
    :param num_packets: 发送数据包数量
    """
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"开始发送{num_packets}个UDP数据包到 {host}:{port}")
    
    for i in range(num_packets):
        # 获取当前时间戳（微秒级精度）
        timestamp = int(time.time() * 1000000)
        
        # 将时间戳打包成字节流
        data = struct.pack('!Q', timestamp)
        
        try:
            # 发送数据包
            sock.sendto(data, (host, port))
            print(f"发送第 {i+1} 个数据包，时间戳: {timestamp}")
            
            # 短暂延时，避免发送过快
            time.sleep(0.01)
            
        except Exception as e:
            print(f"发送数据包时出错: {e}")
            break
    
    print("发送完成")
    sock.close()

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='UDP延时测试发送端')
    parser.add_argument('--host', default='127.0.0.1', help='目标主机IP地址')
    parser.add_argument('--port', type=int, default=5000, help='目标端口号')
    parser.add_argument('--num', type=int, default=100, help='发送数据包数量')
    
    args = parser.parse_args()
    
    # 发送数据包
    send_packets(args.host, args.port, args.num)

if __name__ == '__main__':
    main() 