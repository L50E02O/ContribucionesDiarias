# Imagen oficial n8n: https://hub.docker.com/r/n8nio/n8n
# Configuración de despliegue: deploy.yml (target: railway | render)
FROM n8nio/n8n:latest

ENV N8N_LOG_LEVEL=info \
    GENERIC_TIMEZONE=America/Bogota \
    TZ=America/Bogota \
    NODE_ENV=production

EXPOSE 5678

# Render inyecta PORT; Railway usa 5678. Si existe PORT, n8n escucha en ese puerto.
CMD ["/bin/sh", "-c", "if [ -n \"$PORT\" ]; then export N8N_PORT=$PORT; fi; exec n8n start"]
