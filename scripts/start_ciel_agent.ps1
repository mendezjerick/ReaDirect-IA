param(
    [int] $Port = 8003
)

$ErrorActionPreference = "Stop"

$Repo = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Repo ".venv\Scripts\python.exe"
$Python = if (Test-Path -LiteralPath $VenvPython) { $VenvPython } else { "python" }

Set-Location -LiteralPath $Repo
Write-Host "Starting deterministic Ciel Tutor Agent on http://127.0.0.1:$Port"
Write-Host "LLM enabled: false"
& $Python -m uvicorn main:app --host 127.0.0.1 --port $Port
