# Append URL extra data: "&include=images,media_files"
# No exclude? "&exclude=thumbnail"
$storeURL = "www.WEEBLYSTORE.com"
$user = "131267684"
$site = "874863029496319949"
$prodPerPage = "60" #Default 60, can set lower if less expected
$OHcat = "11ea6d492c1c3ceda2130cc47a2ae378"
$BurialCat = "11ec73f0f798faa4bb6c6abbb74a6a8e"
$cat = $BurialCat

$url = "https://" + $storeURL + "/app/store/api/v8/editor/users/" + $user + "/sites/" + $site + "/products?page=1&per_page=" + $prodPerPage + "&sort_by=category_order&sort_order=asc&categories[]=" + $cat

$timer = 60
#$timer = 10
$failedCalls = 0
$randTimer = $False
$randRange = 10
$user = $env:UserName
$message = "Site Updated!"

# Don't change below
$randMin = $timer - $randRange
$randMax = $timer + $randRange
$tries = 0
$updated = $False
#$charDiff = 100
function alert{
    [console]::beep(2000,500)
    [console]::beep(2000,500)
    if ($args[0]){
        Write-Host $args[0] -ForegroundColor Red
        break
    }
}

Write-Host "Starting Script..."
$webCall = Invoke-WebRequest -Uri $url
if ($webCall.StatusCode -ne 200){
    alert("First Call Failed!")
}
$firstJson = $webCall.Content | ConvertFrom-Json
$firstTotal = $firstJson.data.count
if ($firstTotal -eq $prodPerPage){
    alert("prodPerPage value too low, must increase")
}
DO
{
    $tries++
    #Write-Host "Try: " $tries
    if ($randTimer -eq $True){
        $timer = Get-Random -Minimum $randMin -Maximum $randMax
    }
    Start-Sleep -Seconds $timer
    $moreCalls = Invoke-WebRequest -Uri $url
    if ($moreCalls.StatusCode -eq 200){
        $moreJson = $moreCalls.Content | ConvertFrom-Json
        $moreTotal = $moreJson.data.count
        ## TODO: Nested logic for case product sold out (-lt) before new product added (-gt will not suffice, need new $firstTotal)
        if ($firstTotal -ne $moreTotal){ $updated = $True }
    } else {
        $failedCalls++
        Write-Host "Had a Failed Call:" $failedCalls -ForegroundColor Red
    }
} Until ($updated -eq $True)

# Alert
$timeFinished = Get-Date
msg $user $message
alert
if ($randTimer -eq $False){
    $totalSeconds = $timer * $tries
    Write-Host "UPDATED! took tries: " $tries "Total Seconds: " $totalSeconds "Finished: " $timeFinished -ForegroundColor Yellow
} else {
    Write-Host "UPDATED! took tries: " $tries "Finished: " $timeFinished -ForegroundColor Yellow
}
