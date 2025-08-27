from typing import Callable, Any, Tuple


def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    _cache: dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key: Tuple[Any, ...] = args + tuple(
            sorted(kwargs.items())
        )
        if key in _cache:
            print("Getting from cache")
            return _cache[key]

        print("Calculating new result")
        result = func(*args, **kwargs)
        _cache[key] = result
        return result

    return wrapper
