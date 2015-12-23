
"""grid_search_vw.py

Use grid search to find optimal parameters combinations: learning_rate, l1, l2, threshold ...
For every combination, cross validation is used to calculate average score.

Author: lifematrix <stevenliucx@gmail.com>
"""

from subprocess import check_call
import logging
from utils import initlog, getlogfilename
from vw_to_subm import readpred_vw
import os
from utils import calc_score
import sys

#vw_bin_path = '/root/work/dl/vowpal_wabbit.7.7/vowpalwabbit/vw'
#vw_bin_path = os.environ["VW"]
vw_bin_path = "vw"


train_file = 'data/train.seg.cnt.vw'
test_file = 'data/test.seg.cnt.vw'
model_file = 'data/model.vw'
preds_file = 'data/preds.txt'
cache_file = "data/data.vw.cache"


n_folds = 5
loss_func = "hinge"


def read_vlt(vlt_file):
    with open(vlt_file) as f:
        acct_labels = [ (int(line.split(" ")[0]) + 1)/2 for line in f]

    return acct_labels


def spam_score(preds_file, vlt_file, threshold=0.5):
    vlts = read_vlt(vlt_file)

    preds = readpred_vw(preds_file, loss_func)
    preds = [ 1 if x[1] >= threshold else 0 for x in preds]

    logging.info('threshold: %f, pos ratio of pred: %f, vlts #: %d, pos ratio of vlts: %f' %
                 (threshold, float(sum(preds))/len(preds), len(vlts), sum(vlts)/float(len(vlts))))

    score = calc_score(vlts, preds)
    return score

def check_call_log(arg):
    logfile = getlogfilename()
    with open(logfile, 'a') as f:
        check_call(arg, shell=True, stdout=f, stderr=f)

def train_predict(vlt_num, param_arg):
    arg = '%s %s -f %s --loss_function %s ' % \
          (vw_bin_path, '/dev/stdin', model_file, loss_func)

    if "--passes" in param_arg and int(param_arg['--passes']) > 1:
        arg += "--cache_file %s -k" % cache_file

    # For train
    for k, v in param_arg.items():
        if k[0] == "_" or v == "":
            continue
        arg += ' %s %s' % (k, v)


    cat_cmd = 'cat ' + " ".join([ '%s.%d' % (train_file, i)
                                  for i in range(n_folds) if i != vlt_num ])
    arg = cat_cmd + " | " + arg
    logging.info(arg)
    check_call_log(arg)

    # For validate
    vlt_file = "%s.%d" % (train_file, vlt_num)
    arg = '%s %s -t -i %s -p %s' % \
          (vw_bin_path, vlt_file, model_file, preds_file)
    logging.info(arg)
    check_call_log(arg)

    threshold = float(param_arg["_threshold"])
    s = spam_score(preds_file, vlt_file, threshold)
    return s

def cross_product_params(params_list):
    args = [{}]
    for p_name, p_list in params_list:
        new_args = []
        arg_name = p_list[0]
        for p in p_list[1]:
            if p == "":
                continue
            for a in args:
                d = dict(a)
                d[arg_name] = p
                new_args.append(d)
        args = new_args
    return args

def main():
    params_list = \
    [
        ["ngram", ["--ngram", [2]]],
        #["skips", ["--skips", ["", 3,4,5]]],
        ["learning_rate", ["-l", [0.65]]],
        #["l1", ["--l1", [0, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]]],
        ["l2", ["--l2", [1e-5]]],
        ["passes", ["--passes", [1]]],
        #["decay_learning_rate", ["--decay_learning_rate", [0.2, 0.5, 0.95, 1.0]]],
        ["bits", ["-b", [31]]],
        ["threshold", ["_threshold", [0.34]]],
    ]


    r = []        # results list
    params_args = cross_product_params(params_list)
    print params_args

    for p in params_args:
        s = []
        for i in range(n_folds):
            s.append(train_predict(i, p))
            logging.info('#%d, score: %f' % (i, s[-1]))
        avg_s = sum(s) / n_folds
        r.append([avg_s, p])
        logging.info("average score: %f" % avg_s)
        logging.debug('r = %r' % r)

    logging.debug('r = %r' % r)
    r = sorted(r, key=lambda x: x[0], reverse=True)
    logging.info('sorted r = %r' % r)


    logging.info('Best socre: %r, params: %r' % (r[0][0], r[0][1]))


if __name__ == '__main__':

    initlog()
    logging.info('begin')

    try:
        if len(sys.argv) > 1:
            train_file = sys.argv[1]
        main()
    except Exception as e:
        print('Error in execution: %s' % (e))
        logging.exception('Exception')
        print('Please refer to the log. The program will exit.')

    logging.info('end')


