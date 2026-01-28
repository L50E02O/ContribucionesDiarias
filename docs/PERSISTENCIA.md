# Guía de Persistencia de Datos en Railway

## El Problema: ¿Por qué se pierde todo en cada deploy?

Los contenedores Docker son **efímeros** por naturaleza. Esto significa que:

- Cada deploy crea un contenedor completamente nuevo
- Todo lo que esté dentro del contenedor se borra
- Los archivos, configuraciones y datos se pierden

### ¿Qué se pierde sin configuración de persistencia?

1. **Workflows de n8n** - Tus automatizaciones configuradas
2. **Credenciales de n8n** - Tokens y configuraciones guardadas
3. **Historial de ejecuciones** - Logs de workflows ejecutados
4. **Repositorio Git** - El repositorio clonado en `/repo`
5. **Configuración de Git** - Usuario, email, remotes

---

## La Solución: Dos Enfoques

### ⚠️ Importante: Persistencia Temporal vs Permanente

**Persistencia Temporal (sin volúmenes)**:
- ✅ Los datos persisten **mientras el contenedor NO se reinicie**
- ❌ Los datos se pierden cuando Railway hace un redeploy
- ❌ Los datos se pierden si el contenedor se reinicia por cualquier motivo
- ✅ Útil para pruebas o si no planeas hacer redeploys frecuentes

**Persistencia Permanente (con volúmenes)**:
- ✅ Los datos persisten **incluso después de redeploys**
- ✅ Los datos persisten después de reinicios del contenedor
- ✅ Solución recomendada para producción

### 1. Volumen Persistente (Para n8n)

**Qué es**: Un disco virtual que Railway mantiene entre deploys.

**Configuración**:

1. Railway → Tu servicio → **Settings** → **Volumes**
2. Click **"Add Volume"**
3. Configuración:
   ```
   Mount Path: /home/node/.n8n
   Size: 0.5 GB (máximo en plan gratuito)
   ```
4. Click **"Add"**

**Qué preserva**:
- ✅ Workflows de n8n
- ✅ Credenciales guardadas
- ✅ Configuración de n8n
- ✅ Historial de ejecuciones

**Costo en Plan Gratuito**:
- ✅ Volúmenes están disponibles en el plan gratuito
- 📦 Máximo 0.5 GB por volumen
- 📦 Máximo 1 volumen por proyecto
- 💰 $0.15 por GB/mes (se cobra del crédito mensual de $5)
- 💡 Con 0.5 GB, el costo es ~$0.075/mes (muy bajo)

---

### 2. Clonación Automática (Para el Repositorio Git)

**Qué es**: El script clona automáticamente el repositorio en cada inicio.

**Ventajas**:
- No necesitas volumen adicional
- Siempre tienes la última versión del repo
- Configuración más simple
- Sin costo adicional

**Cómo funciona**:

1. En cada inicio del contenedor, el script verifica si `/repo/.git` existe
2. Si no existe, clona automáticamente el repositorio desde GitHub
3. Usa el token de GitHub para autenticación
4. Configura Git con tus credenciales

**Configuración necesaria**:

#### Variables de entorno en Railway:

```bash
GITHUB_TOKEN=ghp_tu_token_con_permisos_repo
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@ejemplo.com
```

#### Configuración en `/config/config.json`:

```json
{
  "github_repo_owner": "tu_usuario_github",
  "github_repo_name": "nombre_del_repo"
}
```

---

## Configuración Paso a Paso

### Paso 1: Configurar Volumen para n8n (Opcional pero Recomendado)

**Si NO usas volúmenes**:
- Los datos persisten mientras el contenedor no se reinicie
- Si haces un redeploy, perderás los workflows de n8n
- Deberás reimportar los workflows después de cada redeploy

**Si usas volúmenes** (recomendado):

1. Ve a Railway → Tu servicio → **Settings**
2. Scroll hasta **"Volumes"**
3. Si NO hay volumen configurado:
   - Click **"Add Volume"**
   - Mount Path: `/home/node/.n8n`
   - Size: `0.5 GB` (máximo en plan gratuito)
   - Click **"Add"**

Railway reiniciará el servicio automáticamente.

---

### Paso 2: Configurar Variables de Entorno

1. Ve a Railway → Tu servicio → **Variables**
2. Agrega las siguientes variables:

