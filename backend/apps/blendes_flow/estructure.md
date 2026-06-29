# Estrutura do app Blendes Flow

Este documento define o padrao para novas funcionalidades dentro de
`apps.blendes_flow`. O objetivo e manter o app organizado por dominio, sem
misturar responsabilidades e sem acoplar diretamente outros apps.

## Principios

- Toda regra de negocio deve ficar em `services/<dominio>.py`.
- Views devem apenas validar entrada, chamar services e serializar saida.
- Serializers devem ficar em arquivos por dominio, por exemplo
  `serializers/blaves.py`.
- Exceptions de dominio devem ficar em arquivos por dominio, por exemplo
  `exceptions/blaves.py`.
- Recursos comuns reutilizaveis devem ficar em `common`, separados por tipo e
  dominio.
- Um app nao deve importar models de outro app diretamente. Use um arquivo
  `access.py` no app dono dos dados e exponha DTOs ou funcoes de acesso.
- Mensagens de erro e exceptions publicas devem ser em ingles.
- Docstrings e comentarios do codigo do app devem ser em portugues.

## Estrutura esperada

```text
apps/blendes_flow/
    api/
        v1/
            urls.py
            views/
                __init__.py
                <dominio>.py
    common/
        throttles/
            __init__.py
            <dominio>.py
        views/
            __init__.py
            <dominio>.py
    exceptions/
        __init__.py
        <dominio>.py
    serializers/
        __init__.py
        <dominio>.py
    services/
        __init__.py
        <dominio>.py
    models.py
    urls.py
```

Exemplo atual para Blaves:

```text
api/v1/views/blaves.py
common/throttles/blave.py
common/views/blave.py
exceptions/blaves.py
serializers/blaves.py
services/blaves.py
```

## Views de API

As views versionadas ficam em `api/v1/views/<dominio>.py`.

Responsabilidades permitidas:

- Definir `permission_classes` e `throttle_classes`.
- Validar payload com serializer de entrada.
- Chamar uma service do dominio.
- Serializar resposta com serializer de saida.
- Declarar schema com `extend_schema`.

Responsabilidades proibidas:

- Persistir models diretamente.
- Fazer consultas complexas.
- Implementar regra de negocio.
- Importar models de outros apps.

## Views comuns

Views base e contratos publicos de erro ficam em
`common/views/<dominio>.py`.

Use esse local para classes como `BlaveAPIView`, que padronizam:

- Tratamento de exceptions de dominio.
- Respostas de validacao.
- Respostas de autenticacao e permissao.
- Respostas de throttle.

## Throttles

Throttles do dominio ficam em `common/throttles/<dominio>.py`.

Cada throttle deve ter `scope` proprio e o valor deve ser configurado em
`REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`.

Exemplo:

```python
class BlaveManagementRateThrottle(UserRateThrottle):
    """Limita operacoes autenticadas de gerenciamento de blaves."""

    scope = "blaves_management"
```

## Services

Services ficam em `services/<dominio>.py`.

Responsabilidades:

- Aplicar regras de negocio.
- Abrir transacoes com `transaction.atomic` quando houver escrita.
- Criar, atualizar e excluir registros.
- Usar `bulk_create` ou operacoes em lote quando a regra pedir desempenho.
- Controlar escopo de acesso por meio de contratos publicos de outros apps.

Services nao devem:

- Receber `request`.
- Retornar `Response`.
- Importar serializers.
- Importar models de outros apps.

## Acesso entre apps

Quando `blendes_flow` precisar consultar dados de outro app, o app dono dos
dados deve expor um contrato em `access.py`.

Exemplo em `apps.organizations.access`:

```python
@dataclass(frozen=True)
class OrganizationAccessDTO:
    """Dados minimos expostos para integracao com outros apps."""

    id: int
    is_active: bool
```

O app `blendes_flow` deve importar apenas esse contrato publico, nunca
`apps.organizations.models.Organization`.

## Serializers

Serializers ficam em `serializers/<dominio>.py`.

Padrao recomendado:

- `<Dominio>InputSerializerV1` para criacao.
- `<Dominio>PartialInputSerializerV1` para atualizacao parcial.
- `<Dominio>OutputSerializerV1` para resposta.
- Serializers auxiliares do mesmo dominio podem ficar no mesmo arquivo.

Serializers de entrada devem expor somente campos permitidos pela regra de
negocio. Por exemplo, atualizacao de Blave deve aceitar apenas `title`.

## Exceptions

Exceptions ficam em `exceptions/<dominio>.py`.

Padrao:

- Uma exception base do dominio.
- Exceptions especificas com `code` e `message`.
- `message` sempre em ingles.
- Docstring em portugues.

Exemplo:

```python
class BlaveNotFoundError(BlaveDomainError):
    """Excecao para blave nao encontrada ou fora do escopo do usuario."""

    code = "blave_not_found"
    message = "Blave not found"
```

## URLs

O arquivo raiz `apps/blendes_flow/urls.py` inclui as versoes da API.

O arquivo `api/v1/urls.py` registra endpoints versionados. Para recursos que
existem dentro de organizacoes, use rota aninhada:

```text
/api/v1/organizations/<organization_id>/<recurso>/
```

## Testes

Testes do app ficam em `backend/tests/blendes_flow`.

Para cada novo dominio, crie pelo menos:

- `test_services.py` cobrindo regras de negocio e permissoes de escopo.
- `test_api.py` cobrindo contrato REST, autenticacao e erros publicos.
- `factories.py` com helpers pequenos e explicitos quando necessario.

Ao finalizar uma funcionalidade, rode:

```text
python manage.py test tests.blendes_flow --settings=configuration.settings.test
python manage.py test --settings=configuration.settings.test
python manage.py check
python manage.py makemigrations --check --dry-run
```
