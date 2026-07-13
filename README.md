# BlendES Flow

Aplicação Django REST Framework + Vue com configuração centralizada em um
único arquivo `.env` na raiz.

## Primeira execução

Requisitos: Python 3.14, Poetry 2.4+, Node.js 24, npm e Docker Compose atual.

```powershell
python scripts/project.py setup
python scripts/project.py dev
```

O setup cria `.env` automaticamente, instala dependências e aplica migrations.
O frontend fica em `http://localhost:5173` e a API em
`http://127.0.0.1:8000`.

## Docker de desenvolvimento

```powershell
python scripts/project.py dev-docker
```

Depois do primeiro build, normalmente basta:

```powershell
docker compose up
```

O Compose carrega automaticamente `compose.override.yaml`, habilitando hot
reload do backend e HMR do Vite. Acesse `http://localhost:5173`.

Para testar a imagem integrada sem reload:

```powershell
docker compose -f compose.yaml up --build
```

Acesse `http://localhost`.

## Arquivo de ambiente único

Existe somente um arquivo real:

```text
.env
```

Ele é ignorado pelo Git e consumido pelo Django, Docker Compose e Vite. Os
modelos versionados são:

- `.env.example`: desenvolvimento;
- `.env.production.example`: produção.

Para recriar manualmente:

```powershell
Copy-Item .env.example .env
```

`python scripts/bootstrap_env.py` gera credenciais locais fortes e preserva o
arquivo quando ele já existe.

O client ID Google é configurado uma única vez:

```env
GOOGLE_OAUTH_CLIENT_ID=seu-client-id.apps.googleusercontent.com
```

O backend usa o valor diretamente e o Vite expõe somente esse identificador
público ao navegador. Nenhuma senha, JWT ou chave Django é incorporada no
frontend.

## Ambientes Django

- `local`: desenvolvimento nativo com SQLite;
- `docker`: Compose com PostgreSQL e Redis;
- `test`: testes com SQLite em memória;
- `production`: PostgreSQL, HTTPS, cookies seguros e validações estritas.

Os arquivos de settings guardam políticas, não credenciais. A seleção ocorre
pelo processo: `manage.py` usa `local`; o `.env` de desenvolvimento usa
`docker` dentro dos containers; o exemplo de produção seleciona `production`.

## Cache

No Docker, o Compose configura automaticamente o backend para usar o serviço
Redis interno (`redis://cache:6379/1`). O Redis não publica portas no host e os
dados são descartáveis: ele é cache, não armazenamento persistente.

Fora do Docker, deixe `CACHE_URL` vazio. O Django usa `LocMemCache`, portanto
`python scripts/project.py dev` não exige Redis. Para usar um Redis externo,
informe sua URL em `CACHE_URL`; `CACHE_DEFAULT_TIMEOUT` define o TTL padrão e
`CACHE_KEY_PREFIX` separa as chaves de cada ambiente.

## Documentação

- [Como executar e preparar produção](docs/execution/README.md)
- [Guia do frontend](docs/frontend/README.md)
- [Guia do backend](docs/backend/README.md)
