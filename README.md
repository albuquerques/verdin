# Verdin

Verdin é um script Python que roda diariamente e cria um commit automático em um repositório GitHub dedicado, mantendo o gráfico de contribuições do seu perfil sempre ativo. Sem dashboards, sem configurações complexas — apenas um arquivo `.env` e um agendamento.

---

## Pré-requisitos

- Python 3.8 ou superior
- `git` instalado e configurado com nome e e-mail:
  ```bash
  git config --global user.name "Seu Nome"
  git config --global user.email "seu@email.com"
  ```
- Um repositório GitHub já existente e clonado localmente (será o alvo dos commits diários)
- Um [Personal Access Token (PAT)](https://github.com/settings/tokens) com permissão `repo`

---

## Instalação

```bash
git clone https://github.com/<seu-usuario>/verdin.git
cd verdin
pip install python-dotenv
cp .env.example .env
```

Abra o arquivo `.env` e preencha com seus valores reais (veja a seção Configuração abaixo).

---

## Configuração

Edite o arquivo `.env` com as variáveis abaixo:

| Variável               | Obrigatória | Descrição                                                              |
|------------------------|-------------|------------------------------------------------------------------------|
| `VERDIN_GITHUB_TOKEN`  | Sim         | Token de acesso pessoal do GitHub com permissão `repo`                 |
| `VERDIN_REPO_PATH`     | Sim         | Caminho absoluto local do repositório onde os commits serão feitos     |
| `VERDIN_BRANCH`        | Não         | Branch alvo (padrão: `main`)                                           |
| `VERDIN_COMMIT_MSG`    | Não         | Mensagem de commit (padrão: `chore: daily update - {date}`)            |

Exemplo de `.env` preenchido:

```env
VERDIN_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
VERDIN_REPO_PATH=C:\Users\Ricardo\Documents\meu-repo
VERDIN_BRANCH=main
VERDIN_COMMIT_MSG=chore: daily update - {date}
```

---

## Uso manual

```bash
python main.py
```

O script irá:
1. Verificar se já existe um commit hoje — se sim, encerra sem fazer nada.
2. Atualizar o arquivo `verdin-log.txt` no repositório alvo com um timestamp.
3. Criar um commit e fazer push para o GitHub.

---

## Agendamento

### Linux / macOS (cron)

Abra o editor de cron com:

```bash
crontab -e
```

Adicione a linha abaixo para executar todos os dias às 9h:

```
0 9 * * * /usr/bin/python3 /caminho/para/verdin/main.py >> /caminho/para/verdin/cron.log 2>&1
```

Substitua `/caminho/para/verdin/` pelo caminho real onde você clonou o Verdin.

### Windows (Task Scheduler)

1. Abra o **Agendador de Tarefas** (`taskschd.msc`)
2. Clique em **Criar Tarefa Básica**
3. Dê um nome (ex: `Verdin`) e clique em **Avançar**
4. Escolha **Diariamente** e defina o horário desejado
5. Escolha **Iniciar um programa**
6. Em **Programa/script**, coloque o caminho do Python (ex: `C:\Python312\python.exe`)
7. Em **Adicionar argumentos**, coloque o caminho do script (ex: `C:\Users\Ricardo\verdin\main.py`)
8. Clique em **Concluir**

---

## Segurança

- **Nunca commite o arquivo `.env`** — ele contém seu token e já está protegido pelo `.gitignore`.
- O token nunca é salvo em nenhum arquivo nem aparece no histórico de commits — ele é injetado temporariamente apenas na URL do push.
- Se o token for exposto acidentalmente, [revogue-o imediatamente no GitHub](https://github.com/settings/tokens) e gere um novo.
