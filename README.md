# 🤖 Commit Diario Automático para GitHub

Sistema automatizado para mantener una racha de contribuciones en GitHub mediante commits diarios programados.

## 📋 Características

- ✅ Commits automáticos diarios
- 🔢 Número configurable de commits por día
- ⏰ Ejecución programada con n8n
- 🐳 Despliegue sencillo con Docker
- 🌍 Zona horaria configurable (UTC-5 por defecto)
- 📊 Logging completo de operaciones
- 🔄 Push automático a GitHub

## 🚀 Instalación Rápida

### Prerrequisitos

- Docker y Docker Compose instalados
- Git configurado
- Cuenta de GitHub con token de acceso personal (PAT)

### Pasos de Instalación

1. **Clonar o crear el directorio del proyecto**

```bash
cd commitDiario
```

2. **Configurar el repositorio Git**

Opción A: Inicializar un nuevo repositorio
```bash
mkdir repo
cd repo
git init
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd ..
```

Opción B: Clonar un repositorio existente
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git repo
```

3. **Configurar credenciales de Git (para push automático)**

Edita el archivo `config/config.json` con tus datos:

```json
{
  "commits_per_day": 1,
  "repo_path": "/repo",
  "commit_message_template": "Commit automático del {date} #{number}",
  "git_user_name": "Tu Nombre",
  "git_user_email": "tu-email@ejemplo.com",
  "auto_push": true,
  "timezone": "America/Bogota"
}
```

4. **Configurar el token de GitHub (para push HTTPS)**

Si usas HTTPS, necesitas configurar un token de acceso personal:

```bash
cd repo
git config credential.helper store
git push  # Te pedirá usuario y token, se guardará para futuros push
cd ..
```

**Crear un token de acceso personal:**
- Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token → Selecciona `repo` (acceso completo a repositorios)
- Copia el token y úsalo como contraseña en el paso anterior

5. **Iniciar el sistema con Docker**

```bash
docker-compose up -d
```

6. **Acceder a n8n**

- URL: http://localhost:5678
- Usuario: `admin`
- Contraseña: `admin123`

7. **Importar el workflow**

- En n8n, ve a "Workflows" → "Import from File"
- Selecciona el archivo `n8n-workflow.json`
- Activa el workflow (toggle en la esquina superior derecha)

## ⚙️ Configuración

### Archivo `config/config.json`

```json
{
  "commits_per_day": 1,           // Número de commits por día
  "repo_path": "/repo",           // Ruta del repositorio (no cambiar)
  "commit_message_template": "Commit automático del {date} #{number}",
  "git_user_name": "Commit Bot",  // Tu nombre de usuario Git
  "git_user_email": "bot@commitdiario.com",  // Tu email Git
  "auto_push": true,              // Push automático después del commit
  "timezone": "America/Bogota"    // Zona horaria (UTC-5)
}
```

### Cambiar el número de commits diarios

Simplemente edita el valor de `commits_per_day` en `config/config.json`:

```json
{
  "commits_per_day": 3,  // Hará 3 commits cada día
  ...
}
```

No es necesario reiniciar Docker después de cambiar la configuración.

### Cambiar la hora de ejecución

El workflow de n8n está configurado para ejecutarse cada 24 horas. Para cambiar la hora:

1. Accede a n8n (http://localhost:5678)
2. Abre el workflow "GitHub Daily Commit Automation"
3. Haz clic en el nodo "Schedule Trigger"
4. Modifica el horario según tus necesidades
5. Guarda el workflow

### Zona Horaria

El sistema está configurado para UTC-5 (Colombia, Ecuador, Perú). Para cambiar:

Edita `docker-compose.yml`:

```yaml
environment:
  - GENERIC_TIMEZONE=America/New_York  # Cambia según tu zona
  - TZ=America/New_York
```

Lista de zonas horarias: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 🧪 Prueba Manual

Para probar el script sin esperar a la ejecución programada:

```bash
docker-compose exec n8n python3 /scripts/commit_automator.py
```

## 📊 Estructura del Proyecto

```
commitDiario/
├── docker-compose.yml        # Configuración de Docker
├── n8n-workflow.json        # Workflow de n8n para importar
├── README.md                # Este archivo
├── config/
│   └── config.json         # Configuración del script
├── scripts/
│   └── commit_automator.py # Script Python de automatización
└── repo/                   # Tu repositorio Git (crear/clonar aquí)
```

## 🔧 Comandos Útiles

### Docker

```bash
# Iniciar el sistema
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el sistema
docker-compose down

# Reiniciar
docker-compose restart

