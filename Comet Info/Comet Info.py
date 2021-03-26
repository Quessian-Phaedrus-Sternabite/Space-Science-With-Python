import pandas as pd, sqlite3
# Connect to the comet database established in comets.py.
# It is uploaded on github.
con = sqlite3.connect('../_databases/_comets/mpc_comets.db')
# Set a cursor
cur = con.cursor()
# Create a pandas dataframe that contains all numerical variables of the database.
# for P type ...
P_TYPE_DF = pd.read_sql('SELECT PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="P"', con)
# ... and C type comics.
C_TYPE_DF = pd.read_sql('SELECT PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="C"', con)

A_TYPE_DF = pd.read_sql('SELECT PERIHELION_AU, SEMI_MAJOR_AXIS_AU, APHELION_AU, INCLINATION_DEG,'
                        'ECCENTRICITY, ARG_OF_PERIH_DEG, LONG_OF_ASC_NODE_DEG, MEAN_ANOMALY_DEG,'
                        'EPOCH_ET, ABSOLUTE_MAGNITUDE, SLOPE_PARAMETER, TISSERAND_JUP FROM comets_main WHERE '
                        'ORBIT_TYPE="A"', con)

name = \
    ["PERIHELION_AU",
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

x = 0
for i in P_INFO:
    print(name[x])
    print(f'The mean of {name[x]} - P is {i.mean()}')
    print(f'The median of {name[x]} - P is {i.median()}')
    print(f'The maximum of {name[x]} - P is {i.max()}')
    print(f'The minimum of {name[x]} - P is {i.min()}')
    x += 1
    print("\n")

print("---------------------------------------------------------------")

x = 0
for i in C_INFO:
    print(name[x])
    print(f'The mean of {name[x]} - C is {i.mean()}')
    print(f'The median of {name[x]} - C is {i.median()}')
    print(f'The maximum of {name[x]} - C is {i.max()}')
    print(f'The minimum of {name[x]} - C is {i.min()}')
    x += 1
    print("\n")

x = 0
for i in A_INFO:
    print(name[x])
    print(f'The mean of {name[x]} - C is {i.mean()}')
    print(f'The median of {name[x]} - C is {i.median()}')
    print(f'The maximum of {name[x]} - C is {i.max()}')
    print(f'The minimum of {name[x]} - C is {i.min()}')
    x += 1
    print("\n")