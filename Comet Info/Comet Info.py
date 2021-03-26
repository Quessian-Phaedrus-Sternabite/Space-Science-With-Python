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
                        'EPOCH_ET,  FROM comets_main WHERE ORBIT_TYPE="P"',
                        con)

# ... and C type comics.
C_TYPE_DF = pd.read_sql('SELECT NAME, SEMI_MAJOR_AXIS_AU, INCLINATION_DEG,'
                        'ECCENTRICITY FROM comets_main WHERE ORBIT_TYPE="C"'
                        'AND ECCENTRICITY<1', con)

PERI_MEAN = P_TYPE_DF["PERIHELION_AU"].mean()
SEMI_MAJOR_MEAN = P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].mean()
APH_MEAN

print(f'P-Type Perihelion AU Average: {PERI_MEAN}.'
      f'P-Type Semi-Major Axis Average: {SEMI_MAJOR_MEAN}.'
      f'P-Type Aphelion AU Average: {APH_MEAN}')
