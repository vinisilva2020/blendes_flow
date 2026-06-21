# syntax=docker/dockerfile:1.7

FROM node:24-alpine@sha256:fb71d01345f11b708a3553c66e7c74074f2d506400ea81973343d915cb64eef0 AS frontend-build

WORKDIR /app

# Mantém a instalação de dependências em cache durante alterações no código.
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build


FROM nginx:alpine-slim@sha256:3fe7a344f234ac4b84817896c9294ffae74eae03fc1ad0ff502457fef5cebef8 AS runtime

LABEL org.opencontainers.image.title="blendesflow-nginx" \
      org.opencontainers.image.description="Nginx reverse proxy and Vue production assets" \
      org.opencontainers.image.source="blendesflow"

COPY infrastructure/nginx/nginx.conf /etc/nginx/nginx.conf
COPY infrastructure/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY infrastructure/nginx/proxy_params.conf /etc/nginx/proxy_params.conf
COPY --from=frontend-build /app/dist/ /usr/share/nginx/html/

# Assets estáticos e configurações permanecem imutáveis e pertencentes ao root.
# O worker grava somente o PID e dados temporários de requisição em /tmp.
RUN chmod -R u=rwX,go=rX /usr/share/nginx/html \
    && chmod 0444 \
        /etc/nginx/nginx.conf \
        /etc/nginx/conf.d/default.conf \
        /etc/nginx/proxy_params.conf

USER nginx

# O container roda sem privilégios. Publique-o como "80:8080" no Compose.
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://127.0.0.1:8080/healthz || exit 1

STOPSIGNAL SIGQUIT

# Ignora scripts da imagem base que alterariam a configuração no entrypoint.
ENTRYPOINT []
CMD ["nginx", "-g", "daemon off;"]