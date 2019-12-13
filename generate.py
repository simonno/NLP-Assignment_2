import random
from argparse import ArgumentParser
from collections import defaultdict


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r


def main(grammar_file_name, sentences_num=1):
    pcfg = PCFG.from_file(grammar_file_name)
    for i in range(sentences_num):
        print(pcfg.random_sent())


if __name__ == '__main__':
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument("-n", type=int, default=1, help="Number of sentences to generate.")
    parser.add_argument("-grammar_path", type=str, help="Path of grammar file.")
    parser.add_argument("-t", action='store_true', default=False, help="True for derivation tree is, False other.")
    args = parser.parse_args()
    main(args.grammar_path, args.n)
