from environs import Env

env = Env()
env.read_env() # read .env file if it exists

db_database = env.str("DB_PATH")
production = env.str("PRODUCTION")
