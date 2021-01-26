import datetime
import pathlib
import urllib
import os
import numpy as np
import spiceypy
import urllib.request

# We define a function that is useful for downloading SPICE
# kernel files. Some kernels are large and cannot be uploaded on the GitHub
# repository. Thus, this helper function shall support you for future kernel
# management (if needed).
def download_kernel(dl_path, dl_url):
    """
    download_kernel(DL_PATH, DL_URL)
    This helper function supports one to download kernel files from the NASA
    NAIF repository and stores them in the _kernel directory.
    Parameters
    ----------
    DL_PATH : str
        Download path on the local machine, relative to this function.
    DL_URL : str
        Download url of the requested kernel file.
    """

    # Obtain the kernel file name from the url string. The url is split at
    # the "/", thus the very last entry of the resulting list is the file's
    # name
    file_name = dl_url.split('/')[-1]

    # Create necessary sub-directories in the DL_PATH direction (if not
    # existing)
    pathlib.Path(dl_path).mkdir(exist_ok=True)

    # If the file is not present in the download directory -> download it
    if not os.path.isfile(dl_path + file_name):

        # Download the file with the urllib  package
        urllib.request.urlretrieve(dl_url, dl_path + file_name)


# Download the asteroids spk kernel file. First, set a download path, then
# the url and call the download function
PATH = '../_kernels/spk/'
URL = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/asteroids/' \
      + 'codes_300ast_20100725.bsp'

download_kernel(PATH, URL)

# Download an auxiliary file from the repository that contains the NAIF ID
# codes and a reference frame kernel that is needed. Since we have a mixture
# of different kernel types we store the data in a sub-directory called _misc
PATH = '../_kernels/_misc/'
URL = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/asteroids/' \
      + 'codes_300ast_20100725.tf'

download_kernel(PATH, URL)

# Load the SPICE kernels via a meta file
spiceypy.furnsh('kernel_meta.txt')

# Create an initial date-time object that is converted to a string
DATETIME_UTC = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
DATETIME_ET = spiceypy.utc2et(DATETIME_UTC)