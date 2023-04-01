
from Color import Color
import sys
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from Handler import Handler
from GPT import GPT

class TelegramBot():
    def __init__(self, handler):
        self.token = self._get_token()
        self.application = self._build()
        self._set_handlers(handler)

    def start(self):
        Color.OK('application started')
        self.application.run_polling()

    def _get_token(self):
        try:
            f = open('./.token', 'r')
            token = f.read().strip()
            f.close()
            Color.OK('token obtained')
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your api token in `.token` file')
            sys.exit(1)

    def _build(self):
        app = ApplicationBuilder().token(self.token).build()
        Color.OK('application built')
        return app

    def _set_handlers(self, handler):
        start_handler = CommandHandler('start', handler.start)
        new_session_handler = CommandHandler('new', handler.new)
        select_session_handler = CommandHandler('select', handler.select)
        active_sessions_handler = CommandHandler('active', handler.active)
        help_handler = CommandHandler('help', handler.help)
        debug_handler = CommandHandler('debug', handler.debug)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handler.echo)
        self.application.add_handler(start_handler)
        self.application.add_handler(new_session_handler)
        self.application.add_handler(select_session_handler)
        self.application.add_handler(active_sessions_handler)
        self.application.add_handler(help_handler)
        self.application.add_handler(debug_handler)
        self.application.add_handler(echo_handler)
        Color.OK('handlers set')


if __name__ == '__main__':
    gpt = GPT()
    handler = Handler(gpt)
    bot = TelegramBot(handler)
    bot.start()

