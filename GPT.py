
import openai
from Color import Color

class GPT():

    class GPTRole():
        class User(): pass

    def __init__(self, role=None):
        openai.api_key = self._get_token()
        self.model = 'gpt-3.5-turbo'
        if role is None:
            role = 'You are a intelligent assistant'
        self.messages = [{
            'role': 'system',
            'content': role}]

    def query(self, prompt, role='user', temperature=0.5):
        self.messages.append({
            'role': 'user',
            'content': prompt
        })
        response = openai.ChatCompletion.create(
            model=self.model, messages=self.messages
        )
        Color.timestamp()
        try:
            reply = response.choices[0].message.content
        except Exception:
            print(Color.R(str(response)))
            return 'ERROR\n' + str(response)
        self.messages.append({
            "role": "assistant",
            "content": reply})
        return reply

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
    gpt = GPT()
    while True:
        prompt = input('>>> ')
        reply = gpt.query(prompt)
        print('<<<', reply)
