# Guia do frontend

O frontend usa Vue 3, TypeScript, Vite e npm. Ele compartilha o único `.env` da
raiz com o backend e o Docker Compose.

## Requisitos

- Node.js `^22.18.0` ou `>=24.12.0`;
- npm;
- Docker Compose atual, para containers.

```powershell
node --version
npm --version
```

## Configuração única

Não crie `.env` dentro de `frontend/`. O Vite possui `envDir` apontando para a
raiz e lê:

```text
/.env
```

Crie-o com:

```powershell
python scripts/bootstrap_env.py
```

A API possui defaults adequados:

- desenvolvimento: `http://127.0.0.1:8000/api`;
- build Nginx: `/api`.

OAuth Google usa a mesma chave do backend:

```env
GOOGLE_OAUTH_CLIENT_ID=seu-client-id.apps.googleusercontent.com
```

O Vite expõe somente esse identificador público como
`VITE_GOOGLE_OAUTH_CLIENT_ID` no bundle. Embora o Vite leia o arquivo raiz,
somente variáveis `VITE_*` e o client ID explicitamente mapeado ficam acessíveis
no navegador. Secrets Django, JWT e PostgreSQL não são expostos.

## Execução local

```powershell
cd frontend
npm ci
npm run dev
```

Acesse `http://localhost:5173`. Para executar frontend e backend juntos:

```powershell
python scripts/project.py setup
python scripts/project.py dev
```

## Docker com HMR

Primeira execução:

```powershell
python scripts/project.py dev-docker
```

Depois:

```powershell
docker compose up
```

O override monta `frontend/` somente para leitura, executa Vite na porta `5173`
e mantém `node_modules` em volume Linux separado. Alterações Vue, TypeScript,
CSS e assets usam HMR e não exigem build.

Reconstrua quando mudar `package.json`, `package-lock.json` ou Dockerfile:

```powershell
docker compose up --build
```

Depois de alterar `.env`, reinicie o frontend e recrie o backend:

```powershell
docker compose restart frontend
docker compose up --detach --force-recreate backend
```

## Imagem integrada sem HMR

```powershell
docker compose -f compose.yaml up --build --detach
```

Acesse `http://localhost`. O Vite compila os assets no build e o Nginx os serve
sem observar arquivos. O client ID Google é encaminhado como build argument
público; chaves privadas não são passadas ao build do frontend.

## Comandos úteis

Dentro de `frontend/`:

| Comando | Finalidade |
|---|---|
| `npm ci` | Instalar exatamente o lockfile |
| `npm run dev` | Iniciar Vite com HMR |
| `npm run type-check` | Verificar TypeScript/Vue |
| `npm run build` | Type-check e build |
| `npm run build-only` | Build sem type-check |
| `npm run preview` | Visualizar `dist/` |
| `npm run lint` | Executar linters |
| `npm run format` | Formatar `src/` |
| `npm run api:types` | Regerar tipos OpenAPI |

Docker:

```powershell
docker compose logs --follow frontend
docker compose restart frontend
docker compose ps
docker compose down
```

## Problemas comuns

### API indisponível

Confirme `http://127.0.0.1:8000` e consulte os logs do backend.

### CORS no navegador

O `.env.example` libera `localhost:5173` e `127.0.0.1:5173`. Se o `.env` foi
criado manualmente, confirme essas origens e recrie o backend.

### Google não configurado

Preencha `GOOGLE_OAUTH_CLIENT_ID` no `.env` raiz e reinicie/reconstrua conforme o
modo. Não crie uma segunda chave no diretório frontend.
