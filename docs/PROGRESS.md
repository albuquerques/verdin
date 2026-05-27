# Verdin — Progresso de Desenvolvimento

**Sprints concluídas:** 8 / 8  
**Progresso:** ████████████████ 100% ✅

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
| 7      | Testes manuais e validação final       | ✅ Concluída |

---

## Histórico

- **2026-05-27** — Sprint 0 concluída: estrutura de arquivos criada (`verdin.py`, `.gitignore`, `.env.example`, `README.md`, `REQUIREMENTS.md`).
- **2026-05-27** — Sprint 1 concluída: `load_config()` em `config.py`, `log()` em `log.py`, fluxo inicial em `main.py`.
- **2026-05-27** — Sprint 2 concluída: `already_committed_today()` em `git.py`, checagem de idempotência integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 3 concluída: `update_log_file()` em `log.py`, criação/atualização do `verdin-log.txt` em modo append integrada ao fluxo em `main.py`.
- **2026-05-27** — Sprint 4 concluída: `run_git()` e `commit_and_push()` em `git.py`, autenticação via token injetado na URL, mascaramento do token em erros.
- **2026-05-27** — Sprint 5 concluída: tratamento diferenciado de `FileNotFoundError`, `RuntimeError` e `Exception` genérica em `main.py`; `sys.exit(0)` explícito no caminho de sucesso.
- **2026-05-27** — Sprint 6 concluída: `README.md` completo com visão geral, pré-requisitos, instalação, configuração, uso manual, agendamento (cron e Task Scheduler) e segurança.
- **2026-05-27** — Sprint 7 concluída: revisão de código contra todos os critérios de aceitação; correção de inconsistência de `print()` → `log()` em `config.py`; histórico git verificado sem exposição de token. Projeto funcional.

---

## Critérios de Aceitação — Resultado da Revisão

| Critério | Como foi validado | Resultado |
|---|---|---|
| Script cria exatamente um commit | Revisão do fluxo `update_log_file → git add → git commit → git push` | ✅ Aprovado por revisão |
| Commit aparece no gráfico do GitHub | Depende de execução real com credenciais | 🔲 Verificar manualmente |
| Executar duas vezes no mesmo dia não duplica commit | `already_committed_today()` compara data do último commit com hoje | ✅ Aprovado por revisão |
| Token ausente retorna erro descritivo e saída 1 | `load_config()` checa token e chama `sys.exit(1)` | ✅ Aprovado por revisão |
| Pode ser agendado sem intervenção manual | Sem input interativo; README documenta cron e Task Scheduler | ✅ Aprovado por revisão |
| Nenhum token no histórico de commits | `git log --all -p` varrido — apenas referências de código e docs | ✅ Verificado via git |
