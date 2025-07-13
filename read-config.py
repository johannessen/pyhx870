#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, os, sys
import coloredlogs, logging

import hxtool


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()


def config_read(args):
    devices = hxtool.device.enumerate(
        force_model   = args.model,
        force_device  = args.tty,
    )
    if len(devices) != 1:
        wrong_device_count = 'Multiple devices' if devices else 'No device'
        print( f"{wrong_device_count} detected. Try --model or --tty." )
        sys.exit(1)
    h = devices[0]
    if not h.comm.cp_mode or not h.comm.hx_hardware:
        print( "Could not open connection." )
        sys.exit(1)

    # Show device identification, to help users with selecting the right one
    mmsi = h.config.read_mmsi()[0]
    atis = h.config.read_atis()[0]
    callsign = hxtool.callsign.determine(atis)
    if not mmsi or mmsi == "FFFFFFFFF":
        mmsi = "not set"
    if callsign:
        callsign = ", call sign " + callsign
    elif atis and atis != "FFFFFFFFFF" and mmsi == "not set":
        callsign = ", ATIS " + atis
    print( "Device MMSI " + mmsi + callsign )

    sys.stdout.write( f"Reading {h.handle} memory " )
    sys.stdout.flush()
    try:
        coloredlogs.set_level(logging.WARNING)
        config = h.config.config_read(progress_bar)
    except Exception as exc:
        print( " Error!" )
        raise exc
    print( " done" )
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model")
    parser.add_argument("-t", "--tty")
    parser.add_argument("filename")
    args = parser.parse_args()
    try:
        config = config_read(args)
    except KeyboardInterrupt:
        print( "\nAborted. File '" + args.filename + "' unchanged." )
        sys.exit(1)
    with open(args.filename, "wb") as f:
        f.write(config)


main()
