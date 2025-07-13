#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, os, struct, sys
import coloredlogs, logging

import hxtool


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()


def config_write(args, config):
    # Help with device selection: Try to auto-detect the device model for
    # the config data read from disk
    magic = struct.unpack('>h', config[0:2])[0]
    if not args.model:
        for model in hxtool.device.models.keys():
            if magic == hxtool.device.models[model].config_model.CONFIG_MAGIC:
                args.model = model

    devices = hxtool.device.enumerate(
        force_model   = args.model,
        force_device  = args.tty,
    )
    if len(devices) != 1:
        # Include the model determined from the config data in the error message
        device_name = f"{args.model} " if args.model else ""
        wrong_device_count = f"Multiple {device_name}devices" if devices else f"No {device_name}device"
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
    print( f"Device MMSI before writing was {mmsi}{callsign}" )

    sys.stdout.write( f"Writing to {h.handle} memory " )
    sys.stdout.flush()
    try:
        coloredlogs.set_level(logging.WARNING)
        config = h.config.config_write(config, check_region=False, progress=progress_bar)
    except Exception as exc:
        print( " Error!" )
        raise exc
    print( " done" )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model")
    parser.add_argument("-t", "--tty")
    parser.add_argument("filename")
    args = parser.parse_args()
    with open(args.filename, "rb") as f:
        config = f.read()
    try:
        config_write(args, config)
    except KeyboardInterrupt:
        print( "\nAborted. Warning: The device may be in an inconsistent state." )
        sys.exit(1)


main()
