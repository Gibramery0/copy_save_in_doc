import os
import pyperclip
import time
from datetime import datetime

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
log_folder = os.path.join(desktop_path, "Yazılar")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

date_str = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(log_folder, f"{date_str}.txt")

last_clipboard = ""

while True:
    clipboard_content = pyperclip.paste()

    if clipboard_content != last_clipboard:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(clipboard_content + " ")

        last_clipboard = clipboard_content

    time.sleep(1)
