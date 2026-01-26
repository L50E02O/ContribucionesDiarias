#!/usr/bin/env python3
"""
Script de automatización de Pull Requests para GitHub.

Este script crea ramas, hace commits, crea PRs y los mergea automáticamente
para generar contribuciones en GitHub.
"""

import os
import json
import subprocess
import sys
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


class GitHubPRAutomator:
    """Clase para automatizar Pull Requests en GitHub."""

    def __init__(self, config_path: str = "/config/config.json"):
        """
        Inicializa el automatizador de PRs.

        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        self.config = self._load_config(config_path)
        self.repo_path = Path(self.config.get("repo_path", "/repo"))
        self.github_token = self.config.get("github_token") or os.getenv("GITHUB_TOKEN")
        self.repo_owner = self.config.get("github_repo_owner")
        self.repo_name = self.config.get("github_repo_name")
        
        if not self.github_token:
            raise ValueError("❌ GitHub token no configurado. Define 'github_token' en config.json o variable GITHUB_TOKEN")
        
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Carga la configuración desde un archivo JSON.

        Args:
            config_path: Ruta al archivo de configuración

        Returns:
            Diccionario con la configuración
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración no encontrado: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear el archivo de configuración: {e}")
            sys.exit(1)

    def _run_command(self, command: list, cwd: Optional[Path] = None) -> Tuple[bool, str]:
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

    def _extract_repo_info_from_remote(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrae el owner y nombre del repo desde la URL remota.

        Returns:
            Tupla (owner, repo_name)
        """
        success, output = self._run_command(["git", "remote", "get-url", "origin"])
        if not success:
            return None, None

        url = output.strip()
        
        # Parsear URL: https://github.com/owner/repo.git o git@github.com:owner/repo.git
        if "github.com" in url:
            if url.startswith("https://"):
                # https://github.com/owner/repo.git
                parts = url.replace("https://github.com/", "").replace(".git", "").split("/")
            elif url.startswith("git@"):
                # git@github.com:owner/repo.git
                parts = url.replace("git@github.com:", "").replace(".git", "").split("/")
            else:
                return None, None
            
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        return None, None

    def setup_git_config(self) -> bool:
        """
        Configura el usuario y email de Git.

        Returns:
            True si la configuración fue exitosa
        """
        git_user = self.config.get("git_user_name", "PR Bot")
        git_email = self.config.get("git_user_email", "bot@example.com")

        print(f"⚙️  Configurando Git (user: {git_user}, email: {git_email})")

        success_user, _ = self._run_command(["git", "config", "user.name", git_user])
        success_email, _ = self._run_command(["git", "config", "user.email", git_email])

        return success_user and success_email

    def get_base_branch(self) -> str:
        """
        Obtiene la rama base (main o master).

        Returns:
            Nombre de la rama base
        """
        # Verificar si existe main
        success, _ = self._run_command(["git", "rev-parse", "--verify", "main"])
        if success:
            return "main"
        
        # Verificar si existe master
        success, _ = self._run_command(["git", "rev-parse", "--verify", "master"])
        if success:
            return "master"
        
        # Default
        return "main"

    def create_feature_branch(self) -> str:
        """
        Crea una nueva rama para el PR.

        Returns:
            Nombre de la rama creada
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"auto-contribution-{timestamp}"
        
        base_branch = self.get_base_branch()
        
        print(f"🌿 Creando rama: {branch_name}")
        
        # Asegurar que estamos en la rama base
        success, _ = self._run_command(["git", "checkout", base_branch])
        if not success:
            print(f"⚠️  No se pudo cambiar a {base_branch}, intentando crear...")
            self._run_command(["git", "checkout", "-b", base_branch])
        
        # Pull latest changes
        print(f"📥 Actualizando rama {base_branch}...")
        self._run_command(["git", "pull", "origin", base_branch])
        
        # Crear nueva rama
        success, output = self._run_command(["git", "checkout", "-b", branch_name])
        if not success:
            print(f"❌ Error al crear rama: {output}")
            return None
        
        print(f"✅ Rama {branch_name} creada")
        return branch_name

    def create_commit_in_branch(self, branch_name: str) -> bool:
        """
        Crea un commit en la rama actual.

        Args:
            branch_name: Nombre de la rama

        Returns:
            True si el commit fue exitoso
        """
        # Crear contenido para el commit
        now = datetime.now()
        timestamp = now.isoformat()
        readable_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Crear un archivo de feature
        feature_file = self.repo_path / f"feature_{now.strftime('%Y%m%d_%H%M%S')}.md"
        
        content = f"""# Feature Update

**Date:** {readable_date}
**Branch:** {branch_name}
**Timestamp:** {timestamp}

## Changes

This is an automated contribution generated by the PR automation system.

## Details

