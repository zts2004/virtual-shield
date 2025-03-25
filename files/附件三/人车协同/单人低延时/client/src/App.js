import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './App.css';

// WebSocket连接
const socket = io('http://localhost:5000');

function App() {
  // 状态管理
  const [carStatus, setCarStatus] = useState({
    position: { x: 0, y: 0 },
    speed: 0,
    battery: 100
  });

  // 发送控制指令
  const sendCommand = (command, priority = 0) => {
    const message = {
      user_id: "User01",
      command: command,
      timestamp: Date.now(),
      priority: priority
    };
    socket.emit('command', message);
  };

  // 监听状态更新
  useEffect(() => {
    socket.on('status', (status) => {
      setCarStatus(status);
    });

    return () => {
      socket.off('status');
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>树莓派小车控制系统</h1>
      </header>
      
      <main className="control-panel">
        {/* 状态显示面板 */}
        <div className="status-panel">
          <h2>实时状态</h2>
          <div className="status-info">
            <p>位置: ({carStatus.position.x}, {carStatus.position.y})</p>
            <p>速度: {carStatus.speed} m/s</p>
            <p>电量: {carStatus.battery}%</p>
          </div>
        </div>

        {/* 控制按钮 */}
        <div className="control-buttons">
          <button onClick={() => sendCommand('move_forward')}>前进</button>
          <button onClick={() => sendCommand('move_backward')}>后退</button>
          <button onClick={() => sendCommand('turn_left')}>左转</button>
          <button onClick={() => sendCommand('turn_right')}>右转</button>
          <button 
            className="emergency-stop"
            onClick={() => sendCommand('emergency_stop', 1)}
          >
            急停
          </button>
        </div>
      </main>
    </div>
  );
}

export default App; 