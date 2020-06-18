# RA, 2020-06-18

import pandas
import pathlib
import tcga.refs.annotations

class _:
    datapath = pathlib.Path(__file__).parent / "static/data"
    file1 = datapath / "aa_prop1.csv"
    file2 = datapath / "aa_prop2.csv"
    nicer = (lambda s: ' '.join(s.split()))


properties = (
    pandas.read_csv(_.file1, sep='\t', comment='#')
).merge(
    pandas.read_csv(_.file2, sep='\t', comment='#').rename(columns={
        'pH 2': "At pH 2",
        'pH 7': "At pH 7",
    }),
    on='Abbr3',
)

tcga.refs.annotations[properties] = {
    'date': "2020-06-18",
    'source': [
        "https://www.sigmaaldrich.com/life-science/metabolomics/learning-center/amino-acid-reference-chart.html",
        "http://archive.ph/qL8ek",
    ],
    'comments': [
        _.nicer(
            """
            Columns 'At pH 2' and 'At pH 7' contain a measure of hydrophobicity.
            From the SA website: 
            The hydrophobicity index is a measure of the relative hydrophobicity, or how soluble an amino acid is in water. 
            In a protein, hydrophobic amino acids are likely to be found in the interior, 
            whereas hydrophilic amino acids are likely to be in contact with the aqueous environment.
            The values in the table are normalized so that the most hydrophobic residue 
            is given a value of 100 relative to glycine, which is considered neutral (0 value). 
            The scales were extrapolated to residues which are more hydrophilic than glycine.
            """
        ),
    ],
}

if __name__ == '__main__':
    print(properties)
    print(tcga.refs.annotations[properties])
