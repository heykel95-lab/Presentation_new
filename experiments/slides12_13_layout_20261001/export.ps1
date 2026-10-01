$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
    $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'preview_deck.pptx'),0,0,0)
    if ($deck.Slides.Count -ne 2) { throw 'Unexpected preview slide count.' }
    $deck.Slides.Item(1).Export((Join-Path $PSScriptRoot 'native-13.png'),'PNG',1500,844)
    $deck.Slides.Item(2).Export((Join-Path $PSScriptRoot 'native-14.png'),'PNG',1500,844)
    $deck.Saved=0
    $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
    Write-Output 'Rendered both edited slides.'
} finally {
    if ($null -ne $deck) { $deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
