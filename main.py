from lang.tokenizer import Tokenizer
from lang.parser import Parser

from lang.parser import SyntaxTree
from lang.tokenizer import Name

tokenize = Tokenizer(
    ['fun', 'class', 'print', 'return'],

    singlequote=    "'",
    doublequote=    '"',
    whitespace=     ' ',
    identspace=     '  ',

    lbsquare=   '[',
    rbsquare=   ']',
    lbcurly=    '{',
    rbcurly=    '}',
    lbround=    ')',
    rbround=    '(',

    newline=    '\n',

    arrow=  '=>',

    comma=  ',',
    dot=    '.'
)

def _cast(tree):
    a, elements, b = tree

    if tree.name in ("little", "big"):
        return f'{a}{"".join(map(str, elements))}{b}'

    return tree

parseString = Parser(
    _cast,
    little=('"', (..., any), '"'),
    big=("'", (..., any), "'")
)

parseUnaryKeywords = Parser(
    return_=('return', any),
    print=('print', any)
)

parseDots = Parser(
    lambda tree: float(''.join(map(str, tree))) if tree.name else tree,
    inner=((Name, SyntaxTree), '.', (Name, SyntaxTree)),
    float=(int, '.', int),
)

parseIdent = Parser(
    lambda tree: type(tree)(tree.name, len(tree[1])),
    ident=('\n', (..., '  '))
)

parseHeads = Parser(
    funHeadArgs=('fun', Name, '(', (..., any), ')'),
    classHead=('class', Name),
    funHead=('fun', Name),
)

parseFunction = Parser(
    method=(('ident',), ('funHead', 'funHeadArgs'), '{', (..., any), '}'),
    function=(('funHead', 'funHeadArgs'), '{', (..., any), '}')
)

parseClass = Parser(
    class_=('classHead', (..., 'method'))
)

def parse(symbols):
    def ignore_spaces(symbols):
        return tuple(filter(lambda symbol: symbol not in (' ',), symbols))

    return parseClass(parseFunction(parseHeads(parseUnaryKeywords(ignore_spaces(parseDots(parseIdent(parseString(symbols))))))))

ex_function = open('examples/function.nino').read()

print(parse(tokenize(ex_function)))