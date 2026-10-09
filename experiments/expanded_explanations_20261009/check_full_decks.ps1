$ErrorActionPreference='Stop'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
$expected=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'notes.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$files=@('Thesis_Defense_gg0_v3.pptx','Thesis_Defense_Projector_Silent.pptx','02_WebM_Silent.pptx','03_WMV_Silent.pptx')
$report=@()
try {
 foreach($file in $files){
  $deck=$app.Presentations.Open((Join-Path $PSScriptRoot $file),-1,0,0)
  if($deck.Slides.Count -ne 31){throw 'Slide count changed.'}
  $maxHeight=0
  $media=@()
  for($i=1;$i -le 31;$i++){
   $body=$null
   foreach($s in $deck.Slides.Item($i).NotesPage.Shapes){if($s.Type -eq 14 -and $s.PlaceholderFormat.Type -eq 2){$body=$s}}
   $range=$body.TextFrame.TextRange
   $want=($expected[$i-1] | ForEach-Object {$_.runs[0].run}) -join "`r"
   if($range.Text -cne $want){throw "Wrong notes in $file slide $i"}
   if($range.Font.Size -ne 18 -or $range.BoundHeight -gt ($body.Height-10)){throw "Notes layout problem in $file slide $i"}
   $maxHeight=[Math]::Max($maxHeight,$range.BoundHeight)
   foreach($s in $deck.Slides.Item($i).Shapes){if($s.Type -eq 16){$media+=@{slide=$i;durationMs=$s.MediaFormat.Length}}}
  }
  if($media.Count -ne 5){throw "Expected 5 used video shapes in $file"}
  if($file -eq $files[0]){
   $render=Join-Path $PSScriptRoot 'final_slides'
   New-Item -ItemType Directory -Path $render -Force | Out-Null
   for($i=1;$i -le 31;$i++){$deck.Slides.Item($i).Export((Join-Path $render ('slide-{0:d2}.png' -f $i)),'PNG',1440,810)}
  }
  $report+=@{file=$file;slides=31;notesChecked=31;fontSize=18;maxHeight=$maxHeight;media=$media}
  $deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck);$deck=$null
 }
 $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'full_decks_native_check.json') -Encoding UTF8
 Write-Output 'All four full decks opened in PowerPoint: 124 notes checked, all five video objects per deck recognized. All 31 final slides rendered.'
} finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($app.Presentations.Count -eq 0){$app.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
