import datetime
import spiceypy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

spiceypy.furnsh('kernel_meta.txt')

#Create an initial datetime object that is converted into a string
DATETIME_UTC = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

#convert to ET
DATETIME_ET = spiceypy.utc2et(DATETIME_UTC)