# Ver logs solo de n8n
docker-compose logs -f n8n
```

### Acceso al contenedor

```bash
# Acceder al shell del contenedor
docker-compose exec n8n sh

# Ejecutar el script manualmente
docker-compose exec n8n python3 /scripts/commit_automator.py

# Ver el estado del repositorio
docker-compose exec n8n sh -c "cd /repo && git status"
```

## 🐛 Solución de Problemas

### Error: "No hay repositorio remoto configurado"

**Solución:**
```bash
cd repo
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

### Error: "Authentication failed"

**Solución:**
1. Crea un token de acceso personal en GitHub
2. Usa el token como contraseña al hacer push
3. O configura SSH keys

### El script no se ejecuta automáticamente

**Verificar:**
1. El workflow está activado en n8n (toggle verde)
2. Los logs de n8n: `docker-compose logs -f n8n`
3. Ejecuta manualmente para ver errores: `docker-compose exec n8n python3 /scripts/commit_automator.py`

### Error de permisos

**Solución:**
```bash
chmod +x scripts/commit_automator.py
```

## 📝 Notas Importantes

1. **Uso Responsable**: Este sistema está diseñado para mantener actividad en repositorios personales. Úsalo de manera responsable.

2. **Repositorios Privados**: Funciona perfectamente con repositorios privados y públicos.

3. **Backup**: Asegúrate de tener backups de tu configuración y del repositorio.

4. **Seguridad**: 
   - Cambia las credenciales de n8n en `docker-compose.yml`
   - No compartas tu token de GitHub
   - Usa variables de entorno para información sensible

5. **Persistencia**: Los datos de n8n se guardan en un volumen Docker, por lo que persisten entre reinicios.

## 🔐 Seguridad Mejorada

Para mayor seguridad, usa variables de entorno para credenciales:

1. Crea un archivo `.env`:

```env
GIT_USER_NAME=Tu Nombre
GIT_USER_EMAIL=tu-email@ejemplo.com
GITHUB_TOKEN=tu_token_aqui
N8N_BASIC_AUTH_PASSWORD=tu_password_seguro
```

2. Modifica `config/config.json` para usar variables de entorno (requiere modificación del script).

## 🔄 Modo Pull Request

Este sistema ahora soporta dos modos de operación:

### Modo 1: Commits Directos (por defecto)
Hace commits directamente a la rama principal.

### Modo 2: Pull Requests Automáticos
Crea una rama, hace commit, crea PR y lo mergea automáticamente.

**Para activar el modo PR:**

1. Edita `config/config.json`:
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

2. Importa el workflow `n8n-workflow-pr.json` en vez de `n8n-workflow.json`

3. Crea un token de GitHub con permisos completos de `repo`

**Métodos de merge disponibles:**
- `squash` - Combina todos los commits en uno (recomendado)
- `merge` - Merge commit tradicional
- `rebase` - Rebase y fast-forward

## ☁️ Despliegue en Railway (24/7 Gratis)

Para que el sistema funcione automáticamente 24/7 sin tu computadora encendida, despliégalo en Railway:

**¿Por qué Railway?**
- ✅ **$5 crédito gratis/mes** (suficiente para este proyecto)
- ✅ **Sin sleep automático** (funciona 24/7)
- ✅ **Cron jobs funcionan** perfectamente
- ✅ **Setup en 5 minutos**

**Ver guía completa:** [DEPLOYMENT.md](DEPLOYMENT.md)

### Inicio Rápido - Railway:

```bash
# 1. Push tu proyecto a GitHub
git init
git add .
git commit -m "Initial commit: Automated GitHub contributions"
git remote add origin https://github.com/TU_USUARIO/commit-automation.git
git push -u origin main

# 2. Ve a railway.app y regístrate con GitHub
# 3. New Project → Deploy from GitHub repo
# 4. Selecciona tu repositorio
# 5. Configura variables de entorno en Railway
# 6. ¡Accede a n8n y activa el workflow!
```

**Guía detallada paso a paso:** [DEPLOYMENT.md](DEPLOYMENT.md)

## 📈 Mejoras Futuras

- [x] Sistema de Pull Requests automáticos
- [x] Despliegue en cloud (Railway, Render, Fly.io)
- [ ] Notificaciones por email/Slack en caso de error
- [ ] Dashboard web para monitoreo
- [ ] Soporte para múltiples repositorios
- [ ] Estadísticas de contribuciones
- [ ] Integración con webhooks de GitHub

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este sistema, no dudes en crear un issue o pull request.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👨‍💻 Autor

Creado con ❤️ para mantener vivas las rachas de GitHub.

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o consulta la documentación de [n8n](https://docs.n8n.io/) y [Docker](https://docs.docker.com/).
