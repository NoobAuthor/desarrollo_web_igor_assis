#!/usr/bin/env python3
"""
Verification script to check if the Tarea 4 project is properly set up
Run this script to verify all components are working correctly
"""

import sys
import os
import importlib.util
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")

def check_file_exists(file_path, description):
    """Check if a file exists and is readable"""
    if Path(file_path).exists():
        print_status(f"✓ {description} exists", "SUCCESS")
        return True
    else:
        print_status(f"✗ {description} missing: {file_path}", "ERROR")
        return False

def check_directory_exists(dir_path, description):
    """Check if directory exists"""
    if Path(dir_path).is_dir():
        print_status(f"✓ {description} directory exists", "SUCCESS")
        return True
    else:
        print_status(f"✗ {description} directory missing: {dir_path}", "ERROR")
        return False

def check_python_imports():
    """Check if all required Python modules can be imported"""
    required_modules = [
        'flask',
        'flask_wtf',
        'flask_sqlalchemy',
        'pymysql',
        'sqlalchemy',
        'werkzeug'
    ]

    print_status("Checking Python dependencies...", "INFO")
    all_good = True

    for module in required_modules:
        try:
            if module == 'flask_wtf':
                import flask_wtf
            elif module == 'flask_sqlalchemy':
                import flask_sqlalchemy
            else:
                __import__(module)
            print_status(f"✓ {module} imported successfully", "SUCCESS")
        except ImportError as e:
            print_status(f"✗ Failed to import {module}: {e}", "ERROR")
            all_good = False

    return all_good

def check_database_connection():
    """Check if database connection works"""
    try:
        import pymysql
        conn = pymysql.connect(
            host='localhost',
            user='cc5002',
            password='programacionweb',
            database='tarea2'
        )

        # Test basic queries
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM region")
        region_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM comuna")
        comuna_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        print_status(f"✓ Database connection successful", "SUCCESS")
        print_status(f"  - Regions: {region_count}", "INFO")
        print_status(f"  - Comunas: {comuna_count}", "INFO")

        return True

    except Exception as e:
        print_status(f"✗ Database connection failed: {e}", "ERROR")
        return False

def check_flask_app():
    """Check if Flask app can be imported and initialized"""
    try:
        # Change to project root directory
        original_cwd = os.getcwd()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_root)

        # Import app
        from app import app, db
        from models import Actividad, Comentario, Nota

        # Test app context
        with app.app_context():
            # Test database models
            actividad_count = Actividad.query.count()
            comentario_count = Comentario.query.count()
            nota_count = Nota.query.count()

            print_status(f"✓ Flask app initialized successfully", "SUCCESS")
            print_status(f"  - Activities: {actividad_count}", "INFO")
            print_status(f"  - Comments: {comentario_count}", "INFO")
            print_status(f"  - Ratings: {nota_count}", "INFO")

        os.chdir(original_cwd)
        return True

    except Exception as e:
        print_status(f"✗ Flask app initialization failed: {e}", "ERROR")
        os.chdir(original_cwd)
        return False

def main():
    """Main verification function"""
    print("=" * 50)
    print("Tarea 4 - Project Setup Verification")
    print("=" * 50)
    print()

    checks_passed = 0
    total_checks = 0

    # File structure checks
    print_status("Checking file structure...", "INFO")
    file_checks = [
        ("../app.py", "Main Flask application"),
        ("../models.py", "Database models"),
        ("../requirements.txt", "Python requirements"),
        ("../README.md", "Project README"),
        ("../SETUP.md", "Setup guide"),
        ("../database/tarea2.sql", "Main database schema"),
        ("../database/tabla-comentario.sql", "Comments table schema"),
        ("../database/tabla-nota.sql", "Ratings table schema"),
        ("../database/region-comuna.sql", "Regions/communes data"),
        ("../templates/base.html", "Base template"),
        ("../templates/index.html", "Home template"),
        ("../templates/detalle.html", "Detail template"),
        ("../static/style.css", "Main stylesheet"),
        ("../static/script.js", "JavaScript file"),
        ("../static/fotos/.gitkeep", "Photos directory marker")
    ]

    for file_path, description in file_checks:
        if check_file_exists(file_path, description):
            checks_passed += 1
        total_checks += 1

    # Directory structure checks
    print()
    print_status("Checking directory structure...", "INFO")
    dir_checks = [
        ("../database", "Database scripts"),
        ("../docs", "Documentation"),
        ("../static", "Static files"),
        ("../templates", "HTML templates"),
        ("../static/fotos", "Photos upload")
    ]

    for dir_path, description in dir_checks:
        if check_directory_exists(dir_path, description):
            checks_passed += 1
        total_checks += 1

    # Python dependencies check
    print()
    if check_python_imports():
        checks_passed += 1
    total_checks += 1

    # Database connection check
    print()
    if check_database_connection():
        checks_passed += 1
    total_checks += 1

    # Flask app check
    print()
    if check_flask_app():
        checks_passed += 1
    total_checks += 1

    # Summary
    print()
    print("=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)

    success_rate = (checks_passed / total_checks) * 100

    if success_rate == 100:
        print_status(f"All checks passed! ({checks_passed}/{total_checks})", "SUCCESS")
        print_status("Your project is ready to run!", "SUCCESS")
        print()
        print_status("To start the application:", "INFO")
        print_status("  cd .. && python app.py", "INFO")
        print_status("Then visit: http://localhost:5000", "INFO")

    elif success_rate >= 80:
        print_status(f"Most checks passed ({checks_passed}/{total_checks})", "WARNING")
        print_status("Minor issues detected, but should work", "WARNING")

    else:
        print_status(f"Several checks failed ({checks_passed}/{total_checks})", "ERROR")
        print_status("Please fix the issues before running", "ERROR")
        print()
        print_status("Common solutions:", "INFO")
        print_status("  1. Run: pip install -r requirements.txt", "INFO")
        print_status("  2. Set up database using setup.sh", "INFO")
        print_status("  3. Check MySQL is running", "INFO")

    print()
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
