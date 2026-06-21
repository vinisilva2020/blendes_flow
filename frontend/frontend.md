# Frontend

Documentacao operacional do cliente Vue do Blendes Flow.

## Visao geral

O frontend consome a API Django REST por meio de um contrato OpenAPI gerado pelo backend.

Fluxo principal:

```txt
Django REST
  -> schema OpenAPI
  -> src/shared/api/schema.yaml
  -> src/shared/api/schema.ts
  -> domains/*/contracts.ts
  -> domains/*/requests.ts
  -> domains/*/queries.ts
  -> views Vue
```

## Estrutura

```txt
src/
  assets/
  components/
  domains/
    auth/
      contracts.ts
      queries.ts
      requests.ts
    organizations/
      contracts.ts
      queries.ts
      requests.ts
  layouts/
  lib/
    http/
      access-token.ts
      client.ts
      errors.ts
    query/
      client.ts
      install.ts
  router/
  shared/
    api/
      schema.yaml
      schema.ts
  stores/
    authentication.ts
  views/
```

## Regras de organizacao

- `src/lib` centraliza integracoes third-party, como Axios e TanStack Query.
- `src/shared/api/schema.ts` e gerado automaticamente. Nao edite esse arquivo manualmente.
- `src/domains/*/contracts.ts` traduz o contrato OpenAPI para nomes de dominio usados pelo app.
- `src/domains/*/requests.ts` faz chamadas HTTP por dominio.
- `src/domains/*/queries.ts` expoe composables de TanStack Query para as telas.
- `src/views` orquestra dados, rotas e estados de tela.
- `src/components` deve continuar focado em UI reaproveitavel.
- Tokens de acesso ficam em memoria nesta etapa. Nao persistir JWT em `localStorage`.

## Variaveis de ambiente

Crie um arquivo `.env.local` no frontend quando quiser sobrescrever a URL da API:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Em producao, quando o Nginx servir o frontend e encaminhar `/api/` para o backend, a base pode ser:

```env
VITE_API_BASE_URL=/api
```

## Comandos uteis

Instalar dependencias:

```powershell
npm install
```

Rodar o frontend localmente:

```powershell
npm run dev
```

Gerar os tipos TypeScript a partir do schema OpenAPI:

```powershell
npm run api:types
```

Validar TypeScript/Vue:

```powershell
npm run type-check
```

Gerar build de producao:

```powershell
npm run build
```

Formatar arquivos em `src`:

```powershell
npm run format
```

Rodar lint:

```powershell
npm run lint
```

## Atualizacao do contrato da API

Quando o backend mudar serializers, views ou URLs:

```powershell
cd ..\backend
$env:DJANGO_SETTINGS_MODULE="configuration.settings.local"
python manage.py spectacular --file ..\frontend\src\shared\api\schema.yaml

cd ..\frontend
npm run api:types
npm run type-check
```

## Fluxo de autenticacao atual

1. A tela `views/auth/AuthView.vue` envia `identifier` e `password`.
2. `domains/auth/queries.ts` chama a mutation de login.
3. `domains/auth/requests.ts` usa o client Axios centralizado.
4. `stores/authentication.ts` guarda a sessao em memoria.
5. `lib/http/client.ts` injeta o token Bearer nas proximas requisicoes.
6. A tela de organizacoes busca `/v1/organizations/`.

## Proximos cuidados

- Se o backend migrar refresh token para cookie httpOnly, manter o `access_token` em memoria e deixar o refresh transparente no client HTTP.
- Quando houver usuario logado no contrato da API, adicionar um dominio `account`.
- Para rotas protegidas, adicionar guards no `router` usando a store de autenticacao.
