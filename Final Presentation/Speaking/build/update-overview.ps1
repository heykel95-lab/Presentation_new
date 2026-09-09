param([string]$DeckPath='C:\Users\USER\Desktop\Presentation_new\Final Presentation\Thesis_Defense_gg0_v3.pptx')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$zip=[IO.Compression.ZipFile]::Open($DeckPath,[IO.Compression.ZipArchiveMode]::Update)
try {
 function Read-Part([string]$path){
  $r=[IO.StreamReader]::new($zip.GetEntry($path).Open())
  try{return [xml]$r.ReadToEnd()}finally{$r.Dispose()}
 }
 function Namespace-Map($xml){
  $map=[Xml.XmlNamespaceManager]::new($xml.NameTable)
  $map.AddNamespace('p','http://schemas.openxmlformats.org/presentationml/2006/main')
  $map.AddNamespace('a','http://schemas.openxmlformats.org/drawingml/2006/main')
  return ,$map
 }
 $pres=Read-Part 'ppt/presentation.xml';$rels=Read-Part 'ppt/_rels/presentation.xml.rels'
 $overviewPaths=@();$titles=@();$conclusionFound=$false
 foreach($id in $pres.DocumentElement.sldIdLst.sldId){
  $rid=$id.GetAttribute('id','http://schemas.openxmlformats.org/officeDocument/2006/relationships')
  $target=($rels.DocumentElement.Relationship | Where-Object {$_.Id -eq $rid}).Target
  $path=([Uri]::new([Uri]'http://local/ppt/presentation.xml',[string]$target)).AbsolutePath.TrimStart('/')
  $xml=Read-Part $path;$ns=Namespace-Map $xml
  $shape=$xml.SelectSingleNode('//p:sp[p:nvSpPr/p:cNvPr[@name="Slide title"]]',$ns)
  $title=if($shape){($shape.SelectNodes('.//a:t',$ns) | ForEach-Object {$_.InnerText}) -join ''}else{''}
  if($title -eq 'Overview'){$overviewPaths+=$path}
  if($title -eq 'Conclusion'){$conclusionFound=$true}
 }
 if(-not $conclusionFound -or $overviewPaths.Count -ne 1){throw 'Expected one Overview and a Conclusion slide.'}
 foreach($section in $pres.SelectNodes('//*[local-name()="sectionLst"]/*[local-name()="section"]')){
  $name=$section.GetAttribute('name')
  if($name -and $name -ne 'Backup'){$titles+=$name}
 }
 if($titles.Count -eq 0){throw 'Native PowerPoint chapter sections are missing.'}
 if($titles.Count -gt 8){throw 'More than eight chapters requires an Overview layout review.'}
 $perPage=$titles.Count
 for($page=0;$page -lt $overviewPaths.Count;$page++){
  $xml=Read-Part $overviewPaths[$page];$ns=Namespace-Map $xml
  $items=@($xml.SelectNodes('//p:sp[starts-with(p:nvSpPr/p:cNvPr/@name,"Overview item ")]',$ns))
  if($items.Count -eq 0){throw 'Overview item template missing.'}
  $template=$items[0].CloneNode($true);$parent=$items[0].ParentNode
  foreach($node in @($xml.SelectNodes('//p:sp[starts-with(p:nvSpPr/p:cNvPr/@name,"Overview item ") or starts-with(p:nvSpPr/p:cNvPr/@name,"Overview number ")]',$ns))){[void]$parent.RemoveChild($node)}
  $start=$page*$perPage;$count=[Math]::Min($perPage,$titles.Count-$start)
  $step=[Math]::Min(58,350/[Math]::Max(1,$count-1))
  for($row=0;$row -lt $count;$row++){
   $index=$start+$row;$shape=$template.CloneNode($true)
   $meta=$shape.SelectSingleNode('p:nvSpPr/p:cNvPr',$ns);$meta.SetAttribute('id',[string](100+2*$row));$meta.SetAttribute('name','Overview item '+($index+1))
   $off=$shape.SelectSingleNode('p:spPr/a:xfrm/a:off',$ns);$off.SetAttribute('x','1605280');$off.SetAttribute('y',[string][int]((100+$row*$step)*12700))
   $ext=$shape.SelectSingleNode('p:spPr/a:xfrm/a:ext',$ns);$ext.SetAttribute('cx','9276080');$ext.SetAttribute('cy','381000')
   $shape.SelectSingleNode('p:txBody/a:p/a:r/a:t',$ns).InnerText=$titles[$index]
   $run=$shape.SelectSingleNode('p:txBody/a:p/a:r/a:rPr',$ns);$run.SetAttribute('sz','2200');$run.SetAttribute('b','0')
   $run.SelectSingleNode('a:solidFill/a:srgbClr',$ns).SetAttribute('val','17365D')
   $para=$shape.SelectSingleNode('p:txBody/a:p/a:pPr',$ns);$para.SetAttribute('marL','0');$para.SetAttribute('indent','0');$para.SetAttribute('algn','l')
   foreach($marker in @($para.SelectNodes('a:buChar|a:buAutoNum|a:buNone',$ns))){[void]$para.RemoveChild($marker)}
   [void]$para.AppendChild($xml.CreateElement('a','buNone',$ns.LookupNamespace('a')))
   $number=$shape.CloneNode($true)
   $number.SelectSingleNode('p:nvSpPr/p:cNvPr',$ns).SetAttribute('id',[string](101+2*$row))
   $number.SelectSingleNode('p:nvSpPr/p:cNvPr',$ns).SetAttribute('name','Overview number '+($index+1))
   $number.SelectSingleNode('p:spPr/a:xfrm/a:off',$ns).SetAttribute('x','919480')
   $number.SelectSingleNode('p:spPr/a:xfrm/a:ext',$ns).SetAttribute('cx','558800')
   $number.SelectSingleNode('p:txBody/a:p/a:pPr',$ns).SetAttribute('algn','r')
   $number.SelectSingleNode('p:txBody/a:p/a:r/a:t',$ns).InnerText=[string]($index+1)+'.'
   [void]$parent.AppendChild($number);[void]$parent.AppendChild($shape)
  }
  $entry=$zip.GetEntry($overviewPaths[$page]);$entry.Delete();$entry=$zip.CreateEntry($overviewPaths[$page])
  $writer=[IO.StreamWriter]::new($entry.Open(),[Text.UTF8Encoding]::new($false))
  try{$xml.Save($writer)}finally{$writer.Dispose()}
 }
 Write-Output ('Overview synchronized: '+$titles.Count+' chapter names on one slide; detailed slide titles and backups excluded.')
}finally{$zip.Dispose()}
