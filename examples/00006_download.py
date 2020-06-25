# RA, 2020-06-25

from pathlib import Path
from tempfile import gettempdir
from tcga.utils import download

download = download.to(abs_path=(Path(gettempdir()) / "tcga_download_cache"))
print("Will download to:", download.local_folder)
# Will download to: /tmp/tcga_download_cache

# Lambda phage genome
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
