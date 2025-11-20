@echo off
cd /d "%~dp0"

set /p ChangeDiscText="Enter Change Discription: "

git add .
git commit -m "%ChangeDiscText%"
git push

Pause