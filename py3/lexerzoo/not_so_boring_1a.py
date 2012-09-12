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

        self._do_wait = self._do_wait_gen()
        self._do_word = self._do_word_gen()
        self._do_number = self._do_number_gen()

    def run(self):
        state = self._do_wait
        while state != self._do_end:
            state = next(state)
        else:
            self._do_end()

    def _do_wait_gen(self):
        for s in self.input_stream:
            state = self._do_wait_step(s)
            if state:
                yield state
        yield self._do_end

    def _do_wait_step(self, s):
        if s.symbol.isalpha():
            self.buffer.push(s)
            return self._do_word
        elif s.symbol.isdigit():
            self.buffer.push(s)
            return self._do_number
        elif not s.symbol.isspace():
            raise RuntimeError("This shouldn't occur")

    def _do_word_gen(self):
        for s in self.input_stream:
            state = self._do_word_step(s)
            if state:
                yield state
        self._emitoken(TOK_WORD)
        yield self._do_end

    def _do_word_step(self, s):
        if s.symbol.isspace():
            self._emitoken(TOK_WORD)
            return self._do_wait
        elif s.symbol.isalpha() or s.symbol.isdigit():
            self.buffer.push(s)
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_number_gen(self):
        for s in self.input_stream:
            state = self._do_number_step(s)
            if state:
                yield state
        self._emitoken(TOK_NUMBER)
        yield self._do_end

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
