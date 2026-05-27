# Verdin — Documento de Requisitos

> Programa simples para manter o gráfico de contribuições do GitHub sempre verde, criando commits automáticos diariamente.

---

## 1. Visão Geral

O **Verdin** é um script autônomo que roda diariamente e realiza ao menos um commit em um repositório GitHub dedicado, garantindo que o gráfico de contribuições do usuário permaneça ativo. O foco é simplicidade: sem dashboards, sem configurações complexas, sem dependências pesadas.

---

## 2. Requisitos Funcionais

### RF-01 — Criação de commit diário
- O programa deve criar ao menos **um commit por dia** no repositório alvo.
- O commit deve ser válido e reconhecido pelo GitHub como contribuição (pushed para o branch padrão do repositório).

### RF-02 — Conteúdo do commit
- O conteúdo commitado deve ser algo que mude a cada execução para que o commit não seja vazio ou rejeitado.
- Sugestão de implementação: arquivo de log/texto com data e hora da execução, gerado ou atualizado automaticamente.
- A mensagem do commit deve ser gerada automaticamente (ex: `chore: daily update - YYYY-MM-DD`).

### RF-03 — Autenticação com o GitHub
- O programa deve autenticar-se no GitHub de forma segura para realizar o push.
- A autenticação deve utilizar um **token de acesso pessoal (PAT)** ou equivalente, lido a partir de variável de ambiente ou arquivo de configuração — nunca hardcoded no código.

### RF-04 — Execução automática diária
- O programa deve ser executável de forma agendada, sem intervenção manual.
- Deve ser compatível com **cron** (Linux/macOS) ou **Task Scheduler** (Windows).
- O intervalo padrão é uma execução por dia.

### RF-05 — Idempotência
- Caso o programa seja executado mais de uma vez no mesmo dia, ele não deve criar commits duplicados desnecessários ou gerar erros.
- O comportamento ideal é: já existe commit hoje → encerra sem erros.

---

## 3. Requisitos Não Funcionais

### RNF-01 — Leveza
- O programa não deve ter dependências pesadas. Deve ser executável em um ambiente mínimo (ex: Python puro com biblioteca `git` ou chamadas diretas de shell, ou Node.js com pacote mínimo).

### RNF-02 — Portabilidade
- Deve funcionar nos principais sistemas operacionais: Linux, macOS e Windows.

### RNF-03 — Segurança das credenciais
- Tokens e credenciais **jamais** devem ser escritos diretamente no código-fonte.
- Devem ser lidos via variável de ambiente (ex: `VERDIN_GITHUB_TOKEN`) ou arquivo `.env` ignorado pelo `.gitignore`.

### RNF-04 — Logs mínimos
- O programa deve registrar em console (stdout) ao menos:
  - Data/hora da execução.
  - Se o commit foi criado ou se já havia um commit no dia.
  - Qualquer erro que impeça o funcionamento.

### RNF-05 — Falha silenciosa controlada
- Em caso de falha (sem internet, token inválido, etc.), o programa deve encerrar com código de saída diferente de zero e registrar a causa do erro — sem travar o sistema ou deixar arquivos corrompidos.

---

## 4. Configuração

O programa deve suportar as seguintes configurações, preferencialmente via variáveis de ambiente ou arquivo `.env`:

| Variável | Obrigatória | Descrição |
|---|---|---|
| `VERDIN_GITHUB_TOKEN` | Sim | Token de acesso pessoal do GitHub com permissão de `repo` |
| `VERDIN_REPO_PATH` | Sim | Caminho local do repositório onde os commits serão feitos |
| `VERDIN_BRANCH` | Não | Branch alvo (padrão: `main`) |
| `VERDIN_COMMIT_MSG` | Não | Modelo de mensagem de commit (padrão: `chore: daily update - {date}`) |

---

## 5. Estrutura Esperada do Projeto

```
verdin/
├── verdin/               # Módulo Python principal
│   ├── __init__.py
│   ├── config.py         # Carregamento e validação das variáveis de ambiente
│   ├── git.py            # Operações git (subprocess, autenticação, push)
│   └── log.py            # Logger de console e escrita no arquivo de log
├── docs/
│   ├── REQUIREMENTS.md   # Este documento
│   └── verdin-sprints.md # Plano de desenvolvimento por sprints
├── main.py               # Ponto de entrada — orquestra o fluxo principal
├── .env.example          # Exemplo de variáveis de ambiente (sem valores reais)
├── .gitignore            # Deve ignorar .env e arquivos sensíveis
└── README.md             # Instruções de uso e configuração
```

---

## 6. Critérios de Aceitação

Para considerar o Verdin funcional, os seguintes critérios devem ser atendidos:

- [ ] Executar o script uma vez cria exatamente um commit no repositório configurado.
- [ ] O commit aparece no gráfico de contribuições do GitHub.
- [ ] Executar o script duas vezes no mesmo dia não cria commit duplicado.
- [ ] Remover o token da variável de ambiente e executar o script retorna erro descritivo e código de saída `1`.
- [ ] O script pode ser agendado via cron sem nenhuma intervenção manual após a configuração inicial.
- [ ] Nenhum token ou credencial aparece no histórico de commits.

---

## 7. Fora de Escopo

Os itens abaixo **não** fazem parte do Verdin e não devem ser implementados:

- Interface gráfica ou dashboard web.
- Suporte a múltiplos repositórios simultaneamente (na versão inicial).
- Geração de commits falsos com datas retroativas.
- Integração com outros serviços além do GitHub.

---

*Documento gerado na fase de planejamento. Deve ser atualizado conforme o projeto evolui.*
