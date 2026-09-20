@echo off
chcp 65001 > nul
cls
echo ============================================================
echo   🇹🇷 ZCode Desktop Türkçe Yama ve Güncelleyici
echo ============================================================
echo.

if exist "%~dp0ZCode_Tek_Tik_Yama.exe" (
    echo [*] Tek Tık EXE başlatılıyor...
    start "" "%~dp0ZCode_Tek_Tik_Yama.exe"
    goto finish
)

if exist "%~dp0single_click_patcher.py" (
    echo [*] Python yamalayıcı çalıştırılıyor...
    python "%~dp0single_click_patcher.py"
    goto finish
)

if exist "%~dp0patch_zcode_tr.py" (
    echo [*] Python yamalayıcı çalıştırılıyor...
    python "%~dp0patch_zcode_tr.py"
    goto finish
)

echo [-] Yama dosyaları bulunamadı!
pause
exit /b 1

:finish
echo.
echo ============================================================
echo   ⭐ Eğer yamayı faydalı bulduysanız GitHub'da bir Yıldız
echo      bırakıp destek olabilirsiniz!
echo      👉 https://github.com/gmzoztr/zcode-turkish-localization
echo ============================================================
echo.
pause
