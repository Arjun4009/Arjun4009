@echo off
setlocal
py -3.11 manage.py collectstatic --noinput
