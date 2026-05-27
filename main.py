import sys

from verdin.config import load_config
from verdin.git import already_committed_today, commit_and_push
from verdin.log import log, update_log_file


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERRO: {e}")
        sys.exit(1)
