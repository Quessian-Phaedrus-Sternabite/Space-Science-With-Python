# Import the standard modules
import datetime
import pathlib
import sqlite3

# Import installed modules
import pandas as pd
import numpy as np
import spiceypy

# Import the Python script func from the auxiliary folder
import sys

sys.path.insert(1, '../_auxiliary')
import func

# Set a local download path and the URL to the comet data from the Minor
# Planet Center
DL_PATH = 'raw_data/'
DL_URL = 'https://www.minorplanetcenter.net/Extended_Files/cometels.json.gz'

# Download the comet data and store them in the directory
func.download_file(DL_PATH, DL_URL)

# Load the SPICE kernel meta file
spiceypy.furnsh('kernel_meta.txt')