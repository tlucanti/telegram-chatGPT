
import time

_begin = True
def log(*args, **kwargs):
    print(*args, **kwargs)
    return

    global _begin
    if _begin:
        with open('log.txt', 'w'):
            _begin = False
    with open('log.txt', 'a') as f:
        print(*args, **kwargs, file=f)
        print(*args, **kwargs)

class Color():
    @staticmethod
    def OK(msg):
        log(Color._White + '[  ',
              Color._Green + 'OK',
              Color._White + '  ] ',
              msg, Color._Reset,
              sep='')

    @staticmethod
    def FAILED(msg):
        log(Color._White + '[',
              Color._Red + 'FAILED',
              Color._White + '] ',
              msg, Color._Reset,
              sep='')

    @staticmethod
    def timestamp():
        log(Color._White + time.strftime('[%H:%M:%S'),
              f'.{int(time.time() % 1 * 10000):04}] ',
              Color._Reset, sep='', end='')


    @staticmethod
    def G(msg):
        return Color._paint(Color._Green, msg)

    @staticmethod
    def W(msg):
        return Color._paint(Color._White, msg)

    @staticmethod
    def Y(msg):
        return Color._paint(Color._Yellow, msg)

    @staticmethod
    def R(msg):
        return Color._paint(Color._Red, msg)

    @staticmethod
    def P(msg):
        return Color._paint(Color._Purple, msg)

    @staticmethod
    def grey(msg):
        return Color._paint(Color._grey, msg)

    @staticmethod
    def _paint(color, msg):
        return color + msg + Color._Reset

    _grey   = '\033[1;90mm'

    _Black  = '\033[1;30m'
    _Red    = '\033[1;31m'
    _Green  = '\033[1;32m'
    _Yellow = '\033[1;33m'
    _Blue   = '\033[1;34m'
    _Purple = '\033[1;35m'
    _Cyan   = '\033[1;36m'
    _White  = '\033[1;37m'
    _Reset  = '\033[0m'
