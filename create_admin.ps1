$ErrorActionPreference = "Stop"

try {
    $body = @{
        username = "admin"
        email = "admin@example.com"
        password = "admin123"
        is_admin = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body $body
    
    Write-Host "Success! Created user:" -ForegroundColor Green
    Write-Host "Username: admin"
    Write-Host "Password: admin123"
} catch {
    $err = $_.Exception.Response
    if ($null -ne $err -and $err.StatusCode -eq 400) {
       $stream = $err.GetResponseStream()
       $reader = New-Object System.IO.StreamReader($stream)
       $responseBody = $reader.ReadToEnd()
       if ($responseBody -match "Username or email already exists") {
           Write-Host "Admin user already exists. Skipping creation." -ForegroundColor Yellow
           exit 0
       }
    }
    Write-Error "Failed to create user. Ensure the backend is running at http://localhost:8000"
    Write-Error $_.Exception.Message
}
