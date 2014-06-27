#!/usr/bin/env python
import sys, zlib
sys.stdout.write(zlib.decompress(sys.stdin.read()))
