
import time

class Color():
    @staticmethod
    def OK(msg):
        print(Color._White + '[  ',
              Color._Green + 'OK',
              Color._White + '  ] ',
              msg, Color._Reset,
              sep='')

    @staticmethod
    def FAILED(msg):
        print(Color._White + '[',
              Color._Red + 'FAILED',
              Color._White + '] ',
              msg, Color._Reset,
              sep='')

    @staticmethod
    def timestamp():
        print(Color._White + time.strftime('[%H:%M:%S'),
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
    def _paint(color, msg):
        return color + msg + Color._Reset

    _Black  = '\033[1;30m'
    _Red    = '\033[1;31m'
    _Green  = '\033[1;32m'
    _Yellow = '\033[1;33m'
    _Blue   = '\033[1;34m'
    _Purple = '\033[1;35m'
    _Cyan   = '\033[1;36m'
    _White  = '\033[1;37m'
    _Reset  = '\033[0m'
