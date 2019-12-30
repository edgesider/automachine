from typing import Union

from NFA import NFA

accept_chars = '0123456789'

# c_and = ''
c_or = '|'
c_kleene = '*'


def re2nfa(re_str):
    """
    params: re: string of regular experssion
    returns: a NFA instance
    """
    assert re_str
    # First, separate the string by c_or.
    in_brackets = False
    reached = ''
    parted = []
    for c in re_str:
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

    # Second, process every part
    result_nfa: Union[NFA, None] = None
    for part in parted:
        part_nfa: Union[NFA, None] = None
        focusing_nfa: Union[NFA, None] = None
        i = 0
        while i < len(part):
            c = part[i]
            i += 1

            if c == '(':
                j = 0
                depth = 1
                remain = part[i:]
                for j, c in enumerate(remain):
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                        if depth == 0:
                            break
                assert remain[j] == ')'
                bracket_str = remain[0:j]
                i += j + 1
                if bracket_str:
                    if focusing_nfa is not None:
                        if part_nfa is None:
                            part_nfa = focusing_nfa
                        else:
                            part_nfa.concatenate(focusing_nfa)
                    focusing_nfa = re2nfa(bracket_str)
            elif c == ')':
                raise Exception
            elif c == c_kleene:
                assert focusing_nfa is not None
                focusing_nfa.kleene_closure()
                if part_nfa is None:
                    part_nfa = focusing_nfa
                else:
                    part_nfa.concatenate(focusing_nfa)
                focusing_nfa = None
            else:
                if focusing_nfa is not None:
                    if part_nfa is None:
                        part_nfa = focusing_nfa
                    else:
                        part_nfa.concatenate(focusing_nfa)
                focusing_nfa = nfa_single_char(c)

        if focusing_nfa is not None:
            part_nfa.concatenate(focusing_nfa)

        if part_nfa is None:
            part_nfa = focusing_nfa
        if result_nfa is None:
            result_nfa = part_nfa
        else:
            result_nfa.alternate(part_nfa)

    return result_nfa


def nfa_single_char(c):
    assert c in accept_chars
    q = [0, 1]
    s = 0
    e = [1]
    f = {
        0: {
            c: [1]
        }
    }
    return NFA(accept_chars, q, f, s, e)


if __name__ == '__main__':
    nfa = re2nfa('5(6*7)*8|1234')
    print(nfa.run('56667667768'))
