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

