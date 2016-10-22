#!/usr/bin/env python3
# coding: utf-8

import argparse
from itertools import chain
from collections import namedtuple

class Name:
    def __init__(self, normal):
        self.normal = normal
        self.lower = normal.lower()

def iter_selected_upper(src, keys):
    last = 0
    for k in keys:
        yield src[last:k]
        yield src[k].upper()
        last = k + 1
    yield src[last:]

def get_selected_upper(src, keys):
    return ''.join(iter_selected_upper(src, keys))

def value_of_selected_fullname(fullname_normal, keys):
    return sum(10 if 'A' <= fullname_normal[k] <= 'Z' else 1 for k in keys )

def iter_matches_of_names(shortname, fullname):
    short = shortname.lower
    full = fullname.lower
    keys = [-1] * len(short)
    key_at = 0
    end_at = len(full)
    while True:
        key = full.find(short[key_at], keys[key_at] + 1, end_at)
        if key == -1:
            if key_at == 0:
                raise StopIteration
            end_at = keys[key_at]
            key_at -= 1
        else:
            keys[key_at] = key
            if key_at == len(short) - 1:
                yield value_of_selected_fullname(fullname.normal, keys), get_selected_upper(fullname.lower, keys)
            else:
                key_at += 1
                keys[key_at] = key
                end_at += 1

def main():
    parser = argparse.ArgumentParser(description='list avaliable short names')
    parser.add_argument('names', type=argparse.FileType(mode='r'), help='list of full names')
    parser.add_argument('--dataset', nargs='+', type=argparse.FileType(mode='r'), help='lists of short names')
    args = parser.parse_args()

    fullnames = [Name(line[:-1]) for line in args.names if len(line) > 1]
    for line in chain.from_iterable(args.dataset):
        shortname = Name(line[:-1])
        for fullname in fullnames:
            for value, match in iter_matches_of_names(shortname, fullname):
                print('%d\t%s\t%s' % (value, shortname.normal, match))

if __name__ == '__main__':
    main()

