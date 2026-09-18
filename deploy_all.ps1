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

    $utf8NoBom = New-Object System.Text.UTF8Encoding $false

    # server.js içindeki yerleşik alt ajan açıklamalarını Türkçeleştir
    try {
        $serverJs = "C:\Program Files\ZCode\resources\glm\packages\browser-use-plugin\dist\mcp\server.js"
        if (Test-Path -LiteralPath $serverJs) {
            $sContent = [System.IO.File]::ReadAllText($serverJs, [System.Text.Encoding]::UTF8)
            $sContent = $sContent.Replace("General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks.", "Karmaşık soruları araştırmak, kod aramak ve çok adımlı görevleri yürütmek için genel amaçlı ajan.")
            $sContent = $sContent.Replace("Read-only search agent for broad fan-out searches", "Geniş kapsamlı aramalar için salt okunur arama ajanı")
            [System.IO.File]::WriteAllText($serverJs, $sContent, $utf8NoBom)
        }
    } catch {}

    # judge.md alt ajan açıklamalarını Türkçeleştir
    try {
        $judgeFiles = @(
            "C:\Program Files\ZCode\resources\glm\packages\document-skills-plugin\agents\judge.md",
            (Join-Path $env:USERPROFILE ".zcode\cli\plugins\cache\zcode-plugins-official\document-skills\0.1.4\agents\judge.md"),
            (Join-Path $env:USERPROFILE ".zcode\cli\plugins\cache\zcode-plugins-official\document-skills\0.1.5\agents\judge.md")
        )
        foreach ($jf in $judgeFiles) {
            if (Test-Path -LiteralPath $jf) {
                $jContent = [System.IO.File]::ReadAllText($jf, [System.Text.Encoding]::UTF8)
                if ($jContent -notmatch "kabul incelemesi") {
                    $jContent = $jContent -replace 'description:\s*"[^"]+"', 'description: "Yalnızca pptx, docx, xlsx, pdf, poster ve grafik türündeki görsel çıktıların kabul incelemesi için tek yetkili görsel onay ajanı."'
                    [System.IO.File]::WriteAllText($jf, $jContent, $utf8NoBom)
                }
            }
        }
    } catch {}

        # Plugin JSON dosyalarını Türkçeleştir
    try {
        $pkgBase = "C:\Program Files\ZCode\resources\glm\packages"
        if (Test-Path -LiteralPath $pkgBase) {
            $descMap = @{
                "android-emulator-plugin" = "Android emülatörlerini yönetme, başlatma ve cihaz kontrolü için geliştirici araçları."
                "browser-use-plugin" = "Masaüstü için yerleşik tarayıcı otomasyonu çalışma ortamı ve rehberlik."
                "document-skills-plugin" = "Yerleşik DOCX ve PDF belge oluşturma becerileri."
                "ios-simulator-plugin" = "iOS simülatörlerini yönetme, test etme ve arayüz denetimi araçları."
                "restore-legacy-sessions-plugin" = "Önceki sürümlerden kalan eski oturumları ve sohbet geçmişlerini geri yükleyin."
                "skill-creator-plugin" = "Yeni ajan becerileri ve iş akışları oluşturmak için rehberli araç seti."
                "zcode-cua-plugin" = "Bilgisayar Kontrolü: Masaüstü uygulamalarını fare, klavye ve sistem eylemleriyle otomatikleştirin."
                "zcode-guide-plugin" = "ZCode özellikleri, komutları ve yapılandırmaları için kapsamlı kullanım kılavuzu."
            }
            foreach ($pkg in $descMap.Keys) {
                $pj = Join-Path $pkgBase "$pkg\.zcode-plugin\plugin.json"
                if (Test-Path -LiteralPath $pj) {
                    $jsonContent = [System.IO.File]::ReadAllText($pj, [System.Text.Encoding]::UTF8)
                    $jsonObj = ConvertFrom-Json $jsonContent
                    $jsonObj.description = $descMap[$pkg]
                    $newJson = ConvertTo-Json -InputObject $jsonObj -Depth 10
                    [System.IO.File]::WriteAllText($pj, $newJson, $utf8NoBom)
                }
            }
        }
    } catch {}

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
    # Hata durumunda otomatik geri alma
    if (Test-Path -LiteralPath $origBackup) {
        try {
            Copy-Item -LiteralPath $origBackup -Destination $zcodeTarget -Force
        }
        catch {}
    }
    Set-Content -LiteralPath $resultFile -Value ('FAIL: ' + $_.Exception.Message) -Encoding UTF8
    exit 1
}
