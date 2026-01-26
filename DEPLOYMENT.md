# 🚀 Guía de Despliegue en Railway

Esta guía te muestra cómo desplegar el sistema de commits diarios en Railway para que esté siempre disponible 24/7.

## 🚂 ¿Por qué Railway?

Railway es la **mejor opción para este proyecto** porque:

- ✅ **Plan gratuito funcional**: $5 crédito/mes (suficiente para este proyecto)
- ✅ **Sin sleep automático**: Tu servicio permanece activo 24/7
- ✅ **Cron jobs funcionan**: Los workflows de n8n se ejecutan correctamente
- ✅ **Setup en 5 minutos**: La configuración más simple
- ✅ **Interfaz moderna**: Fácil de usar y monitorear
- ✅ **Despliegue automático**: Desde GitHub con un click

## ⚠️ Nota sobre Otras Plataformas

**Vercel NO funciona** - No soporta contenedores de larga ejecución ni cron jobs persistentes.

**Render Free NO funciona** - El servicio se duerme después de 15 minutos, por lo que los cron jobs no se ejecutan.

---

## 🚀 Despliegue en Railway

### 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta de GitHub
- ✅ Cuenta en Railway (puedes registrarte con GitHub)
- ✅ Token de GitHub con permisos `repo`
- ✅ Tu proyecto listo en tu máquina

---

## 🎯 Guía Paso a Paso

### Paso 1: Crear Cuenta en Railway

1. Ve a **https://railway.app/**
2. Click en **"Start a New Project"** o **"Login"**
3. **Regístrate con GitHub** (recomendado para deployment automático)
4. Autoriza Railway para acceder a tus repositorios

---

### Paso 2: Preparar tu Repositorio en GitHub

Abre tu terminal en el directorio del proyecto:

```bash
# Navega al directorio del proyecto
cd C:\Users\leoan\Desktop\commitDiario

# Inicializar git
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Automated GitHub contributions system"

# Crear repositorio en GitHub
# Ve a https://github.com/new y crea un nuevo repositorio
# Nombre sugerido: "commit-automation" o "daily-commits"
# Puede ser público o privado

# Conectar con tu repositorio GitHub (reemplaza TU_USUARIO y TU_REPO)
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

---

### Paso 3: Crear Proyecto en Railway

1. En Railway, click **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Autoriza Railway a acceder a tu repositorio (si es la primera vez)
4. Selecciona el repositorio que acabas de crear
5. Railway detectará automáticamente el `Dockerfile` ✅

**Railway comenzará a desplegar automáticamente**, pero primero necesitamos configurar las variables de entorno.

---

### Paso 4: Configurar Variables de Entorno

Mientras se despliega, configura las variables:

1. En Railway, ve a tu proyecto
2. Click en el servicio (aparecerá automáticamente)
3. Ve a la pestaña **"Variables"**
4. Click en **"New Variable"** y agrega cada una:

#### Variables Obligatorias:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=CambiaEstaPassword123!
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota
N8N_LOG_LEVEL=info
N8N_ENCRYPTION_KEY=genera-clave-aleatoria-larga-aqui-abc123xyz789
```

#### Variables para GitHub (Modo Commits Directos):

```bash
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@ejemplo.com
```

#### Variables Adicionales (Solo si usas Modo PR):

```bash
GITHUB_TOKEN=ghp_tu_token_github_con_permisos_repo
```

**💡 Consejo:** Para generar `N8N_ENCRYPTION_KEY`, usa cualquier texto largo y aleatorio (mínimo 32 caracteres).

---

### Paso 5: Configurar Volumen Persistente

Para mantener tus workflows de n8n guardados:

1. En Railway → Tu servicio → **"Settings"**
2. Scroll hasta **"Volumes"**
3. Click en **"Add Volume"**
4. Configuración:
   - **Mount Path**: `/home/node/.n8n`
   - **Size**: 1 GB (suficiente)
5. Click **"Add"**

Railway reiniciará el servicio para montar el volumen.

---

### Paso 6: Obtener URL del Servicio

1. Ve a la pestaña **"Settings"** de tu servicio
2. En la sección **"Domains"**, verás algo como:
   ```
   https://commit-automation-production-xxxx.up.railway.app
   ```
