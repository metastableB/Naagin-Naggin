#
# @author:Don Dennis (metastableB)
# plotterSkeletel.py
#
# This is a scratchpad I use for analysis purposes.
# Has no real utility.

import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

CELL_WIDTH = 20


def analysis(DATA_FILE, keyString = 'Length'):
    data = pd.read_csv(DATA_FILE, header=None)
    data.columns = ['Score', 'Length']
    # print(data.head())

    # print("Description of Score")
    # print(data['Score'].describe())

    # print("Description of Length")
    # print(data['Length'].describe())
    mean = data[keyString].mean()
    relMean = mean / (CELL_WIDTH * CELL_WIDTH)
    relMean *= 100

    mode = data[keyString].mode()
    relMode = mode / (CELL_WIDTH * CELL_WIDTH)
    relMode *= 100
    relMode = max(relMode)
    mode = max(mode)

    maximum = data[keyString].max()
    relMaximum = maximum / (CELL_WIDTH * CELL_WIDTH)
    relMaximum *= 100
    print("Absolute max %s %f" % (keyString, maximum))
    print("Absolute average %s  %f" % (keyString, mean))
    print("Absolute modal %s  %f" % (keyString, mode))
    print("Relative max %s  %f" % (keyString, relMaximum))
    print("Relative average %s  %f" % (keyString, relMean))
    print("Relative modal %s  %f" % (keyString, relMode))


def main():
    directory = sys.argv[1]
    keyString = sys.argv[2]
    listing = os.listdir(directory)
    for f in listing:
        if not f.endswith('.csv'):
            continue
        if not f.startswith('20_40'):
            continue
        print("Analying: %s" % f)
        analysis(directory + f, keyString)
        print()


if __name__ == "__main__":
    main()
