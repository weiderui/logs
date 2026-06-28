import psutil
import time
from log_utils import write_log
from config import RISK_PROCESS_LIST, CRITICAL_WINDOW_PROCESS
from camera_capture import take_risk_photo

def start_process_monitor():
    write_log("===== 进程监控模块启动 =====")
    old_pid_set = set()

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        old_pid_set.add(proc.info["pid"])

    while True:
        new_pid_set = set()
        for proc in psutil.process_iter(["pid", "name", "exe"]):
            pid = proc.info["pid"]
            proc_name = proc.info["name"].lower()
            exe_path = proc.info["exe"] or "未知程序路径"
            new_pid_set.add(pid)

            if pid not in old_pid_set:
                write_log(f"新程序启动 | PID:{pid} | 程序名:{proc.info['name']} | 路径:{exe_path}")
                is_risk = False

                if proc_name in RISK_PROCESS_LIST:
                    write_log(f"【高危行为】启动风险工具 {proc.info['name']} PID:{pid}")
                    is_risk = True
                if proc_name in CRITICAL_WINDOW_PROCESS:
                    write_log(f"【高危行为】打开系统关键管理工具 {proc.info['name']} PID:{pid}")
                    is_risk = True

                if is_risk:
                    take_risk_photo()

        old_pid_set = new_pid_set
        time.sleep(1)