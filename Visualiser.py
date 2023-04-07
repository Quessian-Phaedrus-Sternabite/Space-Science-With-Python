# Program to visualize the positions of all comets in the database over the next 5 years

import spiceypy
import sqlite3
import pandas as pd


# Load the SPICE kernel meta file
spiceypy.furnsh('kernel_meta.txt')