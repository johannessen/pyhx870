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

def config_write(config):
    h = hxtool.get(HxToolArgs())
    try:
        if not h.comm.cp_mode:
            raise Exception("not in CP mode (region mismatch?)")
        h.comm.sync()
        fw = h.comm.get_firmware_version()
    except Exception as exc:
        print( "Could not open connection to HX870." )
        sys.exit(1)
    print( "Firmware " + fw + " installed on device" )
    sys.stdout.write( "Writing to HX870 memory " )
    sys.stdout.flush()
    try:
        coloredlogs.set_level(logging.WARNING)
        config = h.config.config_write(config, progress=progress_bar)
    except Exception as exc:
        print( " Error!" )
        raise exc
    print( " done" )


def main():
    if not len(sys.argv) == 2:
        sys.stderr.write("Usage:\n    %s <file_name>\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        config = f.read()
    try:
        config_write(config)
    except KeyboardInterrupt:
        print( "\nAborted. Warning: The device may be in an inconsistent state." )
        sys.exit(1)


main()
