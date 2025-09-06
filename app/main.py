from typing import Callable, Any, Tuple


def is_hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    _cache: dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not all(is_hashable(arg) for arg in args) or not all(
            is_hashable(v) for v in kwargs.values()
        ):
            raise TypeError(
                "Todos os argumentos devem ser imutáveis"
                "e hashable"
            )

        key: Tuple[Any, ...] = args + tuple(sorted(kwargs.items()))

        if key in _cache:
            print("Getting from cache")
            return _cache[key]

        print("Calculating new result")
        result = func(*args, **kwargs)
        _cache[key] = result
        return result

    return wrapper
