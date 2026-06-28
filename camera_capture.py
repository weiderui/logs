import cv2
import os
from datetime import datetime
from config import CAPTURE_FOLDER
from log_utils import write_log
from screen_capture import take_screenshot

def take_risk_photo() -> str | None:
    cap = cv2.VideoCapture(0)
    img_path = None

    if cap.isOpened():
        ret, frame = cap.read()
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(CAPTURE_FOLDER, f"risk_{time_str}.jpg")
        if ret:
            cv2.imwrite(img_path, frame)
            write_log(f"摄像头抓拍照片保存成功: {img_path}")
        else:
            write_log("摄像头打开成功，但读取画面失败")
        cap.release()
        cv2.destroyAllWindows()
    else:
        write_log("无法打开摄像头：无设备/权限被安全软件拦截")

    take_screenshot()
    return img_path