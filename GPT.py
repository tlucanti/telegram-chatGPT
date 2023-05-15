
import openai
from Color import Color
from Color import log

class GPT():

    def __init__(self, role=None):
        if role is None:
            role = 'You are an article writing assistant'
            #role = 'You are a intelligent assistant'
        openai.api_key = self._get_token()
        self.model = 'gpt-3.5-turbo'
        self.temperature = 1
        self.temp_value = 'normal'
        self.role = role
        self.messages = [{
            'role': 'system',
            'content': self.role}]

    def query(self, prompt, role='user'):
        self.messages.append({
            'role': 'user',
            'content': prompt
        })
        response = openai.ChatCompletion.create(
            model=self.model, messages=self.messages, temperature=self.temperature
        )
        Color.timestamp()
        try:
            reply = response.choices[0].message.content
            log(str(response))
        except Exception:
            log(Color.R(str(response)))
            return 'ERROR\n' + str(response)
        self.messages.append({
            'role': 'assistant',
            'content': reply})
        return reply

    def reset(self):
        self.messages = [{
            'role': 'system',
            'content': self.role}]

    def get_temperature(self):
        return self.temp_value

    def set_temperature(self, num, value):
        self.temperature = num
        self.temp_value = value

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role

    def _get_token(self):
        try:
            f = open('./.openai.token', 'r')
            token = f.read().strip()
            f.close()
            Color.OK('token obtained')
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your openai api token in `.openai.token` file')
            sys.exit(1)

if __name__ == '__main__':
    gpt = GPT('assistant for solving economic problems')
    while True:
        input()
        with open('test.txt') as f:
            prompt = f.read()
        reply = gpt.query(prompt, 0)
        log('<<<', reply)
