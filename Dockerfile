# Usar Node.js Alpine como base (igual que n8n oficial)
FROM node:20-alpine3.20

# Instalar dependencias del sistema (git, python, etc.)
RUN apk add --no-cache \
    git \
    openssh \
    python3 \
    py3-pip \
    bash \
    curl \
    tini \
    tzdata \
    ca-certificates && \
    # Instalar n8n globalmente
    npm install -g n8n && \
    # Instalar requests de Python
    pip3 install --no-cache-dir --break-system-packages requests && \
    # Limpiar cache
    rm -rf /root/.npm /tmp/*

# Crear usuario node (ya existe en la imagen base)
RUN mkdir -p /home/node/.n8n /scripts /config /repo /logs && \
    chown -R node:node /home/node /scripts /config /repo /logs

# Copiar archivos
COPY --chown=node:node scripts/ /scripts/
COPY --chown=node:node config/ /config/

# Permisos de ejecución
RUN chmod +x /scripts/*.py /scripts/*.sh 2>/dev/null || true

# Cambiar a usuario node
USER node

WORKDIR /home/node

# Variables de entorno
ENV N8N_LOG_LEVEL=info \
    GENERIC_TIMEZONE=America/Bogota \
    TZ=America/Bogota \
    NODE_ENV=production

EXPOSE 5678

# Usar tini como init system
ENTRYPOINT ["tini", "--"]

# Iniciar n8n
CMD ["n8n", "start"]
