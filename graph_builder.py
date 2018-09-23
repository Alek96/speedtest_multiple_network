#!/usr/bin/env python3

# import matplotlib
import os
import sys
from io import StringIO
import json
import datetime
import time
import pytz
import argparse
import numpy as np

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def add_line(ax, x_data, y_data, label, color):
    ax.plot(x_data, savgol_filter(y_data, 31, 5, mode='nearest'), label=label, color=color, alpha=0.6)
    ax.plot(x_data, y_data, color=color, alpha=0.15)


def set_graph_lims(ax, x_lim_left, x_lim_right, y_lim_left, y_lim_right):
    ax.set_xlim(x_lim_left, x_lim_right)
    ax.set_ylim(y_lim_left, y_lim_right)


def set_graph_info(ax, title, x_label, y_label):
    ax.set_xlabel(x_label, fontsize=20)
    ax.set_ylabel(y_label, fontsize=20)
    ax.set_title(title, fontsize=20)
    ax.legend(loc='upper left')


def min_from_dict_array(d, keys):
    return min([min(d[key]) for key in keys])


def max_from_dict_array(d, keys):
    return max([max(d[key]) for key in keys])


def get_if(a, b):
    return a + " " if b else ""


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="input json file (default: tests.json)", default=['tests.json'], nargs='+')
parser.add_argument("-i", "--ip", help="Generated graphs will be divided according to local IP addresses",
                    action="store_true")
parser.add_argument("--isp", help="Generated graphs will be divided by the name of the ISP", action="store_true")
parser.add_argument("--same-scale", dest='sameScale', help="Use the same scale for the graph with same data",
                    action='store_true')

parser.add_argument("--no-ping", dest='noPing', help="Do not generate ping graph", default=False, action="store_true")
parser.add_argument("--no-download", dest='noDownload', help="Do not generate download graph", default=False,
                    action="store_true")
parser.add_argument("--no-upload", dest='noUpload', help="Do not generate upload graph", default=False,
                    action="store_true")

parser.add_argument("-s", "--save", help="Name of saving picture (default: test.png)", default='test.png')
args = parser.parse_args()

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Crete board for graphs
plt.style.use('seaborn-whitegrid')

yDimensions = 3 - int(args.noPing) - int(args.noDownload) - int(args.noUpload)
fig, ax = plt.subplots(yDimensions, len(args.file), figsize=(16, 9))
fig.autofmt_xdate()
if yDimensions == 1:
    ax = [ax]
if len(args.file) == 1:
    for i in range(yDimensions):
        ax[i] = [ax[i]]

maxMaxPing = 0
maxMaxDownload = 0
maxMaxUpload = 0

for fileIdx in range(len(args.file)):
    # Will be used to hold data from json prepared for plotting
    defaultKey = 'key'
    colors = ['blue', 'red', 'green', 'orange', 'grey']
    keys = []
    timestamp = {}
    ping = {}
    download = {}
    upload = {}

    if not os.path.exists(args.file[fileIdx]):
        print("File \"{}\" does not exist.".format(args.file[fileIdx]), file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.file[fileIdx]):
        print("File \"{}\" is no regular file.".format(args.file[fileIdx]), file=sys.stderr)
        sys.exit(1)

    # Process json file containing the data and prepare it for plotting
    with open(args.file[fileIdx], "r") as f:
        for line in f:
            try:
                io = StringIO(line)
                data = json.load(io)
            except:
                # print("unexpected error: ", sys.exc_info()[0])
                continue

            key = get_if(data["client"]["isp"], args.isp) + get_if(data["client"]["ip"], args.ip)
            if key is None:
                key = defaultKey

            if key not in ping:
                keys.append(key)
                timestamp[key] = []
                ping[key] = []
                download[key] = []
                upload[key] = []

            timestamp[key].append(
                datetime.datetime.strptime(data["timestamp"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"))
            ping[key].append(float(data["ping"]))
            download[key].append(float(data["download"]) / 1000 / 1000)
            upload[key].append(float(data["upload"]) / 1000 / 1000)

    keys.sort()
    keyIdx = -1
    for key in keys:
        axIdx = 0
        keyIdx += 1
        color = colors[keyIdx]
        timestamp[key] = np.array(timestamp[key])

        if not args.noPing:
            ping[key] = np.array(ping[key])
            add_line(ax[axIdx][fileIdx], timestamp[key], ping[key], key, color)
            axIdx += 1
        if not args.noDownload:
            download[key] = np.array(download[key])
            add_line(ax[axIdx][fileIdx], timestamp[key], download[key], key, color)
            axIdx += 1
        if not args.noUpload:
            upload[key] = np.array(upload[key])
            add_line(ax[axIdx][fileIdx], timestamp[key], upload[key], key, color)
            axIdx += 1

    minTimestamp = min_from_dict_array(timestamp, keys)
    maxTimestamp = max_from_dict_array(timestamp, keys)
    maxPing = max_from_dict_array(ping, keys)
    maxDownload = max_from_dict_array(download, keys)
    maxUpload = max_from_dict_array(upload, keys)

    if args.sameScale:
        maxMaxPing = max(maxPing, maxMaxPing)
        maxMaxDownload = max(maxDownload, maxMaxDownload)
        maxMaxUpload = max(maxUpload, maxMaxUpload)

    axIdx = 0
    if not args.noPing:
        set_graph_lims(ax[axIdx][fileIdx], minTimestamp, maxTimestamp, 0, maxPing * 11 / 10)
        set_graph_info(ax[axIdx][fileIdx], "Ping", "time", "ms")
        axIdx += 1
    if not args.noDownload:
        set_graph_lims(ax[axIdx][fileIdx], minTimestamp, maxTimestamp, 0, maxDownload * 11 / 10)
        set_graph_info(ax[axIdx][fileIdx], "Download", "time", "Mbit/s")
        axIdx += 1
    if not args.noUpload:
        set_graph_lims(ax[axIdx][fileIdx], minTimestamp, maxTimestamp, 0, maxUpload * 11 / 10)
        set_graph_info(ax[axIdx][fileIdx], "Upload", "time", "Mbit/s")
        axIdx += 1

if args.sameScale:
    for fileIdx in range(len(args.file)):
        axIdx = 0
        if not args.noPing:
            set_graph_lims(ax[axIdx][fileIdx], None, None, 0, maxMaxPing * 11 / 10)
            axIdx += 1
        if not args.noDownload:
            set_graph_lims(ax[axIdx][fileIdx], None, None, 0, maxMaxDownload * 11 / 10)
            axIdx += 1
        if not args.noUpload:
            set_graph_lims(ax[axIdx][fileIdx], None, None, 0, maxMaxUpload * 11 / 10)
            axIdx += 1

# fig.subplots_adjust(wspace=100)
plt.tight_layout()
plt.savefig(args.save)
