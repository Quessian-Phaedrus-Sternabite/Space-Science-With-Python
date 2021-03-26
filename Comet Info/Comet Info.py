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

P_PERI_INFO = [P_TYPE_DF["PERIHELION_AU"].mean(), P_TYPE_DF["PERIHELION_AU"].median(), P_TYPE_DF["PERIHELION_AU"].mode(), P_TYPE_DF["PERIHELION_AU"].max(), P_TYPE_DF["PERIHELION_AU"].minimum()]
P_SEMI_MAJOR_INFO = [P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].mean(), P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].median(), P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].mode(), P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].max(), P_TYPE_DF["SEMI_MAJOR_AXIS_AU"].minimum()]
P_APH_MEAN = P_TYPE_DF["APHELION_AU"].mean()
P_ECC_MEAN = P_TYPE_DF["ECCENTRICITY"].mean()
P_INC_MEAN = P_TYPE_DF["INCLINATION_DEG"].mean()
P_ARG_MEAN = P_TYPE_DF["ARG_OF_PERIH_DEG"].mean()
P_LON_MEAN = P_TYPE_DF["LONG_OF_ASC_NODE_DEG"].mean()
P_MEAN_ANOMALY_DEG_MEAN = P_TYPE_DF["MEAN_ANOMALY_DEG"].mean()
P_EPO_MEAN = P_TYPE_DF["EPOCH_ET"].mean()
P_ABS_MEAN = P_TYPE_DF["ABSOLUTE_MAGNITUDE"].mean()
P_SLOPE_MEAN = P_TYPE_DF["SLOPE_PARAMETER"].mean()
P_TISS_MEAN = P_TYPE_DF["TISSERAND_JUP"].mean()

C_PERI_MEAN = C_TYPE_DF["PERIHELION_AU"].mean()
C_SEMI_MAJOR_MEAN = C_TYPE_DF["SEMI_MAJOR_AXIS_AU"].mean()
C_APH_MEAN = C_TYPE_DF["APHELION_AU"].mean()
C_ECC_MEAN = C_TYPE_DF["ECCENTRICITY"].mean()
C_INC_MEAN = C_TYPE_DF["INCLINATION_DEG"].mean()
C_ARG_MEAN = C_TYPE_DF["ARG_OF_PERIH_DEG"].mean()
C_LON_MEAN = C_TYPE_DF["LONG_OF_ASC_NODE_DEG"].mean()
C_MEAN_ANOMALY_DEG_MEAN = C_TYPE_DF["MEAN_ANOMALY_DEG"].mean()
C_EPO_MEAN = C_TYPE_DF["EPOCH_ET"].mean()
C_ABS_MEAN = C_TYPE_DF["ABSOLUTE_MAGNITUDE"].mean()
C_SLOPE_MEAN = C_TYPE_DF["SLOPE_PARAMETER"].mean()
C_TISS_MEAN = C_TYPE_DF["TISSERAND_JUP"].mean()

print('P Type Comet Info \n ------------------------------------------------ \n')
print(f'P-Type Perihelion AU Average: {P_PERI_INFO}.\n'
      f'P-Type Semi-Major Axis Average: {P_SEMI_MAJOR_MEAN}.\n'
      f'P-Type Aphelion AU Average: {P_APH_MEAN}.\n',
      f'P-Type Eccentricity Average: {P_ECC_MEAN}.\n',
      f'P-Type Inclination Average: {P_INC_MEAN}.\n',
      f'P-Type Argument of Perihelion Degree Average: {P_ARG_MEAN}.\n',
      f'P-Type Longitude of Ascending Node Average: {P_APH_MEAN}.\n',
      f'P-Type Mean Anomaly Degree Average: {P_MEAN_ANOMALY_DEG_MEAN}.\n',
      f'P-Type Epoch ET average: {P_EPO_MEAN}.\n',
      f'P-Type Absolute Magnitude Average: {P_ABS_MEAN}.\n',
      f'P-Type Slope Average: {P_SLOPE_MEAN}.\n',
      f'P-Type Tisserand Parameter Jupiter Average: {P_TISS_MEAN}.\n')

print('C Type Comet Info \n ------------------------------------------------ \n')
print(f'C-Type Perihelion AU Average: {C_PERI_MEAN}.\n'
      f'C-Type Semi-Major Axis Average: {C_SEMI_MAJOR_MEAN}.\n'
      f'C-Type Aphelion AU Average: {C_APH_MEAN}.\n',
      f'C-Type Eccentricity Average: {C_ECC_MEAN}.\n',
      f'C-Type Inclination Average: {C_INC_MEAN}.\n',
      f'C-Type Argument of Perihelion Degree Average: {C_ARG_MEAN}.\n',
      f'C-Type Longitude of Ascending Node Average: {C_APH_MEAN}.\n',
      f'C-Type Mean Anomaly Degree Average: {C_MEAN_ANOMALY_DEG_MEAN}.\n',
      f'C-Type Epoch ET average: {C_EPO_MEAN}.\n',
      f'C-Type Absolute Magnitude Average: {C_ABS_MEAN}.\n',
      f'C-Type Slope Average: {C_SLOPE_MEAN}.\n',
      f'C-Type Tisserand Parameter Jupiter Average: {C_TISS_MEAN}.\n')
