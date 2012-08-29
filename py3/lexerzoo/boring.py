""" Boring lexer prototype.
Using just plain OOP without fancy subroutines or quasi-subroutines(generators).
"""
from lexerzoo.common_stuff import *

# FSM states
WAIT = 0
WORD = 1
NUMBER = 2
END = 3


class Lexer:
    def __init__(self):
        self.input_stream = MailBox()
        self.output_stream = MailBox()
        self.buffer = Buffer()

    def run(self):
        state = WAIT
        while True:
            if state == WAIT:
                state = self._do_wait_step()
            elif state == WORD:
                state = self._do_word_step()
            elif state == NUMBER:
                state = self._do_number_step()
            elif state == END:
                self._do_end_step()
                break
            else:
                raise RuntimeError("Unknown state: ", state)
    
    def _do_wait_step(self):
        try:
            s = self.input_stream.get()
        except EOFError:
            return END
        if s.symbol.isalpha():
            self.buffer.push(s)
            return WORD
        elif s.symbol.isdigit():
            self.buffer.push(s)
            return NUMBER
        elif s.symbol.isspace():
            return WAIT
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_word_step(self):
        try:
            s = self.input_stream.get()
        except EOFError:
            self._emitoken(TOK_WORD)
            return END
        if s.symbol.isspace():
            self._emitoken(TOK_WORD)
            return WAIT
        elif s.symbol.isalpha() or s.symbol.isdigit():
            self.buffer.push(s)
            return WORD
        else:
            raise RuntimeError("This shouldn't occur")

    def _do_number_step(self):
        try:
            s = self.input_stream.get()
        except EOFError:
            self._emitoken(TOK_NUMBER)
            return END
        if s.symbol.isalpha():
            self.buffer.push(s)
            return WORD
        elif s.symbol.isspace():
            self._emitoken(TOK_NUMBER)
            return WAIT
        elif s.symbol.isdigit():
            self.buffer.push(s)
            return NUMBER
        else:
            raise RuntimeError("This shouldn't occur")
        
    def _do_end_step(self):
        if self.buffer:
            raise RuntimeError("This shouldn't occur")
        self._emitoken(TOK_EOF)

    def _emitoken(self, token_type):
        self.output_stream.put(self.buffer.token(token_type))
        self.buffer.reset()
