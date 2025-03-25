const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const dgram = require('dgram');
const net = require('net');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// 创建UDP服务器用于接收指令
const udpServer = dgram.createSocket('udp4');
udpServer.bind(5000);

// 创建TCP服务器用于广播状态
const tcpServer = net.createServer();
tcpServer.listen(6000);

// 存储所有连接的客户端
const clients = new Set();

// 优先级队列
const commandQueue = [];

// 模拟小车状态
let carStatus = {
  position: { x: 0, y: 0 },
  speed: 0,
  battery: 100
};

// WebSocket连接处理
io.on('connection', (socket) => {
  console.log('新客户端连接');
  clients.add(socket);

  // 处理控制指令
  socket.on('command', (command) => {
    // 将指令添加到优先级队列
    if (command.priority === 1) {
      commandQueue.unshift(command);
    } else {
      commandQueue.push(command);
    }
    
    // 通过UDP发送指令
    const message = Buffer.from(JSON.stringify(command));
    udpServer.send(message, 0, message.length, 5000, 'localhost');
  });

  socket.on('disconnect', () => {
    console.log('客户端断开连接');
    clients.delete(socket);
  });
});

// UDP消息处理
udpServer.on('message', (msg, rinfo) => {
  console.log(`收到UDP消息: ${msg}`);
});

// TCP连接处理
tcpServer.on('connection', (socket) => {
  console.log('新的TCP连接');
  
  // 每50ms发送一次状态更新
  const statusInterval = setInterval(() => {
    socket.write(JSON.stringify(carStatus) + '\n');
  }, 50);

  socket.on('close', () => {
    clearInterval(statusInterval);
    console.log('TCP连接关闭');
  });
});

// 启动服务器
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
}); 