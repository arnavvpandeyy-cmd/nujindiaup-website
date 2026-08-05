@echo off
title NUJ UP - Development Server
echo.
echo  ====================================================
echo    NUJ Uttar Pradesh - Development Server Launcher
echo  ====================================================
echo.

cd /d "%~dp0"

echo  [Step 1/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo  ERROR: Could not activate venv. Is it set up?
    pause
    exit /b 1
)

echo  [Step 2/7] Running makemigrations (all apps)...
python manage.py makemigrations
echo.

echo  [Step 3/7] Applying all database migrations...
python manage.py migrate
echo.

echo  [Step 4/7] Loading UP fixture data (phone: 7054000149, 75 cities)...
python manage.py loaddata fixtures/initial_data.json
echo.

echo  [Step 5/7] Creating Django superuser (admin) if missing...
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(username='admin').exists() or U.objects.create_superuser('admin','admin@nujup.org','admin123')"
echo.

echo  [Step 6/7] Creating Portal Super Admin account if missing...
python manage.py shell < scripts\create_superadmin.py
echo.

echo  [Step 7/7] Starting development server...
echo.
echo  ====================================================
echo    Server         : http://localhost:8000/
echo  ----------------------------------------------------
echo    Public Site    : http://localhost:8000/
echo    About          : http://localhost:8000/about/
echo    City Units     : http://localhost:8000/city-units/
echo    Office Bearers : http://localhost:8000/office-bearers/
echo    Newsroom       : http://localhost:8000/newsroom/
echo    Contact        : http://localhost:8000/contact/
echo  ----------------------------------------------------
echo    ADMIN PANEL (Django) : http://localhost:8000/nuj-admin/
echo      Login: admin / admin123
echo  ----------------------------------------------------
echo    SUPER ADMIN PORTAL   : http://localhost:8000/portal/admin/
echo      Login: superadmin / NujUp@2024
echo  ----------------------------------------------------
echo    CUSTOM ADMIN PANEL   : http://localhost:8000/portal/admin-panel/
echo      (All modules, recent actions, full control)
echo  ----------------------------------------------------
echo    MEMBER LOGIN         : http://localhost:8000/membership/login/
echo    MEMBER APPLY         : http://localhost:8000/membership/apply/
echo    MEMBER DASHBOARD     : http://localhost:8000/portal/dashboard/
echo  ----------------------------------------------------
echo    Contact No : 7054000149
echo  ====================================================
echo.
echo  Press Ctrl+C to stop the server.
echo.

python manage.py runserver
pause
