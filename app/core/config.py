import redis


OLLAMA_MODEL = "mistral"  # Change to another model if needed

# Redis configuration (use 'redis' as hostname inside Docker)
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0


DATABASE_URL = "sqlite:///users.db"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Connect to Redis
# Connect to Redis server (used for rate-limiting storage)
# Connect to Redis (inside Docker, use the service name 'redis' instead of 'localhost')
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)
