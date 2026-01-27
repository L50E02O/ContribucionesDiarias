# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-01-26

### Agregado

- Sistema completo de commits diarios automáticos
- Script de Python para commits directos (`commit_automator.py`)
- Script de Python para Pull Requests automáticos (`pr_automator.py`)
- Workflow de n8n para commits directos
- Workflow de n8n para Pull Requests
- Dockerfile optimizado para Railway
- Configuración de Railway (`railway.json`)
- Documentación completa en carpeta `docs/`:
 - Guía de inicio rápido
 - Guía de despliegue en Railway
 - Configuración avanzada
 - Modo Pull Request
 - Solución de problemas
- Archivo de configuración flexible (`config/config.json`)
- Variables de entorno de ejemplo (`.env.example`)
- Licencia MIT
- Guía de contribución
- README principal con badges y estructura completa

### Configuración

- Soporte para zona horaria configurable
- Número de commits por día personalizable
- Mensajes de commit personalizables con templates
- Dos modos de operación: commits directos y Pull Requests
- Auto-push configurable
- Métodos de merge configurables (squash, merge, rebase)

### Despliegue

- Soporte completo para Railway
- Dockerfile basado en Node.js Alpine
- Instalación automática de n8n
- Instalación de Git y Python en el contenedor
- Volúmenes persistentes para datos de n8n

### Documentación

- 8 documentos completos en `docs/`
- README principal con guía completa
- Ejemplos de configuración
- Solución de problemas detallada
- Guía de contribución

### Seguridad

- Variables de entorno para información sensible
- `.gitignore` actualizado
- Tokens nunca en el código
- Documentación de mejores prácticas de seguridad

---

## [Unreleased]

### Planeado

- Dashboard web de monitoreo
- Notificaciones por email/Slack
- Soporte para múltiples repositorios
- Tests automatizados
- Integración con GitLab
- CLI para configuración
- Estadísticas y gráficas

---

## Tipos de Cambios

- ` Agregado` - Para nuevas funcionalidades
- ` Cambiado` - Para cambios en funcionalidades existentes
- ` Deprecado` - Para funcionalidades que serán eliminadas
- ` Eliminado` - Para funcionalidades eliminadas
- ` Arreglado` - Para corrección de bugs
- ` Seguridad` - Para vulnerabilidades de seguridad

---

[1.0.0]: https://github.com/TU_USUARIO/TU_REPO/releases/tag/v1.0.0
[Unreleased]: https://github.com/TU_USUARIO/TU_REPO/compare/v1.0.0...HEAD
