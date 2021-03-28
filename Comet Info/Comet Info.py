import pandas as pd, sqlite3, spiceypy, numpy as np, datetime

spiceypy.furnsh('../_kernels/lsk/naif0012.tls')
spiceypy.furnsh('../_kernels/pck/gm_de431.tpc')

# Connect to the comet database established in comets.py.
# It is uploaded on github.
con = sqlite3.connect('../_databases/_comets/mpc_comets.db')

# Set a cursor
cur = con.cursor()

# Get the date and convert to Ephemeris Time.
DATETIME_UTC = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# convert to ET
DATETIME_ET = spiceypy.utc2et(DATETIME_UTC)


# Create a pandas dataframe that contains all numerical variables of the database.
# for P type ...
P_TYPE_DF = pd.read_sql('SELECT NAME, PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="P"', con)

# ... and C type comics.
C_TYPE_DF = pd.read_sql('SELECT NAME, PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="C"', con)

A_TYPE_DF = pd.read_sql('SELECT PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="A"', con)

ALL_DF = pd.read_sql('SELECT NAME, PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                     'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                     'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main', con)

name = ["PERIHELION_AU",
        "SEMI_MAJOR_AXIS_AU",
        "APHELION_AU",
        "ECCENTRICITY",
        "INCLINATION_DEG",
        "ARG_OF_PERIH_DEG",
        "LONG_OF_ASC_NODE_DEG",
        "MEAN_ANOMALY_DEG",
        "EPOCH_ET",
        "ABSOLUTE_MAGNITUDE",
        "SLOPE_PARAMETER",
        "TISSERAND_JUP"]

P_INFO = []
C_INFO = []
A_INFO = []
for i in name:
    P_INFO.append(P_TYPE_DF[i])
    C_INFO.append(C_TYPE_DF[i])
    A_INFO.append(A_TYPE_DF[i])

P = 0
for i in P_INFO:
    print(name[P])
    print(f'The mean of {name[P]} - P is {i.mean()}')
    print(f'The median of {name[P]} - P is {i.median()}')
    print(f'The maximum of {name[P]} - P is {i.max()}')
    print(f'The minimum of {name[P]} - P is {i.min()}')
    P += 1
    print("\n")

print("---------------------------------------------------------------")

C = 0
for i in C_INFO:
    print(name[C])
    print(f'The mean of {name[C]} - C is {i.mean()}')
    print(f'The median of {name[C]} - C is {i.median()}')
    print(f'The maximum of {name[C]} - C is {i.max()}')
    print(f'The minimum of {name[C]} - C is {i.min()}')
    C += 1
    print("\n")

print("---------------------------------------------------------------")

A = 0
for i in A_INFO:
    print(name[A])
    print(f'The mean of {name[A]} - C is {i.mean()}')
    print(f'The median of {name[A]} - C is {i.median()}')
    print(f'The maximum of {name[A]} - C is {i.max()}')
    print(f'The minimum of {name[A]} - C is {i.min()}')
    A += 1
    print("\n")

STATE_VECTOR_DF = pd.DataFrame

# Extract the G*M value of the Sun and assign it to a constant
_, GM_SUN_PRE = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)
GM_SUN = GM_SUN_PRE[0]

conics = []
computed_conics = []
x = 0

while x <= 900:
    conics.extend([spiceypy.convrt(ALL_DF['PERIHELION_AU'].iloc[x], 'AU', 'km'),
                                  ALL_DF['ECCENTRICITY'].iloc[x],
                                  np.radians(ALL_DF['INCLINATION_DEG'].iloc[x]),
                                  np.radians(ALL_DF['LONG_OF_ASC_NODE_DEG'].iloc[x]),
                                  np.radians(ALL_DF['ARG_OF_PERIH_DEG'].iloc[x]),
                                  0.0,
                                  ALL_DF['EPOCH_ET'].iloc[x],
                                  GM_SUN])
    x += 1

    computed_conics.append(spiceypy.conics(conics, DATETIME_ET))
    conics = []

print(computed_conics)