3. **Copia esta URL** - la necesitarás para acceder a n8n

---

### Paso 7: Acceder a n8n

1. Abre la URL que copiaste en tu navegador
2. Espera 1-2 minutos si es la primera vez (está iniciando)
3. Verás la pantalla de login de n8n
4. Login con:
   - **Usuario**: `admin` (o el que configuraste)
   - **Password**: La que pusiste en `N8N_BASIC_AUTH_PASSWORD`

---

### Paso 8: Importar y Configurar Workflow

1. En n8n, ve a **"Workflows"** (menú lateral)
2. Click en **"Import from File"**
3. Selecciona el archivo:
   - `n8n-workflow.json` (para commits directos)
   - `n8n-workflow-pr.json` (para PRs automáticos)
4. El workflow aparecerá en tu lista
5. Ábrelo y **activa el workflow** (toggle en la esquina superior derecha debe estar verde ✅)

---

### Paso 9: Configurar el Repositorio Target

Ahora necesitas configurar el repositorio donde se harán los commits:

#### Opción A: Dentro del contenedor de Railway

1. En Railway → Tu servicio → Pestaña **"Deploy Logs"**
2. Click en **"⋮"** (tres puntos) → **"Shell"** o usa Railway CLI

```bash
# Conectar vía Railway CLI (instalar si no lo tienes)
railway login
railway link
railway run bash

# Dentro del contenedor, configurar el repo
cd /repo
git init
git config user.name "Tu Nombre"
git config user.email "tu-email@ejemplo.com"
git remote add origin https://github.com/TU_USUARIO/daily-commits.git

# Crear commit inicial
echo "# Daily Commits Repository" > README.md
git add README.md
git commit -m "Initial commit"
git branch -M main

# Push inicial (necesitarás tu token de GitHub)
git push -u origin main
# Usuario: tu_usuario_github
# Password: ghp_tu_token_github
```

#### Opción B: Clonar repo existente

```bash
cd /repo
git clone https://github.com/TU_USUARIO/daily-commits.git .
git config user.name "Tu Nombre"
git config user.email "tu-email@ejemplo.com"
```

---

### Paso 10: Probar Manualmente

Antes de esperar 24 horas, prueba que todo funcione:

1. En Railway → Tu servicio → **"Shell"** o **"Deploy Logs"**
2. Ejecuta el script manualmente:

```bash
# Para commits directos
python3 /scripts/commit_automator.py

# Para PRs automáticos
python3 /scripts/pr_automator.py
```

3. Deberías ver:
```
============================================================
🤖 Iniciando automatización de commits diarios
============================================================
⚙️  Configurando Git...
📊 Commits a realizar: 1
🔄 Realizando commit 1/1...
✅ Commit #1 realizado exitosamente
📤 Empujando commits a la rama 'main'...
✅ Push realizado exitosamente
============================================================
✅ Proceso completado exitosamente
============================================================
```

4. Verifica en GitHub que el commit apareció ✅

---

## ✅ Verificación Final

### Checklist de que Todo Funciona:

- [ ] Railway está corriendo (status: "Active")
- [ ] Puedes acceder a n8n con la URL de Railway
- [ ] El workflow está importado y activado (toggle verde)
- [ ] Las variables de entorno están configuradas
- [ ] El volumen persistente está montado
- [ ] El repositorio Git está configurado en `/repo`
- [ ] La prueba manual del script funcionó
- [ ] El commit apareció en GitHub

Si todo está ✅, ¡tu sistema está listo!

---

## 🔧 Configuración Post-Despliegue

### Configurar el Workflow:

1. **Ajustar hora de ejecución**
   - En n8n, abre tu workflow
   - Click en el nodo **"Schedule Trigger"**
   - Opciones:
     - **Intervalo**: Cada 24 horas (simple)
     - **Cron Expression**: Para hora específica
   
   **Ejemplos de Cron (ya configurado para UTC-5 / America/Bogota):**
   ```
   # Diario a las 9:00 AM (Colombia)
   0 14 * * *
   
   # Diario a las 6:00 PM (Colombia)  
   0 23 * * *
   
   # Diario a la medianoche (Colombia)
   0 5 * * *
   ```

