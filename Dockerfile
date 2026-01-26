# Usar imagen base de Alpine con Node.js
FROM node:18-alpine

# Cambiar a root para instalar todo
USER root

# Instalar dependencias del sistema
RUN apk update && \
    apk add --no-cache \
    git \
    python3 \
    py3-pip \
    bash \
    curl \
    openssl \
    ca-certificates \
    tini \
    tzdata \
    && rm -rf /var/cache/apk/*

# Instalar n8n globalmente
RUN npm install -g n8n

# Instalar dependencias de Python
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir requests

# Crear usuario node si no existe
RUN if ! id -u node > /dev/null 2>&1; then \
    addgroup -g 1000 node && \
    adduser -u 1000 -G node -s /bin/sh -D node; \
    fi

# Crear directorios necesarios
RUN mkdir -p /scripts /config /repo /logs /home/node/.n8n && \
    chown -R node:node /scripts /config /repo /logs /home/node/.n8n

# Copiar scripts
COPY --chown=node:node scripts/ /scripts/

# Copiar configuración
COPY --chown=node:node config/ /config/

# Dar permisos de ejecución
RUN find /scripts -type f -name "*.py" -exec chmod +x {} \; 2>/dev/null || true && \
    find /scripts -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

# Volver al usuario node
USER node

# Variables de entorno
ENV N8N_LOG_LEVEL=info \
    GENERIC_TIMEZONE=America/Bogota \
    TZ=America/Bogota \
    NODE_ENV=production

EXPOSE 5678

WORKDIR /home/node

# Usar tini como init
ENTRYPOINT ["tini", "--"]

CMD ["n8n"]
