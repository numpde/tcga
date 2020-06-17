# RA, 2020-06-17

import pandas


# https://en.wikipedia.org/wiki/Complementarity_(molecular_biology)

class __:
    dna0 = "ACGTWSMKRYBDHVN"
    dna1 = "TGCAWSKMYRVHDBN"
    rna0 = "ACGUWSMKRYBDHVN"
    rna1 = "UGCAWSKMYRVHDBN"

    class MakeComplement:
        def __init__(self, p: str, q: str):
            self._reversed = False
            self.m = dict(zip(p, q))

        def __call__(self, s: str):
            if self._reversed:
                return ''.join(self.m[c] for c in reversed(s))
            else:
                return ''.join(self.m[c] for c in s)

        @property
        def reversed(self):
            self._reversed = not self._reversed
            return self


dna_to_dna = __.MakeComplement(__.dna0, __.dna1)
dna_to_rna = __.MakeComplement(__.dna0, __.rna1)
rna_to_rna = __.MakeComplement(__.rna0, __.rna1)
rna_to_dna = __.MakeComplement(__.rna0, __.dna1)


def backward(s: str) -> str:
    return s[::-1]


nucleotides = pandas.DataFrame(
    columns=[
        "Symbol", "Description", "A", "C", "G", "T", "U",
    ],
    data=[
        ['A', 'adenine', 1, 0, 0, 0, 0],
        ['C', 'cytosine', 0, 1, 0, 0, 0],
        ['G', 'guanine', 0, 0, 1, 0, 0],
        ['T', 'thymine', 0, 0, 0, 1, 0],
        ['U', 'uracil', 0, 0, 0, 0, 1],
        ['W', 'weak', 1, 0, 0, 1, 1],
        ['S', 'strong', 0, 1, 1, 0, 0],
        ['M', 'amino', 1, 1, 0, 0, 0],
        ['K', 'keto', 0, 0, 1, 1, 1],
        ['R', 'purine', 1, 0, 1, 0, 0],
        ['Y', 'pyrimidine', 0, 1, 0, 1, 1],
        ['B', 'not A', 0, 1, 1, 1, 1],
        ['D', 'not C', 1, 0, 1, 1, 1],
        ['H', 'not G', 1, 1, 0, 1, 1],
        ['V', 'not T/U', 1, 1, 1, 0, 0],
        ['N', 'any base', 1, 1, 1, 1, 1],
    ]
)

if __name__ == '__main__':
    print("Nucleotides:", nucleotides, sep='\n')
