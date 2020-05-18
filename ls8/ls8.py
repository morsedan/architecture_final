#!/usr/bin/env python3

"""Main."""

import sys
from sys import argv
from cpu import *

cpu = CPU()

if len(argv) < 2:
    print("Please indicate a program file")
    exit(1)

_, file = argv

cpu.load(file)
cpu.run()