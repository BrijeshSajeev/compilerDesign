gram = {}

def add(str):
    # Parses a grammar rule string and adds it to the grammar dictionary.
    # Replaces whitespace, splits on '->' to separate left and right sides, 
    # splits the right side on '|' to handle multiple productions.
    # Finally stores the rule in the grammar dict.
    str = str.replace(" ", "").replace(" ", "").replace("\n", "")
    x = str.split("->")
    y = x[1]
    x.pop()
    z = y.split("|")
    x.append(z)
    gram[x[0]]=x[1]

def removeDirectLR(gramA, A):
    # Removes direct left recursion from the grammar rule A in gramA.
    # Splits the rule into two rules, one recursive and one not.
    # temp stores the original productions for A.
    # tempCr holds productions that don't start with A after the split.
    # tempInCr holds productions that start with A after the split.
    # The new recursive rule A' is created to hold the left recursive productions.
    # e is appended to A' to allow it to derive empty string.
    # The original rule A is updated to hold the non-left recursive productions.
    # The new rule A' is added to the grammar.
    temp = gramA[A]
    tempCr = []
    tempInCr = []
    for i in temp:
        if i[0] == A:
        #tempInCr.append(i[1:])
            tempInCr.append(i[1:]+[A+"'"])
        else:
        #tempCr.append(i)
            tempCr.append(i+[A+"'"])
    tempInCr.append(["e"])
    gramA[A] = tempCr
    gramA[A+"'"] = tempInCr
    return gramA

def checkForIndirect(gramA, a, ai):
    # Checks if there is indirect left recursion between nonterminals a and ai in grammar gramA.
    # Returns True if ai derives a, False otherwise.
    # Base cases:
    # - If ai is not in gramA, it cannot derive anything, so return False.  
    # - If a == ai, ai derives itself, so return True.
    # Recursive case:
    # - Iterate through the productions of ai.  
    #   - If any production has ai as its first symbol, ai has direct left recursion so return False.
    #   - If any production's first symbol derives a, return True.
    # - If we don't find any productions matching the above cases, ai does not derive a, so return False.
    if ai not in gramA:
        return False
    if a == ai:
        return True
    for i in gramA[ai]:
        if i[0] == ai:
            return False
        if i[0] in gramA:
            return checkForIndirect(gramA, a, i[0])
    return False
def rep(gramA, A):
    # Removes indirect left recursion between nonterminal A and other nonterminals in grammar gramA.
    # Iterates through the productions for A.  
    # For each production, checks if its first symbol derives A indirectly using checkForIndirect().
    # If it does, expands that production by generating new productions with the symbols that derive the first symbol appended.
    # Adds the new expanded productions to newTemp.
    # If the first symbol does not derive A indirectly, just adds the original production to newTemp.
    # Replaces the productions for A in gramA with newTemp.
    # Returns the updated grammar.
    temp = gramA[A]
    newTemp = []
    for i in temp:
        if checkForIndirect(gramA, A, i[0]):
            t = []
            for k in gramA[i[0]]:
                t=[]
                t+=k
                t+=i[1:]
                newTemp.append(t)
        else:
            newTemp.append(i)
    gramA[A] = newTemp
    return gramA

def rem(gram):
    # Removes left recursion from the given grammar 'gram'
    # by eliminating direct left recursion and replacing indirect left recursion 
    # with equivalent right recursive rules.
    #
    # Returns the grammar without left recursion.
    c = 1
    conv = {}
    gramA = {}
    revconv = {}
    for j in gram:
        conv[j] = "A"+str(c)
        gramA["A"+str(c)] = []
        c+=1
    for i in gram:
        for j in gram[i]:
            temp = []
            for k in j:
                if k in conv:
                    temp.append(conv[k])
                else:
                    temp.append(k)
            gramA[conv[i]].append(temp)
    #print(gramA)
    for i in range(c-1,0,-1):
        ai = "A"+str(i)
        for j in range(0,i):
            aj = gramA[ai][0][0]
            if ai!=aj :
                if aj in gramA and checkForIndirect(gramA,ai,aj):
                    gramA = rep(gramA, ai)
    for i in range(1,c):
        ai = "A"+str(i)
        for j in gramA[ai]:
            if ai==j[0]:
                gramA = removeDirectLR(gramA, ai)
                break
    op = {}
    for i in gramA:
        a = str(i)
        for j in conv:
            a = a.replace(conv[j],j)
            revconv[i] = a
    for i in gramA:
        l = []
        for j in gramA[i]:
            k = []
            for m in j:
                if m in revconv:
                    k.append(m.replace(m,revconv[m]))
                else:
                    k.append(m)
            l.append(k)
        op[revconv[i]] = l
    return op

n = int(input("Enter No of Production: "))
for i in range(n):
    txt=input()
    add(txt)
result = rem(gram)
print('After eliminating left recursion : ')
for x,y in result.items():
    print(f'{x} -> ', end="")
    for index, i in enumerate(y):
        for j in i:
            print(j, end="")
            if (index != len(y) - 1):
                print(" | ", end="")
    print()