$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $report=@()
 foreach($variant in @('before','after')){
  $file=if($variant -eq 'before'){Join-Path $PSScriptRoot 'archive/original.pptx'}else{Join-Path $PSScriptRoot 'updated.pptx'}
  $deck=$app.Presentations.Open($file,-1,0,0)
  if($deck.Slides.Count -ne 31){throw 'Slide count changed'}
  $dir=Join-Path $PSScriptRoot $variant
  [void](New-Item -ItemType Directory -Force -Path $dir)
  for($i=1;$i -le 31;$i++){
   $slide=$deck.Slides.Item($i)
   $slide.Export((Join-Path $dir ('slide-{0:D2}.png' -f $i)),'PNG',1440,810)
   if($variant -eq 'after'){
    foreach($shape in $slide.Shapes){
     if($shape.Type -eq 16){
      $mf=$shape.MediaFormat
      $report+=@{slide=$i;shapeId=$shape.Id;name=$shape.Name;length=$mf.Length;videoWidth=$mf.VideoFrameWidth;videoHeight=$mf.VideoFrameHeight;videoFormat=$mf.VideoFormat;audioFormat=$mf.AudioFormat;isEmbedded=$mf.IsEmbedded;isLinked=$mf.IsLinked}
     }
    }
    $body=$null
    foreach($shape in $slide.NotesPage.Shapes){if($shape.Type -eq 14 -and $shape.PlaceholderFormat.Type -eq 2){$body=$shape}}
    if($null -eq $body -or $body.TextFrame.TextRange.Font.Size -ne 18){throw "Notes size changed on slide $i"}
   }
  }
  foreach($slide in $deck.Slides){$slide.SlideShowTransition.Hidden=0}
  $range=$deck.PrintOptions.Ranges.Add(1,31)
  $deck.ExportAsFixedFormat((Join-Path $PSScriptRoot ($variant+'.pdf')),2,2,0,1,1,-1,$range,1)
  $deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck);$deck=$null
  Write-Output "Rendered all 31 slides: $variant"
 }
 $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'powerpoint_media.json') -Encoding utf8
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
