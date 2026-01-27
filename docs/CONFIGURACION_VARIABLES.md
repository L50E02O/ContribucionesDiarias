# Sistema de Configuración - Variables de Entorno y config.json

Guía completa sobre cómo funciona el sistema de configuración del proyecto.

---

## Orden de Prioridad

El sistema de configuración sigue este orden de prioridad (de mayor a menor):

```
1. Variables de Entorno (Railway/Sistema) ← MÁXIMA PRIORIDAD
2. config.json
3. Valores por defecto en el código
```

**Esto significa**: Si defines `GIT_USER_NAME` como variable de entorno en Railway, ese valor se usará aunque `config.json` tenga un valor diferente.

---

## Variables de Entorno Disponibles

### Variables que se Leen Automáticamente

El sistema lee estas variables de entorno y las usa con prioridad sobre `config.json`:

| Variable de Entorno | Clave en config.json | Descripción |
|---------------------|----------------------|-------------|
| `GIT_USER_NAME` | `git_user_name` | Nombre para los commits de Git |
| `GIT_USER_EMAIL` | `git_user_email` | Email para los commits de Git |
| `GITHUB_TOKEN` | `github_token` | Token de GitHub para PRs |
| `GENERIC_TIMEZONE` | `timezone` | Zona horaria del sistema |

### Ejemplo de Uso

**En Railway (Variables):**
```bash
GIT_USER_NAME=Leonardo Holguin
GIT_USER_EMAIL=leoanthonyholguinchavez@gmail.com
GITHUB_TOKEN=ghp_tu_token_aqui
GENERIC_TIMEZONE=America/Bogota
```

**En config.json:**
```json
{
 "git_user_name": "Commit Bot",
 "git_user_email": "bot@example.com"
}
```

**Resultado**: Se usará `Leonardo Holguin` y `leoanthonyholguinchavez@gmail.com` (de las variables de entorno).

---

## Archivo config.json

### Estructura Completa

```json
{
 "_comment": "Las variables de entorno tienen prioridad sobre este archivo",
 "_comment_env": "Variables de entorno: GIT_USER_NAME, GIT_USER_EMAIL, GITHUB_TOKEN, GENERIC_TIMEZONE",
 "commits_per_day": 1,
 "repo_path": "/repo",
 "commit_message_template": "Commit automático del {date} #{number}",
 "_comment_git": "Estos valores se sobrescriben con GIT_USER_NAME y GIT_USER_EMAIL si existen",
 "git_user_name": "Tu Nombre",
 "git_user_email": "tu-email@ejemplo.com",
 "auto_push": true,
 "_comment_timezone": "Se sobrescribe con GENERIC_TIMEZONE si existe",
 "timezone": "America/Bogota",
 "_comment_pr_mode": "Configuración para automatización de Pull Requests",
 "use_pr_workflow": false,
 "_comment_token": "Se sobrescribe con GITHUB_TOKEN si existe",
 "github_token": "",
 "github_repo_owner": "tu_usuario",
 "github_repo_name": "commitDiario",
 "merge_method": "squash",
 "auto_cleanup_branch": true
}
```

### Parámetros Explicados

#### Commits Básicos

- **`commits_per_day`**: Número de commits a realizar cada día
 - Tipo: `number`
 - Ejemplo: `1`, `3`, `5`
 - No se puede sobrescribir con variable de entorno

- **`repo_path`**: Ruta al repositorio Git
 - Tipo: `string`
 - Default: `"/repo"`
 - En Railway siempre debe ser `"/repo"`

- **`commit_message_template`**: Plantilla del mensaje de commit
 - Tipo: `string`
 - Variables: `{date}`, `{number}`
 - Ejemplo: `" Automated commit {date} #{number}"`

#### Configuración de Git

- **`git_user_name`**: Nombre del autor del commit
 - Tipo: `string`
 - Variable de entorno: `GIT_USER_NAME` 
 - Ejemplo: `"Leonardo Holguin"`

- **`git_user_email`**: Email del autor del commit
 - Tipo: `string`
 - Variable de entorno: `GIT_USER_EMAIL` 
 - Ejemplo: `"leoanthonyholguinchavez@gmail.com"`

#### Zona Horaria

- **`timezone`**: Zona horaria para timestamps
 - Tipo: `string`
 - Variable de entorno: `GENERIC_TIMEZONE` 
 - Ejemplo: `"America/Bogota"`, `"America/Lima"`, `"America/Mexico_City"`

#### Modo Pull Request

- **`use_pr_workflow`**: Activar modo Pull Request
 - Tipo: `boolean`
 - Valores: `true`, `false`
 - No se puede sobrescribir con variable de entorno

- **`github_token`**: Token de GitHub
 - Tipo: `string`
 - Variable de entorno: `GITHUB_TOKEN` 
 - Ejemplo: `"ghp_..."`
 - **Recomendación**: Usar variable de entorno por seguridad

