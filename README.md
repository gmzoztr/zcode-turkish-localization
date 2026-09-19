# 🇹🇷 ZCode Desktop Türkçe Dil Paketi & Yerelleştirme Altyapısı
### (Community Turkish Localization for ZCode Desktop)

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tested On](https://img.shields.io/badge/ZCode%20Version-v3.12.3%2B-green.svg)](https://zcode.z.ai)
[![Keys Translated](https://img.shields.io/badge/Translated%20Keys-5%2C539-orange.svg)](tr_dictionary_zcode.json)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Cross--Platform-lightgrey.svg)](#kurulum)

ZCode Desktop yapay zeka destekli IDE ve kodlama asistanı için geliştirilmiş **en kapsamlı, %100 eksiksiz ve bağımsız Türkçe yerelleştirme projesidir**.

Bu proje; arayüz metinlerinden eklenti mağazasına, komutlardan ve yeteneklerden (skills) fiyatlandırma webview'larına kadar ZCode'un tüm katmanlarını Türkçeleştirir.

---

## 🌟 Neler İçerir? (Özellikler)

1. **Tam Kapsamlı Arayüz (5.539+ Anahtar):**
   - React-Intl dil sağlayıcısı (`IntlProvider`) üzerinden 5.539 anahtarın tamamı Türkçe terminoloji standartlarına uygun olarak yerelleştirildi.
   - Electron yerel masaüstü menüleri (Dosya, Düzen, Görünüm, Pencere, Yardım).
2. **Resmi Eklenti Mağazası ve Claude Code Eklentileri (325+ Paket):**
   - 34 Resmi ZCode eklentisinin başlık ve açıklamaları.
   - Claude Code Mağazasındaki 291 eklentinin tamamının Türkçe açıklamaları (orijinal marka ve ürün adları korunarak).
3. **Ajan Becerileri (Skills) ve Komutlar (Slash Commands):**
   - Tüm `/komut` açıklamaları, argüman ipuçları (`[hedef veya sorun açıklaması]`), grup başlıkları (`Android Emülatörü 1`, `iOS Simülatörü 1`, `Eski Oturumları Geri Yükle 1`).
4. **Planı Yükselt & Webview Arayüzü:**
   - Dinamik DOM gözlemcisi ve Webview enjeksiyonu ile Bireysel ve Ekip planları, kredi kotaları, indirimler ve faturalandırma metinleri.
5. **Kalıcı ve Güvenli:**
   - Orijinal `app.asar.orig` fabrika yedeğini saklar; istendiğinde tek tıkla orijinal fabrika ayarlarına geri döndürür.

---

## 🚀 Kurulum (Kullanıcılar İçin)

### Yöntem 1: Tek Tıkla Kurulum (.exe - Önerilen)
1. **[Releases](https://github.com/gmzoztr/zcode-turkish-localization/releases)** sayfasından en son `ZCode_Tek_Tik_Yama.exe` dosyasını indirin.
2. ZCode açıkken veya kapalıyken çift tıklayıp çalıştırın (Gerekirse Yönetici İzni verin).
3. 3 saniye içinde yama uygulanır ve ZCode otomatik olarak Türkçe başlatılır.

### Yöntem 2: Python ile Kurulum (Geliştiriciler İçin)
```bash
git clone https://github.com/gmzoztr/zcode-turkish-localization.git
cd zcode-turkish-localization
python patch_zcode_tr.py
```

---

## 📢 Note to Official ZCode Developers (@zai-org)

> **Dear ZCode Team & Contributors at [@zai-org](https://github.com/zai-org),**

First of all, congratulations on creating **ZCode**! It is an outstanding agentic IDE and coding assistant, and our Turkish developer community truly appreciates the hard work your team is putting into this product.

### Why We Built This
We created this Turkish Localization project to make ZCode accessible to hundreds of thousands of Turkish-speaking developers, engineers, and students. Currently, Turkish is not included in the default `IntlProvider` locales (`zh-CN`, `en-US`), which led us to build this external patching mechanism.

### Our Commitment to Maintenance
* **Continuous Updates:** Whenever a new official ZCode update is released, we actively inspect changes, translate newly added strings, verify syntax with `node --check`, and publish an updated patch release.
* **Open Partnership:** We would love to collaborate directly with the ZCode core team.

### Proposal / Feature Request for ZCode Core
1. **Native `tr-TR` Support:**  
   If the core team can natively integrate Turkish (`tr-TR` or `tr`) into `IntlProvider` alongside `en-US` and `zh-CN`, we are ready to submit our **5,539-key dictionary (`tr_dictionary_zcode.json`)** as an official Pull Request.
2. **Advance Notification / String Diffs:**  
   If you can share string changes or notify us before major version releases, we will happily provide 100% verified Turkish translations ahead of time so Turkish users never experience untranslated UI or broken patches after updates.

Feel free to contact us or open an issue in this repository, or reach out to us on GitHub ([@gmzoztr](https://github.com/gmzoztr)).

---

## 📂 Depo Yapısı (Repository Structure)

```
zcode-turkish-localization/
├── tr_dictionary_zcode.json    # 5.539 anahtarlık eksiksiz Türkçe sözlük
├── patch_zcode_tr.py           # Otomatik ASAR, i18n, menü ve webview yamalayıcı
├── single_click_patcher.py     # Bağımsız tek tık çalıştırıcı kaynak kodu
├── build_and_test_asar.py      # ASAR derleme ve sözdizimi doğrulama motoru
├── apply_packages_tr.py        # Resmi eklenti paketlerini yerelleştirme aracı
├── deploy_all.ps1              # PowerShell tam dağıtım otomasyonu
├── ARCHITECTURE_TR.md          # Detaylı mimarî bilgi grafiği ve hata önleme rehberi
├── LICENSE                     # MIT Lisansı
└── README.md                   # Dokümantasyon
```

---

## 🤝 Katkıda Bulunma (Contributing)

Hatalı veya geliştirilebilecek bir çeviri fark ederseniz lütfen bir **Issue** açın veya **Pull Request** gönderin. Her türlü katkı memnuniyetle karşılanır!

## 📄 Lisans (License)
Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.
