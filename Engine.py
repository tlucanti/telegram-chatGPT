
import time
from Color import Color
from collections import defaultdict

class Engine():
    ExceptionType = None

    class EngineError(ValueError):
        def __init__(self, message):
            super().__init__(message)
            self.message = message

    class Message():
        def __init__(self, request, response):
            self.request = request
            self.response = response

        def __repr__(self):
            return f'{self.request} -> {self.response}'

    class Session():
        def __init__(self, name):
            self.name = name
            self.messages = []

        def add_message(self, request, response):
            self.messages.append(Engine.Message(request, response))

        def __repr__(self):
            return f'Session: {self.messages}'

    class Client():
        def __init__(self):
            self.registered = False
            self.sessions = dict()
            self.current_session = None
            self.message_ids = []
            self.session_counter = 0

        def add_session(self, name):
            if len(self.sessions) >= 10:
                raise Engine.GPTerror('you have session limit')
            self.session_counter += 1
            if name is None:
                name = f'session {self.session_counter}'
            self.current_session = name
            if name in self.sessions:
                raise Engine.GPTerror(f'session `{name}` already exists')
            self.sessions[name] = Engine.Session(name)
            self.current_session = self.sessions[name]
            return name

        def select_session(self, name):
            if name not in self.sessions:
                raise Engine.GPTerror(f'session `{name}` does not exists')
            self.current_session = self.sessions[name]

        def remove_session(self, name):
            if name not in self.sessions:
                raise Engine.GPTerror(f'session `{name}` does not exist')
            del self.sessions[name]

        def remoe_all_sessions(self, name):
            self.sessions = dict()

        def register_message(self, message_id):
            self.message_ids.append(message_id)

        def __repr__(self):
            return f'Client: {self.sessions}'

    def __init__(self, gpt):
        self.gpt = gpt
        self.ExceptionType = self.EngineError
        self.chat_data = defaultdict(self.Client)

    def start(self, client_id):
        self._assert_not_registered(client_id)
        self.chat_data[client_id].registered = True
        response = 'здарова че'
        Color.timestamp()
        print(Color.P('NEW CLIENT') + Color.W(f' : {client_id}'))
        return response

    def new(self, client_id, session_name):
        self._assert_registered(client_id)
        client = self.chat_data[client_id]
        session_name = client.add_session(session_name)
        response = f'session `{session_name}` created'
        Color.timestamp()
        print(Color.Y('new session:'), session_name)
        return response

    def select(self, client_id, session_name):
        self._assert_registered(client_id)
        client = self.chat_data[client_id]
        client.select_session(session_name)
        response = client.current_session.messages
        Color.timestamp()
        print(client_id, 'selecting session', session_name)
        return response

    def delete(self, client_id, session_name):
        self._assert_registered(client_id)
        client = self.chat_data[client_id]
        if session_name is None:
            Color.timestamp()
            print('deleting all sessions')
            client.current_session = None
            cilent.remove_all_sessions()
            return True
        was_current_session = False
        if client.current_session.name == session_name:
            client.current_session = None
            was_current_session = True
        Color.timestamp()
        print('deleing session', session_name)
        client.remove_session(session_name)
        return was_current_session

    def active(self, client_id):
        self._assert_registered(client_id)
        client = self.chat_data[client_id]
        if len(client.sessions) == 0:
            raise self.EngineError('you have no active sessions')
        else:
            response = client.sessions
        Color.timestamp()
        print(client_id, 'getting active sessions')
        return response

    def query(self, client_id, request):
        self._assert_registered(client_id)
        self._assert_active_session(client_id)
        client = self.chat_data[client_id]
        Color.timestamp()
        print(Color.W('REQUEST: ') + request)
        response = self.gpt.query(request)
        Color.timestamp()
        print(Color.W('RESPONSE: ') + response)
        client.current_session.add_message(request, response)
        return response

    def help(self):
        return 'help:\n' \
            '\n' \
            '/start' \
            '  register user\n' \
            '/new [session_name]\n' \
            '  create new chat session with [session_name]\n' \
            '/select [session_name]\n' \
            '  select other session by [session_name]\n' \

    def register_message(self, client_id, message_id):
        self.chat_data[client_id].register_message(message_id)

    def get_client_messages(self, client_id):
        return self.chat_data[client_id].message_ids

    def clear_client_messages(self, client_id):
        self.chat_data[client_id].message_ids = []

    def _query(self, message):
        return message.upper()

    def _assert_not_registered(self, client_id):
        if self.chat_data[client_id].registered:
            raise self.EngineError('you are already registered')

    def _assert_registered(self, client_id):
        if not self.chat_data[client_id].registered:
            raise self.EngineError('you are not registered, type /help')

    def _assert_active_session(self, client_id):
        if self.chat_data[client_id].current_session is None:
            raise self.EnginEerror('you have no active sessions, type /help')

    def __repr__(self):
        repr = ''
        for client in self.chat_data.values():
            repr += f'client: {client.id}\n'
            for session in client.sessions.values():
                repr += f'    session: {session.name}\n'
                for message in session.messages:
                    repr += f'        {message.request} -> {message.response}\n'
        if len(repr) == 0:
            return 'empty'
        return repr
