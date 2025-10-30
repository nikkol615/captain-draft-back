from config.get_env import get_env_data

PORT = int(get_env_data("API_PORT", 8000))
HOST = get_env_data("API_HOST", "0.0.0.0")