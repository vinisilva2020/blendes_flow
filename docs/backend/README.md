# Guia do backend

O backend usa Python 3.14, Django 6, Django REST Framework, Poetry e PostgreSQL.
Toda configuração variável fica no único `.env` da raiz do repositório.

## Requisitos

- Python `>=3.14,<4`;
- Poetry 2.4+;
- Docker Compose atual, para o fluxo com containers.

```powershell
python --version
poetry --version
docker compose version
```

## Configuração

Na primeira execução:

```powershell
python scripts/bootstrap_env.py
```

Esse comando cria `.env` na raiz, gera chaves locais fortes e não sobrescreve
um arquivo existente. Não existem mais arquivos `.env` dentro de `backend/` nem
arquivos em `infrastructure/secrets/`.

Modelos disponíveis:

```text
.env.example               desenvolvimento
.env.production.example    produção
```

Variáveis relevantes incluem:

```env
DJANGO_SECRET_KEY=...
JWT_SIGNING_KEY=...
POSTGRES_DB=blendesflow
POSTGRES_USER=blendesflow
POSTGRES_PASSWORD=...
POSTGRES_HOST=database
GOOGLE_OAUTH_CLIENT_ID=...
```

O `.env` é ignorado pelo Git. Não coloque valores reais nos arquivos example.

## Ambientes Django

| Settings | Uso | Banco |
|---|---|---|
| `configuration.settings.local` | Execução nativa | SQLite |
| `configuration.settings.docker` | Docker local | PostgreSQL |
| `configuration.settings.test` | Testes | SQLite em memória |
| `configuration.settings.production` | Deploy | PostgreSQL |

Os settings contêm comportamento e validações, não credenciais.
`manage.py` seleciona `local` antes de carregar `.env`, portanto o valor Docker
do arquivo não interfere no desenvolvimento nativo. Containers recebem o mesmo
`.env` por `env_file`.

## Execução local

```powershell
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

URLs:

- API: `http://127.0.0.1:8000`;
- Admin: `http://127.0.0.1:8000/admin/`;
- OpenAPI: `http://127.0.0.1:8000/api/schema/`;
- Swagger: `http://127.0.0.1:8000/api/docs/`.

SQLite é usado por padrão. Para executar todo o projeto:

```powershell
python scripts/project.py setup
python scripts/project.py dev
```

## Docker com hot reload

Primeira execução:

```powershell
python scripts/project.py dev-docker
```

O comando verifica o Docker Engine, garante a existência de `.env` e executa
`docker compose up --build`. O override de desenvolvimento monta `backend/`
somente para leitura e configura Gunicorn com `--reload`.

Depois do primeiro build:

```powershell
docker compose up
```

Ou em segundo plano:

```powershell
docker compose up --detach
```

Alterações Python comuns recarregam o worker sem rebuild. Reconstrua quando
mudar Dockerfile, `pyproject.toml`, `poetry.lock` ou dependências:

```powershell
docker compose up --build
```

Depois de alterar `.env`, recrie os containers, pois hot reload não altera o
ambiente de um processo existente:

```powershell
docker compose up --detach --force-recreate
```

## Execução integrada sem reload

```powershell
docker compose -f compose.yaml up --build --detach
```

Esse comando ignora `compose.override.yaml`, usa Gunicorn sem reload e publica
Nginx em `http://localhost`. O `.env` de desenvolvimento ainda seleciona os
settings `docker`; trata-se de uma validação imutável local, não de um deploy.

## Produção

Crie o único arquivo real a partir do modelo:

```powershell
Copy-Item .env.production.example .env
```

Substitua todos os `change-me`. Os settings de produção rejeitam:

- SQLite;
- chaves fracas ou iguais;
- senha de banco fraca;
- host `*`;
- origens CORS/CSRF sem HTTPS;
- HSTS desativado.

Valide antes do deploy:

```powershell
$env:DJANGO_SETTINGS_MODULE="configuration.settings.production"
poetry --directory backend run python backend/manage.py check --deploy
```

O Compose recebe `.env` com `env_file`; valores sensíveis não ficam escritos no
YAML. Como variáveis de container podem ser vistas por administradores do
Docker, restrinja o acesso ao host e ao daemon.

## OAuth Google

Configure uma única chave no `.env`:

```env
GOOGLE_OAUTH_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_ALLOWED_HOSTED_DOMAIN=example.com
```

O Vite mapeia o mesmo client ID público para o frontend. Não é necessária uma
segunda variável `VITE_GOOGLE_OAUTH_CLIENT_ID`.

## Migrations, testes e comandos

```powershell
cd backend
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py showmigrations
poetry run python manage.py createsuperuser
poetry run python manage.py test --settings=configuration.settings.test
poetry run python manage.py check
```

Na raiz:

```powershell
python scripts/project.py test
python scripts/project.py check
```

Docker:

```powershell
docker compose ps
docker compose logs --follow backend
docker compose exec backend python manage.py shell
docker compose restart backend
docker compose stop
docker compose down
```

`docker compose down` preserva volumes. `down --volumes` remove o banco local.

## Problemas comuns

### Docker Engine indisponível

Abra o Docker Desktop e aguarde o engine iniciar:

```powershell
docker info
```

### Variável alterada não foi aplicada

```powershell
docker compose up --detach --force-recreate
```

### Banco não fica saudável

```powershell
docker compose logs database
docker compose ps
```

### Entrypoint não encontrado

Reconstrua a imagem. O repositório força `LF` e o Dockerfile normaliza scripts:

```powershell
docker compose build --no-cache backend
```
