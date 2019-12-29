# {C, Q, F, S, E}
# C: 接受符号
# Q: 状态
# F: 转移函数
# S: 开始状态
# E: 终止状态

from DFA import DFA


class NFA:

    epsilon = ...

    def __init__(self, chars, q, function, start, end):
        self.chars = chars
        self.q = q
        self.function = function
        self.start = list(start)
        self.end = list(end)

    def run(self, input):
        qs = (self.start, )
        for c in input:
            assert c in self.chars
            new_qs = self.f(qs, c)
            qs = new_qs
        if self.is_end(qs):
            return True

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
        # with epsilon closeure
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
        """add new transfer"""
        # TODO
        pass

    def unit_end_state(self):
        """make end state single"""
        # TODO
        pass

    def rename_state(self, old, new):
        """rename state `old` to `new`"""
        # TODO
        pass

    def arrange_state(self, start=0):
        """arrange state number from `start`"""
        # TODO
        pass

    def do_kleene_closeure(self):
        """apply kleene closeure on self."""

        self.unit_end_state()

        # find two available state number
        maxq = max(self.q)
        qstart = maxq + 1
        qend = maxq + 2

        # new start state
        self.function[qstart] = { ...: [self.start, qend] }

        # new end state
        # we called unit_end_state() before,
        # now we only have one end state.
        self.add_transfer(self.end[0], ..., self.start)

        self.start = qstart
        self.end = [qend]

    def do_append(self, nfa: NFA):
        """append another NFA `nfa` to self."""
        self.unit_end_state()
        self.arrange_state(0)
        nfa.arrange_state(len(self.q))

        self.function.update(nfa.function)
        self.add_transfer(self.end[0], ..., nfa.start)
        self.end = nfa.end[:]


def main():
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
    print('Accepted!' if nfa.run('11001111001') else 'Not Accepted!')
    dfa = nfa.to_dfa()
    print('Accepted!' if dfa.run('11001111001') else 'Not Accepted!')


def test_e_closeure():
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


def test_kleene_closeure():
    C = '01'
    Q  = [0, 1]
    F = {
        0: {
            '0': 1
        }
    }
    S = 0
    E = [1]
    nfa = NFA(C, Q, F, S, E)
    nfa.do_kleene_closeure()
    __import__('pprint').pprint(nfa.function)
    __import__('pprint').pprint(nfa.start)
    __import__('pprint').pprint(nfa.end)

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
    nfa.do_kleene_closeure()
    print('Accepted!' if nfa.run('1001') else 'Not Accepted!')
    dfa = nfa.to_dfa()
    print('Accepted!' if dfa.run('11') else 'Not Accepted!')


def test_append():
    # TODO
    pass


if __name__ == '__main__':
    # main()
    # test_e_closeure()
    test_kleene_closeure()
