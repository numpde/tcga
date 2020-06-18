Computational biology & bioinformatics utils
============================================


## About

This python package provides basic tools to work with genomic data.
It is under development (2020-06-18). 
Meanwhile, see examples below.


## Installation

Install or upgrade to newer version with:

```shell
pip install --upgrade tcga
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


## License

MIT/Expat.


## Suggestions

Suggestions and help are most welcome. 
