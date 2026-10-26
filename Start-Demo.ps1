$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$demoPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $demoPython)) {
    py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12, then run this file again.' }
    & $demoPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation did not finish. See README.md.' }
}
& $demoPython -m streamlit run streamlit_app.py --server.port 8502
