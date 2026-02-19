# Guía de Despliegue de n8n en Render

Usa esta guía cuando en **deploy.yml** tengas `target: render`.

Despliegue de n8n en [Render](https://render.com/) con el Dockerfile e imagen oficial [n8nio/n8n](https://hub.docker.com/r/n8nio/n8n).

## Requisitos Previos

- Cuenta de GitHub
- Cuenta en [Render](https://render.com/) (plan free o de pago)
- Repositorio de este proyecto en GitHub

---

## Opción A: Despliegue con Blueprint (render.yaml)

1. **Sube el repositorio a GitHub** (si aún no lo has hecho).

2. **Conecta el repo en Render**:
   - Ve a [dashboard.render.com](https://dashboard.render.com/)
   - **New** → **Blueprint**
   - Conecta tu cuenta de GitHub y selecciona el repositorio `n8nDocker`
   - Render detectará el archivo `render.yaml` en la raíz

3. **Configura las variables obligatorias** cuando Render lo pida (o en **Environment** después):
   - `N8N_BASIC_AUTH_USER`: usuario para login (ej: `admin`)
   - `N8N_BASIC_AUTH_PASSWORD`: contraseña segura
   - `N8N_ENCRYPTION_KEY`: clave aleatoria de al menos 32 caracteres
   - `WEBHOOK_URL`: **después del primer deploy**, pon aquí la URL de tu servicio (ej: `https://n8n-xxxx.onrender.com`)

4. **Aplica el Blueprint** y espera al primer deploy.

5. **Añade WEBHOOK_URL**:
   - En el servicio → **Environment** → añade o edita `WEBHOOK_URL` con la URL que Render te asigna (ej: `https://n8n-xxxx.onrender.com`).
   - Sin esto, los webhooks de n8n no funcionarán correctamente.

### Persistencia en Render

- **Plan free**: no hay disco persistente. Los datos (workflows, credenciales) se pierden en cada redeploy o cuando el servicio se apaga. Útil solo para pruebas.
- **Plan de pago**: el `render.yaml` incluye un disco en `/home/node/.n8n`. Los datos se conservan entre redeploys.

Si usas plan free y quieres persistencia, considera desplegar en **Railway** (ver [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)), donde el plan gratuito permite volúmenes.

---

## Opción B: Despliegue manual (sin Blueprint)

1. **New** → **Web Service** en Render.
2. Conecta tu repo de GitHub y selecciona `n8nDocker`.
3. Configuración:
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./Dockerfile` (por defecto)
4. Añade las mismas variables de entorno que en la Opción A.
5. (Opcional) Si tienes plan de pago: **Disks** → **Add Disk** → Mount Path: `/home/node/.n8n`, tamaño según necesites.
6. **Create Web Service**.

---

## Variables de Entorno en Render

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `N8N_BASIC_AUTH_ACTIVE` | Sí | `true` para activar login |
| `N8N_BASIC_AUTH_USER` | Sí | Usuario de acceso |
| `N8N_BASIC_AUTH_PASSWORD` | Sí | Contraseña de acceso |
| `N8N_ENCRYPTION_KEY` | Sí | Clave de encriptación (mín. 32 caracteres) |
| `WEBHOOK_URL` | Recomendada | URL pública del servicio (ej: `https://n8n-xxx.onrender.com`) |
| `GENERIC_TIMEZONE` | No | Zona horaria (ej: `America/Bogota`) |
| `TZ` | No | Misma zona para el sistema |
| `N8N_LOG_LEVEL` | No | `info` o `debug` |

Render inyecta la variable `PORT`; el contenedor la usa automáticamente para exponer n8n en el puerto correcto.

---

## Verificación

1. Estado del servicio en **Active** (verde).
2. Abre la URL del servicio (ej: `https://n8n-xxxx.onrender.com`).
3. Inicia sesión con `N8N_BASIC_AUTH_USER` y `N8N_BASIC_AUTH_PASSWORD`.
4. Crea un workflow y actívalo para comprobar que n8n responde.

---

## Solución de Problemas

- **Error al iniciar**: Revisa **Logs** y que todas las variables obligatorias estén definidas.
- **Webhooks no funcionan**: Define `WEBHOOK_URL` con la URL exacta de tu servicio en Render (con `https://`).
- **Datos perdidos**: En plan free no hay persistencia. Usa plan de pago y el disco en `render.yaml`, o despliega en Railway con volumen.

---

## Enlaces

- [Documentación de Render](https://docs.render.com/)
- [Imagen oficial n8n en Docker Hub](https://hub.docker.com/r/n8nio/n8n)
- [Documentación de n8n](https://docs.n8n.io/)
