import datetime
import spiceypy
import numpy as np
import pandas as pd

#Load meta-kernel
spiceypy.furnsh('kernel_meta.txt')


#Create Initial and endtime date-time object as a string.
INIT_TIME_UTC_STR = datetime.datetime(year=2020, month=1, day=1) \
                        .strftime('%Y-%m-%dT%H:%M:%S')
END_TIME_UTC_STR = datetime.datetime(year=2020, month=6, day=1) \
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
INNER_SOLSYS_DF.loc[:, 'ET'] = TIME_INTERVAL_ET

# The column UTC transforms all ETs back to a UTC format. The function
# spicepy.et2datetime is NOT an official part of SPICE (there you can find
# et2utc).
# However this function returns immediately a date-time object
INNER_SOLSYS_DF.loc[:, 'UTC'] = \
    INNER_SOLSYS_DF['ET'].apply(lambda x: spiceypy.et2datetime(et=x))

# Compute now the phase angle between Venus and Sun as seen from Earth
#
# For this computation we need the SPICE function phaseq. et is the ET. Based
# on SPICE's logic the target is the Earth (399) and the illumination source
# (illmn) is the Sun (10), the observer (obsrvr) is Venus with the ID 299.
# We apply a correction that considers the movement of the planets and the
# light time (LT+S)
INNER_SOLSYS_DF.loc[:, 'EARTH_VEN2SUN_ANGLE'] = \
    INNER_SOLSYS_DF['ET'].apply(lambda x: #
                                    np.degrees(spiceypy.phaseq(et=x, \
                                                               target='399', \
                                                               illmn='10', \
                                                               obsrvr='299', \
                                                               abcorr='LT+S')))

#Compute the angle between the Moon and the sun. We apply the same
#Function (phase1. The Moon NAIF ID is 301
INNER_SOLSYS_DF[:, 'EARTH_MOON2SUN_ANGLE'] = \
    INNER_SOLSYS_DF['ET'].apply(lambda x: \
                                    np.degrees(spiceypy.phaseq(et=x, \
                                                               target='399', \
                                                               illmn='10', \
                                                               obsrvr='301', \
                                                               abcorr='LT+S')))
#COmpute finally the phase angle between the Moon and Venus
INNER_SOLSYS_DF.loc[:, 'EARTH_MOON2VEN_ANGLE'] = \
    INNER_SOLSYS_DF['ET'].apply(lambda x: \
                                np.degrees(spiceypy.phaseq(et=x, \
                                                           target='399', \
                                                           illmn='299', \
                                                           obsrvr='301', \
                                                           abcorr='LT+S')))