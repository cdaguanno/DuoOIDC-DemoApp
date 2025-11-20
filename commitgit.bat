@echo off
cd /d "%~dp0"

git add .
git commit -m "Add environment-specific settings: base.py, local.py, production.py. Configure IDE to use local settings for development."
git push

Pause