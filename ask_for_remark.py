from pathlib import Path
import tkinter as tk
from tkinter import messagebox

ENCODING = 'GBK'

REMARK_FILE = Path(__file__).parent/'remark.txt'

def on_submit(event=None):
    """处理用户输入"""
    user_input = entry.get().strip()
    root.destroy()  # 关闭窗口
    
    # 打印输入内容
    REMARK_FILE.write_text(user_input, encoding=ENCODING)
    # 如果需要显示弹窗提示，可以取消下面的注释
    # messagebox.showinfo("输入结果", f"您输入的内容是: {user_input}")

# 创建主窗口
root = tk.Tk()
root.title("输入框示例")
root.geometry("300x100")

# 设置窗口在屏幕中央显示
root.eval('tk::PlaceWindow . center')

# 创建标签
label = tk.Label(root, text="请输入内容:")
label.pack(pady=5)

# 创建输入框
entry = tk.Entry(root, width=30)
entry.pack(pady=5)
if REMARK_FILE.exists():
    entry.insert(0, REMARK_FILE.read_text(encoding=ENCODING))
entry.focus()  # 自动聚焦到输入框

# 绑定回车键事件
entry.bind('<Return>', on_submit)

# 创建提交按钮（可选）

# 启动主循环
root.mainloop()
