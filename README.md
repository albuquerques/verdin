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

O objetivo é garantir que o script rode uma vez por dia, independentemente do horário em que o computador for ligado. Se o horário agendado for perdido (PC estava desligado), o script deve executar assim que o computador ligar.

### Windows (Task Scheduler)

1. Abra o **Agendador de Tarefas** (`taskschd.msc`)
2. Clique em **Criar Tarefa Básica**
3. Dê um nome (ex: `Verdin`) e clique em **Avançar**
4. Escolha **Diariamente** e defina um horário de referência (ex: `09:00`)
5. Escolha **Iniciar um programa**
6. Em **Programa/script**, coloque o caminho do Python (ex: `C:\Users\SeuUsuario\AppData\Local\Python\bin\python.exe`)
7. Em **Adicionar argumentos**, coloque o caminho do script (ex: `C:\caminho\para\verdin\main.py`)
8. Clique em **Concluir**
9. Clique com o botão direito na tarefa criada e escolha **Propriedades**
10. Vá na aba **Configurações**
11. Marque a opção **"Executar a tarefa o mais cedo possível se uma execução agendada for perdida"**
12. Clique em **OK**

Com isso, o script roda no horário agendado se o PC já estiver ligado, ou assim que o PC ligar caso o horário tenha passado.

### Linux (anacron)

O `anacron` é a ferramenta ideal para este caso — diferente do `cron`, ele executa tarefas perdidas assim que o sistema iniciar.

Crie um script executável em `/etc/cron.daily/`:

```bash
sudo nano /etc/cron.daily/verdin
```

Cole o conteúdo abaixo, substituindo os caminhos reais:

```bash
#!/bin/bash
/usr/bin/python3 /caminho/para/verdin/main.py >> /caminho/para/verdin/cron.log 2>&1
```

Torne o arquivo executável:

```bash
sudo chmod +x /etc/cron.daily/verdin
```

O `anacron` vai garantir que o script rode uma vez por dia, mesmo que o computador tenha ficado desligado.

### macOS (launchd)

O `launchd` é o agendador nativo do macOS e suporta execução ao iniciar o sistema caso a tarefa tenha sido perdida.

Crie o arquivo de configuração:

```bash
nano ~/Library/LaunchAgents/com.verdin.daily.plist
```

Cole o conteúdo abaixo, substituindo os caminhos reais:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.verdin.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/caminho/para/verdin/main.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/caminho/para/verdin/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/caminho/para/verdin/launchd.log</string>
</dict>
</plist>
```

Registre o agente:

```bash
launchctl load ~/Library/LaunchAgents/com.verdin.daily.plist
```

A chave `RunAtLoad` garante que o script rode assim que o sistema iniciar caso o horário agendado tenha sido perdido.

---

## Segurança

- **Nunca commite o arquivo `.env`** — ele contém seu token e já está protegido pelo `.gitignore`.
- O token nunca é salvo em nenhum arquivo nem aparece no histórico de commits — ele é injetado temporariamente apenas na URL do push.
- Se o token for exposto acidentalmente, [revogue-o imediatamente no GitHub](https://github.com/settings/tokens) e gere um novo.
