import sqlite3
import os
import time
import shutil
from datetime import datetime, timedelta
from log_utils import write_log
from config import EDGE_HISTORY_PATH, BAD_WEBSITE_KEYWORDS
from camera_capture import take_risk_photo

def start_browser_monitor():
    write_log("===== Edge浏览器网址监控模块启动 =====")
    last_check_time = datetime.now() - timedelta(minutes=1)
    temp_db_file = "edge_temp_history.db"

    while True:
        try:
            # Edge占用原文件，复制临时副本读取
            shutil.copy2(EDGE_HISTORY_PATH, temp_db_file)

            conn = sqlite3.connect(temp_db_file)
            cur = conn.cursor()
            # Edge与Chrome表结构一致，查询最新20条访问记录
            cur.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 20")
            records = cur.fetchall()

            for url, title, time_stamp in records:
                visit_time = datetime(1601, 1, 1) + timedelta(microseconds=time_stamp)
                if visit_time > last_check_time:
                    write_log(f"Edge访问 | 页面标题:{title} | 网址:{url}")
                    last_check_time = visit_time

                    page_content = (url + title).lower()
                    for keyword in BAD_WEBSITE_KEYWORDS:
                        if keyword in page_content:
                            write_log(f"【高危行为】Edge访问不良网站，命中关键词:{keyword} URL:{url}")
                            take_risk_photo()
                            break

            conn.close()
            os.remove(temp_db_file)
        except Exception as err:
            write_log(f"Edge历史读取异常: {str(err)}")
        time.sleep(10)