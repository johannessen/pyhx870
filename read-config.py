#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, sys, os
import coloredlogs, logging

import hxtool


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()

class HxToolArgs(object):
    def __init__(self):
        self.model = None
        self.tty = None
        self.simulator = None

def config_read():
    try:
        h = hxtool.get(HxToolArgs())
        h.comm.sync()
    except Exception as exc:
        print( "Could not open connection to HX870." )
        sys.exit(1)
    mmsi = h.config.read_mmsi()[0]
    print( "Device MMSI " + (mmsi if mmsi != "ffffffffff" else "not set") )
    sys.stdout.write( "Reading HX870 memory " )
    sys.stdout.flush()
    coloredlogs.set_level(logging.WARNING)
    config = h.config.config_read(progress_bar)
    print( " done" )
    return config

def main():
    if not len(sys.argv) == 2:
        sys.stderr.write("Usage:\n    %s <file_name>\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    try:
        config = config_read()
    except KeyboardInterrupt:
        print( "\nAborted. File '" + filename + "' unchanged." )
        sys.exit(1)
    with open(filename, "wb") as f:
        f.write(config)


main()
