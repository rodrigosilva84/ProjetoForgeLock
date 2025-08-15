Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   FORGELOCK - AMBIENTE DE DESENVOLVIMENTO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Parando containers existentes..." -ForegroundColor Yellow
docker-compose down

Write-Host "[2/3] Iniciando ambiente PostgreSQL + Django..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "[3/3] Aguardando inicializacao..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    AMBIENTE PRONTO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Django: http://localhost:8000" -ForegroundColor White
Write-Host "PostgreSQL: localhost:5433" -ForegroundColor White
Write-Host ""
Write-Host "Comandos uteis:" -ForegroundColor Cyan
Write-Host "  - Ver logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "  - Parar: docker-compose down" -ForegroundColor Gray
Write-Host "  - Rebuild: docker-compose up --build" -ForegroundColor Gray
Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

