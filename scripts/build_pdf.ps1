$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$html = Join-Path $repo 'exports\html\agent-architecture.html'
$pdf = Join-Path $repo 'exports\pdf\agent-architecture.pdf'
$edgeCandidates = @(
  'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
  'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
)
$edge = $edgeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $edge) { throw 'Microsoft Edge not found; cannot render PDF.' }
if (-not (Test-Path -LiteralPath $html)) { throw "HTML not found: $html" }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $pdf) | Out-Null
$profile = Join-Path $env:TEMP ('codex-agent-kb-pdf-' + [guid]::NewGuid().ToString('N'))
$uri = [System.Uri]::new($html).AbsoluteUri
& $edge --headless=new --disable-gpu --no-pdf-header-footer "--user-data-dir=$profile" "--print-to-pdf=$pdf" $uri
if (-not (Test-Path -LiteralPath $pdf)) { throw 'PDF generation failed.' }
Write-Output "pdf: $pdf"
