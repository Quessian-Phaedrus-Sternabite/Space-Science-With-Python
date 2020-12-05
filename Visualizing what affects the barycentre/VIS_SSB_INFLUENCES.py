import datetime
import spiceypy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#LOAD THE KERNELS
spiceypy.furnsh('kernel_meta.txt')

#We want to compute miscellaneous positions w.r.t. the centre of
#the Sun for a certain time interval.
#First, we set an initial time in UTC
INIT_TIME_UTC = datetime.datetime(year=2000, month=1, day=1, \
                                  hour=0, minute=0, second=0)

DELTA_DAYS = 10000
END_TIME_UTC = INIT_TIME_UTC + datetime.timedelta(days=DELTA_DAYS)

INIT_TIME_UTC_STR = INIT_TIME_UTC.strftime('%Y-%m-%d T%H:%M:%S')
END_TIME_UTC_STR = END_TIME_UTC.strftime('%Y-%m-%d T%H:%M:%S')

print('Init time in UTC: %s' % INIT_TIME_UTC_STR)
print('End time in UTC: %s\n' % END_TIME_UTC_STR)

INIT_TIME_ET = spiceypy.utc2et(INIT_TIME_UTC_STR)
END_TIME_ET = spiceypy.utc2et(END_TIME_UTC_STR)

#Create a numpy  array time interval
TIME_INTERVAL_ET = np.linspace(INIT_TIME_ET, END_TIME_ET, DELTA_DAYS)

# Using km is not intuitive. AU would scale it too severely. Since we compute
# the Solar System Barycentre (SSB) w.r.t. the Sun; and since we expect it to
# be close to the Sun, we scale the x, y, z component w.r.t the radius of the
# Sun. We extract the Sun radii (x, y, z components of the Sun ellipsoid) and
# use the x component
_, RADII_SUN = spiceypy.bodvcd(bodyid=10, item='RADII', maxn=3)

RADIUS_SUN = RADII_SUN[0]

#All computed parameters must be stored and dataframe.
#First, we create an empty one.
SOLAR_SYSTEM_DF = pd.DataFrame()

SOLAR_SYSTEM_DF.loc[:, 'ET'] = TIME_INTERVAL_ET

SOLAR_SYSTEM_DF.loc[:, 'UTC'] = \
    SOLAR_SYSTEM_DF['ET'].apply(lambda x: spiceypy.et2datetime(et=x).date())

#Here, the position of the SSB is computed W.R.T the sun
#spiceypy.spkgps returns the position and
# corresponding light time, we add the index [0] to
#obtain only the position array
SOLAR_SYSTEM_DF.loc[:, 'POS_SSB_WRT_SUN'] = \
    SOLAR_SYSTEM_DF['ET'].apply(lambda x: spiceypy.spkgps(targ=0, \
                                                          et=x, \
                                                          ref='ECLIPJ2000', \
                                                          obs=10)[0])

SOLAR_SYSTEM_DF.loc[:, 'POS_SSB_WRT_SUN_SCALED'] = \
    SOLAR_SYSTEM_DF['POS_SSB_WRT_SUN'].apply(lambda x: x / RADIUS_SUN)

SOLAR_SYSTEM_DF.loc[:, 'SSB_WRT_SUN_SCALED_DIST'] = \
    SOLAR_SYSTEM_DF['POS_SSB_WRT_SUN_SCALED'].apply(lambda x: \
                                                    spiceypy.vnorm(x))


FIG, AX = plt.subplots(figsize=(12, 8))

#plot the distance between Sun and SSB
AX.plot(SOLAR_SYSTEM_DF['UTC'], SOLAR_SYSTEM_DF['SSB_WRT_SUN_SCALED_DIST'], \
        color='tab:blue')

#set labels for the axis
AX.set_xlabel('Date in UTC')
AX.set_ylabel('SSB Dist. in Sun Radii', color='tab:blue')
AX.tick_params(axis='y', labelcolor='tab:blue')

#set limits for the x and y axis
AX.set_xlim(min(SOLAR_SYSTEM_DF['UTC']), max(SOLAR_SYSTEM_DF['UTC']))
AX.set_ylim(0, 2)

#Set a grid
AX.grid(axis='x', linestyle='dashed', alpha=0.5)

#Save the figure in high quality
plt.savefig('SSB2SUN_DISTANCE.png', dpi=300)

#We're going to compute the position vectors of
#the outer gas giants to see how it affects the SSB.
#We define a dictionary with an abbreviation and NAIF ID code.
NAIF_ID_DICT = {'JUB': 5, \
                'SAT': 6, \
                'URA': 7, \
                'NEP': 8}

# Iterate through the dictionary and compute the position vector for each
# planet as seen from the Sun. Further, compute the phase angle between the
# SSB and the planet as seen from the Sun
for planets_name_key in NAIF_ID_DICT:

    # Define the pandas dataframe column for each planet (position and phase
    # angle). Each '%s' substring is replaced with the planets name as
    # indicated after the "%"
    planet_pos_col = 'POS_%s_WRT_SUN' % planets_name_key
    planet_angle_col = 'PHASE_ANGLE_SUN_%s2SSB' % planets_name_key

    #get the corresponding ID of the planet's barycentre
    planet_id = NAIF_ID_DICT[planets_name_key]

    #compute the planets position as seen from the sun
    SOLAR_SYSTEM_DF.loc[:, planet_pos_col] = \
        SOLAR_SYSTEM_DF['ET'].apply(lambda x: \
                                    spiceypy.spkgps(targ=planet_id, \
                                                    et=x, \
                                                    ref='ECLIPJ2000', \
                                                    obs=10)[0])

    #Compute the phase angle between the SSB and the planet as seen from the Sun.
    #Since we apply a lambda function on all columns
    #we need to set axis=1 to avoid errors.
    SOLAR_SYSTEM_DF.loc[:, planet_pos_col] = \
        SOLAR_SYSTEM_DF.apply(lambda x: \
                              np.degrees(spiceypy.vsep(x[planet_pos_col], \
                                                       x['POS_SSB_WRT_SUN'])), \
                                                        axis=1)

    COMP_ANGLE = lambda vec1, vec2: np.arccos(np.dot(vec1, vec2) \
                                              / (np.linalg.norm(vec1) \
                                                 * np.linalg.norm(vec2)))

    print('Phase angle between the SSB and Jupiter as seen from the Sun (first ' \
      'array entry, lambda function): %s' % \
      np.degrees(COMP_ANGLE(SOLAR_SYSTEM_DF['POS_SSB_WRT_SUN'].iloc[0], \
                            SOLAR_SYSTEM_DF['POS_JUP_WRT_SUN'].iloc[0])))


    print('Phase angle between the SSB and Jupiter as seen from the Sun (first ' \
          'array entry, SPICE vsep function): %s' % \
          np.degrees(spiceypy.vsep(SOLAR_SYSTEM_DF['POS_SSB_WRT_SUN'].iloc[0], \
                                   SOLAR_SYSTEM_DF['POS_JUP_WRT_SUN'].iloc[0])))