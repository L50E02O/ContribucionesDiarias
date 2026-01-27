#!/usr/bin/env python3
"""
Script de automatización de commits diarios a GitHub.

Este script realiza commits automáticos en un repositorio Git con el propósito
de mantener una racha de contribuciones en GitHub.
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class GitCommitAutomator:
    """Clase para automatizar commits en un repositorio Git."""

    def __init__(self, config_path: str = "/config/config.json"):
        """
        Inicializa el automatizador de commits.

        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        self.config = self._load_config(config_path)
        self.repo_path = Path(self.config.get("repo_path", "/repo"))
        self.data_file = self.repo_path / "daily_commit_data.txt"

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Carga la configuración desde un archivo JSON y variables de entorno.
        
        Las variables de entorno tienen prioridad sobre el config.json.

        Args:
            config_path: Ruta al archivo de configuración

        Returns:
            Diccionario con la configuración
        """
        # Configuración por defecto
        config = {
            "commits_per_day": 1,
            "repo_path": "/repo",
            "commit_message_template": "Commit automático del {date}",
            "git_user_name": "Commit Bot",
            "git_user_email": "bot@example.com",
            "auto_push": True,
            "timezone": "America/Bogota"
        }
        
        # Cargar desde config.json si existe
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        except FileNotFoundError:
            print(f"ADVERTENCIA: Archivo de configuración no encontrado: {config_path}")
            print("INFO: Usando configuración por defecto y variables de entorno")
        except json.JSONDecodeError as e:
            print(f"ERROR: Error al parsear el archivo de configuración: {e}")
            print("INFO: Usando configuración por defecto y variables de entorno")
        
        # Sobrescribir con variables de entorno (tienen prioridad)
        env_mappings = {
            "GIT_USER_NAME": "git_user_name",
            "GIT_USER_EMAIL": "git_user_email",
            "GITHUB_TOKEN": "github_token",
            "GENERIC_TIMEZONE": "timezone",
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                config[config_key] = env_value
                print(f"OK: Variable de entorno {env_var} cargada")
        
        return config

    def _run_command(self, command: list, cwd: Optional[Path] = None) -> tuple[bool, str]:
        """
        Ejecuta un comando del sistema.

        Args:
            command: Lista con el comando y sus argumentos
            cwd: Directorio de trabajo

        Returns:
            Tupla (éxito, salida)
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def setup_git_config(self) -> bool:
        """
        Configura el usuario y email de Git.

        Returns:
            True si la configuración fue exitosa
        """
        git_user = self.config.get("git_user_name", "Commit Bot")
        git_email = self.config.get("git_user_email", "bot@example.com")

        print(f"CONFIG: Configurando Git (user: {git_user}, email: {git_email})")

        success_user, _ = self._run_command(["git", "config", "user.name", git_user])
        success_email, _ = self._run_command(["git", "config", "user.email", git_email])

        return success_user and success_email

    def init_repo(self) -> bool:
        """
        Inicializa el repositorio Git si no existe.

        Returns:
            True si el repositorio está listo
        """
        if not self.repo_path.exists():
            print(f"INFO: Creando directorio: {self.repo_path}")
            self.repo_path.mkdir(parents=True, exist_ok=True)

        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            print("INFO: Inicializando repositorio Git")
            success, output = self._run_command(["git", "init"])
            if not success:
                print(f"ERROR: Error al inicializar Git: {output}")
                return False

        return self.setup_git_config()

    def create_commit_data(self) -> str:
        """
        Crea contenido para el archivo de datos del commit.

        Returns:
            Contenido generado
        """
        now = datetime.now()
        timestamp = now.isoformat()
        readable_date = now.strftime("%Y-%m-%d %H:%M:%S")

        content = f"""# Commit Automático
Timestamp: {timestamp}
Fecha legible: {readable_date}
Commit número del día: {self._get_today_commit_count() + 1}

---
Este es un commit automático generado por el sistema de commits diarios.
"""
        return content

    def _get_today_commit_count(self) -> int:
        """
        Obtiene el número de commits realizados hoy.

        Returns:
            Número de commits del día actual
        """
        success, output = self._run_command([
            "git", "log", "--since", "midnight", "--oneline"
        ])
        if success:
            return len(output.strip().split('\n')) if output.strip() else 0
        return 0

    def make_commit(self, commit_number: int) -> bool:
        """
        Realiza un commit en el repositorio.

        Args:
            commit_number: Número del commit del día

        Returns:
            True si el commit fue exitoso
        """
        # Crear contenido
        content = self.create_commit_data()
        
        # Escribir archivo
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f"ERROR: Error al escribir archivo: {e}")
            return False

        # Git add
        success, output = self._run_command(["git", "add", "."])
        if not success:
            print(f"ERROR: Error en git add: {output}")
            return False

        # Verificar si hay cambios
        success, output = self._run_command(["git", "status", "--porcelain"])
        if not success or not output.strip():
            print("ADVERTENCIA: No hay cambios para commitear")
            return False

        # Git commit
        date_str = datetime.now().strftime("%Y-%m-%d")
        commit_message = self.config.get(
            "commit_message_template",
            "Commit automático del {date}"
        ).format(date=date_str, number=commit_number)

        success, output = self._run_command(["git", "commit", "-m", commit_message])
        if not success:
            print(f"ERROR: Error en git commit: {output}")
            return False

        print(f"OK: Commit #{commit_number} realizado exitosamente")
        return True

    def push_commits(self) -> bool:
        """
        Empuja los commits al repositorio remoto.

        Returns:
            True si el push fue exitoso
        """
        # Verificar si hay un remoto configurado
        success, output = self._run_command(["git", "remote", "-v"])
        if not success or not output.strip():
            print("ADVERTENCIA: No hay repositorio remoto configurado")
            print("INFO: Para agregar uno, ejecuta:")
            print("   git remote add origin <URL_DEL_REPOSITORIO>")
            return False

        # Obtener la rama actual
        success, branch = self._run_command(["git", "branch", "--show-current"])
        if not success or not branch.strip():
            branch = "main"
        else:
            branch = branch.strip()

        # Push
        print(f"INFO: Empujando commits a la rama '{branch}'...")
        success, output = self._run_command(["git", "push", "origin", branch])
        
        if not success:
            # Intentar push con --set-upstream si es la primera vez
            if "no upstream branch" in output.lower() or "set-upstream" in output.lower():
                print(f"INFO: Configurando upstream para la rama '{branch}'")
                success, output = self._run_command([
                    "git", "push", "--set-upstream", "origin", branch
                ])
        
        if success:
            print("OK: Push realizado exitosamente")
            return True
        else:
            print(f"ERROR: Error en git push: {output}")
            return False

    def run(self) -> bool:
        """
        Ejecuta el proceso completo de commits.

        Returns:
            True si todos los commits fueron exitosos
        """
        print("=" * 60)
        print("INICIO: Automatización de commits diarios")
        print("=" * 60)

        # Inicializar repositorio
        if not self.init_repo():
            print("ERROR: Error al inicializar el repositorio")
            return False

        # Obtener número de commits a realizar
        commits_per_day = self.config.get("commits_per_day", 1)
        print(f"INFO: Commits a realizar: {commits_per_day}")

        # Realizar commits
        all_success = True
        for i in range(1, commits_per_day + 1):
            print(f"\nPROCESO: Realizando commit {i}/{commits_per_day}...")
            if not self.make_commit(i):
                all_success = False
                break

        # Push si está configurado
        if all_success and self.config.get("auto_push", True):
            self.push_commits()

        print("\n" + "=" * 60)
        if all_success:
            print("OK: Proceso completado exitosamente")
        else:
            print("ADVERTENCIA: Proceso completado con algunos errores")
        print("=" * 60)

        return all_success


def main():
    """Función principal del script."""
    try:
        automator = GitCommitAutomator()
        success = automator.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
