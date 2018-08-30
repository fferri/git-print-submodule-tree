#!/usr/bin/env python3

from collections import OrderedDict as odict

def submodules(path):
    from subprocess import check_output as co
    from re import match
    for line in co(['git', 'submodule'], cwd=path).decode('utf8').split('\n'):
        m = match('\s+([0-9a-f]+)\s+(.*)\s+\((.*)\)', line)
        if m: yield m.groups()

class Node:
    def __init__(self, label, children=[]):
        self.label, self.children = label, children

def get_tree(path):
    import os
    return odict([(path1, get_tree(os.path.join(path, path1))) for ver, path1, branch in submodules(path)])

def print_tree(tree, indent=0):
    try:
        import asciitree
        left_aligned = asciitree.LeftAligned()
        print(left_aligned(tree))
    except ModuleNotFoundError:
        for k, v in tree.items():
            print('    '*indent, k)
            print_tree(v, indent+1)

import sys
root = sys.argv[1]
tree = {root: get_tree(root)}
print_tree(tree)
