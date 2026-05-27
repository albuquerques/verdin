from datetime import datetime
from pathlib import Path


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[VERDIN][{timestamp}] {msg}")


def update_log_file(repo_path):
    log_path = Path(repo_path) / "verdin-log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] Verdin daily update\n")

    return "verdin-log.txt"
