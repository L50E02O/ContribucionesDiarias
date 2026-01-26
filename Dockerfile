# Usar la imagen oficial de n8n como base
FROM n8nio/n8n:latest

# Cambiar a root para instalar dependencias adicionales
USER root

# Instalar git, python y otras dependencias (la imagen n8n usa Debian, no Alpine)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar requests para Python
RUN pip3 install --no-cache-dir --break-system-packages requests

# Crear directorios necesarios
RUN mkdir -p /scripts /config /repo /logs && \
    chown -R node:node /scripts /config /repo /logs

# Copiar scripts
COPY --chown=node:node scripts/ /scripts/

# Copiar configuración
COPY --chown=node:node config/ /config/

# Dar permisos de ejecución a los scripts
RUN chmod +x /scripts/*.py 2>/dev/null || true && \
    chmod +x /scripts/*.sh 2>/dev/null || true

# Volver al usuario node por seguridad
USER node

# Variables de entorno adicionales
ENV N8N_LOG_LEVEL=info \
    GENERIC_TIMEZONE=America/Bogota \
    TZ=America/Bogota

# El puerto y CMD ya están definidos en la imagen base n8nio/n8n
# No necesitamos redefinirlos
