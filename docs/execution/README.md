# Como executar o BlendES Flow

Este é o runbook principal para instalar, iniciar, parar e preparar o projeto
para produção. Todos os comandos partem da raiz do repositório.

## Escolha do modo

| Objetivo | Comando principal | URL |
|---|---|---|
| Desenvolver sem Docker | `python scripts/project.py dev` | `http://localhost:5173` |
| Desenvolver com Docker | `docker compose up` | `http://localhost:5173` |
| Testar imagens sem reload | `docker compose -f compose.yaml up --build` | `http://localhost` |
| Produção | Imagens + TLS + settings `production` | Domínio HTTPS |

O projeto possui um único arquivo real de configuração: `.env`, na raiz.
Arquivos `backend/.env` e `frontend/.env` não são utilizados.

## Requisitos gerais

- Git;
- Python 3.14;
- Poetry 2.4 ou superior;
- Node.js 24 e npm;
- Docker Desktop/Engine e Docker Compose atual, para os modos Docker.

Verifique:

```powershell
git --version
python --version
poetry --version
node --version
npm --version
docker compose version
```

## 1. Desenvolvimento local, sem Docker

Esse modo usa Django com SQLite e Vite com hot reload. É o caminho mais rápido
para trabalhar no código.

### Primeira instalação

```powershell
git clone <url-do-repositorio>
cd blendes_flow
python scripts/project.py setup
```

O comando executa:

1. cria `.env` com credenciais locais fortes, caso ainda não exista;
2. instala dependências Python com Poetry;
3. instala dependências frontend com `npm ci`;
4. aplica migrations no SQLite local.

O `.env` é ignorado pelo Git. `bootstrap_env.py` nunca sobrescreve um arquivo
existente.

### Iniciar frontend e backend juntos

```powershell
python scripts/project.py dev
```

Serviços:

- frontend: `http://localhost:5173`;
- API: `http://127.0.0.1:8000`;
- Swagger: `http://127.0.0.1:8000/api/docs/`;
- Admin Django: `http://127.0.0.1:8000/admin/`.

Vue/TypeScript/CSS usam HMR. Django usa o autoreload do `runserver`.

Para encerrar os dois processos, pressione `Ctrl+C`.

### Executar separadamente

Backend:

```powershell
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Frontend, em outro terminal:

```powershell
cd frontend
npm ci
npm run dev
```

### Rotina local

```powershell
# Testes backend
python scripts/project.py test

# Checks Django e TypeScript
python scripts/project.py check

# Criar migration
cd backend
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## 2. Desenvolvimento com Docker

Esse modo usa PostgreSQL, backend em Gunicorn com reload e frontend em Vite com
HMR. `compose.override.yaml` é carregado automaticamente.

### Primeira execução

Inicie o Docker Desktop e aguarde o engine ficar pronto. Depois:

```powershell
python scripts/project.py dev-docker
```

O comando verifica o Docker Engine, garante a existência de `.env`, constrói as
imagens e inicia os serviços.

URLs:

- frontend Vite: `http://localhost:5173`;
- API publicada: `http://127.0.0.1:8000`;
- Swagger: `http://127.0.0.1:8000/api/docs/`.

O Nginx não é iniciado no modo padrão de desenvolvimento. Por isso
`http://localhost` na porta 80 não é a URL desse modo.

### Demais execuções

Depois que as imagens já existem:

```powershell
docker compose up
```

Em segundo plano:

```powershell
docker compose up --detach
```

Alterações comuns em Python, Vue, TypeScript e CSS não exigem rebuild.

Reconstrua quando mudar Dockerfile ou dependências:

```powershell
docker compose up --build
```

Depois de alterar `.env`, recrie os containers:

```powershell
docker compose up --detach --force-recreate
```

### Comandos Docker úteis

```powershell
# Estado
docker compose ps

# Todos os logs
docker compose logs --follow

# Logs por serviço
docker compose logs --follow backend
docker compose logs --follow frontend
docker compose logs --follow database

# Shell Django
docker compose exec backend python manage.py shell

# Migrations
docker compose exec backend python manage.py migrate

# Parar sem remover
docker compose stop

# Remover containers e preservar volumes
docker compose down
```

Não use `docker compose down --volumes` se quiser preservar o PostgreSQL local.

## 3. Teste integrado sem hot reload

Para testar as imagens imutáveis de backend, frontend e Nginx:

```powershell
docker compose -f compose.yaml up --build --detach
```

Acesse:

```text
http://localhost
```

Nesse modo:

- `compose.override.yaml` não é carregado;
- Vite gera `dist/` durante o build;
- Nginx serve o frontend e encaminha `/api/` ao Django;
- Gunicorn roda sem `--reload`;
- o código-fonte não é montado nos containers.

