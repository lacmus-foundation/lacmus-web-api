from starlette.config import Config

config = Config(".env")

API_PREFIX: str = config("API_PREFIX", default="/api/v1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
ROOT_FTP_FOLDER: str = config("ROOT_FTP_FOLDER", default='/etc/ftp_projects')
FTP_SERVER: str = config("FTP_SERVER",default="ftp")
FTP_API_PORT: int = config("FTP_API_PORT", default=5001)

POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD")  # no default intentionaly, will crush if not in env
POSTGRES_SERVER: str = config("POSTGRES_SERVER",default="postgres")
MINIO_ROOT_USER: str = config("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD: str = config("MINIO_ROOT_PASSWORD")
MINIO_SERVER: str = config("MINIO_SERVER",default="minio")

DOCKER_NETWORK: str = config("DOCKER_NETWORK",default="lacmus_server")
DOCKER_IMAGE_NAME: str = config("DOCKER_IMAGE_NAME",default="ml_worker_yolo5")

# Queue size to create new worker
ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER: int = config("ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER", default=100)
ML_WORKER_PORT: int = config("ML_WORKER_PORT", default=5000)
KILL_WORKER_AFTER: int = config("KILL_WORKER_AFTER", default=240)
MAX_ML_WORKERS_COUNT: int = config("MAX_ML_WORKERS_COUNT", default=1)
