import psutil
import time
import re
from dataclasses import dataclass
from typing import List

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI
except: pass

@dataclass
class BlockRule:
    process_name: str
    block_time_periods: List[str]  # 时间范围形如 0600-2000 的格式
    msg: str

RULES = [
    BlockRule("tim.exe", ["0800-1130", "1300-2000"], '白天不要看 QQ，很坏！'),
]

def kill_blocked_processes(block_rules: List[BlockRule]) -> List[str]:
    """
    根据屏蔽规则杀死不在允许时间内的进程
    
    Args:
        block_rules: 屏蔽规则列表
        
    Returns:
        被杀死的进程名列表
    """
    killed_processes = []
    current_time = time.localtime()
    current_minutes = current_time.tm_hour * 60 + current_time.tm_min
    
    # 遍历所有进程
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name']
            # 检查该进程是否在屏蔽规则中
            for rule in block_rules:
                if rule.process_name.lower() != process_name.lower(): continue
                # 检查当前时间是否在允许的时间段内
                is_allowed = False
                for time_period in rule.block_time_periods:
                    if not is_time_in_period(current_minutes, time_period):
                        is_allowed = True
                        break
                
                # 如果不在允许时间内，则杀死进程
                if not is_allowed:
                    try:
                        process.kill()
                        process.wait(timeout=3)  # 等待进程终止
                        killed_processes.append(rule)
                        print(f"已杀死进程: {process_name} (PID: {process.info['pid']})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        print(f"无法杀死进程 {process_name}: {e}")
                    break
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # 进程可能已经结束或没有权限访问
            continue
    
    return killed_processes

def is_time_in_period(current_minutes: int, time_period: str) -> bool:
    """
    检查当前时间是否在指定的时间范围内
    
    Args:
        current_minutes: 当前时间的分钟数（0-1439）
        time_period: 时间范围字符串，格式如 "0600-2000"
        
    Returns:
        是否在时间范围内
    """
    # 验证时间格式
    if not re.match(r'^\d{4}-\d{4}$', time_period):
        raise ValueError(f"无效的时间格式: {time_period}")
    
    start_str, end_str = time_period.split('-')
    
    # 解析开始和结束时间
    start_hour = int(start_str[:2])
    start_minute = int(start_str[2:])
    end_hour = int(end_str[:2])
    end_minute = int(end_str[2:])
    
    # 转换为分钟数
    start_minutes = start_hour * 60 + start_minute
    end_minutes = end_hour * 60 + end_minute
    
    # 处理跨夜情况（如2300-0600）
    if start_minutes > end_minutes:
        return current_minutes >= start_minutes or current_minutes <= end_minutes
    else:
        return start_minutes <= current_minutes <= end_minutes

import tkinter as tk
from tkinter import messagebox

def show_info(message, title="信息提示"):
    """
    使用 tkinter 显示指定信息的函数
    
    参数:
    message: 要显示的信息内容
    title: 窗口标题，默认为"信息提示"
    """
    # 创建主窗口（但不显示）
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 显示信息对话框
    messagebox.showinfo(title, message)
    
    # 销毁窗口
    root.destroy()

# 使用示例
if __name__ == "__main__":
    killed = kill_blocked_processes(RULES)
    if killed:
        show_info('\n'.join(map(lambda x: f'killed {x.process_name}: {x.msg}', killed)))
