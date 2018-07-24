#!/usr/bin/env python

import itertools
import argparse
import json
import csv
import os
import re

from pprint import pprint

POINTS_THRESHOLD = 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            'This script generates makeflows to process the input data')
    parser.add_argument('points_csv', type=str,
            help='A CSV file containing occurrence information. ' \
            + 'Like taxa should be in consecutive rows.')
    parser.add_argument('out_dir', type=str,
            help='Directory to write CSV files to.')
    args = parser.parse_args()

    os.mkdir(args.out_dir)

    with open(args.points_csv) as in_f:
        lines = csv.reader(in_f)
        taxa = itertools.groupby(lines, lambda x: x[13])
        for taxon, lines in taxa:
            name = re.sub('\s', '_', re.split('[^\w\s]', taxon)[0].strip())
            chunk = list(lines)
            if len(chunk) < POINTS_THRESHOLD:
                continue
            chunk_fn = os.path.join(args.out_dir, '{}.csv'.format(name))
            with open(chunk_fn, 'w') as out_f:
                out = csv.writer(out_f)
                for l in chunk:
                    out.writerow([name] + l[14:16])
