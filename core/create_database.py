from core.infrastructure.mysql import MySQL
from core.infrastructure.mock_json_db import MockJSONDB
from core.config import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
    MYSQL_PORT,
    MYSQL_SSL_REQUIRED,

    ENV_MODE
)

if ENV_MODE == "production":
    db = MySQL(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT,
        ssl_required=MYSQL_SSL_REQUIRED,
    )
else:   
    db = MockJSONDB()