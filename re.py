from NFA import NFA

accept_chars = '0123456789'

# c_and = ''
c_or = '|'
c_kleene = '*'

def re2nfa(re):
    """
    params: re: string of regular experssion
    returns: a NFA instance
    """
    # First, separate the string by c_or.
    in_brackets = False
    reached = ''
    parted = []
    for c in re:
        if c == '(':
            in_brackets = True
        elif in_brackets:
            if c == ')':
                in_brackets = False
        elif c == c_or:
            parted.append(reached)
            reached = ''
            continue
        reached += c
    if reached:
        parted.append(reached)
    else:
        raise Exception('error re string')

    print(parted)

    # Second, process every part
    parted_nfa = []
    for part in parted:
        cur_nfa = NFA()
        for c in part:
            if c == '(':
                pass
            elif c == c_kleene:
                cur_nfa = nfa_kleene(cur_nfa)
            else:
                cur_nfa = nfa_and(cur_nfa, c)


def nfa_single_char(c):
    assert c in accept_chars
    q = [1, 2]
    s = 1
    e = 2
    f = {
        1: {
            c: 2
        }
    }
    return NFA(accept_chars, q, f, s, e)


def nfa_kleene(nfa):
    maxq = max(nfa.q)
    qstart = maxq + 1
    qend = maxq + 2

    nfa.function[qstart] = { ...: [nfa.start] }
    if nfa.function.get(nfa.end) is None:
        nfa.function[nfa.end] = {}
    nfa.function[nfa.end][...] = [qend]
    nfa.start = qstart
    nfa.end = [qend]


def nfa_and(nfa):
    pass


def nfa_or(nfa_list):
    pass


if __name__ == '__main__':
    re2nfa('1234|1(2(3|33)4')
