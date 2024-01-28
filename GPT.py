
import openai
from Color import Color
from Color import log

class GPT():

    MAX_CONTEXT = 2000

    def __init__(self, role=None):
        if role is None:
            #role = 'You are an article writing assistant'
            role = 'You are an intelligent assistant'
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
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages, temperature=self.temperature
        )
        Color.timestamp()
        log(f'context size: {cont_len}')
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
