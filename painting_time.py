from pathlib import Path
import re
import json
from datetime import datetime, timedelta

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


def get_drawtimes() -> tuple[int, int, int]:
    """today, week, month, in seconds"""

    history = (Path.home()/'.kra_history/history').read_text(encoding='utf-8')
    history = [i.strip() for i in re.split(r'\r?\n', history) if i.strip()]
    today_sum, week_sum, month_sum = 0, 0, 0
    today_start, week_start, month_start = get_today_start(), get_week_start(), get_month_start()
    for line in history:
        datetime_str, *_, seconds = line.split('##')
        draw_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        if draw_time >= today_start:
            today_sum += int(seconds)
        if draw_time >= week_start:
            week_sum += int(seconds)
        if draw_time >= month_start:
            month_sum += int(seconds)
    return today_sum, week_sum, month_sum

today, week, month = get_drawtimes()

response = {
    'today': today,
    'week': week,
    'month': month,
}
print(json.dumps(response, ensure_ascii=False))