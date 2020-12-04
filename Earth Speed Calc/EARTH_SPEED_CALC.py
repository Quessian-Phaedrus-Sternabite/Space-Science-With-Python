import spiceypy, numpy, scipy, matplotlib, jupyter, pandas, sympy, nose, IPython
import datetime
import math

spiceypy.furnsh('C:/Users/kelle/OneDrive/Desktop/Python Files/Space sciene with python final/_kernels/lsk/naif0012.tls')
spiceypy.furnsh('C:/Users/kelle/OneDrive/Desktop/Python Files/Space sciene with python final/_kernels/spk/de432s.bsp')
spiceypy.furnsh('C:/Users/kelle/OneDrive/Desktop/Python Files/Space sciene with python final/_kernels/pck/gm_de431.tpc')

# Get's date
DATE_TODAY = datetime.datetime.today()

# Turns date into string, replace the table with midnight
DATE_TODAY = DATE_TODAY.strftime('%Y-%m-%dT00:00:00')

# Convert the utc midnight string to Et
ET_TODAY_MIDNIGHT = spiceypy.utc2et(DATE_TODAY)

# prints it
print(ET_TODAY_MIDNIGHT)

# targ : object that should be looked at
# et : the Eastern Time (ET) of the computation
# ref : The reference frame. Here, it's ECLIPJ2000, or the plane measured in 2000
# obs : The observer respective to the center of our state vector computation
EARTH_STATE_WRT_SUN, EARTH_SUN_LT = spiceypy.spkgeo(targ=399, \
                                                    et=ET_TODAY_MIDNIGHT, \
                                                    ref='ECLIPJ2000', \
                                                    obs=10)
print('State vector of the Earth w.r.t the Sun for "today" (midnight):\n', \
      EARTH_STATE_WRT_SUN)

# The distance should be around 1AU. Earth orbits the sun in a near perfect circle orbit. Ths calculates the distance
# in km.
EARTH_SUN_DISTANCE = math.sqrt(EARTH_STATE_WRT_SUN[0] ** 2.0 \
                               + EARTH_STATE_WRT_SUN[1] ** 2.0 \
                               + EARTH_STATE_WRT_SUN[2] ** 2.0)

EARTH_SUN_DISTANCE_AU = spiceypy.convrt(EARTH_SUN_DISTANCE, 'km', 'AU')

print('Current distance between the Earth and the Sun in AU: ', \
      EARTH_SUN_DISTANCE_AU)

EARTH_ORB_SPEED_WRT_SUN = math.sqrt(EARTH_STATE_WRT_SUN[3] ** 2.0 \
                                    + EARTH_STATE_WRT_SUN[4] ** 2.0 \
                                    + EARTH_STATE_WRT_SUN[5] ** 2.0)

print('Current orbital speed of the Earth around the Sun in km/s is: ', \
      EARTH_ORB_SPEED_WRT_SUN)

_, GM_SUN = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)

V_ORB_FUNC = lambda gm, r: math.sqrt(gm / r)
EARTH_ORB_SPEED_WRT_SUN_THEORY = V_ORB_FUNC(GM_SUN[0], EARTH_SUN_DISTANCE)

print('Theoretical orbital speed fo the Earth around the Sun in km/s: ', \
      EARTH_ORB_SPEED_WRT_SUN_THEORY)
