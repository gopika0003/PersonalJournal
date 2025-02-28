
@echo off
cd /d D:\PersonalJournalProject

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install django djangorestframework

echo Creating Django project...
if not exist manage.py (
    django-admin startproject personal_journal_project .
) else (
    echo Django project already exists, skipping creation...
)

echo Creating Django app...
if not exist personal_journal_app (
    django-admin startapp personal_journal_app
) else (
    echo Django app 'personal_journal_app' already exists, skipping creation...
)

echo Running migrations...
if exist manage.py (
    python manage.py migrate
) else (
    echo Error: manage.py not found in D:\PersonalJournalProject
    exit /b 1
)

echo Creating superuser...
set DJANGO_SUPERUSER_USERNAME=journal_admin
set DJANGO_SUPERUSER_EMAIL=admin@journal.com
set DJANGO_SUPERUSER_PASSWORD=journal_pass123
python manage.py createsuperuser --noinput


echo Starting Django server...
python manage.py runserver
