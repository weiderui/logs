import pyautogui
import os
from datetime import datetime
from config import SCREENSHOT_FOLDER
from log_utils import write_log

def take_screenshot() -> str | None:
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(SCREENSHOT_FOLDER, f"screen_{time_str}.jpg")
    try:
        screen_img = pyautogui.screenshot()
        screen_img.save(save_path)
        write_log(f"风险截图保存成功: {save_path}")
        return save_path
    except Exception as e:
        write_log(f"截图功能异常失败: {str(e)}")
        return None