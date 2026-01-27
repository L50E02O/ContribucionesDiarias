# Comandos Rápidos - Referencia

Comandos útiles para gestionar tu sistema de commits automáticos.

---

## Railway CLI

### Instalación y Configuración

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar a tu proyecto
railway link
```

### Comandos Básicos

```bash
# Ver logs en tiempo real
railway logs -f

# Ver logs recientes
railway logs

# Ver variables de entorno
railway variables

# Acceder al contenedor (bash)
railway run bash

# Ejecutar comando en el contenedor
railway run <comando>

# Redeploy manual
railway up
```

---

## Configuración Inicial (Dentro del Contenedor)

```bash
# 1. Acceder al contenedor
railway run bash

# 2. Ejecutar script de configuración automática
bash /scripts/setup_railway.sh

# O configurar manualmente:
cd /repo
git init
git config user.name "Tu Nombre Completo"
git config user.email "tu-email@github.com"
git remote add origin https://github.com/TU_USUARIO/commitDiario.git
git branch -M main

# Commit inicial
echo "# Daily Commits" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

---

## Pruebas y Verificación

### Verificar Configuración

```bash
# Ejecutar test de configuración
railway run python3 /scripts/test_setup.py
```

### Prueba Manual de Commits

```bash
# Modo commit directo
railway run python3 /scripts/commit_automator.py

# Modo Pull Request
railway run python3 /scripts/pr_automator.py
```

### Verificar Estado de Git

```bash
railway run bash

# Dentro del contenedor:
cd /repo
git status
git log --oneline -5
git remote -v
git config --list
```

---

## Editar Configuración

### Ver Configuración Actual

```bash
# Ver config.json
railway run cat /config/config.json

# Ver variables de entorno
railway run env | grep N8N
railway run env | grep GIT
railway run env | grep GITHUB
```

### Editar config.json

**Método 1: Editar localmente y hacer push**

```bash
# En tu máquina local
cd C:\Users\leoan\Desktop\commitDiario
notepad config\config.json

# Guardar cambios y push
git add config/config.json
git commit -m "Update configuration"
git push

# Railway redespleará automáticamente
```

**Método 2: Editar directamente en Railway**

```bash
railway run bash

# Dentro del contenedor:
cd /config
vi config.json # o nano config.json

# Los cambios se aplican inmediatamente
# (pero se perderán en el próximo redeploy)
```

---

## Gestión del Repositorio

### Sincronizar Repositorio

```bash
railway run bash

cd /repo
git pull origin main
git status
```

### Ver Commits Recientes

```bash
railway run bash

cd /repo
git log --oneline -10
git log --since="1 day ago"
```

### Limpiar y Reiniciar Repositorio

```bash
railway run bash

cd /repo
rm -rf .git
git init
git config user.name "Tu Nombre"
git config user.email "tu-email@github.com"
git remote add origin https://github.com/TU_USUARIO/commitDiario.git
```

---

## Monitoreo

### Ver Logs del Sistema

```bash
# Logs de Railway
railway logs -f

# Logs de n8n (dentro del contenedor)
railway run bash
cat /logs/automation_log.json
```

### Verificar Proceso n8n

```bash
railway run bash

# Ver procesos
ps aux | grep n8n

# Ver puerto de n8n
netstat -tlnp | grep 5678
```

---

## Gestión de Tokens y Credenciales

### Actualizar Token de GitHub

```bash
# En Railway Dashboard:
# Variables → GITHUB_TOKEN → Editar → Guardar

# O desde CLI:
railway variables set GITHUB_TOKEN=ghp_nuevo_token_aqui
```

### Actualizar Credenciales de n8n

```bash
railway variables set N8N_BASIC_AUTH_USER=nuevo_usuario
railway variables set N8N_BASIC_AUTH_PASSWORD=nueva_password
```

---

## Debugging

### Ver Errores de Git

```bash
railway run bash

cd /repo
git status
git log -1
git remote -v

# Verificar autenticación
git ls-remote origin
```

### Ver Errores de Python

```bash
# Ejecutar script con debug
railway run python3 -u /scripts/commit_automator.py

# Ver traceback completo
railway run python3 -c "import traceback; exec(open('/scripts/commit_automator.py').read())"
```

### Reiniciar Servicio

```bash
# Desde Railway Dashboard:
# Service → Settings → Restart

# O redeploy:
railway up
```

---

## Actualizar Scripts

### Actualizar desde GitHub

```bash
# En tu máquina local
cd C:\Users\leoan\Desktop\commitDiario

# Editar scripts
notepad scripts\commit_automator.py

# Push cambios
git add scripts/
git commit -m "Update automation scripts"
git push

# Railway redespleará automáticamente
```

