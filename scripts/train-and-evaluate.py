#!/usr/bin/env python
"""
WARNING: Every time you change the --features parameter, you should also change the --name.

TODO: Write all parameters to workdir/parameters
TODO: Log all commands and output to a file.
TODO: We might write the same features file several times, but it is
better than different jobs clobbering each others files.
"""

import sys, string
from common.file import myopen
from common.stats import stats

print >> sys.stderr, "WARNING: Everytime you change the --features parameter, you should also change the --name."

from optparse import OptionParser
parser = OptionParser()

parser.add_option("-n", "--name", dest="name", help="Name of this run")
parser.add_option("--dev", dest="dev", action="store_true", help="Train on train-partition and evaluate on dev-partiton", default=True)
parser.add_option("--test", dest="dev", action="store_false", help="Train on train and evaluate on dev")
parser.add_option("-f", "--features", dest="features", help="Parameters for feature generation", type="string", default="")
parser.add_option("--l2", dest="l2", help="l2 sigma", type="string")

(options, args) = parser.parse_args()
assert len(args) == 0

assert options.name is not None

import os.path, os
from os.path import join
basedir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

datadir = join(basedir, "data")
featurescript = join(basedir, "scripts/to_crfsuite.py")
combinescript = join(basedir, "scripts/combine.pl")
evalscript = join(basedir, "scripts/conlleval.pl")
workdir = join(basedir, "work/%s" % options.name)
print >> sys.stderr, "Working in directory: %s" % workdir
if not os.path.exists(workdir): os.mkdir(workdir)
assert os.path.isdir(workdir)

if options.dev:
    trainfile = "train-partition.txt"
    evalfile = "dev-partition.txt"
else:
    trainfile = "train.txt"
    evalfile = "test.txt"

def run(cmd):
    print >> sys.stderr, cmd
    print >> sys.stderr, stats()
    os.system(cmd)
    print >> sys.stderr, stats()

#TODO: We might write the same features file several times, but it is
#better than different jobs clobbering each others files.
#featurestrainfile = join(workdir, "features-%s" % trainfile)
#featuresevalfile = join(workdir, "features-%s" % evalfile)
featurestrainfile = join(workdir, "features.l2=%s.%s" % (options.l2, trainfile))
featuresevalfile = join(workdir, "features.l2=%s.%s" % (options.l2, evalfile))

predictedevalfile = join(workdir, "predicted.l2=%s.%s" % (options.l2, evalfile))
scoredevalfile = join(workdir, "evaluation.l2=%s.%s" % (options.l2, evalfile))
modelfile = join(workdir, "model.l2=%s.%s" % (options.l2, trainfile))

cmd = "cat %s | %s %s > %s" % (join(datadir, trainfile), featurescript, options.features, featurestrainfile)
run(cmd)

cmd = "crfsuite learn -p algorithm=sgd -p feature.possible_transitions=1 -p feature.possible_states=1  -p regularization.sigma=%s -m %s %s 2>&1 | tee %s.err" % (options.l2, modelfile, featurestrainfile, modelfile)
run(cmd)
run("gzip -f %s" % trainfile)

cmd = "cat %s | %s %s > %s" % (join(datadir, evalfile), featurescript, options.features, featuresevalfile)
run(cmd)

cmd = "crfsuite tag -m %s %s | %s %s - > %s" % (modelfile, featuresevalfile, combinescript, join(datadir, evalfile), predictedevalfile)
run(cmd)
run("gzip -f %s" % featuresevalfile)
run("gzip -f %s" % modelfile)

cmd = "%s < %s > %s" % (evalscript, predictedevalfile, scoredevalfile)
run(cmd)

print >> sys.stderr, "WARNING: Everytime you change the --features parameter, you should also change the --name."
