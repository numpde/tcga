# RA, 2020-06-19

import pandas
import zipfile
import pickle
import tcga.refs
import pathlib


class _:
    file = pathlib.Path(__file__).parent / "static/parsed/aaindex.pkl.zip"
    with zipfile.ZipFile(file, mode='r') as zf:
        with zf.open(str(file.with_suffix(".pkl").name), mode='r') as fd:
            data = pickle.load(fd)

    with (file.parent / F"{file.name}_meta.txt").open('r') as fd:
        meta = fd.read()


indices: pandas.Series
matrices: pandas.Series
potentials: pandas.Series

data = _.data['aaindex']
indices = _.data['list_of_indices']
matrices = _.data['list_of_matrices']
potentials = _.data['list_of_potentials']

tcga.refs.annotations[data]['source'] = _.meta
tcga.refs.annotations[indices]['source'] = _.meta
tcga.refs.annotations[matrices]['source'] = _.meta
tcga.refs.annotations[potentials]['source'] = _.meta

if __name__ == '__main__':
    print(data[indices.sample(1).index[0]].I)
