
import time
from Color import Color

class GPT():
    STATUS_OK = 0x0
    STATUS_ERR = 0x1

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
            self.messages.append(GPT.Message(request, response))

        def __repr__(self):
            return f'Session: {self.messages}'

    class Client():
        E_OK = 0x0
        E_SESSION_EXISTS = 0x1
        E_SESSION_NOT_EXISTS = 0x2

        def __init__(self, id):
            self.id = id
            self.sessions = dict()
            self.current_session = None
            self.message_ids = []

        def add_session(self, name):
            self.current_session = name
            if name in self.sessions:
                return self.E_SESSION_EXISTS
            self.sessions[name] = GPT.Session(name)
            self.current_session = self.sessions[name]
            return self.E_OK

        def select_session(self, name):
            if name not in self.sessions:
                return self.E_SESSION_NOT_EXISTS
            self.current_session = self.sessions[name]
            return self.E_OK

        def remove_session(self, name):
            del self.sessions[name]

        def register_message(self, message_id):
            self.message_ids.append(message_id)

        def __repr__(self):
            return f'Client: {self.sessions}'

    def __init__(self):
        self.chat_data = dict()

    def start(self, client_id):
        Color.timestamp()
        print(Color.Y('NEW CLIENT') + Color.W(f' : {client_id}'))
        if client_id in self.chat_data:
            return 'you are already registered'
        self.chat_data[client_id] = self.Client(client_id)
        return 'здарова че'

    def new(self, client_id, session_name):
        Color.timestamp()
        client = self.chat_data[client_id]
        if client.add_session(session_name):
            return f'session `{session_name}` already exists', self.STATUS_ERR
        print(Color.W('new session:'), session_name)
        return f'session `{session_name}` created', self.STATUS_OK

    def select(self, client_id, session_name):
        Color.timestamp()
        print(client_id, 'selecting session', session_name)
        client = self.chat_data[client_id]
        if client.select_session(session_name):
            return f'session `{session_name}` not exist', self.STATUS_ERR
        return client.current_session.messages, self.STATUS_OK

    def active(self, client_id):
        Color.timestamp()
        print(client_id, 'getting active sessions')
        client = self.chat_data[client_id]
        if len(client.sessions) == 0:
            return 'you have no active sessions'
        else:
            return 'active sessions:\n' + '\n'.join([session for session in client.sessions])

    def query(self, client_id, request):
        Color.timestamp()
        print(Color.W('REQUEST: ') + request)
        client = self.chat_data[client_id]

        response = self._query(request)
        Color.timestamp()
        print(Color.W('RESPONSE: ') + response)
        client.current_session.add_message(request, response)
        return response

    def register_message(self, client_id, message_id):
        self.chat_data[client_id].register_message(message_id)

    def get_client_messages(self, client_id):
        return self.chat_data[client_id].message_ids

    def clear_client_messages(self, client_id):
        self.chat_data[client_id].message_ids = []

    def _query(self, message):
        return message.upper()

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
