param([switch]$Watch)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
        throw 'latexmk is required. Install MiKTeX and Perl and add them to PATH.'
    }
    $buildArgs = @('-pdf', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-outdir=..', '-auxdir=build')
    if ($Watch) { $buildArgs += @('-pvc', '-view=none') }
    & latexmk @buildArgs 'Thesis_Defense_Speaking_Script.tex'
    if ($LASTEXITCODE -ne 0) { throw "LaTeX build failed (exit $LASTEXITCODE). See build/Thesis_Defense_Speaking_Script.log." }
} finally {
    Pop-Location
}
