# RA, 2020-06-17

import pandas


# https://en.wikipedia.org/wiki/Complementarity_(molecular_biology)

class __:
    dna0 = "ACGTWSMKRYBDHVN"
    dna1 = "TGCAWSKMYRVHDBN"
    rna0 = "ACGUWSMKRYBDHVN"
    rna1 = "UGCAWSKMYRVHDBN"

    class Complementer:
        def __init__(self, p: str, q: str):
            self._backward = False
            self._p = p
            self._q = q
            self.m = dict(zip(p, q))

        def __call__(self, s: str):
            if self._backward:
                return ''.join(self.m[c] for c in s[::-1])
            else:
                return ''.join(self.m[c] for c in s)

        @property
        def backward(self):
            other = __.Complementer(self._p, self._q)
            other._backward = not self._backward
            return other

        @property
        def legend(self):
            df = pandas.DataFrame(
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

            return df


dna_to_dna = __.Complementer(__.dna0, __.dna1)
dna_to_rna = __.Complementer(__.dna0, __.rna1)
rna_to_rna = __.Complementer(__.rna0, __.rna1)
rna_to_dna = __.Complementer(__.rna0, __.dna1)

if __name__ == '__main__':
    print("Nucleotides:", dna_to_dna.legend, sep='\n')
