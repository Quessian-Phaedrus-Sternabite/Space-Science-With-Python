# Space-Science-With-Python
These are my programs using SPICE, installed with spiceypy.
Mooost projects are independent, and only require the neccesary kernels (specified in the meta kernels). Others, such as the comet series, are dependent on others.
Enjoy, and feel free to use this for your own projects!

Warning: Current issue on mac where meta Kernel will not work. For fix, simply replace
kernel_meta.txt with the individual paths.

Ex.
spiceypy.furnsh('kernel_meta.txt') --- > spiceypy.furnsh('./kernels/lsk/naif0012.tls')

*The ULTIMATE CALCULATOR is a work in progress but is designed to be able to calculate many different things.*

# Dependencys
```
    spiceypy
    numpy
    scipy
    matplotlib
    jupyter
    pandas
    sympy
    nose
    IPython
```
