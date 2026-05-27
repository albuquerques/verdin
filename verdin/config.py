# pip install python-dotenv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .log import log


def load_config():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    token = os.getenv("VERDIN_GITHUB_TOKEN")
    if not token:
        log("ERRO: VERDIN_GITHUB_TOKEN não encontrado. Defina essa variável no arquivo .env.")
        sys.exit(1)

    repo_path = os.getenv("VERDIN_REPO_PATH")
    if not repo_path:
        log("ERRO: VERDIN_REPO_PATH não encontrado. Defina essa variável no arquivo .env.")
        sys.exit(1)

    return {
        "token": token,
        "repo_path": repo_path,
        "branch": os.getenv("VERDIN_BRANCH", "main"),
        "commit_msg": os.getenv("VERDIN_COMMIT_MSG", "chore: daily update - {date}"),
    }
