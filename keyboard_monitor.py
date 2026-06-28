from pynput import keyboard
from log_utils import write_log

def start_keyboard_monitor():
    write_log("===== 键盘输入监控模块启动（支持主键盘+数字小键盘） =====")

    def on_press(key):
        try:
            # 普通字母、主键盘数字、符号
            char = key.char
            write_log(f"键盘输入 | 普通字符: {char}")
        except AttributeError:
            # 功能键 / 小键盘按键
            key_name = str(key).replace("Key.", "")
            write_log(f"键盘输入 | 功能/小键盘键: {key_name}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()