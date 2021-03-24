# Import the standard modules
import sqlite3

# Import the installed modules
import pandas as pd
import numpy as np

# Import matplotlib for plotting
from matplotlib import pyplot as plt

# WARNING: This data may be slightly off compared to the example, due to differences in time.

# Connect to the comet database. This database has been created in the last file
# however, due to its small size the database is uploaded on GitHub
CON = sqlite3.connect('../_databases/_comets/mpc_comets.db')

# Create a pandas dataframe that contains the aphelion and inclination data
# for P type ...
P_TYPE_DF = pd.read_sql('SELECT APHELION_AU, INCLINATION_DEG '
                        'FROM comets_main WHERE ORBIT_TYPE="P"', CON)

# ... and C type comets. For this type: include also the eccentricity
C_TYPE_DF = pd.read_sql('SELECT APHELION_AU, INCLINATION_DEG, ECCENTRICITY '
                        'FROM comets_main WHERE ORBIT_TYPE="C"', CON)

# Print some descriptive statistics of the P type comets
print('Descriptive statistics of P comets')
print(f'{P_TYPE_DF.describe()}')
print('\n')

# Print some descriptive statistics of the C type comets (differentiate
# between bound (e<1) and un-bound (e>=1) comets)
print('Descriptive statistics of C comets with an eccentricity < 1')
print(f'{C_TYPE_DF.loc[C_TYPE_DF["ECCENTRICITY"] < 1].describe()}')
print('\n')

print('Descriptive statistics of C comets with an eccentricity >= 1')
print(f'{C_TYPE_DF.loc[C_TYPE_DF["ECCENTRICITY"] >= 1].describe()}')
print('\n')

# We plot the Inclination data vs. the aphelion data to determine differences
# between P and C comets.

# Let's set a dark background
plt.style.use('dark_background')

# Set a defualt font size for readability
plt.rcParams.update({'font.size': 14})

# Set a figure with a certain figure size
fig, ax = plt.subplots(figsize=(12, 8))

# Scatter plot of the P type comet inclination vs. the aphelion
ax.scatter(P_TYPE_DF['APHELION_AU'],
           P_TYPE_DF['INCLINATION_DEG'],
           marker='.', color='tab:orange', alpha=0.1, label='P Type')

# Scatter plot of the C type comet inclination vs. the aphelion (consider
# only the bound orbits!)
ax.scatter(C_TYPE_DF[C_TYPE_DF['ECCENTRICITY'] < 1]['APHELION_AU'],
           C_TYPE_DF[C_TYPE_DF['ECCENTRICITY'] < 1]['INCLINATION_DEG'],
           marker='^', color='tab:blue', alpha=0.5, label='C Type')

# The aphelion data vary between a few AU and hundreds of AU. We convert the
# x scale to a log10 scale
ax.set_xscale('log')

# Set a limit for the inclination; between 0 and 180 degrees.
ax.set_ylim(0, 180)

# Set a grid for better readability
ax.grid(axis='both', linestyle='dashed', alpha=0.2)

# Set a title, and labels for the x and y axis
ax.set_title('Comets with an eccentricity e<1')
ax.set_xlabel('Aphelion in AU')
ax.set_ylabel('Inclination in degrees')

# Now we set a legend. However, the marker opacity in the legend has the
# same value as in the plot. A value of 0.1 would be difficult to see ...
leg = ax.legend(fancybox=True, loc='upper right', framealpha=1)

# ... thus, we set the markers' opacity to 1 with this small code
for lh in leg.legendHandles:
    lh.set_alpha(1)

# Save the plot in high quality
plt.savefig('comets_scatter_plot_Q_i.png', dpi=400)

