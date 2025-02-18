import os
import pyperclip
import time
import threading
import sys
from datetime import datetime

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
log_folder = os.path.join(desktop_path, "Yazılar")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

date_str = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(log_folder, f"{date_str}.txt")

last_clipboard = ""
running = True

def listen_for_exit():
    """Kullanıcının 'exit' yazmasını bekler ve programı güvenli şekilde kapatır."""
    global running
    try:
        while running:
            user_input = sys.stdin.readline().strip().lower()  # Daha güvenli okuma
            if user_input == "exit":
                running = False
                print("\nÇıkış yapılıyor...")
                break
    except (EOFError, UnicodeDecodeError):
        pass  # Terminal kapatıldığında hatayı yok sayarak güvenli çıkış sağlıyoruz

# Normal thread (daemon değil)
exit_thread = threading.Thread(target=listen_for_exit)
exit_thread.start()

print("Kopyalama kaydedici çalışıyor... Çıkmak için 'exit' yazıp ENTER'a basın.")

try:
    while running:
        clipboard_content = pyperclip.paste()

        if clipboard_content != last_clipboard:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(clipboard_content + " ")

            last_clipboard = clipboard_content

        time.sleep(1)

except KeyboardInterrupt:
    print("\nCTRL+C ile çıkış yapıldı.")

except pyperclip.PyperclipWindowsException:
    print("\nClipboard erişimi engellendi. Program güvenli şekilde sonlandırılıyor.")

finally:
    running = False  # Thread’in kapanmasını sağlıyoruz
    exit_thread.join()  # Thread'in temiz kapanmasını bekliyoruz
    print("Program kapatıldı.")
