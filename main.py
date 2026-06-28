import threading
import argparse
import os
import sys
import ctypes
import winreg
import psutil
from log_utils import write_log

from mouse_monitor import start_mouse_monitor
from keyboard_monitor import start_keyboard_monitor
from process_monitor import start_process_monitor
from browser_monitor import start_browser_monitor
from file_monitor import start_file_monitor

def is_admin() -> bool:
    """判断当前程序是否拥有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def set_high_priority():
    """设置当前进程为Windows高优先级，优先占用CPU资源"""
    try:
        current_pid = os.getpid()
        proc = psutil.Process(current_pid)
        proc.nice(psutil.HIGH_PRIORITY_CLASS)
        write_log(f"进程优先级已设置为【高优先级】，PID:{current_pid}")
    except Exception as e:
        write_log(f"设置进程高优先级失败，必须管理员运行: {str(e)}")

def add_auto_start():
    """写入注册表实现开机自启（当前用户登录自动运行）"""
    script_path = os.path.abspath(sys.argv[0])
    pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    run_cmd = f'"{pythonw_path}" "{script_path}"'
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "SystemMonitorService"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, run_cmd)
        winreg.CloseKey(reg_key)
        write_log("开机自启配置成功：登录后自动后台运行监控程序")
    except Exception as e:
        write_log(f"配置开机自启失败，需要管理员权限: {str(e)}")

if __name__ == "__main__":
    # 无管理员权限则自动拉起UAC授权重启程序
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    # 设置进程高优先级
    set_high_priority()
    # 写入开机自启注册表项
    add_auto_start()

    # 解析启动参数 -debug
    arg_parser = argparse.ArgumentParser(description="系统行为监控程序")
    arg_parser.add_argument("-debug", "--debug", action="store_true", help="调试模式：保留控制台窗口，实时查看输出")
    args = arg_parser.parse_args()

    write_log("========== 全量监控系统总启动 ==========")

    # 全部后台守护线程：鼠标、键盘、进程、Edge浏览器、文件监控
    threading.Thread(target=start_mouse_monitor, daemon=True).start()
    threading.Thread(target=start_keyboard_monitor, daemon=True).start()
    threading.Thread(target=start_process_monitor, daemon=True).start()
    threading.Thread(target=start_browser_monitor, daemon=True).start()
    threading.Thread(target=start_file_monitor, daemon=True).start()

    # 区分运行模式
    if args.debug:
        write_log("【调试模式开启】控制台窗口常驻，可查看实时日志输出")
        print("监控全部启动完成，按下回车键关闭程序")
        while True:
            input()
    else:
        write_log("【静默后台模式】无debug参数，控制台窗口自动隐藏，后台持续监控")