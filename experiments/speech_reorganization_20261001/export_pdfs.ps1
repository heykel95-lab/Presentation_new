$ErrorActionPreference = 'Stop'
$rootDir = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$sourceDeck = [System.IO.Path]::GetFullPath((Join-Path $rootDir 'Final Presentation/Thesis_Defense_gg0_v3.pptx'))
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($sourceDeck, -1, 0, 0)
    if ($deck.Slides.Count -ne 31) { throw 'Unexpected slide count.' }
    foreach ($slide in $deck.Slides) { $slide.SlideShowTransition.Hidden = 0 }
    $deck.SaveAs((Join-Path $PSScriptRoot 'Thesis_Defense_gg0_v3.pdf'), 32)
    Write-Output 'Exported the full 31-page presentation.'
    $deck.Saved = -1
    $deck.Close()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)
    $deck = $app.Presentations.Open($sourceDeck, -1, 0, 0)
    foreach ($slide in $deck.Slides) { $slide.SlideShowTransition.Hidden = 0 }
    for ($index = 26; $index -ge 1; $index--) { $deck.Slides.Item($index).Delete() }
    if ($deck.Slides.Count -ne 5) { throw 'Unexpected backup count.' }
    $deck.SaveAs((Join-Path $PSScriptRoot 'Supplementary_slides.pdf'), 32)
    Write-Output 'Exported the five supplementary pages.'
} finally {
    if ($null -ne $deck) {
        $deck.Saved = -1
        $deck.Close()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)
    }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
