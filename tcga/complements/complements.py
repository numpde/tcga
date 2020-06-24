# RA, 2020-06-17

import pandas
import tcga.refs


class _:
    dna0 = "ACGTWSMKRYBDHVN"
    dna1 = "TGCAWSKMYRVHDBN"
    rna0 = "ACGUWSMKRYBDHVN"
    rna1 = "UGCAWSKMYRVHDBN"

    meta = {
        'data': "2020-06-17",
        'source': "https://en.wikipedia.org/wiki/Complementarity_(molecular_biology)",
    }

    class Complementer:
        def __init__(self, p: str, q: str):
            self._reversed = False
            self._p = p
            self._q = q
            self.m = dict(zip(p, q))

        def __call__(self, s: str):
            return ''.join(self.m[c] for c in (s[::-1] if self._reversed else s))

        @property
        def reverse(self):
            other = _.Complementer(self._p, self._q)
            other._reversed = not self._reversed
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


dna_to_dna = _.Complementer(_.dna0, _.dna1)
dna_to_rna = _.Complementer(_.dna0, _.rna1)
rna_to_rna = _.Complementer(_.rna0, _.rna1)
rna_to_dna = _.Complementer(_.rna0, _.dna1)

tcga.refs.annotations[dna_to_dna] = _.meta
tcga.refs.annotations[dna_to_rna] = _.meta
tcga.refs.annotations[rna_to_rna] = _.meta
tcga.refs.annotations[rna_to_dna] = _.meta

if __name__ == '__main__':
    print("Nucleotides:", dna_to_dna.legend, sep='\n')
