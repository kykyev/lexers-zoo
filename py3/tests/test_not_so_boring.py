from lexerzoo.not_so_boring import Lexer
from lexerzoo.common_stuff import Asymbol


def test_do_word():
    d = {
        'z': _test_do_word_letter,
        '1': _test_do_word_digit,
        ' ': _test_do_word_space,
        '\t': _test_do_word_tab,
        '\n': _test_do_word_newline,
        None: _test_do_word_eof

    }
    for symb, test in d.items():
        lex = Lexer()
        lex.buffer.push(Asymbol('a', 1, 5))
        lex.input_stream.put(Asymbol(symb, 1, 6) if symb else EOFError)
        yield test, lex


def _test_do_word_letter(lex):
    next_state = lex._do_word_step()
    assert lex._do_word_step == next_state
    assert [Asymbol('a', 1, 5), Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_word_digit(lex):
    next_state = lex._do_word_step()
    assert lex._do_word_step == next_state
    assert [Asymbol('a', 1, 5), Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_word_space(lex):
    next_state = lex._do_word_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_word_tab(lex):
    next_state = lex._do_word_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_word_newline(lex):
    next_state = lex._do_word_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_word_eof(lex):
    next_state = lex._do_word_step()
    assert lex._do_end_step == next_state
    assert [] == lex.buffer.asymbols

    
def test_do_number():
    d = {
        'z': _test_do_number_letter,
        '1': _test_do_number_digit,
        ' ': _test_do_number_space,
        '\t': _test_do_number_tab,
        '\n': _test_do_number_newline,
        None: _test_do_number_eof

    }
    for symb, test in d.items():
        lex = Lexer()
        lex.buffer.push(Asymbol('2', 1, 5))
        lex.input_stream.put(Asymbol(symb, 1, 6) if symb else EOFError)
        yield test, lex

def _test_do_number_letter(lex):
    next_state = lex._do_number_step()
    assert lex._do_word_step == next_state
    assert [Asymbol('2', 1, 5), Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_number_digit(lex):
    next_state = lex._do_number_step()
    assert lex._do_number_step == next_state
    assert [Asymbol('2', 1, 5), Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_number_space(lex):
    next_state = lex._do_number_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_number_tab(lex):
    next_state = lex._do_number_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_number_newline(lex):
    next_state = lex._do_number_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_number_eof(lex):
    next_state = lex._do_number_step()
    assert lex._do_end_step == next_state
    assert [] == lex.buffer.asymbols
    
    
def test_do_wait():
    d = {
        'z': _test_do_wait_letter,
        '1': _test_do_wait_digit,
        ' ': _test_do_wait_space,
        '\t': _test_do_wait_tab,
        '\n': _test_do_wait_newline,
        None: _test_do_wait_eof

    }
    for symb, test in d.items():
        lex = Lexer()
        lex.input_stream.put(Asymbol(symb, 1, 6) if symb else EOFError)
        yield test, lex

def _test_do_wait_letter(lex):
    next_state = lex._do_wait_step()
    assert lex._do_word_step == next_state
    assert [Asymbol('z', 1, 6)] == lex.buffer.asymbols

def _test_do_wait_digit(lex):
    next_state = lex._do_wait_step()
    assert lex._do_number_step == next_state
    assert [Asymbol('1', 1, 6)] == lex.buffer.asymbols

def _test_do_wait_space(lex):
    next_state = lex._do_wait_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_tab(lex):
    next_state = lex._do_wait_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_newline(lex):
    next_state = lex._do_wait_step()
    assert lex._do_wait_step == next_state
    assert [] == lex.buffer.asymbols

def _test_do_wait_eof(lex):
    next_state = lex._do_wait_step()
    assert lex._do_end_step == next_state
    assert [] == lex.buffer.asymbols  