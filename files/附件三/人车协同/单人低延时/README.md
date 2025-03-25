# 树莓派小车控制系统

这是一个基于Web的树莓派小车控制系统，提供低延迟的实时控制功能。

## 功能特点

- 实时方向控制（前进、后退、左转、右转）
- 紧急停止功能
- 实时状态监控（位置、速度、电量）
- 低延迟指令传输（<50ms）
- 优先级指令处理
- 实时状态同步

## 技术栈

### 前端
- React.js
- WebSocket
- CSS3 (Flexbox/Grid)
- HTML5

### 后端
- Node.js
- Express
- WebSocket
- UDP/TCP Socket

## 项目结构

```
├── client/                 # 前端React应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── services/      # WebSocket服务
│   │   └── styles/        # CSS样式文件
│   └── public/            # 静态资源
├── server/                 # 后端Node.js服务
│   ├── src/
│   │   ├── controllers/   # 控制器
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   └── config/            # 配置文件
└── README.md              # 项目文档
```

## 安装和运行

1. 安装依赖
```bash
# 安装前端依赖
cd client
npm install

# 安装后端依赖
cd ../server
npm install
```

2. 运行应用
```bash
# 启动后端服务
cd server
npm start

# 启动前端开发服务器
cd client
npm start
```

## 端口配置

- 前端开发服务器：3000
- 后端WebSocket服务：5000 (UDP), 6000 (TCP)

## 数据格式

### 控制指令格式
```json
{
  "user_id": "User01",
  "command": "move_forward",
  "timestamp": 1630000000,
  "priority": 1
}
```

### 状态数据格式
```json
{
  "position": {"x": 100, "y": 200},
  "speed": 0.5,
  "battery": 80
}
``` 