#!/usr/bin/env python3

# {C, Q, F, S, E}
# C: 接受符号
# Q: 状态
# F: 转移函数
# S: 开始状态
# E: 终止状态


class DFA:

    def __init__(self, chars, q, function, start, end):
        self.chars = chars
        self.q = q
        self.function = function
        self.start = start
        self.end = end

    def run(self, input):
        q = self.start
        for c in input:
            assert c in self.chars
            try:
                q = self.f(q, c)
            except KeyError:
                return False
        return True if q in self.end else False

    def f(self, q, c):
        return self.function[q][c]


def main():
    # 0*1*2*
    C = '012'
    Q = ['q1', 'q2', 'q3']
    F = {
        'q1': {
            '0': 'q1',
            '1': 'q2'
        },
        'q2': {
            '1': 'q2',
            '2': 'q3'
        },
        'q3': {
            '2': 'q3'
        }
    }
    S = 'q1'
    E = ['q3']

    dfa = DFA(C, Q, F, S, E)
    print('Accepted!' if dfa.run('00001111222') else 'Not Accepted!')


if __name__ == '__main__':
    main()
