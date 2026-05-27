import sys

from verdin.config import load_config
from verdin.git import already_committed_today, commit_and_push
from verdin.log import log, update_log_file


def main():
    config = load_config()
    log("Configuração carregada com sucesso.")

    if already_committed_today(config["repo_path"], config["branch"]):
        log("Commit já realizado hoje. Nada a fazer.")
        sys.exit(0)

    file_to_add = update_log_file(config["repo_path"])
    log(f"Arquivo de log atualizado: {file_to_add}")

    commit_and_push(config, file_to_add)
    log("Commit e push realizados com sucesso.")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        log(f"ERRO: Caminho do repositório não encontrado: {e}")
        sys.exit(1)
    except RuntimeError as e:
        log(f"ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"ERRO inesperado ({type(e).__name__}): {e}")
        sys.exit(1)
