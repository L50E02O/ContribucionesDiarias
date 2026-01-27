# Guía Rápida de Despliegue en Railway

## Antes de Desplegar

### 1⃣ Verifica que estos archivos existan:

```bash
# En tu terminal, verifica:
dir scripts # Debe mostrar los archivos .py
dir config # Debe mostrar config.json
type Dockerfile # Debe mostrar el contenido
```

### 2⃣ Asegúrate de hacer commit de TODO:

```bash
# Verifica el estado
git status

# Si hay archivos sin agregar:
git add .
git commit -m "Fix: Agregar archivos de configuración"
git push
```

---

## Pasos de Despliegue

### Paso 1: Push a GitHub

```bash
# Si no has inicializado git:
git init
git add .
git commit -m "Initial commit: Sistema de commits diarios"

# Crear repo en GitHub y conectar:
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Railway

1. Ve a https://railway.app/
2. **Login con GitHub**
3. Click **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Selecciona tu repositorio
6. **Espera** a que Railway detecte el Dockerfile

### Paso 3: Configurar Variables (IMPORTANTE)

Mientras se despliega, configura estas variables en Railway → Variables:

```bash
# Variables básicas (obligatorias)
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=TuPasswordSegura123
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota
N8N_LOG_LEVEL=info

# Clave de encriptación (genera una aleatoria)
N8N_ENCRYPTION_KEY=abc123xyz456def789ghi012jkl345mno

# Configuración de Git
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@ejemplo.com

# Solo si usas modo PR (opcional):
GITHUB_TOKEN=ghp_tu_token_github
```

### Paso 4: Agregar Volumen Persistente

1. Railway → Tu servicio → **Settings**
2. Scroll a **"Volumes"**
3. **Add Volume**:
 - Mount Path: `/home/node/.n8n`
 - Size: 1 GB
4. Click **"Add"**

Railway reiniciará el servicio automáticamente.

---

## Errores Comunes y Soluciones

### Error: "config: not found"

**Causa**: El directorio `config/` no está en GitHub.

**Solución**:
```bash
# Verifica que config.json existe
cat config/config.json

# Si no existe, créalo:
mkdir -p config
echo '{"commits_per_day":1}' > config/config.json

# Haz commit y push:
git add config/
git commit -m "Add config directory"
git push

# En Railway, haz Redeploy
```

### Error: "scripts: not found"

**Causa**: Los scripts no están en GitHub.

**Solución**:
```bash
# Verifica que existen:
ls scripts/

# Si no están, haz:
git add scripts/
git commit -m "Add scripts directory"
git push
```

### Error: "Build failed"

**Causa**: El Dockerfile tiene errores o faltan archivos.

**Solución**:
1. Ve a Railway → **Deploy Logs**
2. Lee el error completo
3. Verifica que todos los archivos estén en GitHub:
 ```bash
 git ls-files
 # Debe mostrar: Dockerfile, scripts/, config/, etc.
 ```

### Error: "Service crashed"

**Causa**: Variables de entorno mal configuradas o faltantes.

**Solución**:
1. Ve a Railway → **Variables**
2. Verifica que todas las variables obligatorias están configuradas
3. Click **"Redeploy"**

---

## Verificación Post-Despliegue

### 1. Verifica que el servicio está corriendo:

- Railway → Tu servicio → Estado debe ser **"Active"** 

### 2. Obtén la URL:

- Railway → Settings → **Domains**
- Copia la URL (ej: `https://xxx.railway.app`)

### 3. Accede a n8n:

- Abre la URL en tu navegador
- Login:
 - Usuario: `admin`
 - Password: La que pusiste en `N8N_BASIC_AUTH_PASSWORD`

### 4. Importa el workflow:

1. En n8n → **Workflows** → **Import from File**
2. Selecciona `n8n-workflow.json` o `n8n-workflow-pr.json`
3. **Activa** el workflow (toggle verde)

### 5. Configura el repositorio Git:

```bash
# Conecta a Railway:
railway login
railway link # Selecciona tu proyecto

# Accede al contenedor:
railway run bash

# Configura el repo:
cd /repo
git init
git config user.name "Tu Nombre"
git config user.email "tu-email@ejemplo.com"
git remote add origin https://github.com/TU_USUARIO/daily-commits.git

# Crea commit inicial:
echo "# Daily Commits" > README.md
git add README.md
git commit -m "Initial commit"
git branch -M main
git push -u origin main
# Usuario: tu_usuario_github
# Password: ghp_tu_token_github
```

### 6. Prueba manual:

```bash
# Ejecuta el script manualmente:
railway run python3 /scripts/commit_automator.py

# Deberías ver:
# Commit realizado exitosamente
# Push realizado exitosamente
```

### 7. Verifica en GitHub:

- Ve a tu repositorio en GitHub
- Debes ver el commit que acabas de hacer 

---

## Checklist Final

Antes de dar por terminado, verifica:

- [ ] Servicio en Railway está **"Active"**
- [ ] Puedes acceder a n8n con la URL de Railway
- [ ] Workflow está importado y **activado** (toggle verde)
- [ ] Variables de entorno están configuradas
- [ ] Volumen persistente está montado (`/home/node/.n8n`)
- [ ] Repositorio Git está configurado en `/repo`
- [ ] Prueba manual funcionó correctamente
- [ ] Commit apareció en GitHub

---

## Si Algo Sale Mal

### Ver logs en tiempo real:

```bash
railway logs -f
```

### Redeploy manual:

```bash
railway up
```

### Ver variables configuradas:

```bash
railway variables
```

### Conectar al contenedor:

```bash
railway run bash
```

---

## ¡Todo Listo!

Si completaste todos los pasos del checklist, tu sistema está funcionando correctamente.

Los commits se generarán automáticamente cada 24 horas según el cron configurado en n8n.

**Verifica mañana tu perfil de GitHub para ver la primera contribución automática.** 
