param(
    [string]$FrontendUrl,
    [string]$BackendUrl
)

if (-not $FrontendUrl -and -not $BackendUrl) {
    Write-Host "Usage: ./scripts/smoke_test.ps1 -FrontendUrl <url> -BackendUrl <url>"
    exit 1
}

if ($FrontendUrl) {
    Write-Host "Testing frontend: $FrontendUrl"
    try {
        $r = Invoke-RestMethod -Uri $FrontendUrl -Method Get -TimeoutSec 10
        Write-Host "Frontend responded (length):" ($r.Length)
    } catch {
        Write-Error "Frontend check failed: $_"
    }
}

if ($BackendUrl) {
    Write-Host "Testing backend /docs: $BackendUrl/docs"
    try {
        $r = Invoke-RestMethod -Uri (Join-Path $BackendUrl 'docs') -Method Get -TimeoutSec 10
        Write-Host "Backend /docs status: OK"
    } catch {
        Write-Error "Backend check failed: $_"
    }
}
