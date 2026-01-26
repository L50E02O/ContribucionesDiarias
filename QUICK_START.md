# ⚡ Guía de Inicio Rápido

Configura tu sistema de commits diarios en 5 minutos.

## 🎯 Paso a Paso

### 1️⃣ Preparar el Repositorio GitHub

```bash
# Opción A: Crear un nuevo repositorio
# Ve a GitHub → New Repository → Crea "daily-commits" (puede ser privado)

# Opción B: Usar un repositorio existente
# Asegúrate de tener la URL del repositorio
```

### 2️⃣ Configurar el Proyecto

```bash
# Clonar o clonar este repositorio existente en tu máquina
cd commitDiario

# Crear el directorio del repositorio
mkdir repo
cd repo

# Inicializar Git y conectar con GitHub
git init
git config user.name "Tu Nombre"
git config user.email "tu-email@example.com"
git remote add origin https://github.com/TU_USUARIO/daily-commits.git

# Crear commit inicial
echo "# Daily Commits" > README.md
git add README.md
git commit -m "Initial commit"
git branch -M main
git push -u origin main
# Usa tu token de GitHub como contraseña

cd ..
```

### 3️⃣ Crear Token de GitHub

1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token (classic)"
3. Selecciona scope: `repo` (acceso completo a repositorios)
4. Genera y copia el token
5. Guárdalo de forma segura

### 4️⃣ Configurar el Sistema

```bash
# Edita config/config.json con tus datos
{
  "commits_per_day": 1,
  "git_user_name": "Tu Nombre Real",
  "git_user_email": "tu-email@example.com",
  "auto_push": true
}
```

### 5️⃣ Iniciar Docker

```bash
# Iniciar el sistema
docker-compose up -d

# Ver los logs (opcional)
docker-compose logs -f
```

### 6️⃣ Configurar n8n

1. Abre: http://localhost:5678
2. Login:
   - Usuario: `admin`
   - Contraseña: `admin123`
3. Import workflow:
   - Click "Workflows" → "Import from File"
   - Selecciona `n8n-workflow.json`
4. Activa el workflow:
   - Toggle en la esquina superior derecha
   - Debe estar en verde

### 7️⃣ Probar Manualmente

```bash
# Ejecutar una prueba
docker-compose exec n8n python3 /scripts/commit_automator.py

# Ver los commits generados
cd repo
git log
cd ..
```

## ✅ Verificación

Si ves esto, ¡todo funciona! ✨

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

## 🎛️ Personalización Rápida

### Cambiar número de commits diarios

Edita `config/config.json`:
```json
{
  "commits_per_day": 3  // Ahora hará 3 commits por día
}
```

### Cambiar hora de ejecución

1. Abre n8n (http://localhost:5678)
2. Edita el workflow
3. Click en "Schedule Trigger"
4. Cambia el intervalo o usa cron:
   - Cada 24h a las 9 AM: `0 9 * * *`
   - Cada 24h a las 6 PM: `0 18 * * *`
   - Cada 12h: Interval 12 hours

### Cambiar mensaje de commit

Edita `config/config.json`:
```json
{
  "commit_message_template": "🎯 Daily activity {date}"
}
```

## 🐛 Problemas Comunes

### "Authentication failed"
**Solución:** Usa tu token de GitHub como contraseña, no tu contraseña real.

### "No remote configured"
```bash
cd repo
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
cd ..
```

### "Permission denied"
```bash
chmod +x scripts/*.py scripts/*.sh
```

### Docker no inicia
```bash
# Ver los logs de error
docker-compose logs

# Reiniciar todo
docker-compose down
docker-compose up -d
```

## 🔄 Modo Pull Request (Opcional)

Si prefieres que el sistema cree PRs en vez de commits directos:

1. **Edita `config/config.json`:**
```json
{
  "use_pr_workflow": true,
  "github_token": "ghp_tu_token_con_permisos_repo",
  "github_repo_owner": "tu_usuario",
  "github_repo_name": "tu_repo"
}
```

2. **Importa el workflow de PRs:**
   - En n8n, importa `n8n-workflow-pr.json` en vez del workflow normal

3. **Prueba:**
```bash
docker-compose exec n8n python3 /scripts/pr_automator.py
```

## ☁️ Desplegar en Railway (24/7)

Para que funcione automáticamente sin tu computadora:

**Railway** (Recomendado):
- ✅ $5 crédito gratis/mes
- ✅ Sin sleep (funciona 24/7)
- ✅ Setup en 5 minutos

**Pasos rápidos:**
1. Push proyecto a GitHub
2. Conecta Railway con tu repo
3. Configura variables de entorno
4. ¡Listo!

**Guía completa:** [DEPLOYMENT.md](DEPLOYMENT.md)

## 📞 Necesitas Ayuda?

- Lee el `README.md` completo para más detalles
- Ver despliegue cloud: `DEPLOYMENT.md`
- Verifica los logs: `docker-compose logs -f`
- Ejecuta el test: `docker-compose exec n8n python3 /scripts/test_commit.py`

## 🎉 ¡Listo!

Tu sistema ahora generará commits automáticamente cada 24 horas. Verifica tu perfil de GitHub mañana para ver tu primera contribución automática.

**Recuerda:** Este sistema está diseñado para repositorios personales. Úsalo de forma responsable.
