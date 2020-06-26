# RA, 2020-06-26

import re
import json
import tcga.strings
import tcga.utils
import tcga.complements
import pathlib
import pandas
import pickle
import datetime
import zipfile

root_path = pathlib.Path(__file__).parent

raw = tcga.utils.download("ftp://ftp.ncbi.nih.gov/entrez/misc/data/gc.prt").to(abs_path=(root_path / "original")).now

# Get lines
lines = raw.text.split('\n')
# Remove spaces
lines = [l.strip() for l in lines]
# Keep the '-- BaseX' comments
lines = [re.sub(r'-- (Base[1-3])(\s+)([TCGA]+)', ', \g<1> "\g<3>"', l) for l in lines]
# Remove comments
lines = [l for l in lines if not l.startswith("--")]
# Remove empty lines
lines = [l for l in lines if l]
# Simplify initial definition
lines = [re.sub(r"([-\w\s]+)(::=)(\s+)", "", l) for l in lines]
# One string
s = ' '.join(lines).strip()
# List instead of set
s = re.sub(r"{(.*)}", "[\g<1>]", s)
# Numbers
s = re.sub(r'(id)(\s+)([0-9]+)', '\g<1> "\g<3>"', s)
# Identifiers
s = re.sub(r'([\w]+)(\s+)"([0-9\w\-*;:, ]+)"', '"\g<1>": "\g<3>"', s)
# Unduplicate 'name' tag
s = re.sub(r'"name": ("SGC[\w]+")', '"short_name": \g<1>', s)
# Numbers again
s = re.sub(r'"id": "([0-9]+)"', '"id": \g<1>', s)

tables = json.loads(s)


def make_table(entry, rna):
    codons = dict(tcga.strings.nnna("".join(
        map(
            "".join,
            zip(entry["Base1"], entry["Base2"], entry["Base3"], entry["ncbieaa"])
        )
    )))

    if rna:
        from tcga.complements import dna_to_rna, dna_to_dna
        from tcga.utils import First
        f = First(dna_to_dna).then(dna_to_rna)
        codons = {f(k): v for (k, v) in codons.items()}
    return codons


tables = [
    {
        'id': table['id'],
        'name': table['name'],
        'short_name': table.get('short_name', None),
        'dna_codons': make_table(tables[0], rna=False),
        'rna_codons': make_table(tables[0], rna=True),
    }
    for table in tables
]

tables = pandas.DataFrame(tables)

# Save to file
parsed = (root_path / "parsed/tables.pkl.zip")
parsed.parent.mkdir(exist_ok=True)

with zipfile.ZipFile(parsed, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    with zf.open("data", mode='w') as fd:
        pickle.dump(tables, fd)
    with zf.open("meta", 'w') as fd:
        fd.write(json.dumps({
            'comments': ["Compiled from the NCBI list of genetic codes.",
                         "https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi"],
            'datetime': datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep=' '),
            'source': raw.meta,
        }).encode())
