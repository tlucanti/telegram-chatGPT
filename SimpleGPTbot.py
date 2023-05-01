
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, MenuButtonCommands
from GPT import GPT
from collections import defaultdict
from Color import Color
from Color import log

class SimpleGPTbot():
    WAIT_FOR_ROLE = 0x1

    def __init__(self, token=None):
        if token is None:
            self.token = self.get_token()
        else:
            self.token = token
        self.application = ApplicationBuilder().token(self.token).build()
        start_handler = CommandHandler('start', self.new_client)
        echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler)
        reset_handler = CommandHandler('reset', self.reset)
        help_handler = CommandHandler('help', self.help)
        temperature_handler = CommandHandler('temp', self.temp)
        button_handler = CallbackQueryHandler(self.button)
        role_handler = ConversationHandler(
            entry_points=[CommandHandler('role', self.role)],
            states={
                self.WAIT_FOR_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_role)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        for handler in start_handler, role_handler, reset_handler, help_handler, \
            temperature_handler, echo_handler, button_handler:
                self.application.add_handler(handler)
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
        self.users[chat_id].reset()
        Color.timestamp()
        log(Color.P('RESET') + Color.W(f' : {chat_id}'))
        await context.bot.send_message(chat_id=chat_id, text='reset completed')

    async def temp(self, update, context):
        chat_id = update.effective_chat.id
        user = self.users[chat_id]
        Color.timestamp()
        log('temp')
        keyboard = [[
            InlineKeyboardButton('low', callback_data='temp_low'),
            InlineKeyboardButton('normal', callback_data='temp_normal'),
            InlineKeyboardButton('high', callback_data='temp_high')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f'select temperature value (current is {user.get_temperature()})'
        msg = await update.message.reply_text(text, reply_markup=reply_markup)

    async def role(self, update, context):
        chat_id = update.effective_chat.id
        user = self.users[chat_id]
        Color.timestamp()
        log('role')
        text = 'select new role (or type /cancel). current role is:\n' + user.get_role()
        await context.bot.send_message(chat_id=chat_id, text=text)
        return self.WAIT_FOR_ROLE

    async def cancel(self, update, context):
        chat_id = update.effective_chat.id
        Color.timestamp()
        log('cancel role change')
        await context.bot.send_message(chat_id=chat_id, text='cancelled')
        return ConversationHandler.END

    async def select_role(self, update, context):
        chat_id = update.effective_chat.id
        user = self.users[chat_id]
        Color.timestamp()
        role_text = update.message.text
        log('selected role: ' + role_text)
        user.set_role(role_text)
        user.reset()
        await context.bot.send_message(chat_id=chat_id, text='selected new role')
        return ConversationHandler.END

    async def button(self, update, context):
        chat_id = update.effective_chat.id
        user = self.users[chat_id]
        query = update.callback_query
        await query.answer()
        data = query.data
        Color.timestamp()
        log(f'temp selected {data}')
        if data == 'temp_low':
            user.set_temperature(0.2, 'low')
            data = 'low'
        elif data == 'temp_normal':
            user.set_temperature(1, 'normal')
            data = 'normal'
        elif data == 'temp_high':
            user.set_temperature(1.5, 'high')
            data = 'high'
        else:
            Color.FAILED(f'unknown button {data}')
        text=f'selected temperature: {data}'
        await query.edit_message_text(text=text)


    async def help(self, update, context):
        chat_id = update.effective_chat.id
        self.users[chat_id] = GPT()
        Color.timestamp()
        log('help')
        text = 'help:\n' \
            '\n' \
            '/start\n' \
            '  start conversation\n' \
            '/help\n' \
            '  prints this message\n' \
            '/reset\n' \
            '  reset gpt instance\n' \
            '/temp\n' \
            '  change temperature value\n' \
            '/role\n' \
            '  change gpt role'
        await context.bot.send_message(chat_id=chat_id, text=text)

    async def new_client(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text[7:].strip()
        Color.timestamp()
        log(Color.P('NEW CLIENT') + Color.W(f' : {chat_id}'))
        await context.bot.set_my_commands([
            ('/start', 'start'),
            ('/help', 'manual'),
            ('/reset', 'reset session'),
            ('/temp', 'select temperature'),
            ('/role', 'change chat role')
        ])
        await context.bot.set_chat_menu_button(chat_id=chat_id, menu_button=MenuButtonCommands())

    @staticmethod
    def get_token(path='./.simplebot.token'):
        try:
            f = open(path, 'r')
            token = f.read().strip()
            f.close()
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your telegram api token in `.simplebot.token` file')
            sys.exit(1)

if __name__ == '__main__':
    #token = SimpleGPTbot.get_token('.telegram.token')
    #bot = SimpleGPTbot(token)
    bot = SimpleGPTbot()
    bot.start()
