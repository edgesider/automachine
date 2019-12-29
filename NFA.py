# {C, Q, F, S, E}
# C: 接受符号
# Q: 状态
# F: 转移函数
# S: 开始状态
# E: 终止状态

from __future__ import annotations
from DFA import DFA


class NFA:

    epsilon = ...

    def __init__(self, chars, q, function, start, end):
        self.chars = chars
        self.q = q
        self.function = function
        self.start = start
        self.end = list(end)

    def run(self, input):
        qs = (self.start, )
        for c in input:
            assert c in self.chars
            new_qs = self.f(qs, c)
            qs = new_qs
        if self.is_end(qs):
            return True
        else:
            return False

    def to_dfa(self):
        """convert this NFA to DFA"""
        dfa_q = [(self.start,)]
        dfa_f = {}
        dfa_s = (self.start,)
        dfa_e = []
        for qs in dfa_q:
            for c in self.chars:
                new_qs = tuple(self.f(qs, c))
                if not new_qs:
                    continue

                # add new state
                if new_qs not in dfa_q:
                    dfa_q.append(new_qs)
                # add new function
                if qs not in dfa_f:
                    dfa_f[qs] = {}
                dfa_f[qs][c] = new_qs
                # add ending state
                if self.is_end(new_qs):
                    dfa_e.append(new_qs)
        return DFA(self.chars, dfa_q, dfa_f, dfa_s, dfa_e)

    def f(self, qs, c):
        # with epsilon closure
        return self.e_loop(self.step(self.e_loop(qs), c))

    def step(self, qs, c):
        """step forward with character `c` in state `qs`,
        return the new state set"""
        new_qs = set()
        for q in qs:
            try:
                new_qs.update(self.function[q][c])
            except KeyError:
                pass
        return new_qs

    def e_loop(self, qs):
        """step with epsilon until there is no changes"""
        qs = {q for q in qs}
        while True:
            new_qs = self.step(qs, self.epsilon)
            if new_qs.issubset(qs):
                break
            qs.update(new_qs)
        return qs

    def is_end(self, qs):
        """check if `qs` is a ending state"""
        for e in self.end:
            if e in qs:
                return True
        return False

    def add_transfer(self, q, c, newq):
        """add new transfer
        :params q: previous state
        :params c: the char trigger this movement
        :params newq: next state.

        `newq` could be a single state or a list of state
        """
        assert c == ... or c in self.chars
        t = self.function.get(q)
        if t is None:
            t = self.function[q] = {c: []}
        elif t.get(c) is None:
            t[c] = []
        if isinstance(newq, list):
            t[c].extend(newq)
        else:
            t[c].append(newq)

    def unit_end_state(self):
        """make end state single"""
        if len(self.end) == 1:
            return
        new_end = max(self.q) + 1
        for e in self.end:
            self.add_transfer(e, ..., new_end)
        self.end = [new_end]
        self.q.append(new_end)

    def rename_state(self, old, new):
        """rename state `old` to `new`"""
        if old not in self.q:
            raise Exception(f'state `{old}` not exist')
        if new in self.q:
            raise Exception(f'state number `{new}` in use')
        
        # f = {
        #   0: {
        #     'a': [0, 1],
        #     'b': [0, 2]
        #   }
        # }
        f = self.function
        newf = {}
        for q, t in f.items():
            for c, qs in t.items():
                newqs = [q if q != old else new for q in qs]
                t[c] = newqs

            if q == old:
                newf[new] = f[q]
            else:
                newf[q] = f[q]
        del f
        self.function = newf
        self.q = [q if q != old else new for q in self.q]
        self.end = [q if q != old else new for q in self.end]
        if old == self.start:
            self.start = new

    def arrange_state(self, start=0):
        """arrange state number start from `start`"""
        max_q = max(self.q)
        for i, e in enumerate(self.q):
            self.rename_state(e, i + max_q + start + 1)
        for i, e in enumerate(self.q):
            self.rename_state(e, i + start)

    def kleene_closure(self):
        """apply kleene closure on self."""

        self.unit_end_state()

        # find two available state number
        maxq = max(self.q)
        qstart = maxq + 1
        qend = maxq + 2

        # new start state
        self.add_transfer(qstart, ..., [self.start, qend])

        # new end state
        # we called unit_end_state() before,
        # now we only have one end state.
        self.add_transfer(self.end[0], ..., [self.start, qend])

        self.start = qstart
        self.end = [qend]

    def append(self, nfa):
        """append another NFA `nfa` to self."""
        self.unit_end_state()
        self.arrange_state(0)
        nfa.arrange_state(len(self.q))

        for q, t in nfa.function.items():
            for c, qs in t.items():
                self.add_transfer(q, c, qs)
        self.add_transfer(self.end[0], ..., nfa.start)
        self.end = nfa.end[:]


