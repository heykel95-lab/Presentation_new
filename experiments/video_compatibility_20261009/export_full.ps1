$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application;$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'updated.pptx'),-1,0,0)
 foreach($slide in $deck.Slides){$slide.SlideShowTransition.Hidden=0}
 $range=$deck.PrintOptions.Ranges.Add(1,31)
 $deck.ExportAsFixedFormat((Join-Path $PSScriptRoot 'regenerated_full.pdf'),2,2,0,1,1,-1,$range,1)
 Write-Output 'Exported the full deck including all six hidden backups.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
