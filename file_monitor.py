import time
from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from log_utils import write_log
from config import MONITOR_DIR_LIST, CRITICAL_FILES, MASS_DELETE_THRESHOLD
from camera_capture import take_risk_photo

delete_record_queue = deque(maxlen=30)

# 过滤1：临时文件、数据库缓存后缀
IGNORE_SUBSTR = {
    ".tmp", ".temp", ".cache", "~$", ".log", ".crdownload", ".db-wal", ".db-shm", ".db",
    "thumbcache_", ".DS_Store", ".ini", ".bak", "tmp_"
}
# 过滤2：软件厂商缓存目录，拦截网易云、VSCode、各类软件后台存储
IGNORE_DIR_NAMES = {
    "globalStorage", "workspaceStorage", "Local Storage", "Session Storage",
    ".vscode", ".git", "__pycache__", ".pytest_cache", "NetEase", "CloudMusic",
    "Tencent", "WeChat", "QQ", "Steam", "Cache", "Cache2"
}

class FileEventHandle(FileSystemEventHandler):
    def _is_ignore(self, path):
        """双重过滤：临时文件 + 软件缓存目录"""
        lower_path = path.lower()
        # 匹配临时文件后缀
        for word in IGNORE_SUBSTR:
            if word in lower_path:
                return True
        # 匹配缓存目录
        dir_segments = lower_path.split("\\")
        for dir_name in IGNORE_DIR_NAMES:
            if dir_name.lower() in dir_segments:
                return True
        return False

    def _is_real_critical_file(self, file_path):
        """精确匹配完整系统敏感文件路径，杜绝普通文件夹误报"""
        file_path_lower = file_path.lower()
        for critical_full_path in CRITICAL_FILES:
            crit_lower = critical_full_path.lower()
            # 完整路径前缀匹配，只有完全命中系统文件才判定高危
            if file_path_lower.startswith(crit_lower):
                return True
        return False

    def on_open(self, event):
        if self._is_ignore(event.src_path):
            return
        file_path = event.src_path
        write_log(f"文件打开 | {event.src_path}")
        if self._is_real_critical_file(file_path):
            write_log(f"【高危行为】访问系统关键敏感文件: {event.src_path}")
            take_risk_photo()

    def on_created(self, event):
        if self._is_ignore(event.src_path):
            return
        file_path = event.src_path
        write_log(f"新建/复制文件 | {event.src_path}")
        if self._is_real_critical_file(file_path):
            write_log(f"【高危行为】复制系统关键文件至：{event.src_path}")
            take_risk_photo()

    def on_modified(self, event):
        if self._is_ignore(event.src_path):
            return
        write_log(f"文件修改 | {event.src_path}")

    def on_deleted(self, event):
        if self._is_ignore(event.src_path):
            return
        write_log(f"文件删除 | {event.src_path}")
        now = time.time()
        delete_record_queue.append(now)
        recent_delete = [t for t in delete_record_queue if now - t < 10]
        if len(recent_delete) >= MASS_DELETE_THRESHOLD:
            write_log(f"【高危行为】10秒内批量删除文件，总量:{len(recent_delete)}个")
            take_risk_photo()

def start_file_monitor():
    observer = Observer()
    for target_dir in MONITOR_DIR_LIST:
        write_log(f"===== 文件监控绑定目录:{target_dir} =====")
        observer.schedule(FileEventHandle(), path=target_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()