
"""convert_feats_seg.py
Convert original train & test datafile to vowpalwabbit format,
tokenize chinese short text and generate some additional features.

Author: lifematrix <stevenliucx@gmail.com>
"""

import argparse
import jieba
from utils import initlog, getlogfilename

HASH_MODE = 1000000    # max 1 million words

def convert(srcfile, destfile, test=False, cut_all=False):

    content_fld = 1 if test else 2
    n = 0

    # pat_xx = [ "".join(['x']*i) for i in range(5, 11)]

    with open(srcfile) as f_in, open(destfile, "w") as f_out:
        for line in f_in:
            c_cnt = 0; w_cnt = 0
            s_x_cnt = ""
            line = line.strip().split('\t')
            id = int(line[0])
            if test:
                label = "-1"
            else:
                label = line[1]
                if label == "0" :
                    label = "-1"
            if len(line) > content_fld:
                # check if content is empty.
                content = line[content_fld]
                c_cnt = len(content)

                content = content.decode('utf-8')
                x_cnt = content.count("x")
                if x_cnt >= 1 and  x_cnt <= 7:
                    s_x_cnt = "x_cnt:%d" % x_cnt

                #logging.info(content)
                seg = jieba.cut(content, cut_all=cut_all)
                #for s in seg: print s
                #seg = [s for s in seg]
                #logging.info(seg)
                content = [hex(hash(s) % HASH_MODE)[2:] for s in seg]
                w_cnt = len(content)
                content = ' '.join(content)
            else:
                content = ""

            #f_out.write("%s '%d |a %s |b c_cnt:%d w_cnt:%d %s\n" %
            #            (label, id, content, c_cnt, w_cnt, s_x_cnt))
            f_out.write("%s '%d |a %s |b c_cnt:%d w_cnt:%d\n" %
                        (label, id, content, c_cnt, w_cnt))
            #f_out.write("%s '%d |a %s\n" %
            #            (label, id, content))


if __name__ == '__main__':
    initlog()
    parse = argparse.ArgumentParser(add_help=False)
    parse.add_argument('-t', action='store_true', default=False, help='for test file')
    parse.add_argument('srcfile')
    parse.add_argument('destfile')
    parse.add_argument('--cut_all', action='store_true', default=False, help='for cut all word')
    args = parse.parse_args()

    convert(args.srcfile, args.destfile, args.t, args.cut_all)
