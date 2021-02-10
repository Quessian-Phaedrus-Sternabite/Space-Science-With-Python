# Import the modules
import datetime
import numpy as np
import spiceypy

spiceypy.furnsh('meta.txt')

# Create an initial date-time object that is converted to a string
DATETIME_UTC = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
DATETIME_ET = spiceypy.utc2et(DATETIME_UTC)

# %%

# ECLIPJ2000_DE405 and ECLIPJ2000 appear to be similar?! A transformation
# matrix between both coordinate systems (for state vectors) should be
# consequently the identity matrix
MAT = spiceypy.sxform(instring='ECLIPJ2000_DE405',
                      tostring='ECLIPJ2000',
                      et=DATETIME_ET)

# Let's print the transformation matrix row-wise (spoiler alert: it is the
# identity matrix)
print('Transformation matrix between ECLIPJ2000_DE405 and ECLIPJ2000')
for mat_row in MAT:
    print(f'{(np.round(mat_row, 2) + 0)}')
print('\n')

# %%

# Compute the state vector of Ceres in ECLIPJ2000 as seen from the Sun
CERES_STATE_VECTOR, _ = spiceypy.spkgeo(targ=2000001,
                                        et=DATETIME_ET,
                                        ref='ECLIPJ2000',
                                        obs=10)
# %%

# Get the G*M value for the Sun
_, GM_SUN_PRE = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)

GM_SUN = GM_SUN_PRE[0]

# %%

# Compute the orbital elements of Ceres using the computed state vector
CERES_ORBITAL_ELEMENTS = spiceypy.oscltx(state=CERES_STATE_VECTOR,
                                         et=DATETIME_ET,
                                         mu=GM_SUN)

# Set and convert the semi-major axis and perihelion from km to AU
CERES_SEMI_MAJOR_AU = spiceypy.convrt(CERES_ORBITAL_ELEMENTS[9],
                                      inunit='km', outunit='AU')
CERES_PERIHELION_AU = spiceypy.convrt(CERES_ORBITAL_ELEMENTS[0],
                                      inunit='km', outunit='AU')

# Set the eccentricity
CERES_ECC = CERES_ORBITAL_ELEMENTS[1]

# Set and convert miscellaneous angular values from radians to degrees:
# inc: Inclination
# lnode: Longitude of ascending node
# argp: Argument of perihelion
CERES_INC_DEG = np.degrees(CERES_ORBITAL_ELEMENTS[2])
CERES_LNODE_DEG = np.degrees(CERES_ORBITAL_ELEMENTS[3])
CERES_ARGP_DEG = np.degrees(CERES_ORBITAL_ELEMENTS[4])

# Set the orbit period. Convert from seconds to years
CERES_ORB_TIME_YEARS = CERES_ORBITAL_ELEMENTS[10] / (86400.0 * 365.0)

# %%

# Compare the results with the data from the Minor Planet Center
# https://www.minorplanetcenter.net/dwarf_planets

# Print the results next to the MPC results
print('Ceres\' Orbital Elements')
print(f'Semi-major axis in AU: {round(CERES_SEMI_MAJOR_AU, 2)} (MPC: 2.77)')
print(f'Perihelion in AU: {round(CERES_PERIHELION_AU, 2)} (MPC: 2.56)')

print(f'Eccentricity: {round(CERES_ECC, 2)} (MPC: 0.08)')

print(f'Inclination in degrees: {round(CERES_INC_DEG, 1)} (MPC: 10.6)')
print(f'Long. of. asc. node in degrees: {round(CERES_LNODE_DEG, 1)} '
      '(MPC: 80.3)')
print(f'Argument of perih. in degrees: {round(CERES_ARGP_DEG, 1)} '
      '(MPC: 73.6)')

print(f'Orbit period in years: {round(CERES_ORB_TIME_YEARS, 2)} '
      '(MPC: 4.61)')
print('\n')

CERES_STATE_RE = spiceypy.conics([CERES_ORBITAL_ELEMENTS[0],
                                  CERES_ORBITAL_ELEMENTS[1],
                                  CERES_ORBITAL_ELEMENTS[2],
                                  CERES_ORBITAL_ELEMENTS[3],
                                  CERES_ORBITAL_ELEMENTS[4],
                                  CERES_ORBITAL_ELEMENTS[5],
                                  CERES_ORBITAL_ELEMENTS[6],
                                  GM_SUN], DATETIME_ET)

print('State vector of Ceres from the kernel:\n' 
      f'{CERES_STATE_VECTOR}')
print('State vector of Ceres based on the determined orbital elements:\n'
      f'{CERES_STATE_RE}')
print('\n')
