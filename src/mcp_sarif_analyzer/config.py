from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
DATA_INPUT=BASE_DIR/"data"/"input"
DEFAULT_SARIF=DATA_INPUT/"zlib-git-master-09a1572.sarif"

SVACER_HOST = "localhost"
SVACER_PORT = "8080"
SVACER_USER = "admin"
SVACER_PASSWORD = "admin"
SVACER_PROJECT = "zlib" # имя проекта
SVACER_BRANCH = "master" # ветка
# SVACER_SNAPSHOT = "first-stat-analyze" # имя снимка
