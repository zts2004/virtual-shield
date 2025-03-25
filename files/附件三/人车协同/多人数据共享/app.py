from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from datetime import datetime
import math
import json

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 数据模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    commands = db.relationship('Command', backref='user', lazy=True)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, executed, conflicted

# 冲突检测函数
def check_conflict(cmd1, cmd2):
    # 计算距离
    distance = math.sqrt((cmd1.x - cmd2.x)**2 + (cmd1.y - cmd2.y)**2)
    
    # 计算时间差（毫秒）
    time_diff = abs((cmd1.timestamp - cmd2.timestamp).total_seconds() * 1000)
    
    # 检查是否冲突
    return (distance <= app.config['CONFLICT_DISTANCE_THRESHOLD'] and 
            time_diff <= app.config['CONFLICT_TIME_THRESHOLD'])

# 冲突解决策略
def resolve_conflict(commands):
    # 1. 优先级覆盖
    admin_cmd = next((cmd for cmd in commands if cmd.user.is_admin), None)
    if admin_cmd:
        return admin_cmd
    
    # 2. 时间戳仲裁
    latest_cmd = max(commands, key=lambda x: x.timestamp)
    return latest_cmd

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 实现登录逻辑
        pass
    return render_template('login.html')

@socketio.on('send_command')
@login_required
def handle_command(data):
    # 创建新命令
    new_cmd = Command(
        x=data['x'],
        y=data['y'],
        action=data['action'],
        user_id=current_user.id
    )
    db.session.add(new_cmd)
    
    # 检查冲突
    pending_cmds = Command.query.filter_by(status='pending').all()
    conflicts = [cmd for cmd in pending_cmds if check_conflict(new_cmd, cmd)]
    
    if conflicts:
        # 触发投票
        emit('conflict_detected', {
            'command_id': new_cmd.id,
            'conflicts': [cmd.id for cmd in conflicts]
        }, broadcast=True)
    else:
        # 直接执行
        new_cmd.status = 'executed'
        db.session.commit()
        emit('command_executed', {
            'command_id': new_cmd.id,
            'user': current_user.username
        }, broadcast=True)

@socketio.on('vote')
@login_required
def handle_vote(data):
    # 实现投票逻辑
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True) 