Computational biology & bioinformatics utils
============================================


## About

This python3 package provides basic tools to work with genomic data.
It is under development (2020-06-18). 
Meanwhile, see examples below.
Note: some examples may require packages 
that are not automatically installed
with this package
(e.g. [ʕ◕ᴥ◕ʔ](https://pandas.pydata.org/)). 


## Installation

Install or upgrade to newer version with:

```shell
pip3 install --upgrade tcga
```


## Usage


### [Example](tcga/examples/00001_codons.py)

```python
from tcga.codons.tables import standard as rna_codons
print("RNA codons:", rna_codons, sep='\n')
```

```
RNA codons:
{'UUU': 'F', 'UUC': 'F', 'UUA': 'L', ...}
```


### [Example](tcga/examples/00002_compose.py)

```python
from tcga.utils import First
from tcga.codons.tables import standard as rna_codons
from tcga.strings.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, backward

X = backward("CACGAACTTGTCGAGACCATTGCC")

f = First(dna_to_dna.backward).then(dna_to_rna).then(triplets).each(rna_codons).join(str)
print(X, "=>", f(X))
```

```
CCGTTACCAGAGCTGTTCAAGCAC => HELVETIA
```


### [Example](tcga/examples/00003_circular.py)

```python
from tcga.strings import Circular
# This creates a circular/periodic view onto the string
c = Circular("ABCDEFG")
print(F"c = {c}", c[0:20], c[-3:20:2], type(c[0:20]), sep=', ')

from tcga.strings import laola
# This this looks at a str/list/tuple in a circular/periodic way
v = laola[-3:20:2]
print(v("ABCDEFG"))
```

```
c = Circular('ABCDEFG'), ABCDEFGABCDEFGABCDEF, EGBDFACEGBDF, <class 'str'>
EGBDFACEGBDF
```


### [Example](tcga/examples/00004_aa_properties1.py)

```python
import json
from tcga.refs import annotations
from tcga.data.sa_aa_ref_chart import properties as aa_properties

print(aa_properties)
print(json.dumps(annotations[aa_properties], indent=2))
```

```
             Name Abbr3 Abbr1  ...  At pH 2 At pH 7    Comment
0         Alanine   Ala     A  ...       47      41        NaN
1        Arginine   Arg     R  ...      -26     -14        NaN
2      Asparagine   Asn     N  ...      -41     -28        NaN
...
18       Tyrosine   Tyr     Y  ...       49      63        NaN
19         Valine   Val     V  ...       79      76        NaN

{
  "date": "2020-06-18",
  "source": [
    "https://www.sigmaaldrich.com/life-science/metabolomics/learning-center/amino-acid-reference-chart.html",
    "http://archive.ph/qL8ek"
  ],
  "comments": [
    "Columns 'At pH 2' and 'At pH 7' contain a measure of hydrophobicity. [...]"
  ]
}
```


### [Example](tcga/examples/00005_aaindex.py)

```python
import json
from tcga.data import aaindex

pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("AAindex objects (excerpts):")
print("indices =   ", pretty(aaindex.indices.head(3)))
print("matrices =  ", pretty(aaindex.matrices.head(3)))
print("potentials =", pretty(aaindex.potentials.head(3)))

print("-" * 42)

key = 'ALTS910101'
print(F"Record for '{key}' =", pretty(aaindex.data[key]))
print("where the matrix M is:")
print(aaindex.data[key]['M'])
```

```
AAindex objects (excerpts):
indices =    {
  "ANDN920101": "alpha-CH chemical shifts (Andersen et al., 1992)",
  "ARGP820102": "Signal sequence helical potential (Argos et al., 1982)",
  "BEGF750101": "Conformational parameter of inner helix (Beghin-Dirkx, 1975)"
}
matrices =   {
  "ALTS910101": "The PAM-120 matrix (Altschul, 1991)",
  "BENS940102": "Log-odds scoring matrix collected in 22-29 PAM (Benner et al., 1994)",
  "BENS940104": "Genetic code matrix (Benner et al., 1994)"
}
potentials = {
  "TANS760101": "Statistical contact potential derived from 25 x-ray protein structures",
  "ROBB790102": "Interaction energies derived from side chain contacts in the interiors of known protein structures",
  "THOP960101": "Mixed quasichemical and optimization-based protein contact potential"
}
------------------------------------------
Record for 'ALTS910101' = {
  "*": NaN,
  "A": "Altschul, S.F.",
  "C": NaN,
  "D": "The PAM-120 matrix (Altschul, 1991)",
  "H": "ALTS910101",
  "I": NaN,
  "J": "J. Mol. Biol. 219, 555-565 (1991)",
  "M": "...",
  "R": "PMID:2051488",
  "T": "Amino acid substitution matrices from an information theoretic perspective"
}
where the matrix M is:
     A    R    N    D    C    Q    E  ...    F    P    S    T     W    Y    V
A  3.0 -3.0  0.0  0.0 -3.0 -1.0  0.0  ... -4.0  1.0  1.0  1.0  -7.0 -4.0  0.0
R -3.0  6.0 -1.0 -3.0 -4.0  1.0 -3.0  ... -4.0 -1.0 -1.0 -2.0   1.0 -6.0 -3.0
N  0.0 -1.0  4.0  2.0 -5.0  0.0  1.0  ... -4.0 -2.0  1.0  0.0  -5.0 -2.0 -3.0
D  0.0 -3.0  2.0  5.0 -7.0  1.0  3.0  ... -7.0 -2.0  0.0 -1.0  -8.0 -5.0 -3.0
...
```



## License

MIT/Expat.


## Suggestions

Suggestions and help are most welcome. 
