# RA, 2020-06-17

"""
All members of this module must be annotated
in particular containing the field 'source'.
"""

import tcga.strings
import tcga.refs
import pathlib
import zipfile
import pickle
import json
import pandas

# On codes
# https://en.wikipedia.org/wiki/Translation_(biology)#Translation_tables

standard_rna = dict(tcga.strings.nnna(
    # (Phe/F) Phenylalanine
    'UUU F' 'UUC F'
    # (Leu/L) Leucine
    'UUA L' 'UUG L' 'CUU L' 'CUC L' 'CUA L' 'CUG L'
    # (Ile/I) Isoleucine
    'AUU I' 'AUC I' 'AUA I'
    # (Met/M) Methionine
    'AUG M'
    # (Val/V) Valine
    'GUU V' 'GUC V' 'GUA V' 'GUG V'
    # (Ser/S) Serine
    'UCU S' 'UCC S' 'UCA S' 'UCG S'
    # (Pro/P) Proline
    'CCU P' 'CCC P' 'CCA P' 'CCG P'
    # (Thr/T) Threonine
    'ACU T' 'ACC T' 'ACA T' 'ACG T'
    # (Ala/A) Alanine
    'GCU A' 'GCC A' 'GCA A' 'GCG A'
    # (Tyr/Y) Tyrosine
    'UAU Y' 'UAC Y'
    # Stop (Ochre, Amber, Opal)
    'UAA *' 'UAG *' 'UGA *'
    # (His/H) Histidine
    'CAU H' 'CAC H'
    # (Gln/Q) Glutamine
    'CAA Q' 'CAG Q'
    # (Asn/N) Asparagine
    'AAU N' 'AAC N'
    # (Lys/K) Lysine
    'AAA K' 'AAG K'
    # (Asp/D) Aspartic acid
    'GAU D' 'GAC D'
    # (Glu/E) Glutamic acid
    'GAA E' 'GAG E'
    # (Cys/C) Cysteine
    'UGU C' 'UGC C'
    # (Trp/W) Tryptophan
    'UGG W'
    # (Arg/R) Arginine
    'CGU R' 'CGC R' 'CGA R' 'CGG R' 'AGA R' 'AGG R'
    # (Ser/S) Serine
    'AGU S' 'AGC S'
    # (Gly/G) Glycine
    'GGU G' 'GGC G' 'GGA G' 'GGG G'
))

tcga.refs.annotations[standard_rna] = {
    'source': "https://en.wikipedia.org/wiki/Genetic_code#Standard_codon_tables",
    'date': "2020-06-17",
}


class _:
    # Load from this file
    parsed = (pathlib.Path(__file__).parent / "static/parsed/tables.pkl.zip")

    with zipfile.ZipFile(parsed, mode='r') as zf:
        with zf.open("data", mode='r') as fd:
            tables = pickle.load(fd)
        with zf.open("meta", mode='r') as fd:
            meta = json.load(fd)


tables: pandas.DataFrame
tables = _.tables.set_index('id')
tcga.refs.annotations[tables] = _.meta

assert hasattr(tables, 'name')
assert hasattr(tables, 'short_name')
assert hasattr(tables, 'dna_codons')
assert hasattr(tables, 'rna_codons')
