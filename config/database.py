from config.get_env import get_env_data
DB_LINK = get_env_data("DB_LINK", "postgresql://postgres:postgres@localhost:5431/postgres")