```bash
# Token de GitHub (OBLIGATORIO)
GITHUB_TOKEN=ghp_tu_token_aqui

# Configuración de Git (OBLIGATORIO)
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@ejemplo.com

# Configuración de n8n
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=TuPasswordSegura123!
N8N_ENCRYPTION_KEY=clave-aleatoria-larga-minimo-32-caracteres

# Zona horaria
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota
```

---

### Paso 3: Configurar config.json

Conecta al contenedor y edita el archivo:

```bash
# Conectar vía Railway CLI
railway login
railway link
railway run bash

# Editar config.json
cat > /config/config.json << 'EOF'
{
  "commits_per_day": 1,
  "repo_path": "/repo",
  "commit_message_template": "Commit automático del {date} #{number}",
  "auto_push": true,
  "timezone": "America/Bogota",
  "github_repo_owner": "TU_USUARIO_GITHUB",
  "github_repo_name": "NOMBRE_DEL_REPO",
  "use_pr_workflow": false
}
EOF
```

**Reemplaza**:
- `TU_USUARIO_GITHUB`: Tu usuario de GitHub
- `NOMBRE_DEL_REPO`: El nombre del repositorio donde se harán los commits

---

### Paso 4: Verificar Configuración

Después de configurar, verifica que todo funcione:

```bash
# Conectar al contenedor
railway run bash

# 1. Verificar volumen de n8n
ls -la /home/node/.n8n
# Deberías ver archivos de n8n

# 2. Verificar que el repo se clonó
cd /repo
git remote -v
# Deberías ver el remote configurado

# 3. Verificar configuración de Git
git config user.name
git config user.email
# Deberían mostrar tus datos

# 4. Probar commit manual
python3 /scripts/commit_automator.py
# Debería hacer un commit y push exitoso
```

---

## Verificación de Persistencia

### Probar que n8n persiste:

1. Importa un workflow en n8n
2. Guárdalo
3. Haz un redeploy: Railway → Settings → **"Redeploy"**
4. Espera a que inicie
5. Accede a n8n nuevamente
6. ✅ El workflow debería seguir ahí

### Probar que el repo se clona automáticamente:

1. Conecta al contenedor: `railway run bash`
2. Borra el repo: `rm -rf /repo/*`
3. Sal del contenedor: `exit`
4. Haz un redeploy
5. Conecta nuevamente: `railway run bash`
6. Verifica: `cd /repo && git remote -v`
7. ✅ El repo debería estar clonado nuevamente

---

## Preguntas Frecuentes

### ¿Puedo mantener datos sin volúmenes si no reinicio el contenedor?

**Respuesta**: **SÍ**, pero con limitaciones importantes:

✅ **Lo que SÍ funciona**:
- Los datos persisten en el sistema de archivos del contenedor
- Los workflows de n8n se mantienen
- La configuración se mantiene
- El repositorio Git se mantiene

❌ **Lo que NO funciona**:
- Si Railway hace un redeploy automático, pierdes todo
- Si el contenedor se reinicia por error, pierdes todo
- Si actualizas el código (push a GitHub), Railway puede hacer redeploy
- Si cambias variables de entorno, Railway puede reiniciar el servicio

**Recomendación**:
- Si solo estás probando y no planeas hacer redeploys: ✅ Funciona sin volúmenes
- Si quieres persistencia garantizada: ✅ Usa volúmenes (costo mínimo ~$0.075/mes)

### ¿Por qué no usar volumen para `/repo` también?

**Respuesta**: No es necesario porque:
- El repositorio se clona automáticamente en segundos
- Siempre tienes la versión más actualizada
- Ahorra espacio en disco (y potencialmente costos)
- Más simple de mantener

### ¿Qué pasa si cambio de repositorio?

**Respuesta**: Solo actualiza `config.json` con el nuevo repositorio:

```json
{
  "github_repo_owner": "nuevo_usuario",
  "github_repo_name": "nuevo_repo"
}
```

En el próximo inicio, clonará el nuevo repositorio.

### ¿Necesito el token de GitHub para commits directos?

**Respuesta**: **Sí**, el token es necesario para:
- Clonar el repositorio (si es privado)
- Hacer push de commits
- Autenticación automática sin contraseña

### ¿Qué permisos necesita el token?

**Respuesta**: Scope `repo` (acceso completo a repositorios).

Para crear el token:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Selecciona scope: `repo`
5. Copia el token

### ¿Puedo usar repositorios privados?

