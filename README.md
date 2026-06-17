# AVITECH - Plataforma Avícola

Sistema integral para gestión de avicultura.

## Características
- Marketplace multicentro
- Módulo de diagnóstico de enfermedades
- Calculadora nutricional
- Control de stock y pedidos

## Instalación
1. Crear entorno virtual: `python -m venv venv`
2. Activar: `source venv/bin/activate` (Linux) o `venv\Scripts\activate` (Windows)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Configurar variables en `.env`
5. Ejecutar migraciones: `flask db init && flask db migrate -m "initial" && flask db upgrade`
6. Ejecutar: `python run.py`

## Tecnologías
- Flask
- SQLAlchemy
- Flask-Login
- Celery + Redis
- Levenshtein para búsquedas