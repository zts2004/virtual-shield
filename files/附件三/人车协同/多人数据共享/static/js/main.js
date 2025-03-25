// 初始化WebSocket连接
const socket = io();

// DOM元素
const conflictPanel = document.getElementById('conflict-panel');
const conflictValue = document.getElementById('conflict-value');
const commandValue = document.getElementById('command-value');
const currentUser = document.getElementById('current-user');

// 控制按钮事件监听
document.querySelectorAll('.control-btn').forEach(button => {
    button.addEventListener('click', () => {
        const action = button.id;
        sendCommand(action);
    });
});

// 坐标控制
document.getElementById('go-to-coord').addEventListener('click', () => {
    const x = parseFloat(document.getElementById('x-coord').value);
    const y = parseFloat(document.getElementById('y-coord').value);
    
    if (isNaN(x) || isNaN(y)) {
        alert('请输入有效的坐标值');
        return;
    }
    
    sendCommand('move_to', { x, y });
});

// 投票按钮事件监听
document.querySelectorAll('.vote-btn').forEach(button => {
    button.addEventListener('click', () => {
        const vote = button.dataset.vote;
        const commandId = conflictPanel.dataset.commandId;
        sendVote(commandId, vote);
    });
});

// 发送命令
function sendCommand(action, data = {}) {
    socket.emit('send_command', {
        action,
        ...data
    });
}

// 发送投票
function sendVote(commandId, vote) {
    socket.emit('vote', {
        command_id: commandId,
        vote: vote
    });
    conflictPanel.style.display = 'none';
}

// WebSocket事件处理
socket.on('connect', () => {
    console.log('WebSocket连接已建立');
    commandValue.textContent = '已连接';
});

socket.on('disconnect', () => {
    console.log('WebSocket连接已断开');
    commandValue.textContent = '未连接';
});

socket.on('conflict_detected', (data) => {
    conflictValue.textContent = '检测到冲突';
    conflictPanel.dataset.commandId = data.command_id;
    conflictPanel.style.display = 'block';
});

socket.on('command_executed', (data) => {
    commandValue.textContent = `指令已执行 (用户: ${data.user})`;
    conflictValue.textContent = '无';
});

socket.on('error', (error) => {
    console.error('WebSocket错误:', error);
    commandValue.textContent = '错误';
});

// 键盘控制
document.addEventListener('keydown', (event) => {
    switch(event.key) {
        case 'ArrowUp':
            sendCommand('forward');
            break;
        case 'ArrowDown':
            sendCommand('backward');
            break;
        case 'ArrowLeft':
            sendCommand('left');
            break;
        case 'ArrowRight':
            sendCommand('right');
            break;
        case ' ':
            sendCommand('stop');
            break;
    }
}); 