""" Not so boring lexer prototype.
Using just plain OOP without fancy subroutines or quasi-subroutines(generators),
but :run: method of lexer is more clever now. That allows to get rid of explicit
FSM states.
"""
from lexerzoo.common_stuff import *


class Lexer:
    def __init__(self):
        self.input_stream = MailBox()
        self.output_stream = MailBox()
        self.buffer = Buffer()

    def run(self):
        state = self._do_wait
        while state != self._do_end:
            state = state()
        else:
            self._do_end()

    def _do_wait(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                return self._do_end
            state = self._do_wait_step(s)
            if state:
                return state

    def _do_wait_step(self, s):
        if s.symbol.isalpha():
            self.buffer.push(s)
            return self._do_word
        elif s.symbol.isdigit():
            self.buffer.push(s)
            return self._do_number
        elif not s.symbol.isspace():
            raise RuntimeError("This shouldn't occur")

    def _do_word(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                self._emitoken(TOK_WORD)
                return self._do_end
            state = self._do_word_step(s)
            if state:
                return state

    def _do_word_step(self, s):
        if s.symbol.isspace():
            self._emitoken(TOK_WORD)
            return self._do_wait
        elif s.symbol.isalpha() or s.symbol.isdigit():
            self.buffer.push(s)
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_number(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                self._emitoken(TOK_NUMBER)
                return self._do_end
            state = self._do_number_step(s)
            if state:
                return state

    def _do_number_step(self, s):
        if s.symbol.isalpha():
            self.buffer.push(s)
            return self._do_word
        elif s.symbol.isspace():
            self._emitoken(TOK_NUMBER)
            return self._do_wait
        elif s.symbol.isdigit():
            self.buffer.push(s)
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_end(self):
        if self.buffer:
            raise RuntimeError("This shouldn't occur")
        self._emitoken(TOK_EOF)

    def _emitoken(self, token_type):
        self.output_stream.put(self.buffer.token(token_type))
        self.buffer.reset()