O `.env` de desenvolvimento seleciona `configuration.settings.docker`.
Portanto, esse fluxo simula uma execução imutável, mas não é um deploy de
produção.

Para voltar ao modo com hot reload:

```powershell
docker compose -f compose.yaml down
docker compose up
```

## 4. Preparação para produção

Produção usa o mesmo nome `.env`, mas seu conteúdo deve partir do modelo
específico. Faça backup do arquivo de desenvolvimento antes de substituí-lo.

```powershell
Copy-Item .env .env.development.backup
Copy-Item .env.production.example .env
```

Edite `.env` e substitua todos os placeholders.

### Valores obrigatórios

```env
DJANGO_SETTINGS_MODULE=configuration.settings.production
DJANGO_SECRET_KEY=<valor-aleatorio-com-50-ou-mais-caracteres>
JWT_SIGNING_KEY=<outro-valor-aleatorio-com-32-ou-mais-bytes>

DJANGO_ALLOWED_HOSTS=app.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://app.example.com
DJANGO_CORS_ALLOWED_ORIGINS=https://app.example.com

POSTGRES_DB=blendesflow
POSTGRES_USER=blendesflow
POSTGRES_PASSWORD=<senha-forte>
POSTGRES_HOST=<host-do-postgresql>
POSTGRES_PORT=5432
```

As chaves Django e JWT devem ser diferentes. Não versione `.env`.

### OAuth Google

Se utilizado:

```env
GOOGLE_OAUTH_CLIENT_ID=<client-id-publico>
GOOGLE_ALLOWED_HOSTED_DOMAIN=example.com
```

O mesmo client ID é incorporado no frontend durante o build. Secrets OAuth não
devem ser colocados em variáveis Vite ou no bundle.

### Validar settings

Com as dependências locais instaladas:

```powershell
$env:DJANGO_SETTINGS_MODULE="configuration.settings.production"
poetry --directory backend run python backend/manage.py check --deploy
```

O startup falha deliberadamente se encontrar chaves fracas, SQLite, senha de
banco fraca, host curinga, origens HTTP ou HSTS desabilitado.

### TLS é obrigatório

O `compose.yaml` atual publica Nginx apenas em HTTP local e sua configuração
não instala certificados. Ele não deve ser promovido diretamente para a
internet como está.

Antes do deploy, escolha uma das opções:

1. terminar TLS em um load balancer/ingress da plataforma e encaminhar
   corretamente `X-Forwarded-Proto: https`;
2. adicionar certificados e `listen 443 ssl` ao Nginx de produção;
3. usar uma plataforma que forneça HTTPS gerenciado.

Confirme também que apenas o proxy pode acessar Gunicorn e PostgreSQL. Nunca
publique a porta `5432` na internet.

### Banco, migrations e estáticos

Antes de liberar tráfego:

```powershell
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

O entrypoint atual executa esses comandos ao iniciar. Em um ambiente com várias
réplicas, prefira uma release job única para migrations, evitando concorrência
entre containers.

Tenha backup validado do PostgreSQL antes de migrations destrutivas.

### Checklist antes de publicar

- `.env` não está versionado;
- `DEBUG=False`;
- `DJANGO_SETTINGS_MODULE=configuration.settings.production`;
- `check --deploy` sem erros;
- TLS ativo e redirecionamento HTTPS testado;
- cookies `Secure` presentes;
- CORS e CSRF limitados aos domínios reais;
- banco não publicado externamente;
- backup e restauração testados;
- migrations executadas uma única vez;
- imagens construídas a partir do lockfile;
- logs e health checks monitorados;
- plano de rollback definido.

## Restaurar o ambiente de desenvolvimento

Se `.env` foi substituído para testar produção:

```powershell
Move-Item -Force .env.development.backup .env
docker compose up --detach --force-recreate
```

## Troubleshooting rápido

### `dockerDesktopLinuxEngine` não encontrado

Abra o Docker Desktop e aguarde o engine iniciar. Confirme com `docker info`.

### `http://localhost` não responde no desenvolvimento

Use `http://localhost:5173`. A porta 80 pertence ao modo integrado com Nginx.

### Google OAuth não aparece

Preencha `GOOGLE_OAUTH_CLIENT_ID` no `.env` raiz e recrie/reconstrua os serviços.

### Variável do `.env` não mudou

Variáveis são lidas ao criar processos/containers:

```powershell
docker compose up --detach --force-recreate
```

Para valores incorporados pelo Vite, também reconstrua a imagem:

```powershell
docker compose -f compose.yaml up --build --detach
```
