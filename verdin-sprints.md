# Verdin — Plano de Desenvolvimento por Sprints

> Documento interno de execução. Cada sprint lista tarefas concretas, arquivos a criar/editar, comportamentos esperados e critérios de conclusão. Seguir na ordem indicada.

---

## Sprint 0 — Scaffolding do Projeto

**Objetivo:** Criar a estrutura de arquivos base do projeto antes de qualquer lógica.

**Tarefas:**

1. Criar o diretório raiz `verdin/`
2. Criar `verdin/.gitignore` com as seguintes entradas:
   - `.env`
   - `__pycache__/`
   - `*.pyc`
   - `*.pyo`
   - `.DS_Store`
3. Criar `verdin/.env.example` com as variáveis sem valores reais:
   ```
   VERDIN_GITHUB_TOKEN=your_pat_here
   VERDIN_REPO_PATH=/absolute/path/to/your/repo
   VERDIN_BRANCH=main
   VERDIN_COMMIT_MSG=chore: daily update - {date}
   ```
4. Criar `verdin/verdin.py` vazio (apenas um comentário de cabeçalho e `pass`)
5. Criar `verdin/README.md` com título e seção de "em construção"
6. Criar `verdin/REQUIREMENTS.md` (copiar o documento de requisitos original)

**Critério de conclusão:** Estrutura de pastas e arquivos existe conforme seção 5 do REQUIREMENTS.md. Nenhum arquivo sensível está fora do `.gitignore`.

---

## Sprint 1 — Leitura de Configuração e Validação de Ambiente

**Objetivo:** Implementar o carregamento seguro das variáveis de ambiente e validar que tudo necessário está presente antes de qualquer ação.

**Arquivo principal:** `verdin/verdin.py`

**Tarefas:**

1. Instalar dependência `python-dotenv` (única dependência externa permitida) — registrar no topo do script com instrução de instalação via comentário.
2. Implementar função `load_config()` que:
   - Tenta carregar `.env` do diretório do script via `dotenv`
   - Lê `VERDIN_GITHUB_TOKEN` — obrigatória; se ausente, imprime erro descritivo e encerra com `sys.exit(1)`
   - Lê `VERDIN_REPO_PATH` — obrigatória; se ausente, encerra com `sys.exit(1)`
   - Lê `VERDIN_BRANCH` — opcional, padrão `"main"`
   - Lê `VERDIN_COMMIT_MSG` — opcional, padrão `"chore: daily update - {date}"`
   - Retorna um dicionário `config` com todos os valores
3. Implementar função `log(msg)` que imprime `[VERDIN][YYYY-MM-DD HH:MM:SS] <msg>` no stdout.
4. No `__main__`, chamar `load_config()` e `log()` confirmando que a config foi carregada.

**Critério de conclusão:**
- Executar sem `.env` → imprime erro claro e sai com código `1`.
- Executar com `.env` válido → imprime confirmação de config carregada e sai com código `0`.

---

## Sprint 2 — Verificação de Idempotência (Commit Já Existe Hoje?)

**Objetivo:** Antes de criar qualquer commit, checar se já existe um commit no repositório feito hoje. Se sim, encerrar sem erros.

**Arquivo principal:** `verdin/verdin.py`

**Tarefas:**

1. Implementar função `already_committed_today(repo_path, branch)` que:
   - Usa `subprocess.run` para executar `git log` no `repo_path` com formato de data
   - Comando sugerido: `git log --after="YYYY-MM-DD 00:00:00" --before="YYYY-MM-DD 23:59:59" --oneline --no-walk=unsorted HEAD`
   - Alternativa mais simples: `git log -1 --format=%cd --date=short` e comparar com `date.today().isoformat()`
   - Retorna `True` se já há commit hoje, `False` caso contrário
   - Em caso de erro no comando git (ex: diretório inválido), lança exceção com mensagem clara
