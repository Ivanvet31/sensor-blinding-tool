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
# LOG_FILE = '/var/log/suricata/fast.log'
LOG_FILE = './text.txt'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE:
            send_to_telegram()


def send_to_telegram():
    try:
        with open(LOG_FILE, 'r') as file:
            last_line = file.readlines()[-1]
        bot.send_message(TELEGRAM_CHAT_ID, last_line)
        print('Message sent to Telegram successfully!')
    except Exception as e:
        print(f'Failed to send message to Telegram: {e}')

if __name__ == "__main__":
    print("Im working")
    bot.send_message(TELEGRAM_CHAT_ID, "Im working")
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOG_FILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("Im done")
        bot.send_message(TELEGRAM_CHAT_ID, "Im done")
        observer.stop()
        observer.join()
