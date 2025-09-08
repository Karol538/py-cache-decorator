from typing import Callable, Any, Dict, Tuple


def is_hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    # Cache exclusivo para a função decorada
    func_cache: Dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Verifica se todos os argumentos são hashable
        for arg in list(args) + list(kwargs.values()):
            if not is_hashable(arg):
                raise TypeError(
                    f"O argumento {arg} não é hashable. "
                    "Certifique-se de usar tipos como tuplas, "
                    "strings, números ou frozensets."
                )

        # Cria chave única e ordenada para kwargs
        key: Tuple[Any, ...] = args + tuple(sorted(kwargs.items()))

        if key in func_cache:
            print("Getting from cache")
            return func_cache[key]

        print("Calculating new result")
        result = func(*args, **kwargs)
        func_cache[key] = result
        return result

    return wrapper
