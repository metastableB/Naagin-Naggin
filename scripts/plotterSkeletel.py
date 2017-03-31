#
# @author:Don Dennis (metastableB)
# plotterSkeletel.py
#
# This is a scratchpad I use for analysis purposes.
# Has no real utility.

import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = '../data/20_100_ReflexAgent_RandomFoodAgent.csv'
CELL_WIDTH = 20
data = pd.read_csv(DATA_FILE, header=None)
data.columns = ['Score', 'Length']
# print(data.head())

# print("Description of Score")
# print(data['Score'].describe())

# print("Description of Length")
# print(data['Length'].describe())
relLength = data['Length'].mean() / (CELL_WIDTH * CELL_WIDTH)
relLength *= 100
relModLength = data['Length'].mode() / (CELL_WIDTH * CELL_WIDTH)
relModLength *= 100
relModLength = max(relModLength)
relMaxLength = data['Length'].max() / (CELL_WIDTH * CELL_WIDTH)
relMaxLength *= 100
print("Relative max length %f" % relMaxLength)
print("Relative average Length %f" % relLength)
print("Relative modal length %f" % relModLength)
