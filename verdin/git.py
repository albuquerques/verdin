import subprocess
from datetime import date


def run_git(args, cwd, env=None):
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def already_committed_today(repo_path, branch):
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=short"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Falha ao ler git log em '{repo_path}': {result.stderr.strip()}")

    last_commit_date = result.stdout.strip()
    return last_commit_date == date.today().isoformat()


def commit_and_push(config, file_to_add):
    repo_path = config["repo_path"]
    branch = config["branch"]
    token = config["token"]
    commit_msg = config["commit_msg"].replace("{date}", date.today().isoformat())

    run_git(["add", file_to_add], cwd=repo_path)
    run_git(["commit", "-m", commit_msg], cwd=repo_path)

    remote_url = run_git(["remote", "get-url", "origin"], cwd=repo_path)

    # Injeta o token na URL sem persistir em nenhum arquivo
    if "https://" in remote_url:
        auth_url = remote_url.replace("https://", f"https://{token}@")
    else:
        raise RuntimeError("A URL remota não usa HTTPS. Autenticação via token não suportada.")

    try:
        run_git(["push", auth_url, branch], cwd=repo_path)
    except RuntimeError as e:
        # Mascara o token antes de propagar o erro
        raise RuntimeError(str(e).replace(token, "***")) from None
