from lexerzoo.not_so_boring_1a import Lexer
from lexerzoo.common_stuff import Asymbol, TOK_NUMBER, TOK_WORD
from mock import Mock

def factory_wait_step():
    def test_do_wait_step():
        d = {
            'z': _test_do_wait_step_letter,
            '1': _test_do_wait_step_digit,
            ' ': _test_do_wait_step_space,
            '\t': _test_do_wait_step_space,
            '\n': _test_do_wait_step_space
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

    return test_do_wait_step


def factory_word_step():
    def test_do_word_step():
        d = {
            'z': _test_do_word_step_letter,
            '1': _test_do_word_step_digit,
            ' ': _test_do_word_step_space,
            '\t': _test_do_word_step_space,
            '\n': _test_do_word_step_space
        }
        for sym, test in d.items():
            lex = Lexer()
            lex.buffer.push(Asymbol('a', 1, 5))
            yield test, lex, Asymbol(sym, 1, 6)


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

    return test_do_word_step


def factory_number_step():
    def test_do_number_step():
        d = {
            'z': _test_do_number_step_letter,
            '1': _test_do_number_step_digit,
            ' ': _test_do_number_step_space,
            '\t': _test_do_number_step_space,
            '\n': _test_do_number_step_space
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
    
    return test_do_number_step


test_do_wait_step = factory_wait_step()
test_do_word_step = factory_word_step()
test_do_number_step = factory_number_step()


def __input_stream(it):
    for item in it:
        if item == EOFError:
            raise StopIteration
        yield item

def test_do_wait():
    d = {
        (' ', 'a'): _test_do_wait_letter,
        ('\t', 'a'): _test_do_wait_letter,
        ('\n', 'a'): _test_do_wait_letter,
        (' ', '1'): _test_do_wait_digit,
        ('\t', '1'): _test_do_wait_digit,
        ('\n', '1'): _test_do_wait_digit,
        (' ', EOFError): _test_do_wait_eof,
        ('\t', EOFError): _test_do_wait_eof,
        ('\n', EOFError): _test_do_wait_eof,
    }
    for input, test in d.items():
        lex = Lexer()
        lex.input_stream = __input_stream(
            sym if sym == EOFError else Asymbol(sym, 1, i + 1)
                for i, sym in enumerate(input)
        )
        yield test, lex

def _test_do_wait_letter(lex):
    next_state = next(lex._do_wait)
    assert next_state == lex._do_word

def _test_do_wait_digit(lex):
    next_state = next(lex._do_wait)
    assert next_state == lex._do_number

def _test_do_wait_eof(lex):
    next_state = next(lex._do_wait)
    assert next_state == lex._do_end


def test_do_word():
    d = {
        ('a', '1', 'b', ' '): _test_do_word_space,
        ('a', '1', 'b', '\t'): _test_do_word_space,
        ('a', '1', 'b', '\n'): _test_do_word_space,
        ('a', '1', 'b', EOFError): _test_do_word_eof,
    }

    for input, test in d.items():
        lex = Lexer()
        lex.input_stream = __input_stream(
            sym if sym == EOFError else Asymbol(sym, 1, i + 1)
                for i, sym in enumerate(input)
        )
        lex._emitoken = Mock()
        yield test, lex

def _test_do_word_space(lex):
    next_state = next(lex._do_word)
    assert next_state == lex._do_wait
    lex._emitoken.assert_called_once_with(TOK_WORD)

def _test_do_word_eof(lex):
    next_state = next(lex._do_word)
    assert next_state == lex._do_end
    lex._emitoken.assert_called_once_with(TOK_WORD)


def test_do_number():
    d = {
        ('1', '2', ' '): _test_do_number_space,
        ('1', '2', '\t'): _test_do_number_space,
        ('1', '2', '\n'): _test_do_number_space,
        ('1', '2', EOFError): _test_do_number_eof,
        ('1', '2', 'a'): _test_do_number_letter,
    }

    for input, test in d.items():
        lex = Lexer()
        lex.input_stream = __input_stream(
            sym if sym == EOFError else Asymbol(sym, 1, i + 1)
                for i, sym in enumerate(input)
        )
        lex._emitoken = Mock()
        yield test, lex

def _test_do_number_space(lex):
    next_state = next(lex._do_number)
    assert next_state == lex._do_wait
    lex._emitoken.assert_called_once_with(TOK_NUMBER)

def _test_do_number_eof(lex):
    next_state = next(lex._do_number)
    assert next_state == lex._do_end
    lex._emitoken.assert_called_once_with(TOK_NUMBER)

def _test_do_number_letter(lex):
    next_state = next(lex._do_number)
    assert next_state == lex._do_word
    assert "".join([asym[0] for asym in lex.buffer.asymbols]) == '12a'