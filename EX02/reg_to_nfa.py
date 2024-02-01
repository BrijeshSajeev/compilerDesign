# def reg_to_nfa(reg_exp):
#     nfa = []
    
#     # Add opening parentheses 
#     reg_exp = reg_exp.replace('(', '( ')
    
#     # Add closing parentheses
#     reg_exp = reg_exp.replace(')', ' )')
    
#     # Split the regular expression into tokens
#     reg_exp = reg_exp.split()
    
#     # Create NFA states for each token
#     for i, token in enumerate(reg_exp):
#         if token == '(':
#             nfa.append(['(', i])
#         elif token == ')':
#             nfa.append([')', i])
#         elif token == '|':
#             nfa.append(['|', i])
#         elif token == '*':
#             nfa.append(['*', i])
#         elif token == '+':
#             nfa.append(['+', i])
#         elif token == '?':
#             nfa.append(['?', i])
#         else:
#             nfa.append([token, i])
#     return nfa




# def print_nfa_transitions(nfa_states):

#     print("NFA transitions:")

#     for i in range(len(nfa_states)-1):
#         cur_state = nfa_states[i]
#         next_state = nfa_states[i+1]
        
#         if cur_state[0] == '*' or next_state[0] == '(':
#             print(f"{cur_state[1]} -> {next_state[1]} on epsilon")
            
#         elif next_state[0] == ')':
#             print(f"{cur_state[1]} -> {nfa_states[-1][1]} on epsilon")
            
#         elif cur_state[0] == '|':
#             print(f"{nfa_states[i-1][1]} -> {next_state[1]} on {next_state[0]}")
            
#         else:
#             print(f"{cur_state[1]} -> {next_state[1]} on {next_state[0]}")

# # reg_exp = "a*(b|c)"
# # nfa = reg_to_nfa(reg_exp)
# # print(nfa)

# if __name__ == '__main__':

#     reg_exp = "a * ( b | c ) "
#     nfa = reg_to_nfa(reg_exp)
#     print(nfa)
#     print_nfa_transitions(nfa)

# def regex_to_nfa(regex):
#     nfa = {'states': [], 'transitions': [], 'start': 0, 'accepting': []}
    
#     state = 0
#     for char in regex:
#         if char.isalpha():
#             nfa['states'].append(state)
#             nfa['transitions'].append((state, char, state+1))
#             state += 1
        
#         elif char == '*':
#             nfa['states'].append(state)
#             nfa['transitions'].append((state-1, 'ε', state))
#             nfa['transitions'].append((state, 'ε', state-1))
#             state += 1
        
#         elif char == '|':
#             nfa['states'].append(state) 
#             nfa['transitions'].append((state-1, 'ε', state))
#             nfa['transitions'].append((state, 'ε', state+1))
#             state += 1
            
#     nfa['accepting'].append(state-1)
#     if char.isalpha():
#   # Add transition on char
#         nfa['transitions'].append((state, char, state+1)) 
#     return nfa
    
def regex_to_nfa(regex):

  nfa = {'states': [], 
         'transitions': [],
         'start': 0,
         'accepting': []}
  
  state = 0
  for char in regex:
  
    if char.isalpha():
      nfa['states'].append(state)
      nfa['transitions'].append((state, char, state+1))
      state += 1
  
    elif char == '*':
      nfa['states'].append(state)
      nfa['transitions'].append((state-1, 'ε', state))
      nfa['transitions'].append((state, 'ε', state-1))
      
      # Fix: Add epsilon transition to continue chain
      if state < len(nfa['states']):
        nfa['transitions'].append((state, 'ε', state+1))
        
      state += 1
  
    elif char == '|':
      # ...logic for alternation  
      
        nfa['accepting'].append(state-1)
    
  return nfa


regex = "a*(b|c)"
nfa = regex_to_nfa(regex)
print(nfa)
