grammar = {}

def add_production(rule):
    rule = rule.replace(" ", "").replace("\n", "")
    parts = rule.split("->")
    body = parts[1]
    parts.pop()
    alternatives = body.split("|")
    parts.append(alternatives)
    grammar[parts[0]] = parts[1]

def removeDirectLR(grammar, non_terminal):
    productions = grammar[non_terminal]
    new_direct = []
    new_indirect = []
    
    for production in productions:
        if production[0] == non_terminal:
            new_indirect.append(production[1:] + [non_terminal + "'"])
        else:
            new_direct.append(production + [non_terminal + "'"])

    new_indirect.append(["e"])
    grammar[non_terminal] = new_direct
    grammar[non_terminal + "'"] = new_indirect
    
    return grammar

def checkForIndirect(grammar, non_terminal, candidate):
    if candidate not in grammar:
        return False
    if non_terminal == candidate:
        return True
    for production in grammar[candidate]:
        if production[0] == candidate:
            return False
        if production[0] in grammar:
            return checkForIndirect(grammar, non_terminal, production[0])
    return False

def replaceIndirectRec(grammar, non_terminal):
    productions = grammar[non_terminal]
    new_productions = []

    for production in productions:
        if checkForIndirect(grammar, non_terminal, production[0]):
            for indirect_production in grammar[production[0]]:
                new_production = []
                new_production += indirect_production
                new_production += production[1:]
                new_productions.append(new_production)
        else:
            new_productions.append(production)

    grammar[non_terminal] = new_productions
    return grammar

def convert_grammar(grammar):
    count = 1
    non_terminal_mapping = {}
    new_grammar = {}
    reverse_mapping = {}

    for symbol in grammar:
        non_terminal_mapping[symbol] = "A" + str(count)
        new_grammar["A" + str(count)] = []
        count += 1

    for symbol in grammar:
        for production in grammar[symbol]:
            new_production = []
            for part in production:
                if part in non_terminal_mapping:
                    new_production.append(non_terminal_mapping[part])
                else:
                    new_production.append(part)
            new_grammar[non_terminal_mapping[symbol]].append(new_production)

    for i in range(count - 1, 0, -1):
        non_terminal_i = "A" + str(i)
        for j in range(0, i):
            non_terminal_j = new_grammar[non_terminal_i][0][0]
            if non_terminal_i != non_terminal_j:
                if non_terminal_j in new_grammar and checkForIndirect(new_grammar, non_terminal_i, non_terminal_j):
                    new_grammar = replaceIndirectRec(new_grammar, non_terminal_i)

    for i in range(1, count):
        non_terminal_i = "A" + str(i)
        for production in new_grammar[non_terminal_i]:
            if non_terminal_i == production[0]:
                new_grammar = removeDirectLR(new_grammar, non_terminal_i)
                break

    result_grammar = {}
    for symbol in new_grammar:
        s = str(symbol)
        for non_terminal in non_terminal_mapping:
            s = s.replace(non_terminal_mapping[non_terminal], non_terminal)
            reverse_mapping[symbol] = s

    for symbol in new_grammar:
        productions = []
        for production in new_grammar[symbol]:
            new_production = []
            for part in production:
                if part in reverse_mapping:
                    new_production.append(part.replace(part, reverse_mapping[part]))
                else:
                    new_production.append(part)
            productions.append(new_production)
        result_grammar[reverse_mapping[symbol]] = productions

    return result_grammar

number_of_productions = int(input("Enter the number of productions: "))
print("Enter the production >> ")
for i in range(number_of_productions):
    production_rule = input()
    add_production(production_rule)

result_grammar = convert_grammar(grammar)
print('After eliminating left recursion:')
for symbol, productions in result_grammar.items():
    print(f'{symbol} -> ', end="")
    for index, production in enumerate(productions):
        for part in production:
            print(part, end="")
        if index != len(productions) - 1:
            print(" | ", end="")
    print()