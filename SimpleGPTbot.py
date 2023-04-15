
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from GPT import GPT
from collections import defaultdict
from Color import Color
from Color import log

class SimpleGPTbot():
    def __init__(self):
        self.token = self._get_token()
        self.application = ApplicationBuilder().token(self.token).build()
        start_handler = CommandHandler('start', self.new_client)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handler)
        reset_handler = CommandHandler('reset', self.reset)
        self.application.add_handler(echo_handler)
        self.application.add_handler(reset_handler)
        self.application.add_handler(start_handler)

        self.users = defaultdict(GPT)

    def start(self):
        log('running')
        self.application.run_polling()

    async def handler(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text
        user = self.users[chat_id]
        Color.timestamp()
        log(Color.W(f'{chat_id} >>>'), request)
        response = user.query(request)
        log(Color.W(f'{chat_id} <<<'), response)
        await context.bot.send_message(chat_id=chat_id, text=response)

    async def reset(self, update, context):
        chat_id = update.effective_chat.id
        self.users[chat_id] = GPT()
        Color.timestamp()
        log(Color.P('RESET') + Color.W(f' : {chat_id}'))
        await context.bot.send_message(chat_id=chat_id, text='reset completed')

    async def new_client(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text[7:].strip()

        Color.timestamp()
        log(Color.P('NEW CLIENT') + Color.W(f' : {chat_id}'))

    def _get_token(self):
        try:
            f = open('./.simplebot.token', 'r')
            token = f.read().strip()
            f.close()
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your telegram api token in `.simplebot.token` file')
            sys.exit(1)

if __name__ == '__main__':
    bot = SimpleGPTbot()
    bot.start()
