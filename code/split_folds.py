"""split_folds.py

Split the dataset(train or test) into n folds randomly for cross-validation.
Argument:
    datafile:  the data file to split
    -n :       n-folds
    --seed:    provide a random seed for generate the same folds every time.
    --prefix:  the prefix of n-folds filenames. The filenames is like: prefix.1, prefix.2, ..., prefeix.n.
               If not prefix specified, use original data filename as default.
    --header:  If the datafile has a header row, just like csv/tsv file.
               If true, every fold file generated will also include a header.

Author: lifematrix <stevenliucx@gmail.com>
"""

import argparse
import random

def splitfolds(datafile, n_folds, seed, prefix, header):

    if seed:
        random.seed(seed)

    if not prefix:
        prefix = datafile

    # s = os.path.splitext(prefix)
    # filenames = [ '%s_%d%s'%(s[0], i+1, s[1]) for i in range(n_folds)]
    # f_folds = [ open(fname, 'w') for fname in filenames]
    if prefix == "":
        prefix = datafile
    filenames = [ '%s.%d' % (prefix, i) for i in range(n_folds)]
    f_folds = [ open(fname, 'w') for fname in filenames]
    f_in = open(datafile, 'r')

    if header:
        line = f_in.readline()
        for f_out in f_folds:
            f_out.write(line)

    for line in f_in:
        i = random.randint(1, n_folds)
        f_folds[i-1].write(line)

    f_in.close()
    for f_out in f_folds:
        f_out.close()


if __name__ == '__main__':
    parse = argparse.ArgumentParser(add_help=False)
    parse.add_argument('datafile')
    parse.add_argument('-n', action='store', dest='n_folds', type=int)
    parse.add_argument('--seed', action='store', dest='seed', type=int)
    parse.add_argument('--prefix', action='store', dest='prefix')
    parse.add_argument('--header', action='store_true', dest='header', default=False)
    args = parse.parse_args()
    print args

    splitfolds(args.datafile, args.n_folds, args.seed, args.prefix, args.header)
