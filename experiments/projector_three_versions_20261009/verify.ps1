param([Parameter(Mandatory=$true)][string]$Variant)
$ErrorActionPreference='Stop'
$dir=Join-Path $PSScriptRoot $Variant
$app=New-Object -ComObject PowerPoint.Application;$deck=$null;$show=$null
try {
 $app.Visible=-1
 $deck=$app.Presentations.Open((Join-Path $dir 'presentation.pptx'),-1,0,-1)
 if($deck.Slides.Count -ne 31){throw 'Slide count changed'}
 $render=Join-Path $dir 'slides';[void](New-Item -ItemType Directory -Force -Path $render)
 $media=@()
 for($i=1;$i -le 31;$i++){
  $slide=$deck.Slides.Item($i)
  $slide.Export((Join-Path $render ('slide-{0:D2}.png' -f $i)),'PNG',1440,810)
  $body=$null
  foreach($s in $slide.NotesPage.Shapes){if($s.Type -eq 14 -and $s.PlaceholderFormat.Type -eq 2){$body=$s}}
  if($null -eq $body -or $body.TextFrame.TextRange.Font.Size -ne 18){throw "Notes changed: $i"}
  foreach($s in $slide.Shapes){if($s.Type -eq 16){$media+=@{slide=$i;id=$s.Id;length=$s.MediaFormat.Length;embedded=$s.MediaFormat.IsEmbedded;linked=$s.MediaFormat.IsLinked}}}
 }
 if($media.Count -ne 5){throw 'Expected five used videos'}
 $media | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $dir 'native_media.json') -Encoding utf8
 Write-Output "Rendered all 31 slides and confirmed 18 pt notes: $Variant"
 $deck.SlideShowSettings.ShowType=2;$show=$deck.SlideShowSettings.Run()
 $results=@()
 foreach($m in $media){
  $show.View.GotoSlide($m.slide);Start-Sleep -Milliseconds 400
  $player=$show.View.Player($m.id);$tests=@()
  foreach($pos in @(0,[int]($m.length/2),[int]($m.length-2000))){
   $player.CurrentPosition=$pos;$player.Play();Start-Sleep -Milliseconds 1200
   $state=$player.State;$actual=$player.CurrentPosition;$waited=1200
   while($actual -le ($pos+200) -and $waited -lt 8000){Start-Sleep -Milliseconds 300;$waited+=300;$state=$player.State;$actual=$player.CurrentPosition}
   $tests+=@{seek_ms=$pos;position_ms=$actual;state=$state;advanced=($actual -gt ($pos+200));waited_ms=$waited}
   if($state -ne 0 -or $actual -le ($pos+200)){throw "Playback failed: $Variant slide $($m.slide) at $pos. State $state position $actual"}
   $player.Pause()
  }
  $player.Stop()
  $results+=@{slide=$m.slide;length_ms=$m.length;tests=$tests}
  $results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $dir 'native_playback.json') -Encoding utf8
  Write-Output "Passed start/middle/end playback: $Variant slide $($m.slide)"
 }
 $show.View.Exit();$show=$null
 foreach($slide in $deck.Slides){$slide.SlideShowTransition.Hidden=0}
 $range=$deck.PrintOptions.Ranges.Add(1,31)
 $deck.ExportAsFixedFormat((Join-Path $dir 'qa_full.pdf'),2,2,0,1,1,-1,$range,1)
} catch {
 $_ | Out-String | Set-Content -LiteralPath (Join-Path $dir 'native_error.txt')
 throw
} finally {
 if($null -ne $show){try{$show.View.Exit()}catch{}}
 if($null -ne $deck){try{$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}catch{}}
 try{if($app.Presentations.Count -eq 0){$app.Quit()}}catch{}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
