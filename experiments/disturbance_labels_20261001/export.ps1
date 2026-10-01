$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'preview_deck.pptx'),0,0,0)
 if ($deck.Slides.Count -ne 3) { throw 'Expected three preview slides.' }
 $deck.Saved=0
 $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
 Write-Output 'Rendered the three updated slides.'
} finally {
 if ($null -ne $deck) {$deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if ($app.Presentations.Count -eq 0) {$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
