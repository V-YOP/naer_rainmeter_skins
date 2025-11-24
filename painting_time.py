import itertools
from pathlib import Path
import re
import json
from datetime import date, datetime, timedelta

CONTINUOUS_THRESHOLD = 15 # X 分钟内有绘画记录就认为能打 combo

def get_30_mins_before() -> datetime:
    now = datetime.now()
    return now - timedelta(minutes=30)

def get_today_start() -> datetime:
    """获取今天开始日期（30小时制下的）"""
    now = datetime.now()
    if now.hour < 6:
        now = now - timedelta(days=1)
    return now.replace(hour=6, minute=0, second=0, microsecond=0)

def get_week_start() -> datetime:
    """获取本周开始日期（星期一为第一天，30小时制下的）"""
    today_start = get_today_start()
    # 计算今天是本周的第几天（星期一为0，星期日为6）
    weekday = today_start.weekday()
    week_start = today_start - timedelta(days=weekday)
    return week_start

def get_month_start() -> datetime:
    """获取本月开始日期（30小时制下的）"""
    today_start = get_today_start()
    month_start = today_start.replace(day=1)
    return month_start

def format_timedelta(td: timedelta):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_history():
    last_time = None
    continuous_duration = 0
    
    with open(Path.home()/'.kra_history/history', 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue 
            
            datetime_str, filename, *_, seconds = line.split('##')
            draw_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            
            # 计算连续绘画时间
            if last_time is not None:
                time_diff = (draw_time - last_time).total_seconds() / 60  # 转换为分钟
                if time_diff <= CONTINUOUS_THRESHOLD:  # 6 分钟以内认为是连续的
                    continuous_duration += time_diff
                else:
                    continuous_duration = 0  # 超过 6 分钟，重置连续时间
            else:
                continuous_duration = 0  # 第一条记录
            last_time = draw_time

            if '-B-' in filename or '-B.' in filename:
                label = 'B'
            elif '-C-' in filename or '-C.' in filename:
                label = 'C'
            else:
                label = 'A'
            yield label, draw_time, int(seconds), int(continuous_duration)

def get_drawtimes():
    """today, week, month, in seconds"""

    today_seconds = {'A': 0, 'B': 0, 'C': 0}
    week_seconds = {'A': 0, 'B': 0, 'C': 0}
    month_seconds = {'A': 0, 'B': 0, 'C': 0}

    today_start, week_start, month_start = get_today_start(), get_week_start(), get_month_start()

    _30_mins_before_num = 0
    _30_mins_before = get_30_mins_before()

    today_combos = []
    last_record = None
    for label, draw_time, seconds, continuous_duration in get_history():
        if draw_time >= today_start:
            today_seconds[label] += seconds
            if continuous_duration == 0 and last_record and last_record[2] != 0:
                today_combos.append({'combo_start_time': f'{last_record[0] - timedelta(minutes=last_record[2]):%Y-%m-%d %H:%M:%S}', 'combo_end_time': f'{last_record[0]:%Y-%m-%d %H:%M:%S}', 'combo': last_record[2]})
            last_record = draw_time, seconds, continuous_duration

        if draw_time >= week_start:
            week_seconds[label] += seconds
        if draw_time >= month_start:
            month_seconds[label] += seconds
        if draw_time >= _30_mins_before:
            _30_mins_before_num += seconds

    return {
        'today_A': today_seconds['A'],
        'today_B': today_seconds['B'],
        'today_C': today_seconds['C'],

        'week_A': week_seconds['A'],
        'week_B': week_seconds['B'],
        'week_C': week_seconds['C'],

        'month_A': month_seconds['A'],
        'month_B': month_seconds['B'],
        'month_C': month_seconds['C'],
        
        'today': sum(today_seconds.values()),
        'week': sum(week_seconds.values()), 
        'month': sum(month_seconds.values()),
        'latest_drawtime': f'{draw_time:%Y-%m-%d %H:%M:%S}',
        '30_mins_before': _30_mins_before_num,
        'current_combo': 0 if (datetime.now() - draw_time).total_seconds() > 60 * CONTINUOUS_THRESHOLD else continuous_duration,
        'today_combos': today_combos,
        'last_days': (date(2026, 1, 25) - datetime.now().date()).days + 1
    }

print(json.dumps(get_drawtimes(), ensure_ascii=False))
