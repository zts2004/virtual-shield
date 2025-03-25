# 振动模式配置

# 无齿锯振动参数
SAW_PATTERNS = {
    'idle': {
        'frequency': 80,
        'power_level': 20
    },
    'normal': {
        'frequency': 100,
        'power_level': 60
    },
    'heavy': {
        'frequency': 120,
        'power_level': 100
    }
}

# 手提链锯振动参数
CHAINSAW_PATTERNS = {
    'idle': {
        'frequency': 100,
        'power_level': 30
    },
    'normal': {
        'frequency': 125,
        'power_level': 70
    },
    'heavy': {
        'frequency': 150,
        'power_level': 100
    }
}

# 工具类型映射
TOOL_PATTERNS = {
    'saw': SAW_PATTERNS,
    'chainsaw': CHAINSAW_PATTERNS
}

def get_pattern(tool_type, intensity='normal'):
    """
    获取指定工具和强度的振动参数
    :param tool_type: 工具类型（'saw' 或 'chainsaw'）
    :param intensity: 强度级别（'idle', 'normal', 或 'heavy'）
    :return: 振动参数字典
    """
    if tool_type not in TOOL_PATTERNS:
        raise ValueError(f"不支持的工具类型: {tool_type}")
    
    patterns = TOOL_PATTERNS[tool_type]
    if intensity not in patterns:
        raise ValueError(f"不支持的强度级别: {intensity}")
    
    return patterns[intensity] 