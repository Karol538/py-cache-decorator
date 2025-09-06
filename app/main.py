from typing import Callable, Any, Tuple

def is_hashable(obj: Any) -> bool:
    """Verifica se o objeto é hashable (imutável e seguro para usar como chave)."""
    try:
        hash(obj)
        return True
    except TypeError:
        return False

def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador que armazena em cache os resultados de chamadas de função
    com base em argumentos posicionais e nomeados.

    Requisitos:
    - Todos os argumentos devem ser imutáveis e hashables.
    - Funções com efeitos colaterais ou retornos mutáveis devem ser usadas com cautela.
    """
    _cache: dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Verifica se todos os argumentos são hashables
        if not all(is_hashable(arg) for arg in args) or not all(is_hashable(v) for v in kwargs.values()):
            raise TypeError("Todos os argumentos devem ser imutáveis e hashable")

        # Cria chave consistente e ordenada
        key: Tuple[Any, ...] = args + tuple(sorted(kwargs.items()))
        if key in _cache:
            print("Getting from cache")
            return _cache[key]

        print("Calculating new result")
        result = func(*args, **kwargs)
        _cache[key] = result
        return result

    return wrapper