2. No fluxo principal:
   - Após `load_config()`, chamar `already_committed_today()`
   - Se `True`: `log("Commit já realizado hoje. Nada a fazer.")` e `sys.exit(0)`
   - Se `False`: prosseguir para próximo sprint

**Critério de conclusão:**
- Executar em repo com commit de hoje → mensagem de "nada a fazer" e saída 0.
- Executar em repo sem commit hoje → prossegue (pode falhar nas próximas etapas, ok por ora).

---

## Sprint 3 — Geração do Conteúdo do Commit

**Objetivo:** Criar ou atualizar o arquivo de log que será commitado, garantindo que cada execução produza uma mudança real no repositório.

**Arquivo principal:** `verdin/verdin.py`

**Tarefas:**

1. Implementar função `update_log_file(repo_path)` que:
   - Define o caminho do arquivo como `<repo_path>/verdin-log.txt`
   - Abre o arquivo em modo append (`"a"`)
   - Escreve uma linha com timestamp completo: `[YYYY-MM-DD HH:MM:SS] Verdin daily update\n`
   - Fecha o arquivo
   - Retorna o caminho relativo do arquivo (ex: `"verdin-log.txt"`) para uso no `git add`
2. Garantir que a função funciona mesmo se o arquivo não existir (primeira execução).

**Critério de conclusão:**
- Após a função executar, `verdin-log.txt` existe no repo_path com ao menos uma linha de timestamp.
- Executar duas vezes adiciona duas linhas distintas (não sobrescreve).

---

## Sprint 4 — Execução do Commit e Push via Git

**Objetivo:** Fazer o `git add`, `git commit` e `git push` usando subprocess, autenticando com o PAT via URL remota.

**Arquivo principal:** `verdin/verdin.py`

**Tarefas:**

1. Implementar função `run_git(args, cwd, env=None)` que:
   - Executa `subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, env=env)`
   - Se `returncode != 0`, lança `RuntimeError` com stderr como mensagem
   - Retorna o stdout
2. Implementar função `commit_and_push(config, file_to_add)` que:
   - Monta a mensagem de commit: substitui `{date}` em `VERDIN_COMMIT_MSG` com `date.today().isoformat()`
   - Executa `git add <file_to_add>`
   - Executa `git commit -m "<mensagem>"`
   - Obtém a URL remota atual via `git remote get-url origin`
   - Injeta o token na URL: transforma `https://github.com/user/repo.git` em `https://<TOKEN>@github.com/user/repo.git`
   - Executa `git push <url_com_token> <branch>` — **sem salvar a URL com token em lugar nenhum**
   - Após push bem-sucedido, restaura a remote para a URL original (sem token) — opcional mas recomendado
3. **Segurança:** O token nunca deve aparecer em logs. Mascarar em qualquer mensagem de erro antes de logar.

**Critério de conclusão:**
- Executar o script em um repo real cria um commit e aparece no `git log`.
- O token não aparece em nenhuma saída de log.
- Falha de push (token inválido) loga erro mascarado e encerra com código `1`.

---

## Sprint 5 — Tratamento de Erros e Códigos de Saída

**Objetivo:** Garantir que qualquer falha seja capturada, logada e resulte em código de saída correto, sem deixar arquivos corrompidos ou estado inconsistente.

**Arquivo principal:** `verdin/verdin.py`

**Tarefas:**

1. Envolver o fluxo principal em `try/except` global:
   ```python
   try:
       main()
   except Exception as e:
       log(f"ERRO: {e}")
       sys.exit(1)
   ```
2. Tratar especificamente:
   - `FileNotFoundError` ao acessar `repo_path` → mensagem: "Caminho do repositório não encontrado: ..."
   - `RuntimeError` do `run_git()` → mensagem do git (com token mascarado)
   - Qualquer outro `Exception` → mensagem genérica + tipo do erro
