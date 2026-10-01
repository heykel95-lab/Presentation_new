$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'preview_deck.pptx'),0,0,0)
 if ($deck.Slides.Count -ne 4) { throw 'Expected four preview slides.' }
 $deck.Saved=0
 $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
 Write-Output 'Rendered four updated slides in PowerPoint.'
} finally {
 if ($null -ne $deck) {$deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if ($app.Presentations.Count -eq 0) {$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
