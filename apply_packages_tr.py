# -*- coding: utf-8 -*-
"""
apply_packages_tr.py
ZCode eklenti, yetenek, komut ve pazar yeri dosyalarını
kusursuz, profesyonel Türkçe ile günceller.
"""

import os
import json
import re

USER_ZCODE = os.path.expanduser(r"~\.zcode")
PROGRAM_PACKAGES = r"C:\Program Files\ZCode\resources\glm\packages"

PLUGIN_TRANSLATIONS = {
    "android-emulator": {
        "displayName": "Android Emulator",
        "description": "ZCode için Android geliştirme iş akışları ve emülatör otomasyonu sağlar."
    },
    "browser-use": {
        "displayName": "Tarayıcı Kullanımı",
        "description": "Yerleşik tarayıcı otomasyonu ve Masaüstü IAB web kontrolü: Sayfaları açın, gezinin, inceleyin, tıklayın, metin girin, ekran görüntüsü alın ve doğrulayın."
    },
    "document-skills": {
        "displayName": "Belge Yetenekleri",
        "description": "Resmi ZCode eklentisi olarak yerleşik DOCX, PDF, XLSX ve PPTX belge üretim ve düzenleme yetenekleri.",
        "examplePrompts": [
            "Notlarımdan biçimlendirilmiş bir Word belgesi oluştur",
            "Bu PDF'deki tabloları bir elektronik tabloya aktar",
            "Bu CSV dosyasından grafikler içeren bir Excel çalışma kitabı oluştur"
        ]
    },
    "ios-simulator": {
        "displayName": "iOS Simulator",
        "description": "ZCode için iOS geliştirme iş akışları ve simülatör otomasyonu sağlar."
    },
    "restore-legacy-sessions": {
        "displayName": "Eski Oturumları Geri Yükle",
        "description": "Eski ACP dönemi ZCode oturumlarını seçin ve yeni ZCode görev ve oturum deposuna geri yükleyin."
    },
    "skill-creator": {
        "displayName": "Yetenek Oluşturucu",
        "description": "Yerel ZCode yetenekleri oluşturun, düzenleyin ve geliştirin."
    },
    "zcode-guide": {
        "displayName": "ZCode Kılavuzu",
        "description": "ZCode kullanım ve tanı kılavuzu: MCP sunucularını, komutları, yetenekleri, kancaları ve eklentileri yapılandırmayı ve yapılandırma sorunlarını çözmeyi öğretir.",
        "examplePrompts": [
            "ZCode'da MCP sunucularını nasıl yapılandırırım?",
            "Mevcut ZCode yapılandırmamı tanıla"
        ]
    },
    "computer-use": {
        "displayName": "Bilgisayar Kontrolü",
        "description": "Bilgisayar Kontrolü: Fare, klavye ve arayüz ögesi kontrolü ile masaüstü uygulamalarını otomatikleştirin."
    },
    "zcode-cua": {
        "displayName": "Bilgisayar Kontrolü",
        "description": "Bilgisayar Kontrolü: Fare, klavye ve arayüz ögesi kontrolü ile masaüstü uygulamalarını otomatikleştirin."
    }
}