3. Garantir que se `update_log_file` falhar após ter escrito parcialmente, o arquivo não fique corrompido (usar try/except local e apagar linha parcial se necessário — ou simplesmente aceitar append como safe por natureza).
4. Verificar que `sys.exit(1)` é chamado em todos os caminhos de erro.
5. Verificar que `sys.exit(0)` é chamado explicitamente no caminho de sucesso.

**Critério de conclusão:**
- Sem internet: erro descritivo, saída 1.
- Token inválido: erro descritivo (sem expor token), saída 1.
- `repo_path` inválido: erro descritivo, saída 1.
- Sucesso: log de confirmação, saída 0.

---

## Sprint 6 — Documentação e README Final

**Objetivo:** Escrever o README completo com instruções de instalação, configuração e agendamento via cron/Task Scheduler.

**Arquivo principal:** `verdin/README.md`

**Tarefas:**

1. Seção **Visão Geral** — o que o Verdin faz em 2-3 linhas.
2. Seção **Pré-requisitos**:
   - Python 3.8+
   - `git` instalado e configurado com nome/email (`git config user.name` e `git config user.email`)
   - Repositório GitHub já existente e clonado localmente
   - Personal Access Token (PAT) com permissão `repo`
3. Seção **Instalação**:
   ```bash
   git clone <este-repo>
   cd verdin
   pip install python-dotenv
   cp .env.example .env
   # editar .env com seus valores reais
   ```
4. Seção **Configuração** — tabela com as 4 variáveis de ambiente (igual ao REQUIREMENTS.md).
5. Seção **Uso manual**:
   ```bash
   python verdin.py
   ```
6. Seção **Agendamento**:
   - **Linux/macOS (cron):**
     ```
     0 9 * * * /usr/bin/python3 /caminho/para/verdin/verdin.py >> /caminho/para/verdin/cron.log 2>&1
     ```
     Instruções para `crontab -e`.
   - **Windows (Task Scheduler):** passos resumidos para criar tarefa diária apontando para `python verdin.py`.
7. Seção **Segurança** — lembrete de nunca commitar o `.env`.

**Critério de conclusão:** README completo, claro, permite que um novo usuário configure e rode o Verdin do zero sem consultar outro documento.

---

## Sprint 7 — Testes Manuais e Validação dos Critérios de Aceitação

**Objetivo:** Executar cada critério de aceitação do REQUIREMENTS.md e confirmar que todos passam.

**Checklist a executar manualmente:**

- [ ] Executar o script uma vez → confirmar que exatamente um commit aparece no `git log`
- [ ] Verificar que o commit aparece no gráfico de contribuições do GitHub (pode levar alguns minutos)
- [ ] Executar o script uma segunda vez no mesmo dia → confirmar mensagem "nada a fazer" e zero commits adicionais
- [ ] Remover `VERDIN_GITHUB_TOKEN` do `.env` → confirmar erro descritivo e saída com código `1`
- [ ] Verificar `echo $?` após cada execução para confirmar os códigos de saída
- [ ] Conferir `git log --all` para garantir que nenhum token aparece em mensagens de commit ou metadados
- [ ] Configurar entrada de cron de teste (ex: 1 minuto no futuro) → confirmar que executa automaticamente sem intervenção

**Critério de conclusão:** Todos os 6 itens do checklist passam. Projeto considerado funcional.

---

## Resumo das Sprints

| Sprint | Entregável Principal | Dependência |
|--------|---------------------|-------------|
| 0 | Estrutura de arquivos | — |
| 1 | Leitura de config + logs | Sprint 0 |
| 2 | Verificação de idempotência | Sprint 1 |
| 3 | Geração do arquivo de log | Sprint 1 |
| 4 | Commit + Push autenticado | Sprints 2 e 3 |
| 5 | Tratamento de erros robusto | Sprint 4 |
| 6 | README e documentação | Sprint 5 |
| 7 | Validação final | Sprint 6 |

---

*Documento gerado para execução autônoma. Seguir a ordem das sprints. Não pular etapas.*
