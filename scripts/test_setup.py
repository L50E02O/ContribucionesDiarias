#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del sistema.

Este script verifica que todos los componentes estén configurados correctamente
antes de activar la automatización.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SetupTester:
    """Clase para probar la configuración del sistema."""

    def __init__(self):
        """Inicializa el tester."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.success_count = 0
        self.total_tests = 0

    def print_header(self, text: str) -> None:
        """
        Imprime un encabezado.

        Args:
            text: Texto del encabezado
        """
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)

    def print_test(self, name: str, passed: bool, message: str = "") -> None:
        """
        Imprime el resultado de un test.

        Args:
            name: Nombre del test
            passed: Si el test pasó o no
            message: Mensaje adicional
        """
        self.total_tests += 1
        if passed:
            self.success_count += 1
            print(f"OK: {name}")
            if message:
                print(f"   INFO: {message}")
        else:
            print(f"ERROR: {name}")
            if message:
                print(f"   ADVERTENCIA: {message}")

    def test_config_file(self) -> bool:
        """
        Verifica que el archivo de configuración exista y sea válido.

        Returns:
            True si el test pasó
        """
        config_path = Path("/config/config.json")
        
        if not config_path.exists():
            self.print_test(
                "Archivo de configuración",
                False,
                f"No se encontró {config_path}"
            )
            self.errors.append("Archivo config.json no encontrado")
            return False

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Verificar campos obligatorios
            required_fields = ["repo_path", "git_user_name", "git_user_email"]
            missing_fields = [f for f in required_fields if f not in config]
            
            if missing_fields:
                self.print_test(
                    "Archivo de configuración",
                    False,
                    f"Faltan campos: {', '.join(missing_fields)}"
                )
                self.errors.append(f"Campos faltantes en config.json: {missing_fields}")
                return False
            
            self.print_test(
                "Archivo de configuración",
                True,
                f"Configurado para {config.get('commits_per_day', 1)} commit(s) por día"
            )
            return True
            
        except json.JSONDecodeError as e:
            self.print_test(
                "Archivo de configuración",
                False,
                f"JSON inválido: {e}"
            )
            self.errors.append("config.json tiene errores de sintaxis")
            return False

    def test_repo_directory(self) -> bool:
        """
        Verifica que el directorio del repositorio exista.

        Returns:
            True si el test pasó
        """
        repo_path = Path("/repo")
        
        if not repo_path.exists():
            self.print_test(
                "Directorio del repositorio",
                False,
                f"{repo_path} no existe"
            )
            self.errors.append("Directorio /repo no encontrado")
            return False
        
        self.print_test("Directorio del repositorio", True, str(repo_path))
        return True

    def test_git_installation(self) -> bool:
        """
        Verifica que Git esté instalado.

        Returns:
            True si el test pasó
        """
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            version = result.stdout.strip()
            self.print_test("Git instalado", True, version)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_test("Git instalado", False, "Git no está instalado")
            self.errors.append("Git no está instalado")
            return False

    def test_git_config(self) -> bool:
        """
        Verifica la configuración de Git.

        Returns:
            True si el test pasó
        """
        repo_path = Path("/repo")
        
        try:
            # Verificar user.name
            result = subprocess.run(
                ["git", "config", "user.name"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            user_name = result.stdout.strip()
            
            # Verificar user.email
            result = subprocess.run(
                ["git", "config", "user.email"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            user_email = result.stdout.strip()
            
            if user_name and user_email:
                self.print_test(
                    "Configuración de Git",
                    True,
                    f"{user_name} <{user_email}>"
                )
                return True
            else:
                self.print_test(
                    "Configuración de Git",
                    False,
                    "Usuario o email no configurado"
                )
                self.warnings.append("Configura Git con: git config user.name y user.email")
                return False
                
        except subprocess.CalledProcessError:
            self.print_test(
                "Configuración de Git",
                False,
                "No se pudo leer la configuración"
            )
            self.warnings.append("Ejecuta el script setup_railway.sh para configurar Git")
            return False

    def test_git_remote(self) -> bool:
        """
        Verifica que haya un repositorio remoto configurado.

        Returns:
            True si el test pasó
        """
        repo_path = Path("/repo")
        
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                remotes = result.stdout.strip().split('\n')
                origin = [r for r in remotes if r.startswith('origin')]
                if origin:
                    self.print_test(
                        "Repositorio remoto",
                        True,
                        origin[0].split()[1]
                    )
                    return True
            
            self.print_test(
                "Repositorio remoto",
                False,
                "No hay remoto configurado"
            )
            self.warnings.append("Ejecuta setup_railway.sh para configurar el remoto")
            return False
            
        except subprocess.CalledProcessError:
            self.print_test(
                "Repositorio remoto",
                False,
                "Error al verificar remoto"
            )
            return False

    def test_python_dependencies(self) -> bool:
        """
        Verifica que las dependencias de Python estén instaladas.

        Returns:
            True si el test pasó
        """
        try:
            import requests
            self.print_test(
                "Dependencias de Python",
                True,
                "requests instalado"
            )
            return True
        except ImportError:
            self.print_test(
                "Dependencias de Python",
                False,
                "requests no está instalado"
            )
            self.errors.append("Instala dependencias: pip install -r /scripts/requirements.txt")
            return False

    def test_github_token(self) -> bool:
        """
        Verifica si hay un token de GitHub configurado (solo para modo PR).

        Returns:
            True si el test pasó
        """
        # Leer config
        try:
            with open("/config/config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            use_pr = config.get("use_pr_workflow", False)
            
            if not use_pr:
                self.print_test(
                    "Token de GitHub",
                    True,
                    "No requerido (modo commit directo)"
                )
                return True
            
            # Verificar token
            token = config.get("github_token") or os.getenv("GITHUB_TOKEN")
            
            if token and token.startswith("ghp_"):
                self.print_test(
                    "Token de GitHub",
                    True,
                    "Token configurado correctamente"
                )
                return True
            else:
                self.print_test(
                    "Token de GitHub",
                    False,
                    "Token no configurado o inválido (modo PR requiere token)"
                )
                self.errors.append("Configura GITHUB_TOKEN en las variables de entorno de Railway")
                return False
                
        except Exception as e:
            self.print_test(
                "Token de GitHub",
                False,
                f"Error al verificar: {e}"
            )
            return False

    def test_scripts_exist(self) -> bool:
        """
        Verifica que los scripts de automatización existan.

        Returns:
            True si el test pasó
        """
        scripts = [
            "/scripts/commit_automator.py",
            "/scripts/pr_automator.py"
        ]
        
        all_exist = True
        for script in scripts:
            if not Path(script).exists():
                self.print_test(
                    f"Script {Path(script).name}",
                    False,
                    f"No encontrado: {script}"
                )
                all_exist = False
            else:
                self.print_test(
                    f"Script {Path(script).name}",
                    True,
                    script
                )
        
        if not all_exist:
            self.errors.append("Faltan scripts de automatización")
        
        return all_exist

    def run_all_tests(self) -> bool:
        """
        Ejecuta todos los tests.

        Returns:
            True si todos los tests pasaron
        """
        self.print_header("TEST: Verificación de Configuración del Sistema")
        
        print("\nINFO: Ejecutando tests...\n")
        
        # Ejecutar tests
        self.test_config_file()
        self.test_repo_directory()
        self.test_git_installation()
        self.test_git_config()
        self.test_git_remote()
        self.test_python_dependencies()
        self.test_github_token()
        self.test_scripts_exist()
        
        # Resumen
        self.print_header("RESUMEN: Resumen de Tests")
        
        print(f"\nOK: Tests exitosos: {self.success_count}/{self.total_tests}")
        
        if self.warnings:
            print("\nADVERTENCIA: Advertencias:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if self.errors:
            print("\nERROR: Errores críticos:")
            for error in self.errors:
                print(f"   - {error}")
            print("\nSOLUCION: Solución:")
            print("   1. Ejecuta: railway run bash")
            print("   2. Ejecuta: bash /scripts/setup_railway.sh")
            print("   3. Vuelve a ejecutar este test")
            return False
        
        if self.warnings:
            print("\nADVERTENCIA: Hay advertencias pero el sistema puede funcionar")
            print("   Considera resolver las advertencias para un funcionamiento óptimo")
        
        print("\n" + "=" * 70)
        if not self.errors:
            print("OK: Sistema configurado correctamente")
            print("=" * 70)
            print("\nINFO: Próximos pasos:")
            print("   1. Ve a n8n en tu URL de Railway")
            print("   2. Importa el workflow correspondiente")
            print("   3. Activa el workflow (toggle verde)")
            print("   4. Prueba manualmente:")
            print("      python3 /scripts/commit_automator.py")
            print("\nINFO: El sistema generará commits automáticos cada 24 horas\n")
            return True
        
        return False


def main():
    """Función principal del script."""
    tester = SetupTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
