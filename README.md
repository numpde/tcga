Computational biology & bioinformatics utils
============================================

Under development (2020-06-18).
Meanwhile, some examples:


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

