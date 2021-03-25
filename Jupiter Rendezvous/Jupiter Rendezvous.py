# Import the standard modules
import sqlite3
import spiceypy

# Import the installed modules
import pandas as pd
import numpy as np

# Import matplotlib for plotting
from matplotlib import pyplot as plt

# Import scipy for the Kernel Density Estimator functionality
from scipy import stats

# Connect to the comet database established in comets.py.
# It is uploaded on github.
con = sqlite3.connect('../_databases/_comets/mpc_comets.db')

# Set a cursor
cur = con.cursor()

# Create a pandas dataframe that contians the name of the comer (needed later),
# the semi-major axis, inclination and eccentricity
# for P type ...
P_TYPE_DF = pd.read_sql('SELECT NAME, SEMI_MAJOR_AXIS_AU, INCLINATION_DEG,'
                        'ECCENTRICITY FROM comets_main WHERE ORBIT_TYPE="P"',
                        con)

# ... and C type comics. For this type: set the eccentricity smaller 1 (bound
# Orbits
C_TYPE_DF = pd.read_sql('SELECT NAME, SEMI_MAJOR_AXIS_AU, INCLINATION_DEG,'
                        'ECCENTRICITY FROM comets_main WHERE ORBIT_TYPE="C"'
                        'AND ECCENTRICITY<1', con)

