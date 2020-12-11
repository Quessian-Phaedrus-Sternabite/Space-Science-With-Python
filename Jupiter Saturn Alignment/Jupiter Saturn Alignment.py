import spiceypy
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

spiceypy.furnsh('kernel_meta.txt')

INIT_TIME_UTC = datetime.datetime(year=2020, month=12, day=1, \
                                  hour=0, minute=0, second=0)

DELTA_DAYS = 182
END_TIME_UTC = INIT_TIME_UTC + datetime.timedelta(days=DELTA_DAYS)

# Convert the datetime objects now to strings
INIT_TIME_UTC_STR = INIT_TIME_UTC.strftime('%Y-%m-%dT%H:%M:%S')
END_TIME_UTC_STR = END_TIME_UTC.strftime('%Y-%m-%dT%H:%M:%S')

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
INIT_TIME_ET = spiceypy.utc2et(INIT_TIME_UTC_STR)
END_TIME_ET = spiceypy.utc2et(END_TIME_UTC_STR)

# Create a numpy array that covers a time interval in delta = 1 day step
TIME_INTERVAL_ET = np.linspace(INIT_TIME_ET, END_TIME_ET, DELTA_DAYS)

# We want to get the phase angles of Saturn and Jupiter. When they are the same, the planets SHOULD BE in alignment.
# This will set up a dataframe to store the values
JUP_SAT_PHASE_DF = pd.DataFrame()

JUP_SAT_PHASE_DF.loc[:, 'ET'] = TIME_INTERVAL_ET

JUP_SAT_PHASE_DF.loc[:, 'PHASE_ANGLE_JUPITER'] = \
    JUP_SAT_PHASE_DF['ET'].apply(
        lambda x: np.degrees(spiceypy.phaseq(et=x, target='5', illmn='10', obsrvr='399', abcorr='LT+S')))

JUP_SAT_PHASE_DF.loc[:, 'PHASE_ANGLE_SATURN'] = \
    JUP_SAT_PHASE_DF['ET'].apply(
        lambda x: np.degrees(spiceypy.phaseq(et=x, target='6', illmn='10', obsrvr='399', abcorr='LT+S')))

JUP_SAT_PHASE_DF.loc[:, 'UTC'] = \
    JUP_SAT_PHASE_DF['ET'].apply(lambda x: spiceypy.et2datetime(et=x).date())

FIG, AX = plt.subplots(figsize=(12, 8))

# Plot the distance between the Sun and the SSB
AX.plot(JUP_SAT_PHASE_DF['UTC'], JUP_SAT_PHASE_DF['PHASE_ANGLE_JUPITER'], \
        color='tab:blue')

AX_add = AX.twinx()

AX_add.set_ylabel('Phase angle of Saturn', color='tab:orange')

AX_add.plot(JUP_SAT_PHASE_DF['UTC'], \
                  JUP_SAT_PHASE_DF['PHASE_ANGLE_SATURN'], \
                  color='tab:orange', \
                  linestyle='-')

# Set a label for the x and y axis and color the y ticks accordingly
AX.set_xlabel('Date in UTC')
AX.set_ylabel('Jupiter Phase Angle', color='tab:blue')
AX.tick_params(axis='y', labelcolor='tab:blue')

# Set limits for the x and y axis
AX.set_xlim(min(JUP_SAT_PHASE_DF['UTC']), max(JUP_SAT_PHASE_DF['UTC']))
AX.set_ylim(-180, 180)

# Set a grid
AX.grid(axis='x', linestyle='dashed', alpha=0.5)

# Saving the figure in high quality
plt.savefig('Jupiter Phase Angle.png', dpi=300)