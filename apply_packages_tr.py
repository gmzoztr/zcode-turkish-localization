# -*- coding: utf-8 -*-
"""
apply_packages_tr.py
ZCode eklenti, yetenek, komut ve pazar yeri dosyalarını
kusursuz, profesyonel Türkçe ile günceller (UTF-8 No BOM).
"""

import os
import json
import re

USER_ZCODE = os.path.expanduser(r"~\.zcode")
PROGRAM_PACKAGES = r"C:\Program Files\ZCode\resources\glm\packages"

CLAUDE_PLUGINS_TR = {}
try:
    _claude_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude_plugins_tr.json")
    if os.path.exists(_claude_json):
        with open(_claude_json, "r", encoding="utf-8") as _f:
            CLAUDE_PLUGINS_TR = json.load(_f)
except Exception as _e:
    pass

PLUGIN_TRANSLATIONS = {
    "android-emulator": {
        "displayName": "Android Emülatörü",
        "description": "Android emülatörlerini yönetme, başlatma ve cihaz kontrolü için geliştirici araçları."
    },
    "browser-use": {
        "displayName": "Browser Use",
        "description": "Masaüstü için yerleşik tarayıcı otomasyonu çalışma ortamı ve rehberlik."
    },
    "document-skills": {
        "displayName": "Belge Becerileri",
        "description": "Yerleşik DOCX ve PDF belge oluşturma becerileri.",
        "examplePrompts": [
            "Notlarımdan biçimlendirilmiş bir Word belgesi oluştur",
            "Bu PDF'deki tabloları bir elektronik tabloya aktar",
            "Bu CSV dosyasından grafikler içeren bir Excel çalışma kitabı oluştur"
        ]
    },
    "ios-simulator": {
        "displayName": "iOS Simülatörü",
        "description": "iOS simülatörlerini yönetme, test etme ve arayüz denetimi araçları."
    },
    "restore-legacy-sessions": {
        "displayName": "Eski Oturumları Geri Yükle",
        "description": "Önceki sürümlerden kalan eski oturumları ve sohbet geçmişlerini geri yükleyin."
    },
    "skill-creator": {
        "displayName": "Beceri Oluşturucu",
        "description": "Yeni ajan becerileri ve iş akışları oluşturmak için rehberli araç seti."
    },
    "zcode-guide": {
        "displayName": "ZCode Rehberi",
        "description": "ZCode özellikleri, komutları ve yapılandırmaları için kapsamlı kullanım kılavuzu.",
        "examplePrompts": [
            "ZCode'da MCP sunucularını nasıl yapılandırırım?",
            "Mevcut ZCode yapılandırmamı tanıla"
        ]
    },
    "computer-use": {
        "displayName": "Bilgisayar Kontrolü",
        "description": "Bilgisayar Kontrolü: Masaüstü uygulamalarını fare, klavye ve sistem eylemleriyle otomatikleştirin."
    },
    "zcode-cua": {
        "displayName": "Bilgisayar Kontrolü",
        "description": "Bilgisayar Kontrolü: Masaüstü uygulamalarını fare, klavye ve sistem eylemleriyle otomatikleştirin."
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
                if "displayName" in tr_info and "displayName" in data and data.get("displayName") != tr_info["displayName"]:
                    data["displayName"] = tr_info["displayName"]
                    changed = True

        if "manifest" in data and "plugins" in data["manifest"]:
            for pl in data["manifest"]["plugins"]:
                pname = pl.get("name")
                tr_info = PLUGIN_TRANSLATIONS.get(pname)
                if tr_info:
                    if "description" in tr_info and pl.get("description") != tr_info["description"]:
                        pl["description"] = tr_info["description"]
                        if "description_i18n" not in pl:
                            pl["description_i18n"] = {}
                        pl["description_i18n"]["tr"] = tr_info["description"]
                        changed = True
                    if "displayName" in tr_info and pl.get("displayName") != tr_info["displayName"]:
                        pl["displayName"] = tr_info["displayName"]
                        changed = True
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
                    if "description" in tr_info and pl.get("description") != tr_info["description"]:
                        pl["description"] = tr_info["description"]
                        if "description_i18n" not in pl:
                            pl["description_i18n"] = {}
                        pl["description_i18n"]["tr"] = tr_info["description"]
                        changed = True
                    if "displayName" in tr_info and pl.get("displayName") != tr_info["displayName"]:
                        pl["displayName"] = tr_info["displayName"]
                        changed = True
                    if "examplePrompts" in tr_info:
                        pl["examplePrompts"] = tr_info["examplePrompts"]
                        if "examplePrompts_i18n" not in pl or not isinstance(pl["examplePrompts_i18n"], dict):
                            pl["examplePrompts_i18n"] = {}
                        pl["examplePrompts_i18n"]["tr"] = tr_info["examplePrompts"]
                        changed = True
                elif CLAUDE_PLUGINS_TR and pname in CLAUDE_PLUGINS_TR:
                    c_desc = CLAUDE_PLUGINS_TR[pname]
                    if pl.get("description") != c_desc:
                        pl["description"] = c_desc
                        if "description_i18n" not in pl or not isinstance(pl["description_i18n"], dict):
                            pl["description_i18n"] = {}
                        pl["description_i18n"]["tr"] = c_desc
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


def patch_special_files():
    # 1. server.js
    server_paths = [
        r"C:\Program Files\ZCode\resources\glm\packages\browser-use-plugin\dist\mcp\server.js",
        os.path.join(USER_ZCODE, r"cli\plugins\cache\zcode-plugins-official\browser-use\0.4.2\dist\mcp\server.js")
    ]
    for sp in server_paths:
        if os.path.exists(sp):
            try:
                with open(sp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                orig_len = len(content)
                content = content.replace("General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks.", "Karmaşık soruları araştırmak, kod aramak ve çok adımlı görevleri yürütmek için genel amaçlı ajan.")
                content = content.replace("Read-only search agent for broad fan-out searches", "Geniş kapsamlı aramalar için salt okunur arama ajanı")
                if len(content) != orig_len or "Karmaşık soruları" in content:
                    with open(sp, "w", encoding="utf-8", newline="\n") as f:
                        f.write(content)
                    print(f"[OK SERVER.JS] {sp}")
            except Exception as e:
                print(f"[ERR SERVER.JS] {sp}: {e}")

    # 2. judge.md
    judge_paths = [
        r"C:\Program Files\ZCode\resources\glm\packages\document-skills-plugin\agents\judge.md",
        os.path.join(USER_ZCODE, r"cli\plugins\cache\zcode-plugins-official\document-skills\0.1.4\agents\judge.md"),
        os.path.join(USER_ZCODE, r"cli\plugins\cache\zcode-plugins-official\document-skills\0.1.5\agents\judge.md")
    ]
    for jp in judge_paths:
        if os.path.exists(jp):
            try:
                with open(jp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "kabul incelemesi" not in content or "Ã" in content:
                    content = re.sub(r'description:\s*"[^"]+"', 'description: "Yalnızca pptx, docx, xlsx, pdf, poster ve grafik türündeki görsel çıktıların kabul incelemesi için tek yetkili görsel onay ajanı."', content)
                    with open(jp, "w", encoding="utf-8", newline="\n") as f:
                        f.write(content)
                    print(f"[OK JUDGE.MD] {jp}")
            except Exception as e:
                print(f"[ERR JUDGE.MD] {jp}: {e}")


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
    patch_special_files()
    scan_and_patch(os.path.join(USER_ZCODE, "cli", "plugins"))
    scan_and_patch(PROGRAM_PACKAGES)
    scan_and_patch(os.path.expanduser(r"~\.agents\skills"))
    scan_and_patch(os.path.expanduser(r"~\.claude\skills"))
    print("Eklenti paketleri başarıyla güncellendi!")


if __name__ == "__main__":
    main()
