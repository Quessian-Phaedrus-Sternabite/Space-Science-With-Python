# Import the standard modules
import datetime
import pathlib
import sqlite3

# Import installed modules
import pandas as pd
import numpy as np
import spiceypy

# Import the Python script func from the auxiliary folder
import sys

sys.path.insert(1, '../_auxiliary')
import func

# Set a local download path and the URL to the comet data from the Minor
# Planet Center
DL_PATH = 'raw_data/'
DL_URL = 'https://www.minorplanetcenter.net/Extended_Files/cometels.json.gz'

# Download the comet data and store them in the directory
func.download_file(DL_PATH, DL_URL)

# Load the SPICE kernel meta file
spiceypy.furnsh('kernel_meta.txt')

# Read the g-zipped json file with pandas read_json. The function allows one
# to read compressed data
c_df = pd.read_json('raw_data/cometels.json.gz', compression='gzip')

# First we parse the date and time information. The dataset contains two
# time related information: the date-time of the last perihelion passage and
# another variable called Epoch. However, "epoch" is not related to the mean
# anomaly related epoch and represents other time information in this case.
#
# For our "actual" Epoch case we need to create a UTC time string based on the
# date and time of the last perihelion passage (the time corresponds to a mean
# anomaly of 0 degrees). The Day is given in DAY.FRACTION_OF_DAY. We extract
# only the day
c_df.loc[:, 'EPOCH_UTC_DATE'] = \
    c_df.apply(lambda x: str(x['Year_of_perihelion']) + '-'
                         + str(x['Month_of_perihelion']) + '-'
                         + str(x['Day_of_perihelion']).split('.')[0],
               axis=1)

# Now we need to parse the .FRACTION_OF_DAY given between (0.0, 1.0). First,
# Create a place-holder date
PRE_TIME = datetime.datetime(year=2000, month=1, day=1)

# Use the pre_time date-time object and add the days and fraction of days with
# the timedelta function from the datetime library. Extract only the time
# substring ...
c_df.loc[:, 'EPOCH_UTC_TIME'] = \
    c_df['Day_of_perihelion'] \
        .apply(lambda x: (PRE_TIME + datetime.timedelta(days=x)).
               strftime('%H:%M:%S'))

# ... and based with the date, create now the UTC date-time
c_df.loc[:, 'EPOCH_UTC'] = c_df.apply(lambda x: x['EPOCH_UTC_DATE']
                                                + 'T'
                                                + x['EPOCH_UTC_TIME'],
                                      axis=1)

# Convert the UTC datetieme to ET
c_df.loc[:, 'EPOCH_ET'] = c_df['EPOCH_UTC'].apply(lambda x: spiceypy.utc2et(x))
