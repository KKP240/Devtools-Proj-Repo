@echo off
REM ====== Batch file for creating Django Project with psycopg2 ======

:: 1) Ask for Django project name
set /p project_name=Enter Django Project Name: 

:: 2) Ask for Django app name (optional)
set /p app_name=Enter Django App Name (leave blank to skip): 

:: 3) Create virtual environment
echo Creating virtual environment...
python -m venv myvenv

:: 4) Activate virtual environment
call myvenv\Scripts\activate

:: 5) Upgrade pip
python -m pip install --upgrade pip

:: 6) Install Django
echo Installing Django...
pip install django

:: 7) Install psycopg2 (PostgreSQL adapter)
echo Installing psycopg2...
pip install psycopg2-binary

:: 8) Check if project name is not empty, then create Django project
if not "%project_name%"=="" (
    echo Creating Django project %project_name% ...
    django-admin startproject %project_name%

    :: 9) Go inside project folder
    cd %project_name%

    :: 10) If user entered app name, create the app
    if not "%app_name%"=="" (
        echo Creating Django app %app_name% ...
        python manage.py startapp %app_name%
    )
) else (
    echo Project name is empty. Skipping Django project creation.
)

pause
