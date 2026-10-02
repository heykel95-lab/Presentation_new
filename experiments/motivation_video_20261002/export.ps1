$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot 'native_preview.pptx'),-1,0,0)
 if ($deck.Slides.Count -ne 2) {throw 'Expected two preview slides.'}
 $records=@()
 for($i=1;$i -le 2;$i++) {
  $slide=$deck.Slides.Item($i)
  $slide.Export((Join-Path $PSScriptRoot ('native-slide-'+$i+'.png')),'PNG',1600,900)
  for($j=1;$j -le $slide.Shapes.Count;$j++) {
   $shape=$slide.Shapes.Item($j)
   if($shape.Name -eq 'Contact demonstration video') {
    $records+=@{slide=$i;name=$shape.Name;type=$shape.Type;mediaType=$shape.MediaType;left=$shape.Left;top=$shape.Top;width=$shape.Width;height=$shape.Height;durationMs=$shape.MediaFormat.Length;volume=$shape.MediaFormat.Volume;playOnEntry=$shape.AnimationSettings.PlaySettings.PlayOnEntry}
   }
  }
 }
 $deck.SaveAs((Join-Path $PSScriptRoot 'native_export.pdf'),32)
 $records | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $PSScriptRoot 'native_media_inspection.json')
 Write-Output 'PowerPoint opened the edited slides, recognized the embedded movie and exported the previews.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
