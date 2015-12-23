
"""utils.py

include some common functions.
    initlog:    for loggging
    calc_score: caculate prediction score for validation set.

Author: lifematrix <stevenliucx@gmail.com>
"""

import os
import logging
import datetime

def initlog(pid=False):
    logging.basicConfig(
        format='%(asctime)s(%(relativeCreated)d) - %(levelname)s %(filename)s(%(lineno)d) :: %(message)s',
        #filename=os.path.join('log', str(datetime.date.today())+'.txt'),
        filename=getlogfilename(pid),
        filemode='a',
        level=logging.DEBUG,
    )

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s\t%(message)s",
                              datefmt='%m/%d/%y %H:%M:%S')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

def getlogfilename(pid=False):

    f_name = str(datetime.date.today())
    if pid:
        f_name += '.' + str(os.getpid())

    return os.path.join('log', f_name +'.txt')


def calc_score(vlts, preds):
    a = b = c = d = 0
    for (v, p) in zip(vlts, preds):
        if v == 0 and p == 0:
            a += 1
        elif v == 0 and p == 1:
            b += 1
        elif v == 1 and p == 0:
            c += 1
        else:
            d += 1

    logging.debug('a = %d, b = %d, c = %d, d = %d' % (a, b, c, d))

    spam_acc = d / float(b + d);  spam_recall = d / float(c + d)
    ham_acc = a / float(a + c);  ham_recall = a / float(a + b)

    score_spam = 0.65 * spam_acc + 0.35 * spam_recall
    score_ham = 0.65 * ham_acc + 0.35 * ham_recall

    logging.debug('spam_acc = %f, spam_recall = %f, ham_acc = %f, ham_recall = %f' %
                  (spam_acc, spam_recall, ham_acc, ham_recall))

    score_final = 0.7 * score_spam + 0.3 * score_ham

    return score_final
