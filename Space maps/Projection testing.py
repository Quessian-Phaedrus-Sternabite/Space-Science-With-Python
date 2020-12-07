from matplotlib import pyplot as plt
import numpy as np
#Create an empty matplotlib example plot to show how matplotlib displays
# projected data

# Use a dark background
plt.style.use('dark_background')

# Set a figure
plt.figure(figsize=(12, 8))

# Apply the aitoff projection and activate the grid
plt.subplot(projection="aitoff")
plt.grid(True)

# Set long. / lat. labels
plt.xlabel('Long. in deg')
plt.ylabel('Lat. in deg')

# Save the figure
plt.savefig('empty_aitoff.png', dpi=300)