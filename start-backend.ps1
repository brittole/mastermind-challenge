$backendPath = "c:\Users\Leticia\projetos\mastermind-challenge\backend"
Push-Location $backendPath
try {
    Write-Host "🚀 Iniciando backend..."
    & python wsgi.py
} finally {
    Pop-Location
}
