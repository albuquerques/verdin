# Verdin — Progresso de Desenvolvimento

**Sprints concluídas:** 6 / 8  
**Progresso:** ████████████░░░░ 75%

---

| Sprint | Descrição                              | Status |
|--------|----------------------------------------|--------|
| 0      | Scaffolding do projeto                 | ✅ Concluída |
| 1      | Leitura de config e validação          | ✅ Concluída |
| 2      | Verificação de idempotência            | ✅ Concluída |
| 3      | Geração do conteúdo do commit          | ✅ Concluída |
| 4      | Commit e push via Git                  | ✅ Concluída |
| 5      | Tratamento de erros e códigos de saída | ✅ Concluída |
| 6      | Documentação e README final            | ✅ Concluída |
| 7      | Testes manuais e validação final       | ⬜ Pendente |

---

## Histórico

- **2026-05-27** — Sprint 0 concluída: estrutura de arquivos criada (`verdin.py`, `.gitignore`, `.env.example`, `README.md`, `REQUIREMENTS.md`).
- **2026-05-27** — Sprint 1 concluída: `load_config()` em `config.py`, `log()` em `log.py`, fluxo inicial em `main.py`.
- **2026-05-27** — Sprint 2 concluída: `already_committed_today()` em `git.py`, checagem de idempotência integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 3 concluída: `update_log_file()` em `log.py`, criação/atualização do `verdin-log.txt` em modo append integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 4 concluída: `run_git()` e `commit_and_push()` em `git.py`, autenticação via token injetado na URL, mascaramento do token em erros.
- **2026-05-27** — Sprint 5 concluída: tratamento diferenciado de `FileNotFoundError`, `RuntimeError` e `Exception` genérica em `main.py`; `sys.exit(0)` explícito no caminho de sucesso.
- **2026-05-27** — Sprint 6 concluída: `README.md` completo com visão geral, pré-requisitos, instalação, configuração, uso manual, agendamento (cron e Task Scheduler) e segurança.
