import pyautogui
import time

try:
        time.sleep(3)
        x, y = pyautogui.position()
        print(f"Posição do Cursor: X={x}, Y={y}")
except KeyboardInterrupt:
    print("\nCaptura de movimento do cursor encerrada.")