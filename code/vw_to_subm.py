

"""vm_to_subm.py
convert vowpalwabbit prediction file to submission file.

Author: lifematrix <stevenliucx@gmail.com>
"""

import argparse
import math


def zygmoid(x):
    #I know it's a common Sigmoid feature, but that's why I probably found
    #it on FastML too: https://github.com/zygmuntz/kaggle-stackoverflow/blob/master/sigmoid_mc.py
    return 1 / (1 + math.exp(-x))

def hinge_convert(x):
    return (x + 1)/2.0

def readpred_vw(pred_file, loss_func="logistic"):
    if loss_func == "logistic":
        convert_func = zygmoid
    elif loss_func == "hinge":
        convert_func = hinge_convert
    else:
        raise ValueError("Unknown loss_func: %s" % loss_func)

    def parse_predline(line):
        row = line.strip().split(" ")
        # Id, Predicted(possibility)
        if len(row) > 1:
            # has Id column
            return [row[1], convert_func(float(row[0]))]
        else:
            return ['', convert_func(float(row[0]))]

    with open(pred_file) as f_in:
        return [parse_predline(line) for line in f_in]

def vw_to_subm(vw_pred_file, subm_file, loss_func, threshold):
    preds = readpred_vw(vw_pred_file, loss_func)
    with open(subm_file, 'w') as f_out:
        for x in preds:
            id = x[0]
            if x[1] >= threshold:
                label = 1
            else:
                label = 0
            f_out.write("%s,%d\n" %(id, label))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(add_help=True)
    parse.add_argument('vw_pred_file')
    parse.add_argument('subm_file')
    parse.add_argument('--loss_func', action='store', dest='loss_func', default="logistic")
    parse.add_argument('--threshold', action='store', dest='threshold', default=0.5)

    args = parse.parse_args()
    vw_to_subm(args.vw_pred_file, args.subm_file, args.loss_func, float(args.threshold))

