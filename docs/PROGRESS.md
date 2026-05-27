# Verdin — Progresso de Desenvolvimento

**Sprints concluídas:** 4 / 8  
**Progresso:** ████████████████ 50%

---

| Sprint | Descrição                              | Status |
|--------|----------------------------------------|--------|
| 0      | Scaffolding do projeto                 | ✅ Concluída |
| 1      | Leitura de config e validação          | ✅ Concluída |
| 2      | Verificação de idempotência            | ✅ Concluída |
| 3      | Geração do conteúdo do commit          | ✅ Concluída |
| 4      | Commit e push via Git                  | ✅ Concluída |
| 5      | Tratamento de erros e códigos de saída | ⬜ Pendente |
| 6      | Documentação e README final            | ⬜ Pendente |
| 7      | Testes manuais e validação final       | ⬜ Pendente |

---

## Histórico

- **2026-05-27** — Sprint 0 concluída: estrutura de arquivos criada (`verdin.py`, `.gitignore`, `.env.example`, `README.md`, `REQUIREMENTS.md`).
- **2026-05-27** — Sprint 1 concluída: `load_config()` em `config.py`, `log()` em `log.py`, fluxo inicial em `main.py`.
- **2026-05-27** — Sprint 2 concluída: `already_committed_today()` em `git.py`, checagem de idempotência integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 3 concluída: `update_log_file()` em `log.py`, criação/atualização do `verdin-log.txt` em modo append integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 4 concluída: `run_git()` e `commit_and_push()` em `git.py`, autenticação via token injetado na URL, mascaramento do token em erros.
