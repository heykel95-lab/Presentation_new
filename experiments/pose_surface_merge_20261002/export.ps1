$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'native_preview.pptx'),-1,0,0)
 if($deck.Slides.Count -ne 2){throw 'Expected merged slide and following controller slide.'}
 for($i=1;$i -le 2;$i++){$deck.Slides.Item($i).Export((Join-Path $PSScriptRoot ('native-slide-'+$i+'.png')),'PNG',1600,900)}
 $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
 Write-Output 'Rendered the merged slide and the following controller slide in PowerPoint.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
