import time
import telebot
import models.bot
from config import Config

def main():
    config = Config()
    bot = models.bot.Bot(config.token)
    bot.register_handlers()
    bot.run()

if __name__ == '__main__':
    main()