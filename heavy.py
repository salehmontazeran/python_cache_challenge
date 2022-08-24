import ctypes
import multiprocessing
import time

from capacity import GLOBAL_CACHE_CAPACITY, LOCAL_CACHE_CAPACITY
from global_cache import global_cache_get, global_cache_put
from lru import LRUCache

local_cache = LRUCache(LOCAL_CACHE_CAPACITY)

global_cache = (
    [multiprocessing.Array(ctypes.c_char, 50) for _ in range(GLOBAL_CACHE_CAPACITY)],
    multiprocessing.Array(ctypes.c_longlong, GLOBAL_CACHE_CAPACITY),
    multiprocessing.Value(ctypes.c_int),
)
global_cache[2].value = 0

cache_lock = multiprocessing.Lock()


def generate_cache_key(key: str) -> str:
    time_key = str(int(time.time() // 30))
    return key + time_key


# Main heavy computational function
def _hcf(s: str) -> str:
    print(f"heavy computation run for {s}")
    return str(reversed(s))


def heavy_computational_function(s: str) -> str:

    key = generate_cache_key(s)

    if lcr := local_cache.get(key):
        return lcr

    if gcr := global_cache_get(global_cache, key):
        return gcr

    # Some heavy computation
    r = _hcf(s)

    local_cache.put(key, r)
    global_cache_put(global_cache, cache_lock, key, r)

    return r
