# Program to visualize the positions of all comets in the database over the next 5 years
import datetime

import spiceypy
import sqlite3
import pandas as pd
import numpy as np
import datetime as dt

# Load the SPICE kernel meta file
spiceypy.furnsh('meta.txt')

# Get the G*M value of the Sun
_, GM_SUN_PRE = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)
GM_SUN = GM_SUN_PRE[0]

# Connect to database
CON = sqlite3.connect('../_databases/_comets/mpc_comets.db')

# Import data into dataframa
Comets_DF = pd.read_sql('SELECT NAME, PERIHELION_AU, ' \
                        'ECCENTRICITY, INCLINATION_DEG, ' \
                        'LONG_OF_ASC_NODE_DEG, ARG_OF_PERIH_DEG, ' \
                        'MEAN_ANOMALY_DEG, EPOCH_ET ' \
                        'FROM comets_main', CON)

"""
# Output the dataframe as a csv
compression_opts = dict(method='zip',
                        archive_name='comets.csv')

Comets_DF.to_csv('comets.zip', index=False,
          compression=compression_opts)
"""

conics = []
computed_conics = []

# User-defined start and end dates
start_date_str = '2023-04-08'
end_date_str = '2023-05-08'
start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

# Define the names of the comets as a list
comet_names = list(Comets_DF.index)

# Initialize an empty DataFrame with the desired index and column labels
time_values = pd.date_range(start=start_date, end=end_date, freq='D')
state_vectors = pd.DataFrame(index=comet_names, columns=time_values)

conics = []
computed_conics = []

# Loop over the time values and compute the state vectors for each comet
for time_value in time_values:
    DATETIME_ET = spiceypy.utc2et(time_value.strftime('%Y-%m-%dT%H:%M:%S'))
    for comet_name in comet_names:
        x = Comets_DF.index.get_loc(comet_name)
        conics = []
        conics.extend([spiceypy.convrt(Comets_DF['PERIHELION_AU'].iloc[x], 'AU', 'km'),
                       Comets_DF['ECCENTRICITY'].iloc[x],
                       np.radians(Comets_DF['INCLINATION_DEG'].iloc[x]),
                       np.radians(Comets_DF['LONG_OF_ASC_NODE_DEG'].iloc[x]),
                       np.radians(Comets_DF['ARG_OF_PERIH_DEG'].iloc[x]),
                       0.0,
                       Comets_DF['EPOCH_ET'].iloc[x],
                       GM_SUN])
        state_vector = spiceypy.conics(conics, DATETIME_ET)
        state_vectors.loc[comet_name, time_value] = state_vector

print(state_vectors)
print(Comets_DF.index)

# Create a copy of state_vectors without the comet names as columns
state_vectors_without_names = state_vectors.copy()
state_vectors_without_names.columns.name = None

# Add a 'NAME' column to state_vectors using pd.concat
state_vectors = pd.concat([Comets_DF['NAME'], state_vectors_without_names], axis=1)

state_vectors = state_vectors.set_index('NAME')

print(state_vectors)


# Output the dataframe as a csv
compression_opts = dict(method='zip',
                        archive_name='SV.csv')

state_vectors.to_csv('SV.zip', index=False,
          compression=compression_opts)