#!/usr/bin/env python3

"""Main."""

import sys
from sys import argv
from cpu import *

# print("here")
cpu = CPU()
if len(argv) < 2:
    print("Please indicate a program file")
    exit(1)

_, file = argv
# print("File:", file)
cpu.load(file)
cpu.run()