#!/usr/bin/env python3

import argparse
import random
import time
import sys
import csv

from pythonosc import osc_message_builder
from pythonosc import udp_client

from pythonosc.osc_bundle_builder import OscBundleBuilder, IMMEDIATELY
from pythonosc.osc_message_builder import OscMessageBuilder

def scale_value(value, ip_range, domain=(0,1)):
    """ Linearly scale value to fit given domain """
    x1, x2 = domain
    y1, y2 = ip_range

    assert(y1 <= value <= y2)

    m = (x2 - x1)/(y2 - y1)
    b = y1 - m * x1
    return m * value - b


def main(args):
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    infile = args.infile

    last_epoch = None
    for row in csv.reader(iter(infile.readline, '')):
        epoch = int(row[0])

        heading_deg = float(row[1])
        heading_unit = scale_value(float(row[1]), [0, 360])
        print("Heading %s %s" % (heading_deg, heading_unit))

        speed = float(row[3])
        speed_unit = scale_value(speed, [0, 5])
        print("Speed %s %s" % (speed, speed_unit))

        if last_epoch is None:
            last_epoch = epoch

        sleep_time = epoch - last_epoch
        print(sleep_time)
        time.sleep(sleep_time)

        obb = OscBundleBuilder(IMMEDIATELY)

        # Adding heading
        heading_msg = OscMessageBuilder('/heading_deg')
        heading_msg.add_arg(heading_deg, arg_type=OscMessageBuilder.ARG_TYPE_FLOAT)
        obb.add_content(heading_msg.build())

        heading_msg = OscMessageBuilder('/heading_unit')
        heading_msg.add_arg(heading_unit, arg_type=OscMessageBuilder.ARG_TYPE_FLOAT)
        obb.add_content(heading_msg.build())

        # Adding speed
        speed_msg = OscMessageBuilder('/speed')
        speed_msg.add_arg(speed_unit, arg_type=OscMessageBuilder.ARG_TYPE_FLOAT)
        obb.add_content(speed_msg.build())

        bundle = obb.build()
        client.send(bundle)
        last_epoch = epoch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The IP of OSC server")
    parser.add_argument("--port",
        type=int, default=5005, help="The port OSC listens on")
    parser.add_argument(
        '--infile', default=sys.stdin, type=argparse.FileType('r'),
        help='file where the csv data should be read from')
    args = parser.parse_args()
    main(args)
