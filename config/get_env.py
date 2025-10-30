import os

def get_env_data(key: str, default: str = None) -> str:
    """
    Получить переменную окружения с опциональным значением по умолчанию.

    Args:
        key: Ключ переменной окружения
        default: Значение по умолчанию
    Returns:
        str: Значение переменной окружения
    """
    return os.getenv(key, default)
