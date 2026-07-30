@echo off
echo ========================================
echo   DESPLIEGUE AUTOMATICO EN RAILWAY
echo ========================================
echo.

echo [1/6] Verificando dependencias...
pip install psycopg2-binary gunicorn whitenoise python-decouple
echo.

echo [2/6] Creando .gitignore...
(
echo *.pyc
echo __pycache__/
echo *.db
echo *.sqlite3
echo .env
echo staticfiles/
echo media/
echo venv/
echo .vscode/
) > .gitignore
echo .gitignore creado
echo.

echo [3/6] Inicializando Git...
git init
git add .
git commit -m "Preparar deploy con PostgreSQL en Railway"
echo.

echo [4/6] ACCION REQUERIDA:
echo    1. Ve a https://github.com/new
echo    2. Crea un repositorio llamado: CoworkSpaceKC
echo    3. NO inicialices con README
echo    4. Copia la URL del repositorio
echo.
set /p REPO_URL="Pega aqui la URL del repositorio (https://github.com/...): "
echo.

echo [5/6] Conectando con GitHub...
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main
echo.

echo [6/6] SIGUIENTE PASO:
echo    1. Ve a https://railway.app/
echo    2. Login con GitHub
echo    3. Click en "New Project"
echo    4. Selecciona "Deploy from GitHub repo"
echo    5. Elige tu repositorio CoworkSpaceKC
echo    6. Click en "+ New" y agrega PostgreSQL
echo    7. Configura variables de entorno:
echo       - SECRET_KEY=django-insecure-8k#m+6@w^t9x$n2p-CAMBIA-ESTO
echo       - DEBUG=False
echo       - ALLOWED_HOSTS=*.railway.app,*.up.railway.app
echo.

echo [EXTRA] Instalar Railway CLI (opcional):
echo    npm install -g @railway/cli
echo    railway login
echo    railway link
echo    railway run python manage.py migrate
echo    railway run python manage.py createsuperuser
echo.

echo ========================================
echo   DESPLIEGUE INICIADO CON EXITO
echo ========================================
echo.
pause
