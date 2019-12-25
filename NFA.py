#!/usr/bin/env python3

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
        self.start = start
        self.end = end

    def run(self, input):
        qs = (self.start, )
        for c in input:
            assert c in self.chars
            new_qs = self.f(qs, c)
            qs = new_qs
        for e in self.end:
            if e in qs:
                return True

    def to_dfa(self):
        dfa_q = [(self.start,)]
        dfa_f = {}
        dfa_s = (self.start,)
        dfa_e = []
        for qs in dfa_q:
            for c in self.chars:
                new_qs = tuple(self.f(qs, c))
                if not new_qs:
                    continue
                if new_qs not in dfa_q:
                    dfa_q.append(new_qs)
                if qs not in dfa_f:
                    dfa_f[qs] = {}
                dfa_f[qs][c] = new_qs
                for e in self.end:
                    if e in new_qs:
                        dfa_e.append(new_qs)
        return DFA(self.chars, dfa_q, dfa_f, dfa_s, dfa_e)

    def f(self, qs, c):
        # with epsilon closeure
        return self.e_loop(self.step(self.e_loop(qs), c))

    def step(self, qs, c):
        new_qs = set()
        for q in qs:
            try:
                new_qs.update(self.function[q][c])
            except KeyError:
                pass
        return new_qs

    def e_loop(self, qs):
        # copy
        qs = {q for q in qs}
        while True:
            new_qs = self.step(qs, self.epsilon)
            if new_qs.issubset(qs):
                break
            qs.update(new_qs)
        return qs


def main():
    # starts and ends with the same char
    # (0(0|1)*0 | 1(0|1)*1)
    C = '01'
    Q = ['q0', 'q1', 'q2', 'q3']
    F = {
        'q0': {
            '0': ['q1'],
            '1': ['q2'],
            ...: ['q1', 'q3']
        },
        'q1': {
            '0': ['q1', 'q3'],
            '1': ['q1'],
        },
        'q2': {
            '0': ['q2'],
            '1': ['q2', 'q3'],
            ...: ['q1', 'q3']
        }
    }
    S = 'q0'
    E = ['q3']

    nfa = NFA(C, Q, F, S, E)
    print('Accepted!' if nfa.run('11001111001') else 'Not Accepted!')
    dfa = nfa.to_dfa()
    print('Accepted!' if dfa.run('11001111001') else 'Not Accepted!')


def test_e_closeure():
    C = '01'
    Q = ['q0', 'q1', 'q2', 'q3', 'q4']
    F = {
        'q0': {
            ...: ['q1']
        },
        'q1': {
            ...: ['q2']
        },
        'q2': {
            'q1': ['q3']
        },
        'q3': {
            ...: ['q4']
        }
    }
    S = 'q0'
    E = ['q1']
    nfa = NFA(C, Q, F, S, E)
    assert nfa.step({'q0'}, ...) == {'q1'}
    assert nfa.e_loop({'q0'}) == {'q0', 'q1', 'q2'}
    assert nfa.f({'q0'}, 'q1') == {'q3', 'q4'}


if __name__ == '__main__':
    main()
    test_e_closeure()
