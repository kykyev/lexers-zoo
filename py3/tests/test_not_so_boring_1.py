from lexerzoo.not_so_boring_1 import Lexer
from lexerzoo.common_stuff import Asymbol


def test_do_word_step():
    d = {
        'z': _test_do_word_step_letter,
        '1': _test_do_word_step_digit,
        ' ': _test_do_word_step_space,
        '\t': _test_do_word_step_tab,
        '\n': _test_do_word_step_newline

    }
    for symb, test in d.items():
        lex = Lexer()
        lex.buffer.push(Asymbol('a', 1, 5))
        yield test, lex, Asymbol(symb, 1, 6)


def _test_do_word_step_letter(lex, s):
    next_state = lex._do_word_step(s)
    assert None == next_state
    assert [Asymbol('a', 1, 5), Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_word_step_digit(lex, s):
    next_state = lex._do_word_step(s)
    assert None == next_state
    assert [Asymbol('a', 1, 5), Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_word_step_space(lex, s):
    next_state = lex._do_word_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols

def _test_do_word_step_tab(lex, s):
    next_state = lex._do_word_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols

def _test_do_word_step_newline(lex, s):
    next_state = lex._do_word_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols



def test_do_number_step():
    d = {
        'z': _test_do_number_step_letter,
        '1': _test_do_number_step_digit,
        ' ': _test_do_number_step_space,
        '\t': _test_do_number_step_tab,
        '\n': _test_do_number_step_newline
    }
    for symb, test in d.items():
        lex = Lexer()
        lex.buffer.push(Asymbol('2', 1, 5))
        yield test, lex, Asymbol(symb, 1, 6)

def _test_do_number_step_letter(lex, s):
    next_state = lex._do_number_step(s)
    assert lex._do_word == next_state
    assert [Asymbol('2', 1, 5), Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_number_step_digit(lex, s):
    next_state = lex._do_number_step(s)
    assert None == next_state
    assert [Asymbol('2', 1, 5), Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_number_step_space(lex, s):
    next_state = lex._do_number_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols

def _test_do_number_step_tab(lex, s):
    next_state = lex._do_number_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols

def _test_do_number_step_newline(lex, s):
    next_state = lex._do_number_step(s)
    assert lex._do_wait == next_state
    assert [] == lex.buffer.asymbols


def test_do_wait_step():
    d = {
        'z': _test_do_wait_step_letter,
        '1': _test_do_wait_step_digit,
        ' ': _test_do_wait_step_space,
        '\t': _test_do_wait_step_tab,
        '\n': _test_do_wait_step_newline
    }
    for symb, test in d.items():
        lex = Lexer()
        yield test, lex, Asymbol(symb, 1, 6)

def _test_do_wait_step_letter(lex, s):
    next_state = lex._do_wait_step(s)
    assert lex._do_word == next_state
    assert [Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_wait_step_digit(lex, s):
    next_state = lex._do_wait_step(s)
    assert lex._do_number == next_state
    assert [Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_wait_step_space(lex, s):
    next_state = lex._do_wait_step(s)
    assert None == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_step_tab(lex, s):
    next_state = lex._do_wait_step(s)
    assert None == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_step_newline(lex, s):
    next_state = lex._do_wait_step(s)
    assert None == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_step_eof(lex, s):
    next_state = lex._do_wait_step(s)
    assert lex._do_end == next_state
    assert [] == lex.buffer.asymbols
  