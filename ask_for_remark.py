from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

ENCODING = 'GBK'

REMARK_FILE = Path(__file__).parent/'remark.txt'

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI
except: pass

def on_submit(event=None):
    """处理用户输入"""
    user_input = text_area.get("1.0", "end-1c").strip()  # 获取文本框内容
    root.destroy()  # 关闭窗口
    
    # 保存输入内容
    REMARK_FILE.write_text(user_input, encoding=ENCODING)
    # 如果需要显示弹窗提示，可以取消下面的注释
    # messagebox.showinfo("输入结果", f"您输入的内容是: {user_input}")

# 创建主窗口
root = tk.Tk()
root.title("新备注")
root.geometry("500x300")  # 增加窗口高度以适应多行文本框

# 设置窗口在屏幕中央显示
root.eval('tk::PlaceWindow . center')

# 创建标签
label = tk.Label(root, text="请输入内容:")
label.pack(pady=5)

# 创建多行文本框（类似HTML的textarea）
text_area = scrolledtext.ScrolledText(root, 
                                     width=50, 
                                     height=10,
                                     wrap=tk.WORD,  # 自动换行
                                     font=("Arial", 10))
text_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# 如果之前有保存的内容，加载到文本框中
if REMARK_FILE.exists():
    text_area.insert("1.0", REMARK_FILE.read_text(encoding=ENCODING))

text_area.focus()  # 自动聚焦到文本框

# 绑定Ctrl+Enter快捷键提交
text_area.bind('<Control-Return>', on_submit)

# 创建提交按钮
submit_btn = tk.Button(root, text="提交 (Ctrl+Enter)", command=on_submit)
submit_btn.pack(pady=5)

# 启动主循环
root.mainloop()
