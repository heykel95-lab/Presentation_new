$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$deck = 'C:\Users\USER\Desktop\Presentation_new\Final Presentation\Thesis_Defense_gg0_v3.pptx'
$backup = Join-Path $PSScriptRoot 'before-overview.pptx'
if (-not (Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $deck -Destination $backup }
$zip = [IO.Compression.ZipFile]::Open($deck, [IO.Compression.ZipArchiveMode]::Update)
try {
 function Read-Part([string]$path) {
  $partReader = New-Object IO.StreamReader($zip.GetEntry($path).Open())
  try { return [xml]$partReader.ReadToEnd() } finally { $partReader.Dispose() }
 }
 $presentation = Read-Part 'ppt/presentation.xml'
 $relationships = Read-Part 'ppt/_rels/presentation.xml.rels'
 $titles = @()
 $overviewPath = $null
 $foundConclusion = $false
 foreach ($slideId in $presentation.DocumentElement.sldIdLst.sldId) {
  $relId = $slideId.GetAttribute('id','http://schemas.openxmlformats.org/officeDocument/2006/relationships')
  $target = ($relationships.DocumentElement.Relationship | Where-Object { $_.Id -eq $relId }).Target
  $partPath = ([Uri]::new([Uri]'http://local/ppt/presentation.xml', [string]$target)).AbsolutePath.TrimStart('/')
  $slideXml = Read-Part $partPath
  $slideNs = New-Object Xml.XmlNamespaceManager($slideXml.NameTable)
  $slideNs.AddNamespace('p','http://schemas.openxmlformats.org/presentationml/2006/main')
  $slideNs.AddNamespace('a','http://schemas.openxmlformats.org/drawingml/2006/main')
  $titleShape = $slideXml.SelectSingleNode('//p:sp[p:nvSpPr/p:cNvPr[@name="Slide title"] or p:nvSpPr/p:nvPr/p:ph[@type="title" or @type="ctrTitle"]]', $slideNs)
  $title = if ($titleShape) { ($titleShape.SelectNodes('.//a:t',$slideNs) | ForEach-Object { $_.InnerText }) -join '' } else { '' }
  if ($title -eq 'Overview') { $overviewPath = $partPath; continue }
  if ($overviewPath -and $slideXml.DocumentElement.GetAttribute('show') -ne '0') {
   if ($slideXml.SelectNodes('//*[local-name()="videoFile"]').Count -gt 0) { continue }
   if (-not $title) { throw "Missing title in $partPath; cannot synchronize Overview." }
   $titles += $title
   if ($title -eq 'Conclusion') { $foundConclusion = $true; break }
  }
 }
 if (-not $overviewPath -or $titles.Count -eq 0) { throw 'Overview or subsequent slide titles not found.' }
 if (-not $foundConclusion) { throw 'Visible Conclusion slide not found after Overview.' }
 # List exact titles in slide order through Conclusion, excluding videos and hidden slides.
 $step = [Math]::Min(34, 374 / [Math]::Max(1, $titles.Count - 1))
 if ($step -lt 30) { throw 'The detailed Overview needs a revised layout to fit more than 13 titles legibly.' }

 $entry = $zip.GetEntry($overviewPath)
 $reader = New-Object IO.StreamReader($entry.Open())
 [xml]$xml = $reader.ReadToEnd()
 $reader.Dispose()
 $ns = New-Object Xml.XmlNamespaceManager($xml.NameTable)
 $ns.AddNamespace('p','http://schemas.openxmlformats.org/presentationml/2006/main')
 $ns.AddNamespace('a','http://schemas.openxmlformats.org/drawingml/2006/main')
 $items = @($xml.SelectNodes('//p:sp[p:txBody/a:p/a:pPr/a:buChar or p:txBody/a:p/a:pPr/a:buAutoNum or starts-with(p:nvSpPr/p:cNvPr/@name,"Overview item ")]', $ns))
 $template = $items[0].CloneNode($true)
 $parent = $items[0].ParentNode
 foreach ($item in $items) { [void]$parent.RemoveChild($item) }
 foreach ($oldNumber in @($xml.SelectNodes('//p:sp[starts-with(p:nvSpPr/p:cNvPr/@name,"Overview number ")]', $ns))) { [void]$parent.RemoveChild($oldNumber) }
 for ($i=0; $i -lt $titles.Count; $i++) {
  $shape = $template.CloneNode($true)
  $meta = $shape.SelectSingleNode('p:nvSpPr/p:cNvPr',$ns)
  $meta.SetAttribute('id', [string](20+2*$i))
  $meta.SetAttribute('name', 'Overview item '+($i+1))
  $shape.SelectSingleNode('p:spPr/a:xfrm/a:off',$ns).SetAttribute('y',[string][int]((82+$i*$step)*12700))
  $shape.SelectSingleNode('p:spPr/a:xfrm/a:ext',$ns).SetAttribute('cy','381000')
  $shape.SelectSingleNode('p:txBody/a:p/a:r/a:t',$ns).InnerText = $titles[$i]
  $shape.SelectSingleNode('p:txBody/a:p/a:r/a:rPr',$ns).SetAttribute('sz','2200')
  $shape.SelectSingleNode('p:txBody/a:p/a:r/a:rPr/a:solidFill/a:srgbClr',$ns).SetAttribute('val','17365D')
  $paragraph = $shape.SelectSingleNode('p:txBody/a:p/a:pPr',$ns)
  $paragraph.SetAttribute('marL','0')
  $paragraph.SetAttribute('indent','0')
  foreach ($marker in @($paragraph.SelectNodes('a:buChar | a:buAutoNum | a:buNone',$ns))) { [void]$paragraph.RemoveChild($marker) }
  [void]$paragraph.AppendChild($xml.CreateElement('a','buNone',$ns.LookupNamespace('a')))
  $shape.SelectSingleNode('p:spPr/a:xfrm/a:off',$ns).SetAttribute('x','1605280')
  $shape.SelectSingleNode('p:spPr/a:xfrm/a:ext',$ns).SetAttribute('cx','9276080')
  $numberShape = $shape.CloneNode($true)
  $numberMeta = $numberShape.SelectSingleNode('p:nvSpPr/p:cNvPr',$ns)
  $numberMeta.SetAttribute('id',[string](21+2*$i))
  $numberMeta.SetAttribute('name','Overview number '+($i+1))
  $numberShape.SelectSingleNode('p:spPr/a:xfrm/a:off',$ns).SetAttribute('x','919480')
  $numberShape.SelectSingleNode('p:spPr/a:xfrm/a:ext',$ns).SetAttribute('cx','558800')
  $numberShape.SelectSingleNode('p:txBody/a:p/a:pPr',$ns).SetAttribute('algn','r')
  $numberShape.SelectSingleNode('p:txBody/a:p/a:r/a:t',$ns).InnerText = [string]($i+1)+'.'
  [void]$parent.AppendChild($numberShape)
  [void]$parent.AppendChild($shape)
 }
 $entry.Delete()
 $newEntry = $zip.CreateEntry($overviewPath)
 $writer = New-Object IO.StreamWriter($newEntry.Open(), (New-Object Text.UTF8Encoding($false)))
 $xml.Save($writer)
 $writer.Dispose()
 Write-Output ('Overview synchronized with ' + $titles.Count + ' slide titles through Conclusion; videos excluded.')
} finally { $zip.Dispose() }