SKILL_TRANSLATIONS = {
    "android-dev": "android-emulator MCP araçlarıyla Android uygulamaları derleyin, çalıştırın, inceleyin ve otomatikleştirin.",
    "control-browser": "Yalnızca ana ajan tarayıcı kullanımı: ZCode içinde web sayfalarını ve yerel HTTP hedeflerini açın, gezinin, inceleyin, tıklayın, form doldurun, ekran görüntüsü alın ve doğrulayın.",
    "web-gui-tester": "Oturumdaki tarayıcı otomasyon araçlarını kullanarak web arayüzlerini etkileşimli olarak test edin, kullanıcı eylemlerini simüle edin, ekran görüntüleriyle doğrulayın ve test raporu oluşturun.",
    "docx": "Revizyonlar, yorumlar, biçimlendirme koruma ve metin çıkarma desteğiyle eksiksiz DOCX belgesi oluşturma, düzenleme ve analiz yetenekleri.",
    "pdf": "PDF belgeleri oluşturma, form doldurma, metin çıkarma ve profesyonel sayfa düzeni desteği.",
    "pptx": "PowerPoint (.pptx) sunumları oluşturma ve düzenleme yetenekleri.",
    "xlsx": "Tablo dosyaları, veri analizleri, formüller ve grafikler için gelişmiş Excel (.xlsx) işleme yetenekleri.",
    "ios-dev": "ios-simulator MCP araçlarıyla iOS simülatör uygulamaları derleyin, çalıştırın, inceleyin ve otomatikleştirin.",
    "restore-legacy-sessions": "Eski ACP dönemi ZCode oturumlarını inceleyin, planlayın ve yeni ZCode oturum deposuna geri yükleyin.",
    "skill-creator": "Yeni yetenekler oluşturun, mevcut yetenekleri düzenleyin ve metinleri iyileştirin.",
    "computer-use": "Erişilebilirlik odaklı semantik eylemler ve görsel doğrulama ile masaüstü kontrolü.",
    "diagnosing-commands": "ZCode istemcisindeki özel eğik çizgi komutu (/komut) yapılandırma sorunlarını tanılayın ve düzeltin.",
    "diagnosing-hooks": "ZCode istemcisindeki kanca (hook) yapılandırma sorunlarını tanılayın ve düzeltin.",
    "diagnosing-mcp": "ZCode istemcisindeki MCP (Model Context Protocol) sunucu yapılandırma sorunlarını tanılayın ve düzeltin.",
    "diagnosing-plugins": "ZCode istemcisindeki eklenti ve pazar yeri sorunlarını tanılayın ve düzeltin.",
    "diagnosing-skills": "ZCode istemcisindeki yetenek (skill) yapılandırma sorunlarını tanılayın ve düzeltin.",
    "zcode-configuration-guide": "ZCode uzantı kaynaklarını (MCP sunucuları, eğik çizgi komutları, yetenekler, kancalar) yapılandırırken veya sorunları giderirken kullanın.",
    "microsoft-foundry": "Microsoft Foundry ajanlarını, modellerini ve kaynaklarını uçtan uca derleyin, dağıtın, değerlendirin, optimize edin ve yönetin.",
    "finetuning": "SFT, DPO veya RFT kullanarak Microsoft Foundry üzerinde modelleri ince ayarlar (fine-tune). Veri kümesi hazırlama, eğitim işi gönderme ve değerlendirmeyi kapsar.",
    "deploy-model": "Akıllı amaç tabanlı yönlendirme ile birleşik Azure OpenAI model dağıtım yeteneği. Hızlı ön ayarlı ve tam özelleştirilmiş dağıtımları yönetir.",
    "capacity": "Bölgeler ve projeler genelinde kullanılabilir Azure OpenAI model kapasitesini keşfeder. Kota sınırlarını analiz eder ve en uygun dağıtım konumlarını önerir.",
    "customize": "Tam özelleştirme kontrolüyle Azure OpenAI modelleri için etkileşimli rehberli dağıtım akışı. Model sürümü, SKU, kapasite ve filtre politikası seçimini sağlar.",
    "preset": "Kullanılabilir tüm bölgelerdeki kapasiteyi analiz ederek Azure OpenAI modellerini en uygun bölgelere akıllıca dağıtır.",
    "chrome-cdp": "Chrome oturumu ile etkileşim kurun, sayfaları denetleyin ve test edin.",
    "codebase-memory": "Yapısal kod sorguları, mimari keşif ve çağrı zinciri analizi için kod tabanı bilgi grafiğini kullanın.",
    "desktop-eye": "Canlı masaüstü ekran görüntüsü alarak arayüz bağlamını anlık olarak doğrulayın."
}

COMMAND_TRANSLATIONS = {
    "android-dev.md": {
        "description": "Android emülatör geliştirme döngüsünü başlatın.",
        "argument-hint": "\"[hedef veya sorun açıklaması]\""
    },
    "ios-dev.md": {
        "description": "iOS simülatör geliştirme döngüsünü başlatın.",
        "argument-hint": "\"[hedef veya sorun açıklaması]\""
    },
    "restore-legacy-sessions.md": {
        "description": "Eski bir ZCode oturumunu seçin ve geri yükleyin.",
        "argument-hint": "\"[ajan/çalışma alanı/oturum filtreleri]\""
    }
}


