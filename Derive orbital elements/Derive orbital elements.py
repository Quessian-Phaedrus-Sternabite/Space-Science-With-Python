import datetime
import pathlib
import urllib
import os
import numpy as np
import spiceypy

# We define a function that is useful for downloading SPICE
# kernel files. Some kernels are large and cannot be uploaded on the GitHub
# repository. Thus, this helper function shall support you for future kernel
# management (if needed).
def download_kernel(dl_path, dl_url):
    """
    download_kernel(DL_PATH, DL_URL)

    This helper function supports one to download kernel files from the
    NASA NAIF repository and stores them in _kernel directory

    Parameters
    ----------
    DL_PATH : str
        Download path on the local machine, relative to this function.
    DL_URL : str
        Download url of the requested kernel file.
    """


