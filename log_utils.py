from datetime import datetime
from config import LOG_FILE, init_log_dir

init_log_dir()

def write_log(content: str):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_str}] {content}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)