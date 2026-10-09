$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'native_preview.pptx'),-1,0,0)
 if($deck.Slides.Count -ne 31){throw 'Expected 31 slides.'}
 $report=@()
 for($i=1;$i -le 31;$i++){
  $body=$null
  foreach($shape in $deck.Slides.Item($i).NotesPage.Shapes){if($shape.Type -eq 14 -and $shape.PlaceholderFormat.Type -eq 2){$body=$shape}}
  if($null -eq $body){throw "Missing notes body on slide $i"}
  $range=$body.TextFrame.TextRange
  if($range.Font.Size -ne 18){throw "Wrong font size on slide $i"}
  if($range.BoundHeight -gt ($body.Height - 10)){throw "Notes overflow on slide $i"}
  $report+=@{slide=$i;text=$range.Text;paragraphs=$range.Paragraphs().Count;left=$body.Left;top=$body.Top;width=$body.Width;height=$body.Height;boundHeight=$range.BoundHeight;fontSize=$range.Font.Size}
 }
 $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'powerpoint_notes_check.json') -Encoding utf8
 foreach($slide in $deck.Slides){$slide.SlideShowTransition.Hidden=0}
 $printRange=$deck.PrintOptions.Ranges.Add(1,31)
 $deck.ExportAsFixedFormat((Join-Path $PSScriptRoot 'notes_preview.pdf'),2,2,0,1,5,-1,$printRange,1)
 Write-Output 'PowerPoint confirmed 18 pt and exported all 31 notes pages.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
