from starlette.config import Config

config = Config(".env")

API_PREFIX: str = config("API_PREFIX", default="/api/v1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
ROOT_FTP_FOLDER: str = config("ROOT_FTP_FOLDER", default='/etc/ftp_projects')
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD")  # no default intentionaly, will crush if not in env
MINIO_ACCESS_KEY: str = config("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY: str = config("MINIO_SECRET_KEY")
DB_SCHEMA_NAME: str = config("DB_SCHEMA_NAME",
                             default='lacmus')  # so far ignored, SQLAlchemy doesn't seems fully supports it
# Queue size to create new worker
# todo - change debug for prod
# debug
ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER: int = config("ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER", default=10)
# ML_WORKER_PORT: int = config("ML_WORKER_PORT", default=4000)
KILL_WORKER_AFTER: int = config("KILL_WORKER_AFTER", default=100)
# prod
# ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER: int = config("ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER", default=400)
ML_WORKER_PORT: int = config("ML_WORKER_PORT", default=5000)
# Kill ml worker if no any task appeared within (sec)
# KILL_WORKER_AFTER: int = config("KILL_WORKER_AFTER", default=240)


MAX_ML_WORKERS_COUNT: int = config("MAX_ML_WORKERS_COUNT", default=3)
ORIGINAL_ML_WORKER_VOLUME: str = config("ORIGINAL_ML_WORKER_VOLUME", default='ubuntu-20-04-1-lacmus-api-worker-cpu')
