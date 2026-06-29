import os
from datetime import datetime
import ctypes.wintypes

def get_user_folder(folder_id):
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, folder_id, None, 0, buf)
    return buf.value

CSIDL_DESKTOP = 0
CSIDL_MYDOCUMENTS = 5
CSIDL_DOWNLOADS = 40

USER_DESKTOP = get_user_folder(CSIDL_DESKTOP)
USER_DOCUMENTS = get_user_folder(CSIDL_MYDOCUMENTS)
USER_DOWNLOADS = get_user_folder(CSIDL_DOWNLOADS)

LOG_ROOT = "./logs"
TODAY_DIR = os.path.join(LOG_ROOT, datetime.now().strftime("%Y%m%d"))
LOG_FILE = os.path.join(TODAY_DIR, "full_monitor.log")
CAPTURE_FOLDER = os.path.join(TODAY_DIR, "risk_capture")
SCREENSHOT_FOLDER = os.path.join(TODAY_DIR, "risk_screenshot")

def init_log_dir():
    dir_list = [LOG_ROOT, TODAY_DIR, CAPTURE_FOLDER, SCREENSHOT_FOLDER]
    for path in dir_list:
        if not os.path.exists(path):
            os.makedirs(path)

MONITOR_DIR_LIST = [
    USER_DESKTOP,
    USER_DOCUMENTS,
    USER_DOWNLOADS
]

EDGE_HISTORY_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History")

RISK_PROCESS_LIST = {
    "crack.exe", "hacktool.exe", "miner.exe", "format.com",
    "rm.exe", "sqlmap.exe", "hydra.exe"
}

BAD_WEBSITE_KEYWORDS = {
    "porn", "sex", "gambling", "casino", "赌博", "色情",
    "博彩", "色情视频", "破解付费", "钓鱼提现"
}

CRITICAL_FILES = [
    r"C:\Windows\System32\SAM",
    r"C:\Windows\System32\config",
    r"C:\Windows\hosts",
    r"C:\Users\%USERNAME%\.ssh",
    r"C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Credentials"
]

CRITICAL_WINDOW_PROCESS = {
    "regedit.exe", "diskmgmt.msc", "gpedit.msc",
    "services.msc", "cmd.exe", "powershell.exe"
}

MASS_DELETE_THRESHOLD = 5