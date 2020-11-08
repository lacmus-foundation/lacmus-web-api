from starlette.config import Config

config = Config(".env")

API_PREFIX: str = config("API_PREFIX", default="/api/v1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
ROOT_FTP_FOLDER:str = config("ROOT_FTP_FOLDER",default='/etc/ftp_projects')
POSTGRES_PASSWORD:str =config("POSTGRES_PASSWORD") # no default intentionaly, will crush if not in env
MINIO_ACCESS_KEY:str=config("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY:str=config("MINIO_SECRET_KEY")
DB_SCHEMA_NAME:str = config("DB_SCHEMA_NAME",default='lacmus')
PROCESSING_BATCH_SIZE: int = config("PROCESSING_BATCH_SIZE", default=5)