- **`github_repo_owner`**: Usuario/organización del repo
 - Tipo: `string`
 - Ejemplo: `"L50E02O"`

- **`github_repo_name`**: Nombre del repositorio
 - Tipo: `string`
 - Ejemplo: `"commitDiario"`

- **`merge_method`**: Método de merge para PRs
 - Tipo: `string`
 - Valores: `"squash"`, `"merge"`, `"rebase"`
 - Recomendado: `"squash"`

- **`auto_cleanup_branch`**: Eliminar rama después del merge
 - Tipo: `boolean`
 - Valores: `true`, `false`
 - Recomendado: `true`

---

## Configuración en Railway

### Método Recomendado: Variables de Entorno

**Ventajas:**
- Más seguro (no se suben a Git)
- Fácil de cambiar sin redeploy
- Tienen prioridad sobre config.json

**Cómo configurar:**

1. Ve a Railway → Tu proyecto → Variables
2. Agrega las variables:

```bash
# Obligatorias
GIT_USER_NAME=Tu Nombre Completo
GIT_USER_EMAIL=tu-email@github.com
GENERIC_TIMEZONE=America/Bogota

# Opcional (solo para modo PR)
GITHUB_TOKEN=ghp_tu_token_aqui
```

3. Railway reinicia automáticamente

### Verificar Configuración

```bash
# Ver variables de entorno
railway run bash -c "env | grep GIT"
railway run bash -c "env | grep GITHUB"
railway run bash -c "env | grep TIMEZONE"

# Probar el script
railway run python3 /scripts/commit_automator.py
```

Deberías ver:
```
 Variable de entorno GIT_USER_NAME cargada
 Variable de entorno GIT_USER_EMAIL cargada
 Variable de entorno GENERIC_TIMEZONE cargada
```

---

## Configuración Local (Desarrollo)

### Usar archivo .env

Para desarrollo local, puedes usar un archivo `.env`:

1. **Crea el archivo `.env`** (ya existe `.env.example` como plantilla):

```bash
# Copiar el ejemplo
cp .env.example .env

# Editar con tus valores
notepad .env
```

2. **Contenido del .env**:

```bash
# Configuración de Git
GIT_USER_NAME=Tu Nombre
GIT_USER_EMAIL=tu-email@github.com

# Zona horaria
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota

# Token de GitHub (opcional)
GITHUB_TOKEN=ghp_tu_token_aqui
```

3. **Cargar variables de entorno** (en PowerShell):

```powershell
# Leer el archivo .env y cargar variables
Get-Content .env | ForEach-Object {
 if ($_ -match '^([^=]+)=(.*)$') {
 [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
 }
}

# Verificar
$env:GIT_USER_NAME
$env:GIT_USER_EMAIL
```

4. **Ejecutar el script**:

```bash
python scripts/commit_automator.py
```

**Importante**: El archivo `.env` está en `.gitignore` y nunca se subirá a GitHub.

---

## Casos de Uso

### Caso 1: Configuración Básica (Solo config.json)

**Escenario**: Desarrollo local sin variables de entorno

```json
// config.json
{
 "commits_per_day": 1,
 "git_user_name": "Leonardo",
 "git_user_email": "leo@example.com",
 "timezone": "America/Bogota",
 "use_pr_workflow": false
}
```

**Resultado**: Se usan los valores del `config.json`

### Caso 2: Railway con Variables de Entorno

**Escenario**: Producción en Railway

**Railway Variables:**
```bash
GIT_USER_NAME=Leonardo Holguin
GIT_USER_EMAIL=leoanthonyholguinchavez@gmail.com
GENERIC_TIMEZONE=America/Bogota
```

**config.json:**
```json
{
 "commits_per_day": 1,
 "git_user_name": "Commit Bot",
 "git_user_email": "bot@example.com",
 "use_pr_workflow": false
}
```

**Resultado**: 
- `git_user_name`: `"Leonardo Holguin"` (de variable de entorno)
- `git_user_email`: `"leoanthonyholguinchavez@gmail.com"` (de variable de entorno)
- `commits_per_day`: `1` (de config.json)
- `use_pr_workflow`: `false` (de config.json)

### Caso 3: Modo Pull Request

**Railway Variables:**
```bash
GIT_USER_NAME=Leonardo Holguin
GIT_USER_EMAIL=leoanthonyholguinchavez@gmail.com
GITHUB_TOKEN=ghp_tu_token_aqui
GENERIC_TIMEZONE=America/Bogota
```

**config.json:**
```json
{
 "commits_per_day": 1,
 "use_pr_workflow": true,
 "github_repo_owner": "L50E02O",
 "github_repo_name": "commitDiario",
 "merge_method": "squash"
}
```