2. **Configurar número de commits**
   - Edita `/config/config.json` desde Railway Shell:
   ```json
   {
     "commits_per_day": 3,  // Cambia esto
     ...
   }
   ```

3. **Guardar cambios**
   - Click **"Save"** en n8n
   - Los cambios se aplicarán en la próxima ejecución

---

## 🔄 Modo Pull Request vs Commits Directos

### Para Activar Modo Pull Request:

1. **Actualiza variables en Railway:**
   - Railway → Variables → Add Variable:
   ```bash
   GITHUB_TOKEN=ghp_tu_token_con_permisos_repo
   ```

2. **Actualiza `config/config.json`** (vía Railway Shell):
   ```json
   {
     "use_pr_workflow": true,
     "github_token": "ghp_tu_token_aqui",
     "github_repo_owner": "tu_usuario",
     "github_repo_name": "nombre_repo",
     "merge_method": "squash",
     "auto_cleanup_branch": true
   }
   ```

3. **Crea token de GitHub con permisos completos:**
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Scope: `repo` (acceso completo a repositorios)
   - Copia el token

4. **Importa el workflow de PRs en n8n:**
   - Importa `n8n-workflow-pr.json` 
   - Activa el workflow

5. **Prueba desde Railway:**
   ```bash
   railway run python3 /scripts/pr_automator.py
   ```

---

## 🔐 Seguridad en Railway

### Mejores Prácticas:

1. **Contraseñas fuertes:**
   ```bash
   N8N_BASIC_AUTH_PASSWORD=UsaContraseñaSegura123!@#
   ```
   - Mínimo 12 caracteres
   - Usa generadores de contraseñas

2. **Encryption Key segura:**
   ```bash
   # Generar clave aleatoria
   N8N_ENCRYPTION_KEY=abc123xyz789MuyLargaYAleatoria456def
   ```
   - Mínimo 32 caracteres aleatorios

3. **Tokens de GitHub:**
   - Nunca compartas tu token
   - Usa tokens con permisos mínimos necesarios
   - Rota tokens periódicamente (cada 3-6 meses)
   - Considera usar Fine-grained tokens

4. **Repositorio privado:**
   - Usa repositorios privados para mayor privacidad
   - Las contribuciones privadas también cuentan en tu perfil
   - Railway accede vía token, no expone credenciales

5. **Variables de entorno:**
   - Todas las credenciales están en Variables de Railway
   - No están en el código
   - Railway las encripta automáticamente

---

## 💰 Costos de Railway

### Plan Gratuito:

- **Crédito mensual**: $5 USD
- **Renovación**: Automática cada mes
- **Consumo estimado**: $1-2/mes para este proyecto
- **Conclusión**: ✅ **Completamente gratis** para este uso

### Uso Real Estimado:

```
Servicio n8n corriendo 24/7:
- CPU: Mínima (solo cuando ejecuta workflow)
- RAM: ~150-200 MB
- Network: Mínimo
- Storage: 1 GB (volumen)

Costo real: ~$1.50/mes
Crédito gratis: $5/mes
Resultado: ✅ GRATIS con margen sobrado
```

### Si Superas los $5:

```bash
# Monitorear uso en Railway
Railway → Project → Usage

# Si te acercas al límite:
- Verifica logs por errores que causen reinicios
- Optimiza la frecuencia del cron si es necesario
- Considera plan Developer ($5/mes + uso)
```

---

## 🐛 Solución de Problemas en Railway

### El servicio no inicia:

**Síntomas**: Estado "Crashed" o "Error"

**Solución**:
1. Ve a **Deploy Logs** para ver el error
2. Verifica que el `Dockerfile` esté correcto
3. Verifica que todas las variables estén configuradas
4. Click en **"Redeploy"** después de corregir

### El workflow no se ejecuta:

**Síntomas**: No hay commits en GitHub después de 24h

**Solución**:
1. Verifica que el workflow esté **activado** en n8n (toggle verde)
2. Revisa los logs: Railway → Deploy Logs
3. Verifica la hora del cron (debe estar en UTC, Railway usa UTC)
4. Prueba manualmente: `railway run python3 /scripts/commit_automator.py`

### Error de autenticación con GitHub:

**Síntomas**: "Authentication failed" en los logs

