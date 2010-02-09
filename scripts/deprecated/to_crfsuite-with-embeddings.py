#!/bin/env python

import sys

assert len(sys.argv) == 2
embeddingsscale = float(sys.argv[1])

#embeddingsfile = "/u/turian/data/share/embeddings-20090916-rcv1.case-intact.LEARNING_RATE=0_000000001_--EMBEDDING_LEARNING_RATE=0_0000032.model-720000000.txt.gz"
embeddingsfile = "/u/turian/data/share/hlbl_reps_clean_1.rcv1.clean.tokenized-CoNLL03.case-intact.txt.gz"

from common.file import myopen
import string
word_to_embedding = {}
for l in myopen(embeddingsfile):
    sp = string.split(l)
    word_to_embedding[sp[0]] = [float(v)*embeddingsscale for v in sp[1:]]

def output_features(fo, seq):
    for i in range(2, len(seq)-2):
        fs = []

        fs.append('U00=%s' % seq[i-2][0])
        fs.append('U01=%s' % seq[i-1][0])
        fs.append('U02=%s' % seq[i][0])
        fs.append('U03=%s' % seq[i+1][0])
        fs.append('U04=%s' % seq[i+2][0])

        for name, pos in zip(["U00", "U01", "U02", "U03", "U04"], [i-2,i-1,i,i+1,i+2]):
            w = seq[pos][0]
            if w not in word_to_embedding: w = "*UNKNOWN*"
            for d in range(len(word_to_embedding[w])):
                fs.append("%se%d=1:%g" % (name, d, word_to_embedding[w][d]))

        fs.append('U05=%s/%s' % (seq[i-1][0], seq[i][0]))
        fs.append('U06=%s/%s' % (seq[i][0], seq[i+1][0]))

        fs.append('U10=%s' % seq[i-2][1])
        fs.append('U11=%s' % seq[i-1][1])
        fs.append('U12=%s' % seq[i][1])
        fs.append('U13=%s' % seq[i+1][1])
        fs.append('U14=%s' % seq[i+2][1])
        fs.append('U15=%s/%s' % (seq[i-2][1], seq[i-1][1]))
        fs.append('U16=%s/%s' % (seq[i-1][1], seq[i][1]))
        fs.append('U17=%s/%s' % (seq[i][1], seq[i+1][1]))
        fs.append('U18=%s/%s' % (seq[i+1][1], seq[i+2][1]))
        
        fs.append('U20=%s/%s/%s' % (seq[i-2][1], seq[i-1][1], seq[i][1]))
        fs.append('U21=%s/%s/%s' % (seq[i-1][1], seq[i][1], seq[i+1][1]))
        fs.append('U22=%s/%s/%s' % (seq[i][1], seq[i+1][1], seq[i+2][1]))

        fo.write('%s\t%s\n' % (seq[i][2], '\t'.join(fs)))
    fo.write('\n')

def encode(x):
    x = x.replace('\\', '\\\\')
    x = x.replace(':', '\\:')
    return x
    
fi = sys.stdin
fo = sys.stdout

d = ('', '', '')

seq = [d, d]
for line in fi:
    line = line.strip('\n')
    if not line:
        seq.append(d)
        seq.append(d)
        output_features(fo, seq)
        seq = [d, d]
    else:
        fields = line.strip('\n').split(' ')
        seq.append((encode(fields[0]), encode(fields[1]), encode(fields[2])))
