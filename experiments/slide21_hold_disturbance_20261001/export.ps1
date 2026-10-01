$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
    $sourceFile=[System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../Final Presentation/Thesis_Defense_gg0_v3.pptx'))
    $deck=$app.Presentations.Open($sourceFile,-1,0,0)
    if ($deck.Slides.Count -ne 31) { throw 'Unexpected slide count.' }
    foreach ($slide in $deck.Slides) { $slide.SlideShowTransition.Hidden=0 }
    $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
    Write-Output 'Rendered the revised deck.'
} finally {
    if ($null -ne $deck) { $deck.Saved=-1; $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
