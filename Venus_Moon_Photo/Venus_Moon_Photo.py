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
INIT_TIME_ET = spiceypy.utc2et(INIT_TIME_UTC_STR)
END_TIME_ET = spiceypy.utc2et(END_TIME_UTC_STR)

#Set the number of seconds per hour. This value is used to compute
#The phase angles in one hour steps.
DELTA_HOUR_IN_SECONDS = 3600.0
TIME_INTERVAL_ET = np.arange(INIT_TIME_ET, END_TIME_ET, DELTA_HOUR_IN_SECONDS)

#Create a pandas dataframe to store computed parameters, positions, etc.
INNER_SOLSYS_DF = pd.DataFrame()

#Set the ET column thatg stors all ET
INNER_SOLSYS_DF.loc[:, 'ET']