def patch_json_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        changed = False

        name = data.get("name")
        if name:
            clean_name = name.replace("-plugin", "")
            tr_info = PLUGIN_TRANSLATIONS.get(clean_name) or PLUGIN_TRANSLATIONS.get(name)
            if tr_info:
                if "description" in tr_info and data.get("description") != tr_info["description"]:
                    data["description"] = tr_info["description"]
                    changed = True

        if "manifest" in data and "plugins" in data["manifest"]:
            for pl in data["manifest"]["plugins"]:
                pname = pl.get("name")
                tr_info = PLUGIN_TRANSLATIONS.get(pname)
                if tr_info:
                    if "description" in tr_info:
                        pl["description"] = tr_info["description"]
                        if "description_i18n" not in pl:
                            pl["description_i18n"] = {}
                        pl["description_i18n"]["tr"] = tr_info["description"]
                    if "examplePrompts" in tr_info:
                        pl["examplePrompts"] = tr_info["examplePrompts"]
                        if "examplePrompts_i18n" not in pl:
                            pl["examplePrompts_i18n"] = {}
                        pl["examplePrompts_i18n"]["tr"] = tr_info["examplePrompts"]
                    changed = True

        if "plugins" in data and isinstance(data["plugins"], list):
            for pl in data["plugins"]:
                pname = pl.get("name")
                tr_info = PLUGIN_TRANSLATIONS.get(pname)
                if tr_info:
                    if "description" in tr_info:
                        pl["description"] = tr_info["description"]
                        if "description_i18n" not in pl:
                            pl["description_i18n"] = {}
                        pl["description_i18n"]["tr"] = tr_info["description"]
                    if "examplePrompts" in tr_info:
                        pl["examplePrompts"] = tr_info["examplePrompts"]
                        if "examplePrompts_i18n" not in pl:
                            pl["examplePrompts_i18n"] = {}
                        pl["examplePrompts_i18n"]["tr"] = tr_info["examplePrompts"]
                    changed = True

        if changed:
            with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK JSON] {filepath}")
    except Exception as e:
        print(f"[ERR JSON] {filepath}: {e}")


def patch_markdown_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        changed = False

        if os.path.basename(filepath) == "SKILL.md":
            for skill_name, tr_desc in SKILL_TRANSLATIONS.items():
                if re.search(rf"^name:\s*{re.escape(skill_name)}\b", content, re.MULTILINE):
                    new_content, n = re.subn(
                        r"(^description:\s*)([^\n>]+)",
                        rf'\g<1>"{tr_desc}"',
                        content,
                        flags=re.MULTILINE
                    )
                    if n > 0:
                        content = new_content
                        changed = True
                    else:
                        new_content, n = re.subn(
                            r"(^description:\s*>\n(?:\s+[^\n]+\n)+)",
                            f'description: "{tr_desc}"\n',
                            content,
                            flags=re.MULTILINE
                        )
                        if n > 0:
                            content = new_content
                            changed = True

        cmd_name = os.path.basename(filepath)
        if cmd_name in COMMAND_TRANSLATIONS:
            cmd_info = COMMAND_TRANSLATIONS[cmd_name]
            tr_desc = cmd_info["description"]
            tr_hint = cmd_info.get("argument-hint")

            new_content, n = re.subn(
                r"(^description:\s*)([^\n]+)",
                rf'\g<1>"{tr_desc}"',
                content,
                flags=re.MULTILINE
            )
            if n > 0:
                content = new_content
                changed = True

            if tr_hint:
                new_content, n2 = re.subn(
                    r"(^argument-hint:\s*)([^\n]+)",
                    rf'\g<1>{tr_hint}',
                    content,
                    flags=re.MULTILINE
                )
                if n2 > 0:
                    content = new_content
                    changed = True

        if changed:
            with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            print(f"[OK MD] {filepath}")
    except Exception as e:
        print(f"[ERR MD] {filepath}: {e}")


def scan_and_patch(root_dir):
    if not os.path.exists(root_dir):
        return
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            p = os.path.join(root, f)
            if f in ("plugin.json", "bundled-marketplace.json", "cdn-marketplace.json", "marketplace.json"):
                patch_json_file(p)
            elif f == "SKILL.md" or (f.endswith(".md") and "commands" in root):
                patch_markdown_file(p)


def main():
    print("ZCode Eklenti ve Paket Türkçe Yamalama Başlatılıyor...")
    scan_and_patch(os.path.join(USER_ZCODE, "cli", "plugins"))
    scan_and_patch(PROGRAM_PACKAGES)
    scan_and_patch(os.path.expanduser(r"~\.agents\skills"))
    scan_and_patch(os.path.expanduser(r"~\.claude\skills"))
    print("İşlem tamamlandı!")


if __name__ == "__main__":
    main()
