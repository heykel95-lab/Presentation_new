$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
    $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'updated.pptx'),-1,0,0)
    if ($deck.Slides.Count -ne 31) { throw 'Unexpected slide count.' }
    foreach ($slide in $deck.Slides) { $slide.SlideShowTransition.Hidden=0 }
    $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
    Write-Output 'Exported 31 slides for verification.'
} finally {
    if ($null -ne $deck) { $deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
