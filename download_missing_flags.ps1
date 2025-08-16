# Script PowerShell para baixar bandeiras faltantes
$missingFlags = @(
    "ai", "by", "gl", "gu", "mp", "vi", "vg", "ms", "pr", "ss", "tv", "va"
)

$flagsDir = "forgelock-web-platform/static/images/flags"

Write-Host "🚩 Baixando bandeiras faltantes..." -ForegroundColor Green

foreach ($flag in $missingFlags) {
    $url = "https://flagcdn.com/$flag.svg"
    $output = "$flagsDir/$flag.svg"
    
    try {
        Write-Host "⬇️  Baixando $flag..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
        Write-Host "✅ $flag baixado com sucesso" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Erro ao baixar $flag: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "🎉 Download concluído!" -ForegroundColor Green
