import time
import telebot


class Bot:
    def __init__(self, API_key=None):
        if not API_key or not isinstance(API_key, str):
            raise TypeError(f"Argument name must be str, got {type(name).__name__}")

        self.bot = telebot.TeleBot(API_key)

    def register_handlers(self):
        from handlers import register_all
        register_all(self.bot)

    def run(self):
        try:
            self.bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"ERROR: {e}")
            time.sleep(5)
            self.run()

    def stop(self):
        self.bot.stop_polling()