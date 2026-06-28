from pynput import mouse
from log_utils import write_log

def start_mouse_monitor():
    write_log("===== 鼠标监控模块启动（仅记录真人物理点击） =====")

    def on_click(x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                btn_text = "左键"
            elif button == mouse.Button.right:
                btn_text = "右键"
            else:
                btn_text = "中键"
            write_log(f"鼠标点击 | 屏幕坐标({x},{y}) | {btn_text}")

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()