**Respuesta**: **Sí**, con el token de GitHub puedes usar repositorios privados sin problema.

### ¿Qué pasa si el token expira?

**Respuesta**: 
1. Los tokens clásicos no expiran por defecto
2. Si usas tokens con expiración, genera uno nuevo antes de que expire
3. Actualiza la variable `GITHUB_TOKEN` en Railway
4. Redeploy el servicio

---

## Costos de Persistencia

### Plan Gratuito de Railway:

- **Crédito mensual**: $5 USD
- **Volumen máximo**: 0.5 GB por volumen
- **Costo del volumen**: $0.15 por GB/mes
- **Costo estimado con 0.5 GB**: ~$0.075/mes

### Uso Real Estimado:

```
Servicio n8n + volumen 0.5GB:
- Costo del servicio: ~$1.50-2.00/mes
- Costo del volumen: ~$0.075/mes
- Total: ~$1.58-2.08/mes
- Crédito gratis: $5.00
- Resultado: GRATIS (dentro del crédito mensual)
```

### Sin Volúmenes (Persistencia Temporal):

- **Costo**: $0 adicional
- **Limitación**: Los datos se pierden en cada redeploy
- **Ventaja**: Funciona perfectamente mientras no reinicies el contenedor

---

## Solución de Problemas

### El volumen no se monta:

**Síntomas**: Los workflows se pierden en cada deploy

**Solución**:
1. Verifica en Railway → Settings → Volumes
2. Debe aparecer: `/home/node/.n8n` → 0.5 GB (o el tamaño que configuraste)
3. Si no está, agrégalo
4. Redeploy el servicio

**Nota**: Si no usas volúmenes, esto es normal. Los datos solo persisten mientras el contenedor no se reinicie.

### El repositorio no se clona:

**Síntomas**: Error "No hay repositorio remoto configurado"

**Solución**:
1. Verifica las variables de entorno:
   - `GITHUB_TOKEN` debe estar configurado
   - Debe tener permisos `repo`
2. Verifica `config.json`:
   - `github_repo_owner` debe estar configurado
   - `github_repo_name` debe estar configurado
3. Verifica los logs: `railway logs`
4. Busca mensajes de error relacionados con Git

### Error "Authentication failed":

**Síntomas**: No puede clonar o hacer push

**Solución**:
1. Verifica que el token sea válido
2. Verifica que tenga permisos `repo`
3. Genera un nuevo token si es necesario
4. Actualiza `GITHUB_TOKEN` en Railway

---

## Checklist de Persistencia

Usa este checklist para verificar que todo esté configurado:

- [ ] Volumen montado en `/home/node/.n8n`
- [ ] Variable `GITHUB_TOKEN` configurada
- [ ] Variable `GIT_USER_NAME` configurada
- [ ] Variable `GIT_USER_EMAIL` configurada
- [ ] `config.json` tiene `github_repo_owner`
- [ ] `config.json` tiene `github_repo_name`
- [ ] Workflow importado y activado en n8n
- [ ] Prueba manual exitosa: `python3 /scripts/commit_automator.py`
- [ ] Commit apareció en GitHub
- [ ] Redeploy realizado y workflows persisten

Si todos los checks están ✅, tu sistema está correctamente configurado y persistirá entre deploys.

---

## Resumen

### Lo que PERSISTE (con volumen):
- ✅ Workflows de n8n
- ✅ Credenciales de n8n
- ✅ Configuración de n8n
- ✅ Persiste incluso después de redeploys

### Lo que PERSISTE temporalmente (sin volumen):
- ✅ Workflows de n8n (mientras el contenedor no se reinicie)
- ✅ Credenciales de n8n (mientras el contenedor no se reinicie)
- ⚠️ Se pierde en cada redeploy o reinicio

### Lo que se REGENERA automáticamente:
- ✅ Repositorio Git (clonado en cada inicio)
- ✅ Configuración de Git (aplicada en cada inicio)

### Lo que NUNCA se pierde:
- ✅ Variables de entorno (guardadas en Railway)
- ✅ Commits en GitHub (están en el repositorio remoto)
- ✅ Configuración del servicio (Railway la mantiene)

**Resultado**: 
- **Con volúmenes**: Sistema completamente funcional y persistente entre deploys. 🎉
- **Sin volúmenes**: Sistema funcional mientras no se reinicie el contenedor. ⚠️
