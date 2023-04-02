
from Color import Color

class Handler():
    def __init__(self, processor):
        self.processor = processor

    async def echo(self, update, context):
        await self._echo(update, context)

    async def start(self, update, context):
        chat_id = update.effective_chat.id
        try:
            response = self.processor.start(chat_id)
        except processor.ExceptionType as exc:
            response = exc.message
        msg = await context.bot.send_message(chat_id=chat_id, text=response)
        self.processor.register_message(chat_id, update.message.id)
        self.processor.register_message(chat_id, msg.id)

    async def new(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text[4:].strip()
        self.processor.register_message(chat_id, update.message.id)
        try:
            response = self.processor.new(chat_id, request)
        except self.processor.ExceptionType as exc:
            msg = await context.bot.send_message(chat_id=chat_id, text=exc.message)
            self.processor.register_message(chat_id, msg.id)
            return
        msg = await context.bot.send_message(chat_id=chat_id, text=response)
        await self._clear_history(context.bot, chat_id)
        self.processor.register_message(chat_id, msg.id)

    async def select(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text[7:].strip()
        self.processor.register_message(chat_id, update.message.id)
        try:
            response = self.processor.select(chat_id, request)
        except self.processor.ExceptionType as exc:
            msg = await context.bot.send_message(chat_id=chat_id, text=exc.message)
            self.processor.register_message(chat_id, msg.id)
            return
        await self._clear_history(context.bot, chat_id)
        await self._restore_history(context.bot, chat_id, response)

    async def active(self, update, context):
        chat_id = update.effective_chat.id
        try:
            response = self.processor.active(chat_id)
        except self.processor.ExceptionType as exc:
            response = exc.message
        msg = await context.bot.send_message(chat_id=chat_id, text=response)
        self.processor.register_message(chat_id, update.message.id)
        self.processor.register_message(chat_id, msg.id)

    async def help(self, update, context):
        chat_id = update.effective_chat.id
        response = self.processor.help()
        msg = await context.bot.send_message(chat_id=chat_id, text=response)
        self.processor.register_message(chat_id, update.message.id)
        self.processor.register_message(chat_id, msg.id)

    async def debug(self, update, context):
        chat_id = update.effective_chat.id
        response = str(self.processor)
        msg = await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        self.processor.register_message(chat_id, update.message.id)
        self.processor.register_message(chat_id, msg.id)

    async def echo(self, update, context):
        chat_id = update.effective_chat.id
        request = update.message.text
        try:
            response = self.processor.query(update.effective_chat.id, request)
        except self.processor.ExceptionType as exc:
            msg = await context.bot.send_message(chat_id=chat_id, text=exc.message)
            self.processor.register_message(chat_id, update.message.id)
            self.processor.register_message(chat_id, msg.id)
            return
        await context.bot.delete_message(chat_id, update.message.id)
        response = '>>> ' + request + '\n\n' + response
        msg = await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        self.processor.register_message(chat_id, msg.id)

    async def _clear_history(self, bot, chat_id):
        for message_id in self.processor.get_client_messages(chat_id):
            Color.timestamp()
            print('deleting message', message_id)
            await bot.delete_message(chat_id, message_id)
        self.processor.clear_client_messages(chat_id)

    async def _restore_history(self, bot, chat_id, messages):
        for message in messages:
            Color.timestamp()
            print('restoring message', message)
            text = '>>> ' + message.request + '\n\n' + message.response
            msg = await bot.send_message(chat_id=chat_id, text=text)
            self.processor.register_message(chat_id, msg.id)

