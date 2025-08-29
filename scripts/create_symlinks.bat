@echo off
echo 🔗 Создание симлинков для схем...

cd C:\Users\pbolk\Documents\GitHub\ai-instructions

REM Создаем симлинк для deepseek-instructions
cd schemas\deepseek-instructions
if exist latest.schema.json del latest.schema.json
powershell -Command "New-Item -ItemType SymbolicLink -Name 'latest.schema.json' -Target 'v1.5.schema.json'"
echo ✅ Создан симлинк: deepseek-instructions/latest.schema.json

REM Создаем симлинк для context-config  
cd ..\context-config
if exist latest.schema.json del latest.schema.json
powershell -Command "New-Item -ItemType SymbolicLink -Name 'latest.schema.json' -Target 'v1.5.schema.json'"
echo ✅ Создан симлинк: context-config/latest.schema.json

cd ..\..
echo 🎉 Симлинки успешно созданы!