**Solución**:
1. Verifica la variable `GITHUB_TOKEN` en Railway → Variables
2. Verifica que el token tenga permisos `repo`
3. Verifica que el token no haya expirado
4. Genera un nuevo token si es necesario

### No puedo acceder a n8n:

**Síntomas**: "Cannot connect" o timeout

**Solución**:
1. Verifica que el servicio esté **"Active"** (no crashed)
2. Verifica la URL en Settings → Domains
3. Espera 1-2 minutos si acabas de desplegar
4. Verifica las credenciales:
   ```bash
   Usuario: admin
   Password: (el de N8N_BASIC_AUTH_PASSWORD)
   ```

### El repositorio Git no está configurado:

**Síntomas**: "No hay repositorio remoto configurado"

**Solución**:
```bash
# Conectar a Railway
railway run bash

# Configurar repo
cd /repo
git init
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

### Logs muestran "Permission denied":

**Síntomas**: Scripts no pueden ejecutarse

**Solución**:
Los permisos ya están configurados en el `Dockerfile`, pero si persiste:
```bash
railway run bash
chmod +x /scripts/*.py /scripts/*.sh
```

---

## 📈 Monitoreo en Railway

### Ver Logs en Tiempo Real:

1. Railway → Tu servicio → **"Deploy Logs"**
2. Los logs se actualizan automáticamente
3. Busca mensajes de error o warnings

### Métricas de Uso:

1. Railway → Project → **"Usage"**
2. Monitorea:
   - CPU usage
   - Memory usage
   - Network egress
   - Costo acumulado del mes

### Alertas:

Railway te enviará email si:
- El servicio crashea repetidamente
- Te acercas al límite de $5
- Hay problemas de deployment

### Comandos Útiles de Railway CLI:

```bash
# Ver logs en tiempo real
railway logs

# Ver estado del servicio
railway status

# Conectar al contenedor
railway run bash

# Ejecutar comando específico
railway run python3 /scripts/commit_automator.py

# Ver variables configuradas
railway variables

# Redeploy
railway up
```

---

## 🎉 ¡Sistema Desplegado!

Tu sistema de commits diarios está ahora corriendo 24/7 en Railway.

### ✅ Qué Esperar:

- **Hoy**: Sistema configurado y corriendo
- **Mañana**: Primer commit automático aparecerá en GitHub
- **Diario**: Commits automáticos a la hora configurada
- **Tu perfil**: Racha de contribuciones constante 🔥

### 📊 Verificación Diaria:

1. Revisa tu perfil de GitHub
2. Verifica los commits en el repositorio
3. Monitorea el uso en Railway (debería estar bajo $2/mes)

---

## 🚀 Próximos Pasos

### Personalizar el Sistema:

1. **Cambiar hora de ejecución**: Edita el cron en n8n
2. **Cambiar número de commits**: Edita `config/config.json`
3. **Activar modo PR**: Sigue la guía en la sección "Modo Pull Request"
4. **Agregar más repos**: Duplica el workflow en n8n

### Optimizaciones:

- Configura dominios personalizados en Railway
- Agrega notificaciones (Discord/Slack) en n8n para monitoreo
- Crea múltiples workflows para diferentes repos

---

## 📚 Recursos Útiles

- [Railway Documentation](https://docs.railway.app/)
- [Railway CLI Guide](https://docs.railway.app/develop/cli)
- [n8n Documentation](https://docs.n8n.io/)
- [GitHub API - Commits](https://docs.github.com/en/rest/commits)
- [GitHub API - Pull Requests](https://docs.github.com/en/rest/pulls)

---

## 💬 Soporte

Si tienes problemas:

1. **Revisa los logs** en Railway → Deploy Logs
2. **Consulta la sección** de Solución de Problemas arriba
3. **Revisa la documentación** de Railway y n8n
4. **Prueba manualmente** con `railway run python3 /scripts/commit_automator.py`

---

## 🎊 ¡Felicitaciones!

Has desplegado exitosamente un sistema de automatización completo en la nube. Ahora tu perfil de GitHub mantendrá una racha de contribuciones constante sin esfuerzo manual.

**Recuerda**: Usa este sistema de manera responsable y ética. 

**¡Disfruta tu racha de commits! 🔥**
