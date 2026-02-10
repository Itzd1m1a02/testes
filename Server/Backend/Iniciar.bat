@echo off
echo Verificando e instalando dependencias
pip install -r requeriments.txt

echo.
echo Dependencias OK
echo.
echo Iniciando servidor
echo.
uvicorn main:app --reload
pause