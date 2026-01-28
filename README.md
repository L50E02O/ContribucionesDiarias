# Sistema de Commits Diarios Automáticos para GitHub

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Railway](https://img.shields.io/badge/deploy-railway-blueviolet.svg)
![n8n](https://img.shields.io/badge/automation-n8n-orange.svg)

**Mantén tu racha de contribuciones en GitHub automáticamente** 

[Inicio Rápido](docs/QUICK_START.md) • [Documentación](docs/) • [Licencia](#-licencia)
         
</div>

---

## Descripción

Sistema automatizado que genera commits diarios en GitHub para mantener una racha constante de contribuciones. Funciona 24/7 en Railway (gratis) usando n8n para la automatización y Python para los scripts.

### Características Principales

- **Completamente Gratis** - Funciona en el plan gratuito de Railway ($5 crédito/mes)
- **Automático 24/7** - Sin necesidad de tu computadora encendida
- **Flexible** - Configura número de commits, horarios y mensajes
- **Dos Modos** - Commits directos o Pull Requests automáticos
- **Fácil Setup** - Configuración en menos de 10 minutos
- **Código Abierto** - Totalmente transparente y personalizable

---

## Inicio Rápido

### Requisitos Previos

- Cuenta de GitHub
- Cuenta en [Railway](https://railway.app/) (gratis)
- Token de GitHub con permisos `repo`

### Instalación en 5 Pasos

```bash
# 1. Clonar o descargar este repositorio
git clone https://github.com/TU_USUARIO/commit-automation.git
cd commit-automation

# 2. Subir a tu GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main

# 3. Desplegar en Railway
# Ve a railway.app → New Project → Deploy from GitHub repo

# 4. Configurar variables de entorno en Railway
# Ver docs/QUICK_START.md para la lista completa

# 5. Acceder a n8n e importar workflow
# Railway te dará una URL → Importa workflows/n8n-workflow.json
```

**Guía completa**: [docs/QUICK_START.md](docs/QUICK_START.md)

---

## Documentación

### Guías Principales

| Documento | Descripción |
|-----------|-------------|
| [Inicio Rápido](docs/QUICK_START.md) | Configuración paso a paso en 10 minutos |
| [Persistencia de Datos](docs/PERSISTENCIA.md) | **IMPORTANTE: Evita perder datos en cada deploy** |
| [Configuración del Workflow](docs/CONFIGURACION_WORKFLOW.md) | Guía completa para configurar tu workflow en Railway (UTC-5) |
| [Despliegue en Railway](docs/RAILWAY_DEPLOY.md) | Guía detallada de despliegue en la nube |
| [Configuración Avanzada](docs/CONFIGURATION.md) | Personalización completa del sistema |
| [Modo Pull Request](docs/PR_MODE.md) | Automatización de PRs para más contribuciones |
| [Solución de Problemas](docs/TROUBLESHOOTING.md) | Errores comunes y soluciones |

### Documentación Técnica

- [Arquitectura del Sistema](docs/DEPLOYMENT.md)
- Scripts y API (próximamente)

---

## Configuración Básica

### Archivo `config/config.json`

```json
{
 "commits_per_day": 1,
 "commit_message_template": "Commit automático del {date} #{number}",
 "git_user_name": "Tu Nombre",
 "git_user_email": "tu-email@ejemplo.com",
 "auto_push": true,
 "timezone": "America/Bogota"
}
```

### Variables de Entorno (Railway)

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=tu_password_seguro
GENERIC_TIMEZONE=America/Bogota
TZ=America/Bogota
GIT_USER_NAME=Tu Nombre
GIT_USER_EMAIL=tu-email@ejemplo.com
```

---

## Modos de Operación

### Modo 1: Commits Directos (Por Defecto)

Hace commits directamente a la rama principal.

- **Contribuciones**: 1 por día
- **Configuración**: Simple
- **Workflow**: `workflows/n8n-workflow.json`

### Modo 2: Pull Requests Automáticos

Crea ramas, PRs y los mergea automáticamente.

- **Contribuciones**: 2+ por día (commit + merge)
- **Configuración**: Requiere token con permisos `repo`
- **Workflow**: `workflows/n8n-workflow-pr.json`

**Guía completa**: [docs/PR_MODE.md](docs/PR_MODE.md)

---

## Estructura del Proyecto

```
commitDiario/
 README.md # Este archivo
 LICENSE # Licencia MIT
 Dockerfile # Configuración de Docker
 railway.json # Configuración de Railway
 config/ # Configuración
 config.json # Archivo de configuración principal
 scripts/ # Scripts de Python
 commit_automator.py # Script de commits directos
 pr_automator.py # Script de Pull Requests
 requirements.txt # Dependencias de Python
 docs/ # Documentación completa
 README.md # Índice de documentación
 QUICK_START.md # Guía de inicio rápido
 RAILWAY_DEPLOY.md # Guía de despliegue
 CONFIGURATION.md # Configuración avanzada
 PR_MODE.md # Modo Pull Request
 TROUBLESHOOTING.md # Solución de problemas
 workflows/ # Workflows de n8n
   n8n-workflow.json # Workflow de commits directos
   n8n-workflow-pr.json # Workflow de Pull Requests
```

---

## Tecnologías Utilizadas

- **[n8n](https://n8n.io/)** - Automatización de workflows
- **[Python 3](https://www.python.org/)** - Scripts de automatización
- **[Railway](https://railway.app/)** - Hosting y despliegue
- **[Docker](https://www.docker.com/)** - Containerización
- **[GitHub API](https://docs.github.com/en/rest)** - Integración con GitHub

---

## Casos de Uso

### Ideal Para:

- Mantener racha de contribuciones durante vacaciones
- Proyectos personales de aprendizaje
- Demostrar actividad constante en tu perfil
- Automatizar tareas repetitivas de Git

### No Recomendado Para:

- Proyectos profesionales o de equipo
- Repositorios públicos importantes
- Inflar artificialmente estadísticas para empleadores
- Uso deshonesto o engañoso

---

## Seguridad y Privacidad

- **Código abierto** - Todo el código es visible y auditable
- **Sin acceso a datos** - Solo interactúa con tu repositorio específico
- **Tokens seguros** - Usa variables de entorno, nunca en el código
- **Repositorios privados** - Funciona perfectamente con repos privados
- **Control total** - Tú controlas qué, cuándo y dónde

---

## Costos

### Railway (Recomendado)

- **Plan Gratuito**: $5 crédito/mes
- **Uso real**: ~$1-2/mes
- **Resultado**: **Completamente gratis**

El plan gratuito de Railway es más que suficiente para este proyecto.

---

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este sistema:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas de Mejoras

- [ ] Dashboard web para monitoreo
- [ ] Notificaciones por email/Slack
- [ ] Soporte para múltiples repositorios
- [ ] Estadísticas y gráficas
- [ ] Integración con más plataformas (GitLab, Bitbucket)

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

```
MIT License - Copyright (c) 2026
```

Esto significa que puedes:
- Usar comercialmente
- Modificar
- Distribuir
- Uso privado

Con la condición de:
- ℹ Incluir la licencia y copyright

---

## Disclaimer

Este proyecto es para fines educativos y personales. Úsalo de manera responsable y ética. No está diseñado para engañar a empleadores o inflar artificialmente estadísticas de contribuciones de manera deshonesta.

Las contribuciones generadas son reales y están en tu repositorio, pero considera ser transparente sobre el uso de automatización si es relevante en tu contexto profesional.

---

## Soporte

### ¿Necesitas ayuda?

1. **Revisa la documentación**: [docs/](docs/)
2. **Solución de problemas**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
3. **Abre un issue**: [GitHub Issues](https://github.com/TU_USUARIO/TU_REPO/issues)

### Enlaces Útiles

- [Documentación de Railway](https://docs.railway.app/)
- [Documentación de n8n](https://docs.n8n.io/)
- [GitHub API](https://docs.github.com/en/rest)

---

## Agradecimientos

- [n8n.io](https://n8n.io/) por la increíble plataforma de automatización
- [Railway](https://railway.app/) por el hosting gratuito
- La comunidad de código abierto

---

## Roadmap

- [x] Sistema de commits directos
- [x] Sistema de Pull Requests automáticos
- [x] Despliegue en Railway
- [x] Documentación completa
- [ ] Dashboard web de monitoreo
- [ ] Notificaciones
- [ ] Soporte multi-repositorio
- [ ] Integración con GitLab

---

<div align="center">

**¿Te resultó útil este proyecto? Dale una en GitHub!**

Hecho con para mantener vivas las rachas de GitHub

[Documentación](docs/) • [Licencia](LICENSE) • [Contribuir](#-contribuciones)

</div>
