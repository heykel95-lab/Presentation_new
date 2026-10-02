$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'labels.pptx'),-1,0,0)
 $deck.SaveAs((Join-Path $PSScriptRoot 'labels_native.pdf'),32)
 $deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck);$deck=$null
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'native_preview.pptx'),-1,0,0)
 for($i=1;$i -le $deck.Slides.Count;$i++) {
  $deck.Slides.Item($i).Export((Join-Path $PSScriptRoot ('native-slide-'+$i+'.png')),'PNG',1600,900)
 }
 $deck.SaveAs((Join-Path $PSScriptRoot 'native_preview.pdf'),32)
 Write-Output 'Exported all chapter-label variants and three representative content slides in PowerPoint.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
