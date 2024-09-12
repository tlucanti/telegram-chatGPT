
import openai
from Color import Color
from Color import log

class GPT():

    MAX_CONTEXT = 2000
    DEFAULT_ROLE = 'You are an intelligent assistant'

    def __init__(self, role=None):
        if role is None:
            role = self.DEFAULT_ROLE
        self.client = openai.OpenAI(api_key=self._get_token())
        self.model = 'gpt-4'
        self.temperature = 1
        self.temp_value = 'normal'
        self.role = role
        self.messages = [{
            'role': 'system',
            'content': self.role}]

    def cut_context(self, context):
        ret = []
        cont_len = 0
        for c in context[::-1]:
            ret.append(c)
            cont_len += len(c['content'])
            if cont_len > self.MAX_CONTEXT:
                break
        return ret[::-1], cont_len

    def query(self, prompt, role='user'):
        self.messages.append({
            'role': 'user',
            'content': prompt
        })
        self.messages, cont_len = self.cut_context(self.messages)
        response = None
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=self.messages, temperature=self.temperature
            )
        except openai.RateLimitError:
            log(Color.R('RATE LIMIT ERROR'))
            return '[INTERNAL ERROR]: бабло кончилось, наболтались'
        except Exception as e:
            log(Color.R(str(response)))
            return f'[INTERNAL ERROR]: {e}'

        Color.timestamp()
        log(f'context size: {cont_len}')
        reply = response.choices[0].message.content

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

    def set_role(self, role=None):
        if role is None:
            role = self.DEFAULT_ROLE
        self.role = role

    def _get_token(self):
        try:
            f = open('./.openai.token', 'r')
            token = f.read().strip()
            f.close()
            Color.OK('OpenAI token obtained')
            return token
        except FileNotFoundError as e:
            Color.FAILED('place your openai api token in `.openai.token` file')
            sys.exit(1)

if __name__ == '__main__':
    gpt = GPT()
    while True:
        input()
        with open('test.txt') as f:
            prompt = f.read()
        reply = gpt.query(prompt, 0)
        log('<<<', reply)
