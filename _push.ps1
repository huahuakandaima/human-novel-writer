$ErrorActionPreference = 'Stop'
$owner = 'huahuakandaima'
$repo = 'human-novel-writer'
$root = 'C:\Users\28917\.zcode\workspace\default\_pub_human-novel-writer'

# 1) copy skill contents into staging root
$src = 'C:\Users\28917\.zcode\skills\human-novel-writer'
Get-ChildItem -Force $src | ForEach-Object {
    Copy-Item $_.FullName $root -Recurse -Force
}

$files = Get-ChildItem -Recurse -File $root | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
    [PSCustomObject]@{ Path = $rel; Full = $_.FullName }
}
Write-Host "Total files: $($files.Count)"

# 2) create blobs for every file
$treeItems = @()
foreach ($f in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($f.Full)
    $b64 = [System.Convert]::ToBase64String($bytes)
    $body = @{ content = $b64; encoding = 'base64' } | ConvertTo-Json -Compress
    $resp = $body | gh api "repos/$owner/$repo/git/blobs" --input - | ConvertFrom-Json
    $treeItems += @{ path = $f.Path; mode = '100644'; type = 'blob'; sha = $resp.sha }
    Write-Host "blob: $($f.Path) -> $($resp.sha.Substring(0, 7))"
}

# 3) create tree
$treeBody = @{ tree = $treeItems } | ConvertTo-Json -Depth 5 -Compress
$treeResp = $treeBody | gh api "repos/$owner/$repo/git/trees" --input - | ConvertFrom-Json
Write-Host "tree: $($treeResp.sha)"

# 4) create commit
$commitBody = @{
    message = 'Initial import: human-novel-writer skill (workflow + anti-AI rules + density/prose gates)'
    tree    = $treeResp.sha
    parents = @()
} | ConvertTo-Json -Depth 5 -Compress
$commitResp = $commitBody | gh api "repos/$owner/$repo/git/commits" --input - | ConvertFrom-Json
Write-Host "commit: $($commitResp.sha)"

# 5) create main branch ref
$refBody = @{ ref = 'refs/heads/main'; sha = $commitResp.sha } | ConvertTo-Json -Compress
$refResp = $refBody | gh api "repos/$owner/$repo/git/refs" --input - | ConvertFrom-Json
Write-Host "ref: $($refResp.ref) -> $($refResp.object.sha)"
Write-Host "DONE"
