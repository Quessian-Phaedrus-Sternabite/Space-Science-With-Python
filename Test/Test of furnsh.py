import spiceypy

"""
spiceypy.furnsh('naif0012.tls')
spiceypy.furnsh('gm_de431.tpc')
spiceypy.furnsh('codes_300ast_20100725.bsp')
spiceypy.furnsh('codes_300ast_20100725.tf')
spiceypy.furnsh('de432s.bsp')
"""

spiceypy.furnsh('meta.txt')

x = spiceypy.ktotal("ALL")
print(x)