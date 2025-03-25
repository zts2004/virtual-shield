# UDP网络延时测试工具

这是一个用于测试网络延时的UDP工具，包含发送端和接收端两个程序。

## 项目结构
- `udp_sender.py`: 发送端程序
- `udp_receiver.py`: 接收端程序
- `requirements.txt`: 项目依赖文件

## 使用说明

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行接收端（在树莓派上）：
```bash
python udp_receiver.py
```

3. 运行发送端（在测试机器上）：
```bash
python udp_sender.py
```

## 功能说明
- 发送端会发送100个UDP数据包
- 每个数据包包含发送时间戳
- 接收端记录接收时间并计算延时
- 最终输出统计信息，包括：
  - 平均延时
  - 最大延时
  - 最小延时
  - 标准差
  - 丢包率

## 注意事项
- 确保两台机器在同一局域网内
- 确保防火墙允许UDP通信
- 建议使用Wireshark进行抓包分析 