import os
import time
import telebot
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


with open('../credentials.json', 'r') as file:
    credentials = json.load(file)

TELEGRAM_BOT_TOKEN = credentials["bot_token"]
TELEGRAM_CHAT_ID = '-4206118494'
FAST_LOG_FILE = '/var/log/suricata/fast.log'
NETWORK_LOG_FILE = '/var/log/suricata/network_all.log'


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == FAST_LOG_FILE:
            send_to_telegram(FAST_LOG_FILE)
        elif event.src_path == NETWORK_LOG_FILE:
            send_to_telegram(NETWORK_LOG_FILE)


def send_to_telegram(log_file):
    try:
        with open(log_file, 'r') as file:
            last_line = file.readlines()[-1]
        message = f"::___network_log___::{last_line}" if log_file == NETWORK_LOG_FILE else last_line
        bot.send_message(TELEGRAM_CHAT_ID, message)
        print('Message sent to Telegram successfully!')
    except Exception as e:
        print(f'Failed to send message to Telegram: {e}')


if __name__ == "__main__":
    print("I'm working")
    bot.send_message(TELEGRAM_CHAT_ID, "I'm working")
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FAST_LOG_FILE), recursive=False)
    observer.schedule(event_handler, path=os.path.dirname(NETWORK_LOG_FILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("I'm done")
        bot.send_message(TELEGRAM_CHAT_ID, "I'm done")
        observer.stop()
        observer.join()
