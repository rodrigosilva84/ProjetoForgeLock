@echo off
echo ========================================
echo    FORGELOCK - AMBIENTE DE DESENVOLVIMENTO
echo ========================================
echo.

echo [1/3] Parando containers existentes...
docker-compose down

echo [2/3] Iniciando ambiente PostgreSQL + Django...
docker-compose up -d

echo [3/3] Aguardando inicializacao...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo    AMBIENTE PRONTO!
echo ========================================
echo.
echo Django: http://localhost:8000
echo PostgreSQL: localhost:5433
echo.
echo Comandos uteis:
echo   - Ver logs: docker-compose logs -f
echo   - Parar: docker-compose down
echo   - Rebuild: docker-compose up --build
echo.
pause

