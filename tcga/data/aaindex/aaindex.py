# RA, 2020-06-19

import pandas
import zipfile
import pickle
import tcga.refs
import pathlib
import json


class _:
    file = pathlib.Path(__file__).parent / "static/parsed/aaindex.pkl.zip"
    with zipfile.ZipFile(file, mode='r') as zf:
        with zf.open("data", mode='r') as fd:
            data = pickle.load(fd)
        with zf.open("meta", mode='r') as fd:
            meta = {'source': json.loads(fd.read().decode())}


data: pandas.Series
indices: pandas.Series
matrices: pandas.Series
potentials: pandas.Series

data = _.data['aaindex']
indices = _.data['list_of_indices']
matrices = _.data['list_of_matrices']
potentials = _.data['list_of_potentials']

tcga.refs.annotations[data] = _.meta
tcga.refs.annotations[indices] = _.meta
tcga.refs.annotations[matrices] = _.meta
tcga.refs.annotations[potentials] = _.meta

if __name__ == '__main__':
    print(data[indices.sample(1).index[0]].I)
    print(data['DOSZ010101'].M)
    print(_.meta)

del _
