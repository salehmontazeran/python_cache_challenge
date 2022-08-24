import typing

from capacity import GLOBAL_CACHE_CAPACITY


def global_cache_get(cache, key: str) -> typing.Union[str, None]:
    cache_values = cache[0]
    cache_keys = cache[1]

    # TODO: Should use another method for generate hash key
    hashed_key = hash(key)

    for i in range(GLOBAL_CACHE_CAPACITY):
        if hashed_key == cache_keys[i]:
            return cache_values[i].value.decode()

    return None


def global_cache_put(cache, cache_lock, key: str, value: str) -> None:
    cache_values = cache[0]
    cache_keys = cache[1]
    cache_head = cache[2]

    # TODO: Should use another method for generate hash key
    hashed_key = hash(key)

    with cache_lock:
        for i in range(GLOBAL_CACHE_CAPACITY):
            if hashed_key == cache_keys[i]:
                return

        cache_keys[cache_head.value] = hashed_key
        cache_values[cache_head.value].value = value.encode("ascii")

        cache_head.value = (cache_head.value + 1) % GLOBAL_CACHE_CAPACITY
