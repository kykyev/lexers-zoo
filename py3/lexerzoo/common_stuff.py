"""
"""
from collections import namedtuple
from queue import Queue

__all__ = [
    'TOK_WORD', 'TOK_NUMBER', 'TOK_EOF',
    'Token',
    'MailBox',
    'Buffer'
]

# token's types
TOK_WORD = 'TOK_WORD'
TOK_NUMBER = 'TOK_NUMBER'
TOK_EOF = 'TOK_EOF'

# type - token's type
# value - token's value
# meta - token's meta information
Token = namedtuple('Token', 'type value meta')

# lineno - line number
# start - token's start position in line
# end - token's end position
TokenMetaInfo = namedtuple('TokenMetaInfo', 'lineno start end')

# annotated symbol
# symbol - plain symbol
# lineno - line number
# column - column number
Asymbol = namedtuple('Asymbol', 'symbol lineno column')


class MailBox:
    def __init__(self):
        self.box = Queue()

    def put(self, item):
        self.box.put(item)

    def get(self):
        item = self.box.get()
        if item == EOFError:
            raise EOFError
        return item

    def __iter__(self):
        for item in self.box:
            if item == EOFError:
                raise StopIteration
            yield item


class Buffer:
    def __init__(self):
        self.asymbols = []

    def push(self, s):
        self.asymbols.append(s)

    def reset(self):
        self.asymbols = []

    def token(self, type):
        _asymbols = self.asymbols
        value = "".join(s.symbol for s in _asymbols)
        meta = TokenMetaInfo(_asymbols[0].lineno, _asymbols[0].column, _asymbols[-1].column)
        return Token(type, value, meta)

    def __iter__(self):
        return iter(self.asymbols)