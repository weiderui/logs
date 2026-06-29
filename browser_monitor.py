import sqlite3
import os
import time
import shutil
from datetime import datetime, timedelta
from log_utils import write_log
from camera_capture import take_risk_photo

def get_all_browser_history_paths():
    """自动获取 Edge + Chrome 全部用户配置的History文件"""
    local_appdata = os.environ["LOCALAPPDATA"]
    # 两款浏览器根目录
    browser_roots = [
        os.path.join(local_appdata, r"Microsoft\Edge\User Data"),
        os.path.join(local_appdata, r"Google\Chrome\User Data")
    ]
    history_paths = []
    for root in browser_roots:
        if not os.path.exists(root):
            continue
        for dir_name in os.listdir(root):
            sub_dir = os.path.join(root, dir_name)
            hist_file = os.path.join(sub_dir, "History")
            if os.path.isfile(hist_file):
                history_paths.append((root, hist_file))
    return history_paths

def start_browser_monitor():
    write_log("===== Edge/Chrome浏览器网址监控模块启动（兼容多用户） =====")
    temp_db_file = "browser_temp_history.db"
    profile_last_time = {}
    # 东八区UTC+8时区偏移，修正时间差
    UTC8_OFFSET = timedelta(hours=8)

    while True:
        all_hist_pairs = get_all_browser_history_paths()
        if len(all_hist_pairs) == 0:
            write_log("【错误】未找到Edge/Chrome任何用户历史文件")
            time.sleep(10)
            continue

        for root_dir, hist_path in all_hist_pairs:
            # 区分浏览器类型
            if "Microsoft\\Edge" in root_dir:
                browser_name = "Edge"
            else:
                browser_name = "Chrome"

            if hist_path not in profile_last_time:
                profile_last_time[hist_path] = datetime.now() - timedelta(days=7)
            last_dt = profile_last_time[hist_path]

            try:
                shutil.copyfile(hist_path, temp_db_file)
                conn = sqlite3.connect(temp_db_file)
                cur = conn.cursor()
                cur.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                records = cur.fetchall()
                new_count = 0
                max_visit_dt = last_dt

                for url, title, ts in records:
                    # 转换UTC时间 +8小时修正北京时间
                    utc_dt = datetime(1601, 1, 1) + timedelta(microseconds=ts)
                    local_dt = utc_dt + UTC8_OFFSET
                    if local_dt > last_dt:
                        new_count += 1
                        write_log(f"{browser_name}访问 | 时间:{local_dt.strftime('%H:%M:%S')} 标题:{title} 网址:{url}")
                        if local_dt > max_visit_dt:
                            max_visit_dt = local_dt
                        # 不良网站关键词检测
                        full_text = (url + title).lower()
                        bad_keywords = {"porn", "sex", "gambling", "casino", "赌博", "色情", "博彩"}
                        for kw in bad_keywords:
                            if kw in full_text:
                                write_log(f"【高危行为】{browser_name}访问不良网站，关键词:{kw} URL:{url}")
                                take_risk_photo()
                                break
                profile_last_time[hist_path] = max_visit_dt
                conn.close()
                os.remove(temp_db_file)
            except PermissionError:
                write_log(f"【提示】{browser_name}配置占用：{hist_path}，关闭该账号所有窗口才能读取新记录")
            except Exception as e:
                write_log(f"【读取失败】{browser_name} {hist_path} 错误：{repr(e)}")
        time.sleep(10)