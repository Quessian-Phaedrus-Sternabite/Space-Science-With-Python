# Import the standard modules
import sqlite3

# Import the installed modules
import pandas as pd
import numpy as np

# Import matplotlib for plotting
from matplotlib import pyplot as plt

# Connect to the comet database. This database has been created in the comets file,
# however, due to its small size the database is uploaded on GitHub
CON = sqlite3.connect('../_databases/_comets/mpc_comets.db')

# Create a pandas dataframe that contains the aphelion and inclination data
# for P type ...
P_TYPE_DF = pd.read_sql('SELECT APHELION_AU, INCLINATION_DEG '
                        'FROM comets_main WHERE ORBIT_TYPE="P"', CON)

# ... and C type comets. For this type: include also the eccentricity
C_TYPE_DF = pd.read_sql('SELECT APHELION_AU, INCLINATION_DEG, ECCENTRICITY '
                        'FROM comets_main WHERE ORBIT_TYPE="C"', CON)


