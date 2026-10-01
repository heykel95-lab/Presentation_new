$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
    $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'preview_deck.pptx'),0,0,0)
    if ($deck.Slides.Count -ne 1) { throw 'Unexpected preview slide count.' }
    $deck.Slides.Item(1).Export((Join-Path $PSScriptRoot 'native-18.png'),'PNG',1500,844)
    $deck.Saved=0
    $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
    Write-Output 'Rendered the three legends beneath their plots.'
} finally {
    if ($null -ne $deck) { $deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
