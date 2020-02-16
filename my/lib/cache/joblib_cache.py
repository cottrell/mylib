import pathlib
import joblib

from ..paths import cache_basepath as _cache_basepath

_basepath = cache_basepath / 'joblib_cache'

memory = joblib.Memory(_basepath, verbose=10)

