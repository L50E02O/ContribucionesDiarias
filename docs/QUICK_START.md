# Guía de Inicio Rápido

Configura tu sistema de commits diarios en 10 minutos.

## Requisitos Previos

- Cuenta de GitHub
- Cuenta en Railway (gratis)
- Token de GitHub con permisos `repo`

## Pasos de Configuración

### 1⃣ Preparar Repositorio GitHub

```bash
# Crear un nuevo repositorio en GitHub
# Ve a github.com/new → Nombre: "daily-commits"
# Puede ser público o privado

# Clonar este proyecto
cd commitDiario

# Inicializar git
git init
git add .
git commit -m "Initial commit: Sistema de commits automáticos"

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/commit-automation.git
git branch -M main
git push -u origin main
```

### 2⃣ Crear Token de GitHub

1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Selecciona scope: `repo` (acceso completo)
4. Genera y **copia el token** (lo necesitarás después)

### 3⃣ Desplegar en Railway

1. Ve a https://railway.app/
2. **Login con GitHub**
3. Click **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Selecciona tu repositorio
6. Espera a que termine el build (2-3 minutos)

### 4⃣ Configurar Variables de Entorno

En Railway → Tu servicio → **Variables**, agrega:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=TuPasswordSegura123
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota
N8N_LOG_LEVEL=info
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@ejemplo.com
```

### 5⃣ Generar Dominio

1. Railway → Tu servicio → **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Puerto: **5678**
4. Copia la URL generada

### 6⃣ Configurar n8n

1. Abre la URL de Railway en tu navegador
2. Login con `admin` / tu password
3. **Workflows** → **Import from File**
4. Selecciona `n8n-workflow.json`
5. **Activa** el workflow (toggle verde)

### 7⃣ Configurar Repositorio Target

En Railway → Shell o usando Railway CLI:

```bash
railway run bash

# Dentro del contenedor:
cd /repo
git init
git config user.name "Tu Nombre"
git config user.email "tu-email@ejemplo.com"
git remote add origin https://github.com/TU_USUARIO/daily-commits.git

# Commit inicial
echo "# Daily Commits" > README.md
git add README.md
git commit -m "Initial commit"
git branch -M main
git push -u origin main
# Usuario: tu_usuario_github
# Password: ghp_tu_token_github
```

### 8⃣ Agregar Volumen Persistente

1. Railway → Tu servicio → **Settings** → **Volumes**
2. **Add Volume**:
 - Mount Path: `/home/node/.n8n`
 - Size: 1 GB
3. Click **"Add"**

## Verificación

- [ ] Servicio en Railway está "Active"
- [ ] Puedes acceder a n8n con la URL
- [ ] Workflow está importado y activado
- [ ] Variables de entorno configuradas
- [ ] Volumen persistente agregado
- [ ] Repositorio Git configurado
- [ ] Prueba manual funcionó

## Prueba Manual

```bash
railway run python3 /scripts/commit_automator.py
```

Deberías ver:
```
 Commit realizado exitosamente
 Push realizado exitosamente
```

## ¡Listo!

Tu sistema generará commits automáticamente cada 24 horas.

**Verifica mañana tu perfil de GitHub** para ver la primera contribución automática.

## Siguiente Paso

- [Configuración Avanzada](CONFIGURATION.md)
- [Modo Pull Request](PR_MODE.md)
- [Solución de Problemas](TROUBLESHOOTING.md)
