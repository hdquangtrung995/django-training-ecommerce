1. Basic setup
    #1 Run: "pyenv install 3.12"

    #2 Run: "python3 -m venv venv" 

    #3 Run: "source venv/bin/activate" (or run "deactivate" to deactivate)

    #4 (Optional) Run: "pip install -r requirements.txt" to install all dependencies in case you don't have "venv" file installed

    #5 (Optional) Run: "pip freeze > requirements.txt" to lists all installed packages and their versions by overwriting existing

    #6 (Optional) Run: "pip uninstall -r requirements.txt -y" to uninstall all packages

2. Run the server
    #0 Run: "django-admin startproject <project-name> ." to create a new project

    #1 Run "cd <project-name>"

    #2 Run: "python3 manage.py runserver"

    #3 (Optional) Run "python3 manage.py startapp <app_name>" to create a new app

    #4 (Optional) Run "python3 manage.py makemigrations <app_name>" to generate a migration file

    #5 (Optional) Run "python3 manage.py sqlmigrate <app_name> <migration_id>". The sqlmigrate command takes migration names and returns their SQL

    #6 (Optional) Run "python3 manage.py migrate" to run the migration

    #7 Run "python3 manage.py createsuperuser" to create super user admin

    #8 Run "python3 manage.py tailwind start" to start tailawindcss

    #9 Run "python3 manage.py shell" to open interactive django shell, input exit() or quit() to close the shell
