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