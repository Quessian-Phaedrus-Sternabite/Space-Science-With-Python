import datetime
import spiceypy
import numpy as np
import pandas as pd

#Load meta-kernel
spiceypy.furnsh('kernel_meta.txt')


#Create Initial and endtime date-time object as a string.
INIT_TIME_UTC_STR = datetime.datetime(year=2020, month=8, day=1) \
                        .strftime('%Y-%m-%dT%H:%M:%S')
END_TIME_UTC_STR = datetime.datetime(year=2021, month=1, day=1) \
                        .strftime('%Y-%m-%dT%H:%M:%S')

#conver to Ephemeris Time (ET) using utc2et
INT_TIME_ET = spiceypy.utc2et(INIT_TIME_UTC_STR)
END_TIME_ET = spiceypy.utc2et(END_TIME_UTC_STR)

#Set the number of seconds per hour. This value is used to compute
#The phase angles in one hour steps.