def test_nfa():
    # NFA: starts and ends with the same char
    # (0(0|1)*0 | 1(0|1)*1)
    C = '01'
    Q = [0, 1, 2, 3]
    F = {
        0: {
            '0': [1],
            '1': [2],
        },
        1: {
            '0': [1, 3],
            '1': [1],
        },
        2: {
            '0': [2],
            '1': [2, 3],
        }
    }
    S = 0
    E = [3]

    nfa = NFA(C, Q, F, S, E)
    assert nfa.run('11') is True
    assert nfa.run('00') is True
    assert nfa.run('00101011010') is True
    assert nfa.run('10') is False
    assert nfa.run('0001011101') is False
    dfa = nfa.to_dfa()
    assert dfa.run('11') is True
    assert dfa.run('00') is True
    assert dfa.run('00101011010') is True
    assert dfa.run('10') == False
    assert dfa.run('0001011101') is False


def test_e_closure():
    # e-NFA: no meaning, just test
    C = '01'
    Q = [0, 1, 2, 3, 4]
    F = {
        0: {
            ...: [1]
        },
        1: {
            ...: [2]
        },
        2: {
            '1': [3]
        },
        3: {
            ...: [4]
        }
    }
    S = 0
    E = [1]
    nfa = NFA(C, Q, F, S, E)
    assert nfa.step({0}, ...) == {1}
    assert nfa.e_loop({0}) == {0, 1, 2}
    assert nfa.f({0}, '1') == {3, 4}


def test_kleene_closure():
    C = '01'
    Q  = [0, 1]
    F = {
        0: {
            '0': [1]
        }
    }
    S = 0
    E = [1]
    nfa = NFA(C, Q, F, S, E)
    nfa.kleene_closure()
    # __import__('pprint').pprint(nfa.function)
    # __import__('pprint').pprint(nfa.start)
    # __import__('pprint').pprint(nfa.end)

    # NFA: starts and ends with different characters
    # (0(0|1)*1 | 1(0|1)*0)
    C = '01'
    Q = [0, 1, 2, 3]
    F = {
        0: {
            '0': [1],
            '1': [2],
        },
        1: {
            '1': [1, 3],
            '0': [1],
        },
        2: {
            '1': [2],
            '0': [2, 3],
        }
    }
    S = 0
    E = [3]

    nfa = NFA(C, Q, F, S, E)
    nfa.kleene_closure()
    assert nfa.run('1001') is True
    assert nfa.run('1111') is False
    assert nfa.run('1010') is True


def test_unit_end_state():
    C = '01'
    Q = [0, 1, 2, 3]
    F = {
        0: {
            '0': [1],
            '1': [2],
        },
        1: {
            '1': [1, 3],
            '0': [1],
        },
        2: {
            '1': [2],
            '0': [2, 3],
        }
    }
    S = 0
    E = [0, 1, 2, 3]

    nfa = NFA(C, Q, F, S, E)
    nfa.unit_end_state()
    assert len(nfa.end) == 1
    assert len(nfa.q) == 5


def test_rename_state():
    C = '01'
    Q = [0, 1, 2]
    F = {
        0: {
            '0': [0],
            '1': [0],
        },
        1: {
            '1': [0, 2],
            '0': [2],
        }
    }
    S = 0
    E = [0, 2]

    nfa = NFA(C, Q, F, S, E)
    nfa.rename_state(0, 8)
    assert nfa.start == 8
    assert nfa.end == [8, 2]
    assert nfa.function == {
        8: {
            '0': [8],
            '1': [8],
        },
        1: {
            '1': [8, 2],
            '0': [2],
        }
    }
    nfa.rename_state(1, 9)
    assert nfa.function == {
        8: {
            '0': [8],
            '1': [8],
        },
        9: {
            '1': [8, 2],
            '0': [2],
        }
    }


def test_arrange_state():
    C = '01'
    Q = [2, 9, 4]
    F = {
        2: {
            '0': [2],
            '1': [9],
        },
        9: {
            '1': [4, 9],
            '0': [2],
        }
    }
    S = 2
    E = [9, 4]

    nfa = NFA(C, Q, F, S, E)
    nfa.arrange_state()
    assert sorted(nfa.q) == [0, 1, 2]
    assert nfa.start == 0
    assert sorted(nfa.end) == [1, 2]
    assert nfa.function == {
        0: {
            '0': [0],
            '1': [1],
        },
        1: {
            '1': [2, 1],
            '0': [0],
        }
    }


def test_append():
    C = '01'
    Q = [0, 1]
    F = {
        0: {
            '0': [1]
        }
    }
    S = 0
    E = [1]
    nfa1 = NFA(C, Q, F, S, E)
    
    C = '01'
    Q = [0, 1]
    F = {
        0: {
            '1': [1]
        }
    }
    S = 0
    E = [1]
    nfa2 = NFA(C, Q, F, S, E)

    nfa1.append(nfa2)
    assert nfa1.run('01') is True


if __name__ == '__main__':
    test_nfa()
    test_e_closure()
    test_kleene_closure()
    test_unit_end_state()
    test_rename_state()
    test_arrange_state()
    test_append()
