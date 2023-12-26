import re

# Define token patterns using regular expressions
patterns = [
    ('FLOAT', r'\d+\.\d+'),
    ('INT', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OPERATOR', r'[+\-*/=]'),
    ('LPARENTHISIS', r'\('),
    ('RPARENTHISIS', r'\)'),
    ('WHITESPACE', r'\s+'),
]

def lexer(source_code):
    tokens = []
    for code in source_code:
        for token_type, pattern in patterns:
            match = re.match(pattern, code)
            if match:
                value = match.group()
                tokens.append((token_type, value))
                # source_code = source_code[len(value):]
                break
        else:
            raise Exception(f"Invalid character in source code: {code}")
    
    return tokens

# Example usage
# code = "3.14 + 42 * (foo - 7)"
code ="x = 3 + 42 * ( foo - 7 )"
source_code = code.split(" ")
tokens = lexer(source_code)

for token in tokens:
    print(token)