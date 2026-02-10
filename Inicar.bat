@echo off
cd Server/Backend
echo Verificando e instalando dependencias
pip install -r requeriments.txt

echo.
echo Dependencias OK
echo.
echo Iniciando servidor
echo.
python -m uvicorn main:app --reload
pause