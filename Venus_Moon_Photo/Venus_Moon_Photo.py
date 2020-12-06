import datetime
import spiceypy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as matpl_dates

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
    INNER_SOLSYS_DF['ET'].apply(lambda x: \
                                    np.degrees(spiceypy.phaseq(et=x, \
                                                               target='399', \
                                                               illmn='10', \
                                                               obsrvr='299', \
                                                               abcorr='LT+S')))

#Compute the angle between the Moon and the sun. We apply the same
#Function (phase1. The Moon NAIF ID is 301
INNER_SOLSYS_DF.loc[:, 'EARTH_MOON2SUN_ANGLE'] = \
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

# Are photos of both objects "photogenic"? Let's apply a pandas filtering
# with some artificially set angular distances and create a binary tag for
# photogenic (1) and non-photogenic (0) constellations
#
# Angular distance Venus - Sun: > 30 degrees
# Angular distance Moon - Sun: > 30 degrees
# Angular distance Moon - Venus: < 10 degree
INNER_SOLSYS_DF.loc[:, 'PHOTOGENIC'] = \
    INNER_SOLSYS_DF.apply(lambda x: 1 if (x['EARTH_VEN2SUN_ANGLE'] > 30.0) \
                                       & (x['EARTH_MOON2SUN_ANGLE'] > 30.0) \
                                       & (x['EARTH_MOON2VEN_ANGLE'] < 10.0) \
                                      else 0, axis=1)

print('Number of hours computed: %s (around %s days)' \
      % (len(INNER_SOLSYS_DF), round(len(INNER_SOLSYS_DF) / 24)))

print('Number of photogenic hours: %s (around %s days)' \
      % (len(INNER_SOLSYS_DF.loc[INNER_SOLSYS_DF['PHOTOGENIC'] == 1]), \
         round(len(INNER_SOLSYS_DF.loc[INNER_SOLSYS_DF['PHOTOGENIC'] == 1]) \
               / 24)))

#Set a figure
FIG, AX = plt.subplots(figsize=(12,8))

#Plot the phase anfles; apply different colours for the curves
#and set a legend label
AX.plot(INNER_SOLSYS_DF['UTC'], INNER_SOLSYS_DF['EARTH_VEN2SUN_ANGLE'], \
        color='tab:orange', label='Venus - Sun')

AX.plot(INNER_SOLSYS_DF['UTC'], INNER_SOLSYS_DF['EARTH_MOON2SUN_ANGLE'], \
        color='tab:gray', label='Moon - Sun')

AX.plot(INNER_SOLSYS_DF['UTC'], INNER_SOLSYS_DF['EARTH_MOON2VEN_ANGLE'], \
        color='black', label='Moon - Venus')

#Set labels
AX.set_xlabel('Date in UTC')
AX.set_ylabel('Angle in degrees')

#Set limits
AX.set_xlim(min(INNER_SOLSYS_DF['UTC']), max(INNER_SOLSYS_DF['UTC']))

#Set a grid
AX.grid(axis='x', linestyle='dashed', alpha=0.5)

#Set a month and day locators
AX.xaxis.set_major_locator(matpl_dates.MonthLocator())
AX.xaxis.set_minor_locator(matpl_dates.DayLocator())

#Set a format for the date-time (Year + Month name)
AX.xaxis.set_major_formatter(matpl_dates.DateFormatter('%Y-%b'))

# Iterate through the "photogenic" results and draw vertical lines where the
# "photogenic" conditions apply
for photogenic_utc in INNER_SOLSYS_DF.loc[INNER_SOLSYS_DF['PHOTOGENIC'] == 1]['UTC']:
    AX.axvline(photogenic_utc, color='tab:blue', alpha=.2)

#Create the legend in the top right corner of the plot
AX.legend(fancybox=True, loc='upper right', framealpha=1)

#Rotate the date-times
plt.xticks(rotation=45)

#Save the figure!
plt.savefig('VENUS_SUN_MOON.png', dpi=400)