### Actualizar Workflow de n8n

```bash
# Editar workflow localmente
notepad n8n-workflow.json

# Push
git add n8n-workflow.json
git commit -m "Update n8n workflow"
git push

# En n8n:
# 1. Exportar workflow actual (backup)
# 2. Importar nuevo workflow desde archivo
# 3. Activar workflow
```

---

## Limpieza y Mantenimiento

### Limpiar Logs Antiguos

```bash
railway run bash

# Limpiar logs
rm -f /logs/*.json

# O mantener solo los últimos 10
cd /logs
ls -t *.json | tail -n +11 | xargs rm -f
```

### Limpiar Ramas Antiguas (Modo PR)

```bash
railway run bash

cd /repo
git branch -a | grep auto-contribution | xargs git branch -D
git push origin --delete $(git branch -r | grep auto-contribution | sed 's/origin\///')
```

---

## Cambiar Modo de Operación

### De Commits Directos a Pull Requests

```bash
# 1. Editar config.json
notepad config\config.json
# Cambiar: "use_pr_workflow": true

# 2. Agregar token de GitHub en Railway
railway variables set GITHUB_TOKEN=ghp_tu_token

# 3. Push cambios
git add config/config.json
git commit -m "Enable PR workflow mode"
git push

# 4. En n8n, importar n8n-workflow-pr.json
```

### De Pull Requests a Commits Directos

```bash
# 1. Editar config.json
notepad config\config.json
# Cambiar: "use_pr_workflow": false

# 2. Push cambios
git add config/config.json
git commit -m "Disable PR workflow mode"
git push

# 3. En n8n, importar n8n-workflow.json
```

---

## Comandos de Emergencia

### Detener Automatización

```bash
# En n8n:
# Workflows → Tu workflow → Desactivar (toggle rojo)
```

### Pausar Servicio

```bash
# Railway Dashboard:
# Service → Settings → Sleep
```

### Eliminar Todo y Empezar de Nuevo

```bash
# Railway Dashboard:
# Service → Settings → Delete Service

# Luego vuelve a desplegar desde GitHub
```

---

## Checklist de Mantenimiento Semanal

```bash
# 1. Verificar que el workflow está activo
# n8n → Workflows → Verificar toggle verde

# 2. Ver últimas ejecuciones
# n8n → Executions → Verificar ejecuciones exitosas

# 3. Verificar commits en GitHub
# https://github.com/TU_USUARIO/commitDiario/commits

# 4. Ver logs de errores
railway logs | grep -i error

# 5. Verificar uso de créditos
# Railway Dashboard → Usage
```

---

## Enlaces Útiles

### Railway

- Dashboard: https://railway.app/dashboard
- Documentación: https://docs.railway.app/

### n8n

- Tu instancia: https://tu-proyecto.railway.app
- Documentación: https://docs.n8n.io/

### GitHub

- Tu repositorio: https://github.com/TU_USUARIO/commitDiario
- Tokens: https://github.com/settings/tokens

---

## Tips y Trucos

### Ejecutar Múltiples Comandos

```bash
# Encadenar comandos
railway run bash -c "cd /repo && git status && git log -5"
```

### Copiar Archivos desde/hacia el Contenedor

```bash
# No es posible directamente con Railway
# Alternativa: Usar git para sincronizar archivos
```

### Backup de Configuración

```bash
# Exportar configuración actual
railway run cat /config/config.json > config_backup.json

# Exportar workflow de n8n
# n8n → Workflows → Export → Guardar JSON
```

### Cambiar Zona Horaria

```bash
# Actualizar variables en Railway
railway variables set GENERIC_TIMEZONE=America/Mexico_City
railway variables set TZ=America/Mexico_City

# Redeploy
railway up
```

---

## Comandos Más Usados (Top 10)

```bash
# 1. Ver logs en tiempo real
railway logs -f

# 2. Acceder al contenedor
railway run bash

# 3. Probar commit manual
railway run python3 /scripts/commit_automator.py

# 4. Ver configuración
railway run cat /config/config.json

# 5. Ver estado de Git
railway run bash -c "cd /repo && git status"

# 6. Ver commits recientes
railway run bash -c "cd /repo && git log --oneline -5"

# 7. Ver variables de entorno
railway variables

# 8. Redeploy
railway up

# 9. Test de configuración
railway run python3 /scripts/test_setup.py

# 10. Ver remoto de Git
railway run bash -c "cd /repo && git remote -v"
```

---

¿Necesitas más ayuda? Consulta la [documentación completa](README.md).
