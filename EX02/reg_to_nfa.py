class State:
    def __init__(self, label=None):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.label = label

class NFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

def regex_to_nfa(regex):
    stack = []
    postfix = infix_to_postfix(regex)

    for symbol in postfix:
        if symbol.isalpha():
            state = State(label=symbol)
            stack.append(state)
        elif symbol == '|':
            state2 = stack.pop()
            state1 = stack.pop()
            new_start = State()
            new_start.epsilon_transitions.update([state1, state2])
            stack.append(new_start)
        elif symbol == '*':
            state1 = stack.pop()
            new_start = State()
            new_accept = State()
            new_start.epsilon_transitions.update([state1, new_accept])
            state1.epsilon_transitions.update([new_start, new_accept])
            stack.append(new_start)
        else:
            raise ValueError(f"Invalid symbol in regular expression: {symbol}")

    if len(stack) == 1:
        raise ValueError("Invalid regular expression")

    return NFA(stack[0], {state for state in stack[0].epsilon_transitions if not state.epsilon_transitions})

def infix_to_postfix(infix):
    precedence = {'*': 2, '|': 1, '(': 0}
    output = []
    operator_stack = []

    for symbol in infix:
        if symbol.isalpha():
            output.append(symbol)
        elif symbol == '(':
            operator_stack.append(symbol)
        elif symbol == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Discard the '('
        else:
            while operator_stack and precedence[operator_stack[-1]] >= precedence[symbol]:
                output.append(operator_stack.pop())
            operator_stack.append(symbol)

    while operator_stack:
        output.append(operator_stack.pop())

    return output

# Example usage
regex = "(a|b)*a*b"

nfa = regex_to_nfa(regex)
print(infix_to_postfix(regex))
