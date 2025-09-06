from typing import Callable, Any, Dict, Tuple


def is_hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    _global_cache: Dict[Callable[..., Any], Dict[Tuple[Any, ...], Any]] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Verifica se todos os argumentos são hashable
        for arg in list(args) + list(kwargs.values()):
            if not is_hashable(arg):
                raise TypeError(
                    f"O argumento {arg} não é imutável ou hashable. "
                    "Todos os argumentos devem ser tipos como tuplas,"
                    "strings ou números."
                )

        # Cria chave única e ordenada para kwargs
        key: Tuple[Any, ...] = args + tuple(sorted(kwargs.items()))

        # Cache isolado por função decorada
        func_cache = _global_cache.setdefault(func, {})

        if key in func_cache:
            print("Getting from cache")
            return func_cache[key]

        print("Calculating new result")
        result = func(*args, **kwargs)
        func_cache[key] = result
        return result
    return wrapper