- Type: Automated feature
- Purpose: GitHub contribution tracking
- Status: Ready for review
"""
        
        try:
            with open(feature_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f"❌ Error al escribir archivo: {e}")
            return False
        
        # Git add
        success, output = self._run_command(["git", "add", "."])
        if not success:
            print(f"❌ Error en git add: {output}")
            return False
        
        # Git commit
        commit_message = f"feat: automated contribution {now.strftime('%Y-%m-%d')}"
        success, output = self._run_command(["git", "commit", "-m", commit_message])
        if not success:
            print(f"❌ Error en git commit: {output}")
            return False
        
        print(f"✅ Commit creado: {commit_message}")
        return True

    def push_branch(self, branch_name: str) -> bool:
        """
        Empuja la rama al repositorio remoto.

        Args:
            branch_name: Nombre de la rama

        Returns:
            True si el push fue exitoso
        """
        print(f"📤 Empujando rama {branch_name}...")
        success, output = self._run_command(["git", "push", "-u", "origin", branch_name])
        
        if not success:
            print(f"❌ Error en git push: {output}")
            return False
        
        print(f"✅ Rama {branch_name} empujada exitosamente")
        return True

    def create_pull_request(self, branch_name: str) -> Optional[int]:
        """
        Crea un Pull Request en GitHub.

        Args:
            branch_name: Nombre de la rama source

        Returns:
            Número del PR creado o None si falló
        """
        # Obtener info del repo si no está configurada
        if not self.repo_owner or not self.repo_name:
            owner, repo = self._extract_repo_info_from_remote()
            if not owner or not repo:
                print("❌ No se pudo determinar owner/repo. Configura 'github_repo_owner' y 'github_repo_name'")
                return None
            self.repo_owner = owner
            self.repo_name = repo
        
        base_branch = self.get_base_branch()
        
        pr_data = {
            "title": f"🤖 Automated Contribution - {datetime.now().strftime('%Y-%m-%d')}",
            "body": f"""## Automated Contribution

This is an automated pull request created by the contribution automation system.

### Details
- **Branch:** `{branch_name}`
- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type:** Automated feature update

### Changes
- Added automated feature documentation
- Updated contribution tracking

---
*This PR was automatically generated and will be merged automatically.*
""",
            "head": branch_name,
            "base": base_branch
        }
        
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls"
        
        print(f"📝 Creando Pull Request en {self.repo_owner}/{self.repo_name}...")
        
        try:
            response = requests.post(url, headers=self.headers, json=pr_data)
            response.raise_for_status()
            
            pr_number = response.json()["number"]
            pr_url = response.json()["html_url"]
            
            print(f"✅ Pull Request #{pr_number} creado exitosamente")
            print(f"🔗 URL: {pr_url}")
            
            return pr_number
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al crear Pull Request: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Respuesta: {e.response.text}")
            return None

    def merge_pull_request(self, pr_number: int) -> bool:
        """
        Mergea un Pull Request automáticamente.

        Args:
            pr_number: Número del PR a mergear

        Returns:
            True si el merge fue exitoso
        """
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/merge"
        
        merge_data = {
            "commit_title": f"Merge automated contribution #{pr_number}",
            "commit_message": "Automated merge of daily contribution PR",
            "merge_method": self.config.get("merge_method", "squash")  # squash, merge, rebase
        }
        
        print(f"🔄 Mergeando Pull Request #{pr_number}...")
        
        try:
            response = requests.put(url, headers=self.headers, json=merge_data)
            response.raise_for_status()
            
            print(f"✅ Pull Request #{pr_number} mergeado exitosamente")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al mergear Pull Request: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Respuesta: {e.response.text}")
            return False

    def cleanup_branch(self, branch_name: str) -> bool:
        """
        Elimina la rama después del merge.

        Args:
            branch_name: Nombre de la rama a eliminar

        Returns:
            True si la eliminación fue exitosa
        """
        # Volver a la rama base
        base_branch = self.get_base_branch()
        self._run_command(["git", "checkout", base_branch])
        
        # Pull para actualizar
        self._run_command(["git", "pull", "origin", base_branch])
        
        # Eliminar rama local
        print(f"🗑️  Eliminando rama local {branch_name}...")
        success_local, _ = self._run_command(["git", "branch", "-D", branch_name])
        
        # Eliminar rama remota
        print(f"🗑️  Eliminando rama remota {branch_name}...")
        success_remote, _ = self._run_command(["git", "push", "origin", "--delete", branch_name])
        
        if success_local and success_remote:
            print(f"✅ Rama {branch_name} eliminada completamente")
            return True
        else:
            print(f"⚠️  Rama {branch_name} eliminada parcialmente")
            return False

    def run(self) -> bool:
        """
        Ejecuta el proceso completo de PR automatizado.

        Returns:
            True si todo fue exitoso
        """
        print("=" * 70)
        print("🤖 Iniciando automatización de Pull Request")
        print("=" * 70)
        
        try:
            # Configurar Git
            if not self.setup_git_config():
                print("❌ Error al configurar Git")
                return False
            
            # Crear rama
            branch_name = self.create_feature_branch()
            if not branch_name:
                return False
            
            # Crear commit
            if not self.create_commit_in_branch(branch_name):
                return False
            
            # Push rama
            if not self.push_branch(branch_name):
                return False
            
            # Crear PR
            pr_number = self.create_pull_request(branch_name)
            if not pr_number:
                return False
            
            # Esperar un momento (opcional)
            import time
            print("⏳ Esperando 5 segundos antes del merge...")
            time.sleep(5)
            
            # Mergear PR
            if not self.merge_pull_request(pr_number):
                return False
            
            # Limpiar rama (opcional)
            if self.config.get("auto_cleanup_branch", True):
                self.cleanup_branch(branch_name)
            
            print("\n" + "=" * 70)
            print("✅ Proceso de PR completado exitosamente")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Función principal del script."""
    try:
        automator = GitHubPRAutomator()
        success = automator.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
