#-----------------------------------------------------------------------------------------
# Constants

cdef int _CF_IEEE   = 0
cdef int _CF_CLASSIC = 1
cdef double _TA_MIN = -90.0
cdef double _TA_MAX =  90.0
cdef double _TC_MIN =  -90.0
cdef double _TC_MAX = 2000.0
cdef double _TENSION_MAX = 50000
#cdef double _ITER_MAX = 20000

CF_IEEE = _CF_IEEE
CF_CLASSIC = _CF_CLASSIC
TA_MIN = _TA_MIN
TA_MAX = _TA_MAX
TC_MIN = _TC_MIN
TC_MAX = _TC_MAX
TENSION_MAX = _TENSION_MAX
#ITER_MAX = _ITER_MAX