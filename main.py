import os
import argparse
from djvu2txt import convert
from inverted_index import InvertedIndex
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--indir', type=str, help='directory for .djvu documnets recursive search')
parser.add_argument('--outdir', type=str, default='', help='directory for results')
parser.add_argument('--partlen', type=int, default=1000000, help='Number of symbols in one part of text (for inverted '
                                                                 'index)')
args = parser.parse_args()

indir = args.indir
outdir = args.outdir
N = args.partlen
convert(indir, outdir)

path = os.path.join(outdir, 'djvu2txt')
to_process_txt = []

for rootdir, dirs, files in os.walk(path):
    for file in files:
        if file.split('.')[-1] == 'txt':
            to_process_txt.append(os.path.join(rootdir, file))

index = InvertedIndex()
for filename in to_process_txt:
    with open(filename, 'r') as f:
        text = f.read()
        parts_cnt = len(text) // N
        for i in range(parts_cnt):
            index.add_document(text[i * N: (i + 1) * N])

with open(os.path.join(outdir, 'index.pkl'), 'wb') as f:
    pickle.dump(index, f)
