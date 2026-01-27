# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! Toda ayuda es bienvenida.

## Cómo Contribuir

### 1. Fork el Repositorio

Click en el botón "Fork" en la esquina superior derecha de GitHub.

### 2. Clona tu Fork

```bash
git clone https://github.com/TU_USUARIO/commit-automation.git
cd commit-automation
```

### 3. Crea una Rama

```bash
git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/arreglo-de-bug
```

### 4. Haz tus Cambios

Asegúrate de seguir las convenciones del proyecto (ver abajo).

### 5. Commit tus Cambios

```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

### 6. Push a tu Fork

```bash
git push origin feature/mi-nueva-funcionalidad
```

### 7. Abre un Pull Request

Ve a tu fork en GitHub y click "New Pull Request".

---

## Convenciones de Código

### Python (PEP 8)

- Usa 4 espacios para indentación
- Líneas máximo 100 caracteres
- Docstrings para todas las funciones y clases
- Type hints cuando sea posible

```python
def mi_funcion(parametro: str) -> bool:
 """
 Descripción breve de la función.
 Args:
 parametro: Descripción del parámetro
 Returns:
 Descripción del retorno
 """
 return True
```

### Commits (Conventional Commits)

Usa el formato:

```
tipo(scope): descripción corta

Descripción más detallada si es necesario.
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, sin cambios de código
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Mantenimiento, dependencias

**Ejemplos**:
```
feat(scripts): agregar soporte para múltiples repos
fix(workflow): corregir error en cron schedule
docs(readme): actualizar instrucciones de instalación
```

---

## Testing

Antes de hacer un PR:

```bash
# Prueba los scripts manualmente
python3 scripts/commit_automator.py
python3 scripts/pr_automator.py

# Verifica que el Dockerfile buildea
docker build -t test-commit-automation .

# Prueba el contenedor
docker run -it --rm test-commit-automation
```

---

## Documentación

Si agregas nuevas funcionalidades:

1. **Actualiza el README.md** con la nueva característica
2. **Agrega documentación** en `docs/` si es necesario
3. **Incluye ejemplos** de uso
4. **Actualiza CONFIGURATION.md** si agregas nuevas opciones

---

## Reportar Bugs

### Antes de Reportar

1. Busca si ya existe un issue similar
2. Verifica que estás usando la última versión
3. Revisa [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

### Al Reportar

Incluye:

- **Descripción clara** del problema
- **Pasos para reproducir**
- **Comportamiento esperado** vs **comportamiento actual**
- **Logs relevantes** (sin tokens o información sensible)
- **Configuración** (sin tokens)
- **Entorno**: Railway, Docker local, etc.

**Template**:

```markdown
## Descripción
Descripción clara y concisa del bug.

## Pasos para Reproducir
1. Ir a '...'
2. Click en '...'
3. Ver error

## Comportamiento Esperado
Lo que debería pasar.

## Comportamiento Actual
Lo que realmente pasa.

## Logs
```
Pega logs aquí (sin tokens)
```

## Configuración
```json
{
 "commits_per_day": 1,
 ...
}
```

## Entorno
- Railway / Docker local
- Versión de Python: 3.x
- Sistema operativo: ...
```

---

## Sugerir Funcionalidades

### Antes de Sugerir

1. Verifica que no exista ya la funcionalidad
2. Busca si alguien más ya la sugirió
3. Piensa si encaja con el propósito del proyecto

### Al Sugerir

Incluye:

- **Descripción clara** de la funcionalidad
- **Caso de uso**: ¿Por qué es útil?
- **Propuesta de implementación** (opcional)
- **Alternativas consideradas**

---

## Áreas que Necesitan Ayuda

### Alta Prioridad

- [ ] Tests automatizados
- [ ] Dashboard web de monitoreo
- [ ] Notificaciones (email/Slack)
- [ ] Soporte multi-repositorio

### Media Prioridad

- [ ] Integración con GitLab
- [ ] Estadísticas y gráficas
- [ ] CLI para configuración
- [ ] Webhooks de GitHub

### Baja Prioridad

- [ ] Interfaz gráfica
- [ ] Soporte para Bitbucket
- [ ] Plugins/extensiones
- [ ] Temas personalizables

---

## Recursos

- [Python PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub API](https://docs.github.com/en/rest)
- [n8n Documentation](https://docs.n8n.io/)
- [Railway Documentation](https://docs.railway.app/)

---

## Checklist antes del PR

- [ ] El código sigue las convenciones del proyecto
- [ ] Los commits siguen Conventional Commits
- [ ] La documentación está actualizada
- [ ] Los scripts funcionan correctamente
- [ ] El Dockerfile buildea sin errores
- [ ] No hay información sensible (tokens, passwords)
- [ ] El PR tiene una descripción clara

---

## Código de Conducta

### Nuestro Compromiso

Crear un ambiente acogedor y respetuoso para todos.

### Comportamiento Esperado

- Ser respetuoso y considerado
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros

### Comportamiento Inaceptable

- Lenguaje ofensivo o discriminatorio
- Acoso o intimidación
- Spam o autopromoción excesiva
- Publicar información privada de otros

---

## Contacto

Si tienes preguntas sobre cómo contribuir:

- Abre un issue con la etiqueta `question`
- Revisa la documentación en `docs/`

---

## Reconocimiento

Todos los contribuidores serán mencionados en el README.md.

¡Gracias por hacer este proyecto mejor! 
