@echo off
setlocal

if "%DJ_SUPERUSER_USERNAME%"=="" (
  echo [ERROR] Set DJ_SUPERUSER_USERNAME, DJ_SUPERUSER_EMAIL, DJ_SUPERUSER_PASSWORD first.
  echo Example:
  echo   set DJ_SUPERUSER_USERNAME=Arjun
  echo   set DJ_SUPERUSER_EMAIL=arjun@example.com
  echo   set DJ_SUPERUSER_PASSWORD=Bubbles
  echo   CREATE_SUPERUSER.bat
  pause
  exit /b 1
)

py -3.11 manage.py shell -c "from django.contrib.auth import get_user_model; \
User=get_user_model(); \
u=User.objects.filter(username=r'%DJ_SUPERUSER_USERNAME%').first(); \
import os; \
if not u: \
    User.objects.create_superuser(username=os.environ.get('DJ_SUPERUSER_USERNAME'), \
                                  email=os.environ.get('DJ_SUPERUSER_EMAIL',''), \
                                  password=os.environ.get('DJ_SUPERUSER_PASSWORD')); \
    print('Created superuser:', os.environ.get('DJ_SUPERUSER_USERNAME')); \
else: \
    print('Superuser already exists:', u.username)"
