import os
from datetime import datetime
import ctypes.wintypes

# Windows系统API获取用户常用文件夹路径
def get_user_folder(folder_id):
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, folder_id, None, 0, buf)
    return buf.value

# Windows文件夹ID常量
CSIDL_DESKTOP = 0
CSIDL_MYDOCUMENTS = 5
CSIDL_DOWNLOADS = 40

# 自动读取当前用户桌面、文档、下载目录
USER_DESKTOP = get_user_folder(CSIDL_DESKTOP)
USER_DOCUMENTS = get_user_folder(CSIDL_MYDOCUMENTS)
USER_DOWNLOADS = get_user_folder(CSIDL_DOWNLOADS)

# 日志存储根目录
LOG_ROOT = "./logs"
# 按日期生成独立文件夹，格式：20260628
TODAY_DIR = os.path.join(LOG_ROOT, datetime.now().strftime("%Y%m%d"))
# 当日总日志文件
LOG_FILE = os.path.join(TODAY_DIR, "full_monitor.log")
# 风险触发摄像头抓拍存储目录
CAPTURE_FOLDER = os.path.join(TODAY_DIR, "risk_capture")
# 风险触发屏幕截图存储目录
SCREENSHOT_FOLDER = os.path.join(TODAY_DIR, "risk_screenshot")

def init_log_dir():
    """程序启动自动创建全套日志文件夹，无需手动新建"""
    dir_list = [LOG_ROOT, TODAY_DIR, CAPTURE_FOLDER, SCREENSHOT_FOLDER]
    for path in dir_list:
        if not os.path.exists(path):
            os.makedirs(path)

# 需要监控的用户目录：桌面、文档、下载
MONITOR_DIR_LIST = [
    USER_DESKTOP,
    USER_DOCUMENTS,
    USER_DOWNLOADS
]

# Microsoft Edge浏览器历史记录数据库路径
EDGE_HISTORY_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History")

# 高危进程黑名单，启动即判定风险并取证
RISK_PROCESS_LIST = {
    "crack.exe", "hacktool.exe", "miner.exe", "format.com",
    "rm.exe", "sqlmap.exe", "hydra.exe"
}

# 不良网站关键词，Edge访问匹配后触发抓拍
BAD_WEBSITE_KEYWORDS = {
    "porn", "sex", "gambling", "casino", "赌博", "色情",
    "博彩", "色情视频", "破解付费", "钓鱼提现"
}

# 系统核心敏感文件列表，精确完整路径匹配，杜绝普通文件夹误报
CRITICAL_FILES = [
    r"C:\Windows\System32\SAM",
    r"C:\Windows\System32\config",
    r"C:\Windows\hosts",
    r"C:\Users\%USERNAME%\.ssh",
    r"C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Credentials"
]

# 高危系统管理工具，打开后判定风险
CRITICAL_WINDOW_PROCESS = {
    "regedit.exe", "diskmgmt.msc", "gpedit.msc",
    "services.msc", "cmd.exe", "powershell.exe"
}

# 批量删除阈值：10秒内删除文件超过该数值判定批量删除高危行为
MASS_DELETE_THRESHOLD = 5