**Resultado**: 
- Token se toma de variable de entorno (más seguro)
- Configuración de PR se toma de config.json
- Git user/email se toman de variables de entorno

---

## Mejores Prácticas de Seguridad

### Hacer

1. **Usar variables de entorno para datos sensibles**:
 - `GITHUB_TOKEN` → Variable de entorno
 - `GIT_USER_EMAIL` → Variable de entorno

2. **Usar config.json para configuración**:
 - `commits_per_day`
 - `commit_message_template`
 - `use_pr_workflow`

3. **Mantener .env en .gitignore**:
 ```gitignore
 .env
 .env.local
 .env.*.local
 ```

### NO Hacer

1. Nunca subir `.env` a Git
2. Nunca poner tokens en `config.json` que se sube a Git
3. Nunca hacer commit de credenciales

---

## Verificar Configuración

### Script de Prueba

Ejecuta el script de verificación:

```bash
railway run python3 /scripts/test_setup.py
```

Esto verificará:
- Archivo config.json existe y es válido
- Variables de entorno están configuradas
- Prioridad de configuración es correcta

### Verificación Manual

```bash
# Acceder al contenedor
railway run bash

# Ver configuración cargada
python3 << 'EOF'
import json
import os

# Cargar config.json
with open('/config/config.json') as f:
 config = json.load(f)

print(" Configuración desde config.json:")
print(f" git_user_name: {config.get('git_user_name')}")
print(f" git_user_email: {config.get('git_user_email')}")

print("\n Variables de entorno:")
print(f" GIT_USER_NAME: {os.getenv('GIT_USER_NAME')}")
print(f" GIT_USER_EMAIL: {os.getenv('GIT_USER_EMAIL')}")
print(f" GITHUB_TOKEN: {'***' if os.getenv('GITHUB_TOKEN') else 'No configurado'}")

print("\n Valores finales (con prioridad):")
final_name = os.getenv('GIT_USER_NAME') or config.get('git_user_name')
final_email = os.getenv('GIT_USER_EMAIL') or config.get('git_user_email')
print(f" git_user_name: {final_name}")
print(f" git_user_email: {final_email}")
EOF
```

---

## Ejemplos Completos

### Ejemplo 1: Configuración Mínima

**Railway Variables:**
```bash
GIT_USER_NAME=Leonardo
GIT_USER_EMAIL=leo@example.com
```

**config.json:**
```json
{
 "commits_per_day": 1,
 "use_pr_workflow": false
}
```

### Ejemplo 2: Configuración Completa con PRs

**Railway Variables:**
```bash
GIT_USER_NAME=Leonardo Holguin
GIT_USER_EMAIL=leoanthonyholguinchavez@gmail.com
GITHUB_TOKEN=ghp_tu_token_aqui_ejemplo
GENERIC_TIMEZONE=America/Bogota
```

**config.json:**
```json
{
 "commits_per_day": 1,
 "commit_message_template": " Daily automated contribution {date}",
 "auto_push": true,
 "use_pr_workflow": true,
 "github_repo_owner": "L50E02O",
 "github_repo_name": "commitDiario",
 "merge_method": "squash",
 "auto_cleanup_branch": true
}
```

---

## Solución de Problemas

### Problema: Variables de entorno no se cargan

**Síntoma**: El script usa valores de config.json aunque hay variables de entorno

**Solución**:
```bash
# Verificar que las variables existen
railway run bash -c "env | grep GIT"

# Si no aparecen, agregarlas en Railway
railway variables set GIT_USER_NAME="Tu Nombre"
railway variables set GIT_USER_EMAIL="tu@email.com"
```

### Problema: Commits con autor incorrecto

**Síntoma**: Los commits aparecen con "Commit Bot" en lugar de tu nombre

**Solución**:
1. Verifica variables de entorno en Railway
2. Asegúrate de que `GIT_USER_NAME` y `GIT_USER_EMAIL` estén configuradas
3. Redeploy el servicio

### Problema: Token no funciona

**Síntoma**: Error "Bad credentials" en modo PR

**Solución**:
```bash
# Verificar que el token está configurado
railway run bash -c "echo \$GITHUB_TOKEN | cut -c1-10"

# Debe mostrar: ghp_...
# Si no, configurarlo:
railway variables set GITHUB_TOKEN=ghp_tu_token_aqui
```

---

## Documentación Relacionada

- [Guía del Token de GitHub](GITHUB_TOKEN_GUIDE.md)
- [Configuración del Workflow](CONFIGURACION_WORKFLOW.md)
- [Comandos Rápidos](COMANDOS_RAPIDOS.md)
- [Solución de Problemas](TROUBLESHOOTING.md)

---

**¿Tienes dudas?** Revisa la [documentación completa](README.md) o abre un issue en el repositorio.
