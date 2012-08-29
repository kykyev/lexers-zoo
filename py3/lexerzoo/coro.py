""" Not so boring lexer prototype.
Using just plain OOP without fancy subroutines or quasi-subroutines(generators),
but :run: method of lexer is more clever now. That allows to get rid of explicit
FSM states.
"""
from greenlet import greenlet
from lexerzoo.common_stuff import *


class Lexer:
    def __init__(self):
        self.input_stream = MailBox()
        self.output_stream = MailBox()

        self._buffer = Buffer()

        self._wait_state = greenlet(self._do_wait)
        self._word_state = greenlet(self._do_word)
        self._number_state = greenlet(self._do_number)
        self._end_state = greenlet(self._do_end)

    def run(self):
        self._wait_state.switch()

    def _do_wait(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                return self._end_state.switch()
            state = self._do_wait_step(s)
            if state is not None:
                state.switch()

    def _do_wait_step(self, s):
        if s.symbol.isalpha():
            self._buffer.push(s)
            return self._word_state
        elif s.symbol.isdigit():
            self._buffer.push(s)
            return self._number_state
        elif not s.symbol.isspace():
            raise RuntimeError("This shouldn't occur")

    def _do_word(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                self._emitoken(TOK_WORD)
                self._end_state.switch()
            state = self._do_word_step(s)
            if state is not None:
                return state.switch()

    def _do_word_step(self, s):
        if s.symbol.isspace():
            self._emitoken(TOK_WORD)
            return self._wait_state
        elif s.symbol.isalpha() or s.symbol.isdigit():
            self._buffer.push(s)
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_number(self):
        while True:
            try:
                s = self.input_stream.get()
            except EOFError:
                self._emitoken(TOK_NUMBER)
                self._end_state.switch()
            state = self._do_number_step(s)
            if state is not None:
                return state.switch()

    def _do_number_step(self, s):
        if s.symbol.isalpha():
            self._buffer.push(s)
            return self._word_state
        elif s.symbol.isspace():
            self._emitoken(TOK_NUMBER)
            return self._wait_state
        elif s.symbol.isdigit():
            self._buffer.push(s)
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_end(self):
        if self._buffer:
            raise RuntimeError("This shouldn't occur")
        self._emitoken(TOK_EOF)

    def _emitoken(self, token_type):
        self.output_stream.put(self.buffer.token(token_type))
        self.buffer.reset()
__author__ = 'me'
