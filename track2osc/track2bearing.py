#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import calendar
import MySQLdb as mdb
import sys
import math
import csv

TRACK_ID=9


def get_bearing(coord_pair):
    """
        Get bearing from start to end
        https://gist.github.com/jeromer/2005586

        θ = atan2(sin(Δlong).cos(lat2),
        cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    """
    start, end = coord_pair
    lat1 = math.radians(start[0])
    lat2 = math.radians(end[0])

    diffLong = math.radians(end[1] - start[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# Columns
# id, time, user_id, track_id, latitude, longitude, altitude, speed,
# bearing, accuracy, provider, comment, image_id


time = lambda x: calendar.timegm(x[1].utctimetuple())
lat = lambda x: x[4]
lon = lambda x: x[5]
speed = lambda x: x[7]
bearing = lambda x: x[8] if x[8] is not None else -1
accuracy = lambda x: x[9]
latlon = lambda x :tuple(f(x) for f in (lat, lon))

def track_to_bearings(track):
    latlons = list(map(latlon, track))
    segments = zip(latlons, latlons[1::1])
    bearings = map(get_bearing, segments)
    times = map(time, track)
    speeds = map(speed, track)
    sent_bearing = map(bearing, track)
    return zip(times, bearings, sent_bearing, speeds)


def load_track(track_id):
    try:
        con = mdb.connect('localhost', 'ulogger', 'ulogger', 'ulogger');
        cur = con.cursor()
        cur.execute((
            'select * from positions '
            'where track_id = %s '
            'and provider = "gps" '
            'and accuracy < 5 '
            'and speed > 0 '
            'order by time;'),
            (track_id,)
        )
        track = cur.fetchall()
    except mdb.Error as e:
        print("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)
    finally:
        if con:
            con.close()
    return track


def main():
    track = load_track(TRACK_ID)
    bearings = track_to_bearings(track)
    writer = csv.writer(sys.stdout)
    for bearing in bearings:
        writer.writerow(bearing)

if __name__ == '__main__':
    main()
