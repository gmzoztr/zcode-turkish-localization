# 🇹🇷 ZCode Desktop Türkçe Dil Paketi & Yerelleştirme Altyapısı
### (Community Turkish Localization & Engineering Infrastructure for ZCode Desktop)

<div align="center">

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tested On](https://img.shields.io/badge/ZCode%20Version-v3.14.3%2B-green.svg)](https://zcode.z.ai)
[![Keys Translated](https://img.shields.io/badge/Translated%20Keys-6%2C295-orange.svg)](tr_dictionary_zcode.json)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Cross--Platform-lightgrey.svg)](#-kurulum-installation)
[![Maintenance Commitment](https://img.shields.io/badge/Maintenance-Day--0%20SLA-blue.svg)](#-note-to-official-zcode-developers-zai-org)
[![GitHub stars](https://img.shields.io/github/stars/gmzoztr/zcode-turkish-localization?style=social)](https://github.com/gmzoztr/zcode-turkish-localization)

[📥 **Tek Tıkla İndir (.exe)**](https://github.com/gmzoztr/zcode-turkish-localization/releases/latest) • 
[⭐ **Yıldız Ver (Star)**](https://github.com/gmzoztr/zcode-turkish-localization) • 
[💬 **Geri Bildirim / Hata Bildir**](https://github.com/gmzoztr/zcode-turkish-localization/issues) • 
[🏛️ **Proposal for ZCode Team**](#-note-to-official-zcode-developers-zai-org)

</div>

---

> [!TIP]
> 🌟 **Projeyi beğendiyseniz sağ üst köşeden bir ⭐ Yıldız (Star) bırakarak bize destek olabilirsiniz!**  
> GitHub yıldızlarınız, ZCode resmi ekibinin Türkçe dilini doğrudan çekirdeğe (native) entegre etmesini hızlandırmak ve projenin görünürlüğünü artırmak için en büyük katkıdır.

ZCode Desktop yapay zeka destekli IDE ve kodlama asistanı için geliştirilmiş **en kapsamlı, %100 eksiksiz ve bağımsız Türkçe yerelleştirme projesidir**.

Bu proje; arayüz metinlerinden eklenti mağazasına, komutlardan ve yeteneklerden (skills) fiyatlandırma webview'larına, v3.14.0 ile gelen 3 adımlı karşılama sihirbazından iş akışlarına (workflows) kadar ZCode'un tüm katmanlarını Türkçeleştirir.

---

## 📢 Note to Official ZCode Developers (@zai-org)

> **Dear ZCode Team & Contributors at [@zai-org](https://github.com/zai-org) / Zhipu AI,**

First of all, congratulations on creating **ZCode**! It is an outstanding agentic IDE and coding assistant, and our Turkish developer community truly appreciates the hard work your team is putting into this product.

### Why We Built This Project
We created this Turkish Localization infrastructure to make ZCode accessible to hundreds of thousands of Turkish-speaking developers, engineers, and students. Currently, Turkish is not included in the default `IntlProvider` locales (`zh-CN`, `en-US`), which led us to engineer this comprehensive external patching mechanism.

### Our Commitment to Maintenance & Day-0 SLA
* **Continuous Updates:** Whenever a new official ZCode update is released, we immediately inspect changes, translate newly added strings, verify syntax with `node --check`, and publish an updated patch release within hours.
* **Production-Grade Quality:** 6,295 verified keys covering `IntlProvider`, native desktop menus, subagents, and official extension stores.

### Proposal / Feature Request for ZCode Core
1. **Native `tr-TR` Support:**  
   If the core team can natively integrate Turkish (`tr-TR` or `tr`) into `IntlProvider` alongside `en-US` and `zh-CN`, we are ready to submit our **6,295-key dictionary (`tr_dictionary_zcode.json`)** as an official Pull Request.
2. **Advance Notification / String Diffs:**  
   If you can share string changes or notify us before major version releases, we will happily provide 100% verified Turkish translations ahead of time so Turkish users never experience untranslated UI after updates.
3. **Official Community Partnership:**  
   We are available to maintain the Turkish language ecosystem, documentation, and user support as an official community partner.

📩 **Let's Connect:**
- **Official Team Inquiry:** [Open a Core Team Inquiry](https://github.com/gmzoztr/zcode-turkish-localization/issues/new?template=official_inquiry.md)
- **Direct Email:** `abdurrahmanavci@gmail.com`
- **GitHub:** [@gmzoztr](https://github.com/gmzoztr)

---

## 🌟 Neler İçerir? (Özellikler)

1. **Tam Kapsamlı Arayüz (6.295+ Anahtar):**
   - React-Intl dil sağlayıcısı (`IntlProvider`) üzerinden **6.295 anahtarın tamamı** Türkçe terminoloji standartlarına uygun olarak yerelleştirildi.
   - v3.14.0 ile gelen 3 adımlı Karşılama Sihirbazı (Onboarding), İş Akışları (Workflows) merkezi, Araç Çağrısı (ToolCalls) arayüzleri ve yeni ayarlar.
   - Electron yerel masaüstü menüleri (Dosya, Düzen, Görünüm, Pencere, Yardım).
   - Güncelleyici diyalogları ve Türkçe yerel tarih biçimlendirmesi (`19 Eylül 2026`).
2. **Resmi Eklenti Mağazası ve Claude Code Eklentileri (330+ Paket):**
   - 40 Resmi ZCode eklentisinin (Plugin Creator, PDF, Documents, Presentations, Spreadsheets, Finans, Güvenlik vb.) başlık ve Türkçe açıklamaları.
   - Claude Code Mağazasındaki 291 eklentinin tamamının Türkçe açıklamaları (orijinal marka ve ürün adları korunarak).
3. **Ajan Becerileri (Skills) ve Komutlar (Slash Commands):**
   - Tüm `/komut` açıklamaları, argüman ipuçları (`[hedef veya sorun açıklaması]`), grup başlıkları (`Android Emülatörü 1`, `iOS Simülatörü 1`, `Eski Oturumları Geri Yükle 1`).
4. **Planı Yükselt & Webview Arayüzü:**
   - Dinamik DOM gözlemcisi ve Webview enjeksiyonu ile Bireysel ve Ekip planları, kredi kotaları, indirimler ve faturalandırma metinleri.
5. **Kalıcı ve Güvenli:**
   - Orijinal `app.asar.orig` fabrika yedeğini saklar; istendiğinde tek tıkla orijinal fabrika ayarlarına geri döndürür.

---

## 🚀 Kurulum (Installation)

### Yöntem 1: Tek Tıkla Kurulum (.exe - Önerilen)
1. **[Releases](https://github.com/gmzoztr/zcode-turkish-localization/releases/latest)** sayfasından en son `ZCode_Tek_Tik_Yama.exe` dosyasını indirin.
2. ZCode açıkken veya kapalıyken çift tıklayıp çalıştırın (Gerekirse Yönetici İzni verin).
3. 3 saniye içinde yama uygulanır ve ZCode otomatik olarak Türkçe başlatılır.

### Yöntem 2: Tek Tıkla Toplu İş (.bat ile)
Depoyu klonladıysanız veya ZIP olarak indirdiyseniz, klasördeki **`TURKCELESTIR.bat`** dosyasına çift tıklayarak yamayı kolayca başlatabilirsiniz.

### Yöntem 3: Python ile Kurulum (Geliştiriciler İçin)
```bash
git clone https://github.com/gmzoztr/zcode-turkish-localization.git
cd zcode-turkish-localization
python patch_zcode_tr.py
```

---

## 📂 Depo Yapısı (Repository Structure)

```
zcode-turkish-localization/
├── tr_dictionary_zcode.json    # 6.295 anahtarlık eksiksiz Türkçe sözlük
├── TURKCELESTIR.bat            # Windows için tek tıkla kurulum bat dosyası
├── patch_zcode_tr.py           # Otomatik ASAR, i18n, menü ve webview yamalayıcı
├── single_click_patcher.py     # Bağımsız tek tık çalıştırıcı kaynak kodu
├── build_and_test_asar.py      # ASAR derleme ve sözdizimi doğrulama motoru
├── apply_packages_tr.py        # Resmi eklenti paketlerini yerelleştirme aracı
├── deploy_all.ps1              # PowerShell tam dağıtım otomasyonu
├── ARCHITECTURE_TR.md          # Detaylı mimarî bilgi grafiği ve hata önleme rehberi
├── CONTRIBUTING.md              # Katkıda bulunma rehberi
├── SECURITY.md                  # Güvenlik politikası
├── LICENSE                     # MIT Lisansı
└── README.md                   # Dokümantasyon
```

---

## 🤝 Katkıda Bulunma & İletişim

* **Hata Bildir:** [Issues](https://github.com/gmzoztr/zcode-turkish-localization/issues)
* **Topluluk Tartışmaları:** [Discussions](https://github.com/gmzoztr/zcode-turkish-localization/discussions)
* **Pull Request:** [Pull Requests](https://github.com/gmzoztr/zcode-turkish-localization/pulls)

## 📄 Lisans (License)
Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.
