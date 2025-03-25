import os

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///robot_control.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 冲突检测配置
    CONFLICT_DISTANCE_THRESHOLD = 20  # 厘米
    CONFLICT_TIME_THRESHOLD = 100     # 毫秒
    
    # WebSocket配置
    SOCKETIO_MESSAGE_QUEUE = 'redis://'
    
    # 投票配置
    VOTING_TIMEOUT = 30  # 秒 