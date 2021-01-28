import datetime, os, numpy as np, spiceypy

# Load the SPICE kernels via a meta file
spiceypy.furnsh('kernel_meta.txt')

# Create an initial date-time object that is converted to a string
DATETIME_UTC = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
DATETIME_ET = spiceypy.utc2et(DATETIME_UTC)

# ECLIPJ2000_DE405 and ECLIPJ2000 appear to be similar?! A transformation
# matrix between both coordinate systems (for state vectors) should be
# consequently the identity matrix
MAT = spiceypy.sxform(instring='ECLIPJ2000_DE405', \
                      tostring='ECLIPJ2000', \
                      et=DATETIME_ET)

# Let's print the transformation matrix row-wise (spoiler alert: it is the
# identity matrix)
print('Transformation matrix between ECLIPJ000_DE405 and ECLIPJ2000')
for mat_row in MAT:
    print(f'{(np.round(mat_row, 2) + 0)}')
print('\n')

CERES_STATE_VECTOR, _ = spiceypy.spkgeo(targ=2000001, \
                                        et=DATETIME_ET, \
                                        ref='ECLIPJ2000', \
                                        obs=10)

_, GM_SUN_PRE = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)

GM_SUN = GM_SUN_PRE[0]

# Compute the orbital elements of Ceres using the computed state vector
CERES_ORBITAL_ELEMENTS = spiceypy.oscltx(state=CERES_STATE_VECTOR, \
                                         et=DATETIME_ET, \
                                         mu=GM_SUN)

# Set and convert the semi-major axis and perihelion from km to AU
CERES_SEMI_MAJOR_AU = spiceypy.convrt(CERES_ORBITAL_ELEMENTS[9], \
                                      inunit='km', outunit='AU')
CERES_PERIHELION_AU = spiceypy.convrt(CERES_ORBITAL_ELEMENTS[0], \
                                      inunit='km', outunit='AU')

# Set the eccentricity
CERES_ECC = CERES_ORBITAL_ELEMENTS[1]

# Set and convert miscellaneous angular values from raidians
