#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def delete(top):
    for root, dirs, files in os.walk(top):
        for name in files:
            if '.pyc' in name:
                os.remove(os.path.join(root, name))

if __name__ == '__main__':

    path = sys.argv[1]
    delete(path)
