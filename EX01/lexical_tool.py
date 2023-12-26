from ply import lex


tokens = (
    'INT',
    'FLOAT',
    'ID',
    'OP',
    'LPAREN',
    'RPAREN',
    'WHITESPACE',
)


t_INT = r'\d+'
t_FLOAT = r'\d+\.\d+'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_OP = r'[+\-*/]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_WHITESPACE = r'\s+'


def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()


source_code = "3.14+42*fooo"
lexer.input(source_code)


for token in lexer:
    print(token)
