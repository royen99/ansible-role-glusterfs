#!/usr/bin/env python3

import gfapi
import sys

BYTES_IN_KB = 1024

def computeVolumeStats(data):
    total = data.f_blocks * data.f_bsize
    return float(total)

vname = sys.argv[1].encode("ascii")
data = gfapi.getVolumeStatvfs(vname)
volumeCapacity = computeVolumeStats(data)

print(volumeCapacity)
