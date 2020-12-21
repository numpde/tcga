Computational biology & bioinformatics utils
============================================

## About

This python3 package provides basic tools to work with genomic data. It is under creeping development. Meanwhile, see
examples below. Note: some examples may require packages that are not automatically installed with this package
(e.g. [ʕ◕ᴥ◕ʔ](https://pandas.pydata.org/)).

## Installation

Install or upgrade to newer version with:

```shell
pip3 install --upgrade tcga
```

## Usage

### [Example](examples/00000_utils.py)

Miscellaneous utilities.

```python
import io
from pathlib import Path

from tcga.utils import mkdir
# A wrapper for Path.mkdir:
# path = mkdir(Path("/path/to/folder"))

from tcga.utils import unlist1
# Returns the object from a list
# iff the list is a singleton
assert 43 == unlist1([43])
# An iterable will be consumed:
assert 36 == unlist1((x ** 2) for x in [6])
# These fail with a ValueError:
# unlist1([])
# unlist1([1, 2])

from tcga.utils import relpath
# Returns the path relative to the script

from tcga.utils import first
# Returns the first element of an iterable
assert 'A' == first("ABCD")

from tcga.utils import at_most_n
# Lazy cut-off for iterables
print(list(at_most_n("ABCD", n=2)))
# ['A', 'B']

from tcga.utils import whatsmyname
def rose():
    print(whatsmyname())
    # Prints the name of
    # the function: rose

from tcga.utils import assert_exists
# If `file` is a filename or path then
#   assert_exists(file)
# either raises FileNotFoundError
# or returns back `file`

from tcga.utils import md5
# Computes the md5 hash of a text stream chunkwise.
# Attempts to rewind the stream back using .tell()
print(md5(io.StringIO("I know that I shall meet my fate")))
# 06a118b2f090ed1b39a1d07efdaa5d78

from tcga.utils import from_iterable
# Wraps chain.from_iterable, i.e.
print(set(from_iterable([[1, 2, 5], [4, 5]])))
print(from_iterable([[1, 2, 5], [4, 5]], type=set))
# {1, 2, 4, 5}

from tcga.utils import minidict
# A minimalistic read-only dictionary
minidict({1: 'A', 2: 'B'})

from tcga.utils import seek_then_rewind
# Context manager for rewinding file descriptors
with open(__file__, mode='r') as fd:
    with seek_then_rewind(fd, seek=2):
        print(fd.readline().strip())
        # port io
    print(fd.readline().strip())
    # import io
```

### [Example](examples/00001_codons.py)

DNA/RNA codons. 

```python
from tcga.codons import standard_rna

print("RNA codons (standard):")
print(standard_rna)
# {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', ...}

from tcga.codons import tables

print("Other codon tables:")
print(tables.name)
# 1: Standard, 2: Vertebrate Mitochondrial, 3: Yeast Mitochondrial ...

print("For example:")
print(tables.loc[1])
# name                                                   Standard
# short_name                                                 SGC0
# dna_codons    {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L...
# rna_codons    {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L...

# Those are the same
assert tables.rna_codons[1] == standard_rna

import json
from tcga.refs import annotations

print(json.dumps(annotations[tables], indent=2))
# {
#   "comments": [
#     "Compiled from the NCBI list of genetic codes.",
#     "https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi"
#   ],
#   "datetime": "2020-06-26 16:07:16.284170+00:00",
#   "source": {
#     "source": "ftp://ftp.ncbi.nih.gov/entrez/misc/data/gc.prt",
#     "datetime": "2020-06-26 14:38:28.600903+00:00"
#   }
# }
```

### [Example](examples/00002_compose.py)

Function composition.

```python
from tcga.utils import First
from tcga.codons import standard_rna as rna_codons
from tcga.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, reverse

X = reverse("CACGAACTTGTCGAGACCATTGCC")

f = First(dna_to_dna.reverse).then(dna_to_rna).then(triplets).each(rna_codons).join(str)
print(X, "=>", f(X))
```

```
CCGTTACCAGAGCTGTTCAAGCAC => HELVETIA
```

### [Example](examples/00003_circular.py)

Circular strings.

```python
from tcga.utils import Circular

# This creates a circular view onto the string
c = Circular("ABCDEFG")
print(F"c = {c}", c[0:20], c[-3:20:2], type(c[0:20]), sep=", ")

from tcga.utils import laola

# This this looks at a str/list/tuple in a circular way
v = laola[-3:20:2]
print(v("ABCDEFG"))
```

```
c = Circular('ABCDEFG'), ABCDEFGABCDEFGABCDEF, EGBDFACEGBDF, <class 'str'>
EGBDFACEGBDF
```

### [Example](examples/00004_aa_properties1.py)

Tracking of information sources.

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

### [Example](examples/00005_aaindex.py)

AAindex amino acid property repository.

```python
import json
from tcga.data import aaindex
from tcga.refs import annotations

pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("AAindex objects (excerpts):")
print("indices", pretty(aaindex.indices.head(3)), sep=" = ")
print("matrices", pretty(aaindex.matrices.head(3)), sep=" = ")
print("potentials", pretty(aaindex.potentials.head(3)), sep=" = ")

print("-" * 42)

key = 'ALTS910101'
print(F"Record for '{key}'", pretty(aaindex.data[key]), sep=" = ")
print("where the matrix M is:")
print(aaindex.data[key]['M'])

print("-" * 42)

print("Source:")
print(annotations[aaindex.data]['source'])
```

```
AAindex objects (excerpts):
indices = {
  "ANDN920101": "alpha-CH chemical shifts (Andersen et al., 1992)",
  "ARGP820102": "Signal sequence helical potential (Argos et al., 1982)",
  "BEGF750101": "Conformational parameter of inner helix (Beghin-Dirkx, 1975)"
}
matrices = {
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
------------------------------------------
Source:
Created on 2020-06-19 14:59:55.332753+00:00 using
...
list_of_matrices: 
Downloaded on 2020-06-18 15:00:16.545749+00:00 from
https://www.genome.jp/aaindex/AAindex/list_of_matrices
...
```

### [Example](examples/00006_download.py)

Downloading files directly to a compressed file
and attaching metainformation.

```python
from tcga.utils import download

from pathlib import Path
from tempfile import gettempdir

download = download.to(abs_path=(Path(gettempdir()) / "tcga_download_cache"))
print("Will download to:", download.local_folder)
# Will download to: /tmp/tcga_download_cache

data = download("https://www.ebi.ac.uk/ena/browser/api/fasta/J02459.1").again(False).now

print(data.meta)  # same as tcga.refs.annotations[data]
# {'source': 'https://www.ebi.ac.uk/ena/browser/api/fasta/J02459.1', 'datetime': '2020-06-25 07:18:52.065826+00:00'}

print(data.text[0:42], "...", data.text[330:350], "...")
# >ENA|J02459|J02459.1 Escherichia phage Lam ... CAGGGAATGCCCGTTCTGCG ...

print(data.local_file)
# /tmp/tcga_download_cache/Z9tBKiJCqrfWuYy5BlgrA3zZAWav2CUd4xrPsya93Os=.zip

try:
    from Bio import SeqIO
except ImportError:
    print("Need `biopython`")
else:
    with data.open(mode='r') as fd:
        print(SeqIO.read(fd, format='fasta'))
# ID: ENA|J02459|J02459.1
# Name: ENA|J02459|J02459.1
# Description: ENA|J02459|J02459.1 Escherichia phage Lambda, complete genome.
# Number of features: 0
# Seq('GGGCGGCGACCTCGCGGGTTTTCGCTATTTATGAAAATTTTCCGGTTTAAGGCG...ACG', SingleLetterAlphabet())
```

### [Example](examples/00007_blosum62.py)

BLOSUM matrices.

```python
import json

pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("[BLOSUM62 -- AAindex]")
from tcga.data.aaindex import data

# https://www.genome.jp/dbget-bin/www_bget?aaindex:HENS920102
i = 'HENS920102'  # ID of BLOSUM62
A = data[i].M
print(data[i].D, data[i]['*'], sep='\n')
print("Matrix:", A.astype(int).head(3), "...", sep='\n')

print("[BLOSUM62 -- FASTA]")
from tcga.data.blosum import blosum62_12 as B
from tcga.refs import annotations

print(pretty(annotations[B]), sep="\n")
print("Matrix:", B.head(3), "...", sep='\n')
```

```
[BLOSUM62 -- AAindex]
BLOSUM62 substitution matrix (Henikoff-Henikoff, 1992)
matrix in 1/3 Bit Units
Matrix:
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V
A  6 -2 -2 -3 -1 -1 -1  0 -2 -2 -2 -1 -1 -3 -1  2  0 -4 -3  0
R -2  8 -1 -2 -5  1  0 -3  0 -4 -3  3 -2 -4 -3 -1 -2 -4 -3 -4
N -2 -1  8  2 -4  0  0 -1  1 -5 -5  0 -3 -4 -3  1  0 -6 -3 -4
...
[BLOSUM62 -- FASTA]
{
  "source": "https://github.com/wrpearson/fasta36/tree/7c0dba1dfe5fc92d937f2bd5f9c90b8bfdb14743/data",
  "date": "2020-06-15",
  "comments": [
    "BLOSUM62 is in 1/2 bit units, the others are in 1/3 bit units.",
    "The BLOSUM62 matrix is the original, miscalculated one according to [1, Supplementary Fig 4]."
  ],
  "references": [
    "[1] Styczynski, M., Jensen, K., Rigoutsos, I. et al. BLOSUM62 miscalculations improve search performance. Nat Biotechnol 26, 274-275 (2008). https://doi.org/10.1038/nbt0308-274"
  ]
}
Matrix:
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X
A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0 -2 -1  0
R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3 -1  0 -1
N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3  3  0 -1
...
```

## License

MIT/Expat.

## Suggestions

Suggestions and help are most welcome. 
