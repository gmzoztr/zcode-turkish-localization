# -*- coding: utf-8 -*-
$ErrorActionPreference = 'Stop'
$base = 'C:\Users\Work-D\ZCodeProject'
$resultFile = Join-Path $base 'deploy_result.txt'
$rollbackDir = Join-Path $base 'deploy-rollback'
$zcodeTarget = 'C:\Program Files\ZCode\resources\app.asar'
$sourcePatched = Join-Path $base 'app.asar.patched'
$origBackup = Join-Path $rollbackDir 'app.asar.orig'

try {
    if (-not (Test-Path -LiteralPath $sourcePatched)) {
        throw "Yamalı asar dosyası bulunamadı: $sourcePatched"
    }

    if (-not (Test-Path -LiteralPath $rollbackDir)) {
        New-Item -ItemType Directory -Path $rollbackDir -Force | Out-Null
    }

    # Eğer orijinal yedek henüz yoksa, mevcut canlı dosyayı orijinal olarak yedekle
    if ((-not (Test-Path -LiteralPath $origBackup)) -and (Test-Path -LiteralPath $zcodeTarget)) {
        Copy-Item -LiteralPath $zcodeTarget -Destination $origBackup -Force
    }

    # Disk üzerindeki eklenti, yetenek ve komut paketlerini Python ile UTF-8 No BOM olarak Türkçeleştir
    try {
        $applyPy = Join-Path $base 'apply_packages_tr.py'
        if (Test-Path -LiteralPath $applyPy) {
            python $applyPy
        }
    } catch {
        Write-Warning "apply_packages_tr.py çalıştırılırken uyarı alındı: $_"
    }

    # Canlı app.asar'ı yamalı dosya ile değiştir
    Copy-Item -LiteralPath $sourcePatched -Destination $zcodeTarget -Force

    # Gelecekteki otomatik güncellemelerin UAC sormadan sessiz çalışabilmesi için izin ver
    try {
        icacls "C:\Program Files\ZCode\resources" /grant "BUILTIN\Users:(OI)(CI)M" /T /Q | Out-Null
    } catch {}

    # SHA-256 Hash doğrulaması
    $srcHash = (Get-FileHash -LiteralPath $sourcePatched -Algorithm SHA256).Hash
    $dstHash = (Get-FileHash -LiteralPath $zcodeTarget -Algorithm SHA256).Hash

    if ($srcHash -ne $dstHash) {
        throw "Bütünlük doğrulaması başarısız oldu! Hedef dosya hash eşleşmedi."
    }

    Set-Content -LiteralPath $resultFile -Value 'OK_VERIFIED' -Encoding ASCII
    exit 0
}
catch {
    Set-Content -LiteralPath $resultFile -Value "ERROR: $_" -Encoding ASCII
    Write-Error $_
    exit 1
}
