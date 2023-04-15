
from Color import Color
import sys
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from Handler import Handler
from Engine import Engine
import traceback

#logging.basicConfig(
#    format="[%(asctime)s]: %(message)s",
#    level=logging.INFO
#)
logging.basicConfig(
    format="[%(asctime)s]: %(message)s",
    level=logging.ERROR
)

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
            f = open('./.telegram.token', 'r')
            token = f.read().strip()
            f.close()
            Color.OK('token obtained')
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your telegram api token in `.telegram.token` file')
            sys.exit(1)

    def _build(self):
        app = ApplicationBuilder().token(self.token).build()
        Color.OK('application built')
        return app

    @staticmethod
    async def _error_handler(update, context):
        Color.FAILED(context.error)
        #print(Color._Red)
        #traceback.print_tb(context.error.__traceback__)
        #print(Color._Reset)
        raise context.exception

    def _set_handlers(self, handler):
        start_handler = CommandHandler('start', handler.start)
        new_session_handler = CommandHandler('new', handler.new)
        delete_session_handler = CommandHandler('delete', handler.delete)
        select_session_handler = CommandHandler('select', handler.select)
        help_handler = CommandHandler('help', handler.help)
        debug_handler = CommandHandler('debug', handler.debug)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handler.echo)
        button_handler = CallbackQueryHandler(handler.button)
        self.application.add_handler(start_handler)
        self.application.add_handler(new_session_handler)
        self.application.add_handler(select_session_handler)
        self.application.add_handler(delete_session_handler)
        self.application.add_handler(help_handler)
        self.application.add_handler(debug_handler)
        self.application.add_handler(echo_handler)
        self.application.add_handler(button_handler)
        self.application.add_error_handler(self._error_handler)
        Color.OK('handlers set')


if __name__ == '__main__':
    engine = Engine()
    handler = Handler(engine)
    bot = TelegramBot(handler)
    bot.start()

