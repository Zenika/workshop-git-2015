#!/usr/bin/env python
import sys, zlib
sys.stdout.write(zlib.compress(sys.stdin.read()))
