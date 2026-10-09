param([string]$DeckName='updated.pptx',[string]$ReportName='powerpoint_playback.json')
$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null;$show=$null
try {
 $app.Visible=-1
 $deck=$app.Presentations.Open((Join-Path $PSScriptRoot $DeckName),-1,0,-1)
 Write-Output 'Opened deck for playback.'
 $deck.SlideShowSettings.ShowType=2
 $show=$deck.SlideShowSettings.Run()
 Write-Output 'Started windowed slideshow.'
 $results=@()
 foreach($i in @(2,12,20,21,26)){
  $show.View.GotoSlide($i)
  Start-Sleep -Milliseconds 400
  $slide=$deck.Slides.Item($i)
  foreach($shape in $slide.Shapes){
   if($shape.Type -ne 16){continue}
   $player=$show.View.Player($shape.Id)
   $tests=@()
   foreach($pos in @(0,[int]($shape.MediaFormat.Length/2),[int]($shape.MediaFormat.Length-2000))){
    $player.CurrentPosition=$pos
    $player.Play()
    Start-Sleep -Milliseconds 1100
    $state=$player.State;$actual=$player.CurrentPosition
    $tests+=@{seek_ms=$pos;position_ms=$actual;state=$state;advanced=($actual -gt ($pos+200))}
    if($state -ne 0 -or $actual -le ($pos+200)){throw "Playback failed on slide $i at $pos ms. State $state, position $actual"}
    $player.Pause()
   }
   $player.Stop()
   $results+=@{slide=$i;shapeId=$shape.Id;length_ms=$shape.MediaFormat.Length;tests=$tests}
   $results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $PSScriptRoot $ReportName) -Encoding utf8
   Write-Output "PowerPoint played video on slide $i at start, middle and end."
  }
 }
} catch {
 $_ | Out-String | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'playback_error.txt')
 throw
} finally {
 if($null -ne $show){try{$show.View.Exit()}catch{}}
 if($null -ne $deck){try{$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}catch{}}
 try{if($app.Presentations.Count -eq 0){$app.Quit()}}catch{}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
