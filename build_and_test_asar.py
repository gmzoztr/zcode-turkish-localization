# -*- coding: utf-8 -*-
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"C:\Users\Work-D\ZCodeProject"
ZCODE_RESOURCES = r"C:\Program Files\ZCode\resources"
ORIG_ASAR = os.path.join(ZCODE_RESOURCES, "app.asar.orig") if os.path.exists(os.path.join(ZCODE_RESOURCES, "app.asar.orig")) else os.path.join(ZCODE_RESOURCES, "app.asar")
PATCHED_ASAR = os.path.join(BASE_DIR, "app.asar.patched")
DICT_PATH = os.path.join(BASE_DIR, "tr_dictionary_zcode.json")

MENU_TR_V2 = {
    "titleBar.menu.file": "Dosya",
    "titleBar.menu.edit": "Düzen",
    "titleBar.menu.view": "Görünüm",
    "titleBar.menu.window": "Pencere",
    "titleBar.menu.help": "Yardım",
    "titleBar.menu.file.newTask": "Yeni Görev",
    "titleBar.menu.file.openWorkspace": "Çalışma Alanı Aç...",
    "titleBar.menu.file.closeWindow": "Pencereyi Kapat",
    "titleBar.menu.edit.undo": "Geri Al",
    "titleBar.menu.edit.redo": "Yinele",
    "titleBar.menu.edit.cut": "Kes",
    "titleBar.menu.edit.copy": "Kopyala",
    "titleBar.menu.edit.paste": "Yapıştır",
    "titleBar.menu.edit.delete": "Sil",
    "titleBar.menu.edit.selectAll": "Tümünü Seç",
    "titleBar.menu.view.toggleFullScreen": "Tam Ekranı Aç/Kapat",
    "titleBar.menu.view.actualSize": "Gerçek Boyut",
    "titleBar.menu.view.zoomIn": "Yakınlaştır",
    "titleBar.menu.view.zoomOut": "Uzaklaştır",
    "titleBar.menu.window.minimize": "Küçült",
    "titleBar.menu.window.zoom": "Büyüt",
    "titleBar.menu.window.bringAllToFront": "Tümünü Öne Getir",
    "titleBar.menu.app.services": "Hizmetler",
    "titleBar.menu.app.hide": "{appName} Gizle",
    "titleBar.menu.app.hideOthers": "Diğerlerini Gizle",
    "titleBar.menu.app.showAll": "Tümünü Göster",
    "titleBar.menu.app.quit": "{appName} Uygulamasından Çık",
    "titleBar.menu.help.about": "ZCode Hakkında",
    "titleBar.menu.help.whatsNew": "Yenilikler",
    "titleBar.menu.help.checkForUpdates": "Güncellemeleri Denetle...",
    "titleBar.menu.help.toggleDevTools": "Geliştirici Araçlarını Aç/Kapat",
    "titleBar.menu.help.resourceManager": "Dosya Gezgini",
    "titleBar.menu.help.toggleZCodeStdioTap": "Ajan Stdio İletişimini Yakala",
    "titleBar.menu.help.zcodeEndpoint": "ZCode Uç Noktası",
    "titleBar.menu.help.zcodeEndpoint.production": "Production (Varsayılan)",
    "titleBar.menu.help.zcodeEndpoint.test": "Test",
    "titleBar.menu.help.zcodeEndpoint.custom": "Özel...",
    "titleBar.menu.help.zcodeEndpoint.reset": "Varsayılana Sıfırla",
    "titleBar.menu.help.feedback": "Geri Bildirim Bildir...",
    "titleBar.menu.help.exportLogs": "Günlükleri Dışa Aktar",
    "titleBar.menu.help.clearAllData": "Tüm Verileri Temizle",
    "desktopMenu.help.checkingForUpdates": "Güncellemeler denetleniyor...",
    "desktopMenu.help.updateAvailableVersion": "Yeni sürüm mevcut: {version}",
    "desktopMenu.help.downloadingUpdateVersion": "Güncelleme indiriliyor: {version}...",
    "desktopMenu.help.downloadingUpdateProgress": "Güncelleme indiriliyor... {progress}",
    "desktopMenu.help.restartToUpdate": "Yeniden Başlat ve Güncelle ({version})",
    "dock.menu.showCurrentWindow": "Mevcut Pencereyi Göster",
    "tray.tooltip": "ZCode",
    "tray.menu.openZCode": "ZCode'u Aç",
    "tray.menu.quit": "Çıkış"
}

def parse_asar_header(f):
    header_raw = f.read(16)
    if len(header_raw) < 16:
        raise ValueError("Geçersiz ASAR başlığı")
    u1, str_len, u2, json_len = struct.unpack("<IIII", header_raw)
    json_bytes = f.read(json_len)
    header = json.loads(json_bytes.decode("utf-8"))
    base_offset = 8 + str_len
    return header, base_offset, str_len

def find_node(header_json, path_parts):
    node = header_json
    for part in path_parts:
        if "files" not in node or part not in node["files"]:
            return None
        node = node["files"][part]
    return node

def extract_file(f_src, node, base_offset):
    offset = int(node["offset"])
    size = int(node["size"])
    f_src.seek(base_offset + offset)
    return f_src.read(size)

def find_target_paths(header, f_src, base_offset):
    renderer_assets = header.get("files", {}).get("out", {}).get("files", {}).get("renderer", {}).get("files", {}).get("assets", {}).get("files", {})
    main_files = header.get("files", {}).get("out", {}).get("files", {}).get("main", {}).get("files", {})

    intl_file = None
    styles_file = None
    usage_parts_file = None

    for k in renderer_assets.keys():
        if k.startswith("IntlProvider-") and k.endswith(".js"):
            intl_file = k
        elif k.startswith("styles-") and k.endswith(".js"):
            styles_file = k
        elif k.startswith("usageStatsUiParts-") and k.endswith(".js"):
            usage_parts_file = k

    menu_file = None
    for k, node in main_files.items():
        if k.startswith("chunk-") and k.endswith(".js"):
            offset = int(node["offset"])
            size = int(node["size"])
            f_src.seek(base_offset + offset)
            c = f_src.read(size).decode("utf-8", errors="ignore")
            if 'titleBar.menu.file' in c or 'Kp={"zh-CN":' in c or 'pp={' in c:
                menu_file = k
                break

    if not intl_file:
        raise FileNotFoundError("IntlProvider bundle bulunamadı!")
    if not styles_file:
        raise FileNotFoundError("Styles bundle bulunamadı!")
    if not usage_parts_file:
        raise FileNotFoundError("usageStatsUiParts bundle bulunamadı!")
    if not menu_file:
        raise FileNotFoundError("Menu chunk bundle bulunamadı!")

    return {
        "intl": ["out", "renderer", "assets", intl_file],
        "styles": ["out", "renderer", "assets", styles_file],
        "usage_parts": ["out", "renderer", "assets", usage_parts_file],
        "menu": ["out", "main", menu_file],
        "main": ["out", "main", "index.js"],
        "html": ["out", "renderer", "index.html"],
    }

def patch_intl(js_content, tr_dict):
    tr_json = json.dumps(tr_dict, ensure_ascii=False)
    replacement = f'g={{"zh-CN":p,"en-US":Object.assign({{}},m,{tr_json})}}'

    pos_obj = js_content.find('g={"zh-CN":p,"en-US":Object.assign({},m,')
    if pos_obj != -1:
        pos_after = js_content.find(',_=`zcode-locale-preference`', pos_obj)
        if pos_after != -1:
            return js_content[:pos_obj] + replacement + js_content[pos_after:]

    target = 'g={"zh-CN":p,"en-US":m}'
    pos_g = js_content.find(target)
    if pos_g != -1:
        return js_content[:pos_g] + replacement + js_content[pos_g + len(target):]
    return js_content

def patch_menu(js_content):
    pos_kp = js_content.find('Kp={"zh-CN":')
    if pos_kp != -1:
        pos_end_kp = js_content.find('};function db(', pos_kp)
        kp_str = js_content[pos_kp + 3:pos_end_kp + 1]
        kp_data = json.loads(kp_str)
        for k, v in MENU_TR_V2.items():
            if "en-US" in kp_data:
                kp_data["en-US"][k] = v
            if "zh-CN" in kp_data:
                kp_data["zh-CN"][k] = v
        new_kp_json = json.dumps(kp_data, ensure_ascii=False)
        return js_content[:pos_kp + 3] + new_kp_json + js_content[pos_end_kp + 1:]

    # Fallback to pp menu
    pos_pp = js_content.find("pp={")
    if pos_pp != -1:
        pos_by = js_content.find("function by(", pos_pp)
        if pos_by != -1:
            pp_str = js_content[pos_pp + 3:pos_by].strip().rstrip(";")
            try:
                pp_data = json.loads(pp_str)
                if "en-US" in pp_data:
                    for k, v in MENU_TR_V2.items():
                        pp_data["en-US"][k] = v
                new_pp_json = json.dumps(pp_data, ensure_ascii=False)
                return js_content[:pos_pp] + f"pp={new_pp_json};" + js_content[pos_by:]
            except Exception:
                pass
    return js_content

def patch_styles(js_content):
    pos_sb = js_content.find('const styleId = "zcode-coding-plan-hide-scrollbar";')
    if pos_sb != -1:
        pos_fn_start = js_content.rfind("function ", 0, pos_sb)
        pos_fn_end = js_content.find("function rMe(", pos_sb)
        if pos_fn_end == -1:
            pos_fn_end = js_content.find("function ", pos_sb)

        TR_MAP_CODE = r'''const TR_MAP = {
    "Personal plans": "Bireysel Planlar",
    "Team plans": "Ekip Planları",
    "Personal Plans": "Bireysel Planlar",
    "Team Plans": "Ekip Planları",
    "Monthly": "Aylık",
    "Quarterly -20%": "3 Aylık -%20",
    "Yearly -30%": "Yıllık -%30",
    "Quarterly": "3 Aylık",
    "Yearly": "Yıllık",
    "-20%": "-%20",
    "-30%": "-%30",
    "/month": "/ay",
    "/ month": "/ay",
    " /month": " /ay",
    " / month": " /ay",
    "Ideal for getting started": "Başlangıç için ideal",
    "5-day free trial, including:": "5 günlük ücretsiz deneme, şunları içerir:",
    "5-day free trial, including": "5 günlük ücretsiz deneme, şunları içerir",
    "5-day free trial": "5 günlük ücretsiz deneme",
    "including:": "şunları içerir:",
    "including": "şunları içerir",
    "Configure custom models with BYOK": "BYOK ile özel modelleri yapılandırın",
    "Occasional free token offers": "Dönemsel ücretsiz token teklifleri",
    "Weekend Build": "Hafta Sonu Derlemesi",
    "Global Build": "Küresel Derleme",
    "Ended": "Sona Erdi",
    "Expired": "Süresi Doldu",
    "Lightweight repo iteration": "Hafif repo geliştirmesi",
    "Rolling access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere kesintisiz erişim",
    "Supports 20+ coding tools, including ZCode": "ZCode dahil 20+ kodlama aracını destekler",
    "ZCode-exclusive benefits:": "ZCode'a özel avantajlar:",
    "ZCode-exclusive benefits": "ZCode'a özel avantajlar",
    "Idle-time tasks: 1/day Free token": "Boş zaman görevleri: Günde 1 Ücretsiz token",
    "Idle-time tasks: 3/day Free token": "Boş zaman görevleri: Günde 3 Ücretsiz token",
    "Idle-time tasks: 5/day Free token": "Boş zaman görevleri: Günde 5 Ücretsiz token",
    "Idle-time tasks: 1/day": "Boş zaman görevleri: Günde 1",
    "Idle-time tasks: 3/day": "Boş zaman görevleri: Günde 3",
    "Idle-time tasks: 5/day": "Boş zaman görevleri: Günde 5",
    "Idle-time tasks:": "Boş zaman görevleri:",
    "Idle-time tasks": "Boş zaman görevleri",
    "Idle-time task": "Boş zaman görevi",
    "Free token": "Ücretsiz token",
    "free token": "ücretsiz token",
    "Reset the 5-hour quota during idle hours": "Boş zaman saatlerinde 5 saatlik kotayı sıfırlama",
    "ZCode MCP benefits": "ZCode MCP avantajları",
    "150% quota with a limited-time usage multiplier discount": "Sınırlı süreli kullanım çarpanı indirimiyle %150 kota",
    "Subscribe": "Abone Ol",
    "Subscribe now": "Şimdi Abone Ol",
    "Everything in Lite": "Lite'taki her şey dahil",
    "Everything in Pro": "Pro'daki her şey dahil",
    "Priority access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere öncelikli erişim",
    "Includes a curated selection of MCP tools": "Seçkin MCP araçları koleksiyonu içerir",
    "Faster generation speeds": "Daha yüksek üretim hızları",
    "Built for advanced users working on mid-to-large repos": "Orta ve büyük repolarda çalışan ileri düzey kullanıcılar için üretildi",
    "First access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere ilk erişim",
    "Dedicated resources during peak times": "Yoğun saatlerde ayrılmış kaynaklar",
    "For Individuals": "Bireysel İçin",
    "For Teams": "Ekipler İçin",
    "Start Plan": "Başlangıç Planı",
    "8M GLM tokens daily": "Günlük 8M GLM token",
    "GLM-5.3 · 3M tokens daily": "GLM-5.3 · Günlük 3M token",
    "GLM-5.3-Flash · 5M tokens daily": "GLM-5.3-Flash · Günlük 5M token",
    "Included": "Dahil",
    "GLM Coding Lite": "GLM Coding Lite",
    "10,000 Credits / week": "Haftalık 10.000 Kredi",
    "10,000 Credits/week": "Haftalık 10.000 Kredi",
    "Small repo iteration": "Küçük proje geliştirme",
    "Latest models over time": "Zamanla en güncel modeller",
    "20+ coding tools": "20+ kodlama aracı",
    "Select": "Seç",
    "GLM Coding Pro": "GLM Coding Pro",
    "Mid-sized repo development": "Orta ölçekli proje geliştirme",
    "Priority model access": "Öncelikli model erişimi",
    "Curated MCP tools": "Seçkin MCP araçları",
    "GLM Coding Max": "GLM Coding Max",
    "Mid-to-large repo work": "Orta ve büyük ölçekli proje geliştirme",
    "First model access": "En yeni modellere ilk erişim",
    "Peak-time priority": "Yoğun saatlerde öncelik",
    "Pro Team": "Pro Ekip",
    "Max Team": "Max Ekip",
    "Shared team quota": "Ortak ekip kotası",
    "Higher shared team quota": "Daha yüksek ortak ekip kotası",
    "For small teams that need shared quota and seat management.": "Ortak kota ve kullanıcı yönetimine ihtiyaç duyan küçük ekipler için.",
    "For high-throughput engineering teams that need more quota and flexible seats.": "Daha fazla kotaya ve esnek kullanıcı sayısına ihtiyaç duyan yüksek tempolu mühendislik ekipleri için.",
    "Shared quota, seat management, and centralized billing.": "Ortak kota, kullanıcı yönetimi ve merkezi faturalandırma.",
    "Seats, shared quota, and centralized billing are coming later.": "Koltuklar, paylaşılan kota ve merkezi faturalandırma daha sonra sunulacaktır.",
    "Single-seat pricing": "Tek kullanıcı fiyatlandırması",
    "Team-seat pricing": "Ekip fiyatlandırması",
    "Assign members to your team plan": "Ekip planınıza üye atayın",
    "Manage team plan": "Ekip planını yönet",
    "Seats": "Kullanıcı Sayısı",
    "Seat": "Kullanıcı",
    "seats": "kullanıcı",
    "seat": "kullanıcı",
    "per kullanıcı/ay": "/ kullanıcı / ay",
    "per user/month": "/ kullanıcı / ay",
    "per user / month": "/ kullanıcı / ay",
    "per seat/month": "/ kullanıcı / ay",
    "per seat / month": "/ kullanıcı / ay",
    "Unified kullanıcı & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Unified user & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Unified seat & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Team analytics & dashboard": "Ekip analizleri ve gösterge paneli",
    "Flexible usage billing": "Esnek kullanım faturalandırması",
    "Centralized billing & invoicing": "Merkezi faturalandırma ve fatura yönetimi",
    "Default data privacy": "Varsayılan veri gizliliği",
    "All Standard benefits": "Tüm Standart avantajları dahil",
    "Early access to new models & features": "Yeni modellere ve özelliklere erken erişim",
    "Priority resource allocation during peak hours": "Yoğun saatlerde öncelikli kaynak tahsisi",
    "66,000 Credits / week": "Haftalık 66.000 Kredi",
    "155,000 Credits / week": "Haftalık 155.000 Kredi",
    "Credits / week": "Kredi / hafta",
    "Credits/week": "Kredi / hafta",
    "Save 10% annually": "Yıllık %10 indirim",
    "Save 10%": "%10 Tasarruf Edin",
    "/month": "/ ay",
    "Annual discount": "Yıllık indirim",
    "Save 20%": "%20 Tasarruf Edin",
    "Save 30%": "%30 Tasarruf Edin",
    "Calculating payment amount": "Ödeme tutarı hesaplanıyor",
    "Please wait. Confirmation and payment use the same payment details.": "Lütfen bekleyin. Onay ve ödeme aynı ödeme ayrıntılarını kullanır.",
    "Payment amount is unavailable. Go back and choose the billing cycle again.": "Ödeme tutarı mevcut değil. Geri dönün ve faturalandırma döngüsünü tekrar seçin.",
    "Choose billing cycle": "Faturalandırma döngüsünü seçin",
    "Continue to payment": "Ödemeye devam et",
    "Due today": "Bugün ödenecek",
    "Service period": "Hizmet süresi",
    "Auto-renews every": "Otomatik yenilenme:",
    "Renewal policy": "Yenileme politikası",
    "I understand and agree to the renewal policy and subscription terms.": "Yenileme politikasını ve abonelik koşullarını anlıyor ve kabul ediyorum.",
    "Preparing payment": "Ödeme hazırlanıyor",
    "Waiting for security verification": "Güvenlik doğrulaması bekleniyor",
    "Waiting for payment confirmation": "Ödeme onayı bekleniyor",
    "Payment in progress": "Ödeme devam ediyor",
    "Payment successful": "Ödeme başarılı",
    "Payment failed": "Ödeme başarısız oldu",
    "Payment method": "Ödeme yöntemi",
    "Credit card": "Kredi kartı",
    "Card number": "Kart numarası",
    "Expiration date": "Son kullanma tarihi",
    "Security code": "Güvenlik kodu",
    "Country or region": "Ülke veya bölge",
    "Pay": "Öde",
    "Cancel": "İptal",
    "Close": "Kapat",
    "Maybe later": "Belki daha sonra",
    "Back": "Geri",
    "Confirm": "Onayla"
  };

  const SORTED_KEYS = Object.keys(TR_MAP).sort((a, b) => b.length - a.length);

  function translateNode(n) {
    if (!n) return;
    if (n.nodeType === 3) {
      let raw = n.nodeValue;
      if (!raw) return;
      let rawNorm = raw.replaceAll(String.fromCharCode(160), " ");
      let clean = rawNorm.trim().replace(/\\s+/g, " ");
      if (!clean) return;
      if (TR_MAP[clean]) {
        let mLead = rawNorm.match(/^\\s+/);
        let mTrail = rawNorm.match(/\\s+$/);
        let lead = mLead ? mLead[0] : "";
        let trail = mTrail ? mTrail[0] : "";
        n.nodeValue = lead + TR_MAP[clean] + trail;
        return;
      }
      let modified = rawNorm;
      for (const en of SORTED_KEYS) {
        if (modified.includes(en)) {
          modified = modified.replaceAll(en, TR_MAP[en]);
        }
      }
      if (clean.startsWith("6x Lite usage") || clean.startsWith("6× Lite usage")) {
        modified = "6 kat Lite kullanımı + Tüm Lite avantajları";
      } else if (clean.startsWith("14x Lite usage") || clean.startsWith("14× Lite usage")) {
        modified = "14 kat Lite kullanımı + Tüm Lite avantajları";
      } else if (clean.startsWith("20x Lite usage") || clean.startsWith("20× Lite usage")) {
        modified = "20 kat Lite kullanımı + Tüm Pro avantajları";
      } else if (clean.startsWith("Save 10% annually")) {
        modified = clean.replace("Save 10% annually", "Yıllık %10 indirim").replace("From", "Başlangıç:").replace("/month", "/ ay").replace("/ay", "/ ay");
      } else if (clean.startsWith("Unified")) {
        modified = "Birleşik kullanıcı ve yetki yönetimi";
      }
      if (modified.includes("per kullanıcı/ay") || modified.includes("per user/month") || modified.includes("per seat/month")) {
        modified = modified.replace("per kullanıcı/ay", "/ kullanıcı / ay").replace("per user/month", "/ kullanıcı / ay").replace("per seat/month", "/ kullanıcı / ay");
      }
      if (modified.includes("Credits / week") || modified.includes("Credits/week")) {
        modified = modified.replace("Credits / week", "Kredi / hafta").replace("Credits/week", "Kredi / hafta");
      }
      if (modified !== raw) n.nodeValue = modified;
    } else if (n.nodeType === 1) {
      if (n.tagName === "SCRIPT" || n.tagName === "STYLE") return;
      if (n.placeholder && TR_MAP[n.placeholder.trim()]) n.placeholder = TR_MAP[n.placeholder.trim()];
      if (n.title && TR_MAP[n.title.trim()]) n.title = TR_MAP[n.title.trim()];
      if (n.getAttribute && n.getAttribute("aria-label")) {
        const aria = n.getAttribute("aria-label").trim();
        if (TR_MAP[aria]) n.setAttribute("aria-label", TR_MAP[aria]);
      }
      for (let c = n.firstChild; c; c = c.nextSibling) {
        translateNode(c);
      }
    }
  }

  if (document.body) translateNode(document.body);
  if (window.__zcode_tr_obs__) {
    try { window.__zcode_tr_obs__.disconnect(); } catch (e) {}
  }
  const obs = new MutationObserver(muts => {
    for (const m of muts) {
      if (m.type === "childList") {
        for (let i = 0; i < m.addedNodes.length; i++) translateNode(m.addedNodes[i]);
      } else if (m.type === "characterData") {
        translateNode(m.target);
      }
    }
  });
  obs.observe(document.documentElement || document.body, { childList: true, subtree: true, characterData: true });
  window.__zcode_tr_obs__ = obs;

  if (window.__zcode_tr_interval__) {
    try { clearInterval(window.__zcode_tr_interval__); } catch (e) {}
  }
  window.__zcode_tr_interval__ = setInterval(() => {
    if (document.body) translateNode(document.body);
  }, 400);'''

        fn_sig = js_content[pos_fn_start:js_content.find("{", pos_fn_start)+1]
        new_fn_body = f"""return`(() => {{
  const styleId = "zcode-coding-plan-hide-scrollbar";
  if (!document.getElementById(styleId)) {{
    const style = document.createElement("style");
    style.id = styleId;
    style.textContent = "html, body, * {{ scrollbar-width: none !important; }} html::-webkit-scrollbar, body::-webkit-scrollbar, *::-webkit-scrollbar {{ display: none !important; width: 0 !important; height: 0 !important; }}";
    document.head.appendChild(style);
  }}

  {TR_MAP_CODE}
}})()`}}"""

        js_content = js_content[:pos_fn_start] + fn_sig + new_fn_body + js_content[pos_fn_end:]

    # Webview navigation hook to re-run nMe() on page finish or navigation
    target_r_i = 'r=()=>{T(e=>({...e,isLoading:!1})),j(e)},i=()=>{j(e)}'
    replacement_r_i = 'r=()=>{T(e=>({...e,isLoading:!1})),j(e),e.executeJavaScript(nMe(),!0).catch(()=>{})},i=()=>{j(e),e.executeJavaScript(nMe(),!0).catch(()=>{})}'
    if target_r_i in js_content:
        js_content = js_content.replace(target_r_i, replacement_r_i, 1)

    # Skill description regex
    skill_pattern = r'function\s+(\w+)\(e,t\)\{return\((\w+)\(e\)\?(\w+)\[e\.name\]\?\.\[t\?\?`en-US`\]:void 0\)\?\?e\.description\}'
    js_content = re.sub(skill_pattern, r'function \1(e,t){return e.description||(\2(e)?\3[e.name]?.[t??`en-US`]:void 0)}', js_content)

    # Date format
    js_content = js_content.replace("Intl.DateTimeFormat(t,{day:`numeric`,month:`short`", 'Intl.DateTimeFormat("tr-TR",{day:`numeric`,month:`short`')

    # Computer use labels
    js_content = js_content.replace("title:`Computer Use`", "title:`Bilgisayar Kontrolü`")
    js_content = js_content.replace("kind??`Computer Use`", "kind??`Bilgisayar Kontrolü`")
    js_content = js_content.replace("children:`Parameters`", "children:`Parametreler`")

    # Suggested prompts Wz replacement
    bt = chr(96)
    wz_pattern = rf"function\s+(\w+)\(e,t\)\{{let\s+n=t\.startsWith\({bt}zh{bt}\)\?e\.cn:e\.en,r=t\.startsWith\({bt}zh{bt}\)\?e\.en:e\.cn;return\s+n\?\.trim\(\)\|\|r\?\.trim\(\)\|\|{bt}{bt}\}}"
    replacement = (
        r'function \1(e,t){const _tr={"Weekly Summary":"Haftalık Özet","Error Fix":"Hata Düzeltme",'
        r'"PPT Creation":"Sunum (PPT) Hazırlama","Idle-time task":"Boş Zaman Görevi","Idle-time Task":"Boş Zaman Görevi",'
        r'"idle-time task":"Boş Zaman Görevi","Idle-time tasks":"Boş Zaman Görevleri","Idle-time Tasks":"Boş Zaman Görevleri",'
        r'"Code Review":"Kod İncelemesi","Refactor":"Yeniden Düzenleme","Explain Code":"Kodu Açıkla",'
        r'"Generate Tests":"Test Üret","Optimize":"Optimize Et"};'
        f'let n=t.startsWith({bt}zh{bt})?e.cn:(e.tr||e.en),r=t.startsWith({bt}zh{bt})?(e.tr||e.en):e.cn;'
        f'let s=n?.trim()||r?.trim()||{bt}{bt};return _tr[s]||s}}'
    )
    js_content = re.sub(wz_pattern, replacement, js_content)

    # Automation template cards e4 translation
    e4_pattern = rf"function\s+(\w+)\(e,t\)\{{let\s+n=t\?\.startsWith\({bt}zh{bt}\)\?\?!1,r=n\?e\.cn:e\.en,i=n\?e\.en:e\.cn;return\s+r\?\.trim\(\)\|\|i\?\.trim\(\)\|\|{bt}{bt}\}}"
    e4_replacement = (
        r'function \1(e,t){const _tr={"Morning dev brief":"Sabah Geliştirici Özeti","Risk scan":"Risk Taraması","Release brief":"Sürüm Özeti","Documentation sync check":"Belge Senkronizasyon Kontrolü","Customize":"Özelleştir"};'
        r'const _trD={"Summarize commits":"Önceki iş gününden bu yana yapılan commitleri, modül değişikliklerini, CI durumunu ve takipleri özetleyin; stand-up için hazır maddeler çıkarın.",'
        r'"Inspect code changes":"Çalışma zamanı hataları, veri kaybı, yetkilendirme açıkları ve kaynak sorunları gibi yüksek riskli durumlar için son 24 saatteki kod değişikliklerini inceleyin.",'
        r'"Organize PRs and commits":"Bu hafta birleştirilen PRları ve commitleri Özellikler, Düzeltmeler, Deneyim iyileştirmeleri ve Mühendislik geliştirmeleri olarak düzenleyin.",'
        r'"Compare code, configuration":"Son yedi gündeki kod, yapılandırma, API ve dokümantasyon değişikliklerini karşılaştırın; belgelerin güncellenmesi gereken noktaları belirleyin."};'
        f'let n=t?.startsWith({bt}zh{bt})??!1,r=n?e.cn:(e.tr||e.en),i=n?(e.tr||e.en):e.cn;let s=r?.trim()||i?.trim()||{bt}{bt};'
        r'if(_tr[s])return _tr[s];for(const[k,v]of Object.entries(_trD)){if(s.startsWith(k))return v}return s}'
    )
    js_content = re.sub(e4_pattern, e4_replacement, js_content)

    # Plugin marketplace card titles and descriptions m4/h4 replacement
    m4_target = "function m4(e,t){return Dn(e,t)}function h4(e,t){return pne(t,e.summary?.description??e.info?.description??e.installedMeta?.description,e.listing?.descriptionI18n)}"
    m4_replacement = (
        'const TR_P_NAMES={"Restore Legacy Sessions":"Eski Oturumları Geri Yükle","Skill Creator":"Beceri Oluşturucu","ZCode Guide":"ZCode Rehberi","Android Emulator":"Android Emülatörü","iOS Simulator":"iOS Simülatörü","browser-use":"Browser Use","computer-use":"Bilgisayar Kontrolü","document-skills":"Belge Becerileri","dingtalk-cli":"DingTalk CLI","lark-cli":"Lark CLI","obsidian":"Obsidian","alibaba-cloud-cli":"Alibaba Cloud CLI","android-emulator":"Android Emulator","ios-simulator":"iOS Simulator","skill-creator":"Beceri Oluşturucu","restore-legacy-sessions":"Eski Oturumları Geri Yükle","zcode-guide":"ZCode Rehberi","video-agent-kit":"Video Ajan Kiti","video2code":"Video2Code","accounting-and-reporting":"Muhasebe ve Raporlama","assess-credit":"Sabit Getiri ve Kredi Araştırması","find-clients":"Kurumsal Müşteri Kazanımı","model-deals":"İşlem Modelleme ve Yapılandırma","pick-funds":"Fon ve Portföy Araştırması","read-macro":"Makro Strateji Analizi","run-fpa":"Finansal Planlama ve Analiz (FP&A)","vet-companies":"Şirket Durum Tespiti (Due Diligence)","watch-positions":"Pozisyon ve Portföy Takibi","write-research":"Yatırım ve Hisse Araştırması","hexin":"Tonghuashun iFinD","wind":"Wind Finansal Veri","tianyancha":"Tianyancha Şirket Bilgileri","finance-search":"Finansal Arama","mimosa":"Kod Güvenlik Koruması","github":"GitHub CLI","gitlab":"GitLab CLI","tencent-meeting-cli":"Tencent Meeting CLI","wecom-cli":"WeCom CLI","cloudbase-skills":"CloudBase Becerileri"};'
        'const TR_P_DESCS={"browser-use":"Masaüstü için yerleşik tarayıcı otomasyonu çalışma ortamı ve rehberlik.","computer-use":"Bilgisayar Kontrolü: Masaüstü uygulamalarını fare, klavye ve sistem eylemleriyle otomatikleştirin.","document-skills":"Yerleşik DOCX ve PDF belge oluşturma becerileri.","dingtalk-cli":"OAuth/cihaz yetkilendirmesi, profil kontrolleri ve yeteneklerle DingTalk Çalışma Alanı CLI iş akışları.","lark-cli":"Belgeler, tablolar, Base, takvim ve mesajlaşma için rehberli kurulum ve OAuth girişli Lark CLI iş akışları.","obsidian":"Obsidian Markdown notları, Bases veritabanı görünümleri, Canvas panoları, CLI otomasyonu ve görselleştirme becerileri.","alibaba-cloud-cli":"Kimlik bilgisi kurulumu, profil kontrolleri ve güvenli bulut kaynak işlemleri için Alibaba Cloud CLI iş akışları.","android-emulator":"Android emülatörlerini yönetme, başlatma ve cihaz kontrolü için geliştirici araçları.","ios-simulator":"iOS simülatörlerini yönetme, test etme ve arayüz denetimi araçları.","skill-creator":"Yeni ajan becerileri ve iş akışları oluşturmak için rehberli araç seti.","restore-legacy-sessions":"Önceki sürümlerden kalan eski oturumları ve sohbet geçmişlerini geri yükleyin.","zcode-guide":"ZCode özellikleri, komutları ve yapılandırmaları için kapsamlı kullanım kılavuzu.","video-agent-kit":"Otomatik video düzenleme araç seti: Bulut ses transkripsiyonu ve sentezi, kare analizi, zaman çizelgesi ve önizleme.","video2code":"ZCode yerleşik Browser Use WebView ile WebM kaydı ve ffmpeg ile MP4 dönüştürme/yeniden oluşturma.","cloudbase-skills":"Web, WeChat Mini Programı, veritabanı, bulut fonksiyonları ve yapay zeka projeleri için CloudBase geliştirme becerileri ve MCP entegrasyonu.","mimosa":"ZCode için yazma öncesi kancalar, tur sonu incelemesi, Git kapıları ve güvenlik taraması becerisiyle yerel öncelikli güvenlik koruması.","github":"Commit, pull request, issue, release, Actions ve repolar için GitHub CLI iş akışları.","gitlab":"Merge request, issue, CI/CD ve repolar için GitLab resmi ajan becerilerine dayalı GitLab CLI iş akışları.","tencent-meeting-cli":"OAuth2 kurulumu, toplantı yönetimi, kayıtlar ve katılımcı raporlarıyla Tencent Meeting CLI iş akışları.","wecom-cli":"Mesajlar, belgeler, tablolar, takvim, toplantılar ve kişiler için QR doğrulamalı WeCom CLI iş akışları.","accounting-and-reporting":"Şirket defterinden muhasebe kapanışı ve yasal raporlama: ay sonu kontrolleri ve mutabakat.","assess-credit":"Sabit getirili menkul kıymetler ve kredi araştırması: tahvil profilleri, ihraççı değerlendirmesi ve getiri eğrisi analizi.","find-clients":"Kurumsal bankacılık müşteri kazanımı: bölgeye ve sektöre göre potansiyel müşteri taraması ve fırsat analizi.","model-deals":"İşlem yapılandırma ve modelleme: M&A, IPO ve sermaye artırımı seyreltme analizi.","pick-funds":"Fon ve fon yöneticisi araştırması: çok kriterli fon taraması, portföy ve stil analizi.","read-macro":"Yukarıdan aşağıya makro strateji: büyüme, enflasyon, likidite ve çapraz varlık dağılım görünümleri.","run-fpa":"Kurumsal finansman ve FP&A: yönetim raporlaması, nakit akışı tahminleri ve bütçe-gerçekleşen varyans analizi.","vet-companies":"Karşı taraf ve şirket durum tespiti: yapılandırılmış DD raporları, tedarik zinciri haritalama ve risk taraması.","watch-positions":"İzleme listesi ve portföy takibi: kapanış sonrası özetler, pozisyon olay uyarıları ve gün içi hareket analizi.","write-research":"Uçtan uca yatırım araştırma raporları, sektör analizi, kazanç güncellemeleri ve değerleme modelleri.","hexin":"RoyalFlush iFinD hisse senedi, küresel hisseler, endeks, fon ve tahvil verileri için MCP hizmetleri.","wind":"Wind hisse senedi, küresel hisseler, endeks, fon, tahvil, ekonomik ve doküman verileri için MCP hizmetleri.","tianyancha":"Tianyancha şirket bilgileri sorguları için MCP hizmeti.","finance-search":"SEC EDGAR dosyalama araması ve finansal web/haber aramaları için MCP hizmetleri."};'
        'function m4(e,t){let k=(e&&(e.name||e.id||(e.listing&&e.listing.displayName)))||"";let base=String(k).replace(/@.*$/,"").replace(/^plugin:/,"").trim();if(TR_P_NAMES[base])return TR_P_NAMES[base];if(TR_P_NAMES[k])return TR_P_NAMES[k];let res=Dn(e,t);if(TR_P_NAMES[res])return TR_P_NAMES[res];return res}'
        'function h4(e,t){let k=(e&&(e.name||e.id))||"";let base=String(k).replace(/@.*$/,"").replace(/^plugin:/,"").trim();if(TR_P_DESCS[base])return TR_P_DESCS[base];if(TR_P_DESCS[k])return TR_P_DESCS[k];let res=pne(t,e.summary?.description??e.info?.description??e.installedMeta?.description,e.listing?.descriptionI18n);if(typeof res==="string"){if(res.startsWith("Built-in browser automation"))return TR_P_DESCS["browser-use"];if(res.startsWith("Computer Use: automate"))return TR_P_DESCS["computer-use"];if(res.startsWith("Built-in DOCX and PDF"))return TR_P_DESCS["document-skills"];if(res.startsWith("DingTalk Workspace CLI"))return TR_P_DESCS["dingtalk-cli"];if(res.startsWith("Lark CLI workflows"))return TR_P_DESCS["lark-cli"];if(res.startsWith("Obsidian authoring skills"))return TR_P_DESCS["obsidian"];if(res.startsWith("Alibaba Cloud CLI"))return TR_P_DESCS["alibaba-cloud-cli"];if(res.startsWith("Local-first security guardrails"))return TR_P_DESCS["mimosa"];if(res.startsWith("CloudBase development skills"))return TR_P_DESCS["cloudbase-skills"];if(res.startsWith("GitHub CLI workflows"))return TR_P_DESCS["github"];if(res.startsWith("GitLab CLI workflows"))return TR_P_DESCS["gitlab"];if(res.startsWith("Tencent Meeting CLI workflows"))return TR_P_DESCS["tencent-meeting-cli"];if(res.startsWith("WeCom CLI workflows"))return TR_P_DESCS["wecom-cli"];if(res.startsWith("Accounting close and statutory"))return TR_P_DESCS["accounting-and-reporting"];if(res.startsWith("Fixed-income and credit"))return TR_P_DESCS["assess-credit"];if(res.startsWith("Corporate-banking client"))return TR_P_DESCS["find-clients"];if(res.startsWith("Transaction structuring"))return TR_P_DESCS["model-deals"];if(res.startsWith("Fund and fund-manager"))return TR_P_DESCS["pick-funds"];if(res.startsWith("Top-down macro"))return TR_P_DESCS["read-macro"];if(res.startsWith("Corporate finance and FP&A"))return TR_P_DESCS["run-fpa"];if(res.startsWith("Counterparty and company"))return TR_P_DESCS["vet-companies"];if(res.startsWith("Watchlist and portfolio"))return TR_P_DESCS["watch-positions"];if(res.startsWith("End-to-end investment"))return TR_P_DESCS["write-research"];if(res.startsWith("MCP services for RoyalFlush"))return TR_P_DESCS["hexin"];if(res.startsWith("MCP services for Wind"))return TR_P_DESCS["wind"];if(res.startsWith("MCP service for Tianyancha"))return TR_P_DESCS["tianyancha"];if(res.startsWith("MCP services for SEC EDGAR"))return TR_P_DESCS["finance-search"];if(res.includes("自动化视频剪辑工具包"))return TR_P_DESCS["video-agent-kit"];if(res.includes("基于 ZCode 内置 Browser Use"))return TR_P_DESCS["video2code"]}return res}'
    )
    if m4_target in js_content:
        js_content = js_content.replace(m4_target, m4_replacement, 1)

    # Subagents descriptions MHt replacement
    if "function _trAgentDesc(" not in js_content:
        subagent_helpers = (
            'const TR_AGENT_DESCS={"general-purpose":"Karmaşık soruları araştırmak, kod aramak ve çok adımlı görevleri yürütmek için genel amaçlı ajan.",'
            '"Explore":"Geniş kapsamlı aramalar için salt okunur arama ajanı.",'
            '"explore":"Geniş kapsamlı aramalar için salt okunur arama ajanı.",'
            '"judge":"Yalnızca pptx, docx, xlsx, pdf, poster ve grafik türündeki görsel çıktıların kabul incelemesi için tek yetkili görsel onay ajanı."};'
            'function _trAgentDesc(e){let n=(e&&(e.name||e.id))||"";let b=n.includes(":")?n.slice(n.indexOf(":")+1):n;'
            'if(TR_AGENT_DESCS[b])return TR_AGENT_DESCS[b];if(TR_AGENT_DESCS[n])return TR_AGENT_DESCS[n];'
            'let d=(e&&e.description)||"";if(typeof d==="string"){'
            'if(d.startsWith("General-purpose agent"))return TR_AGENT_DESCS["general-purpose"];'
            'if(d.startsWith("Read-only search agent"))return TR_AGENT_DESCS["Explore"];'
            'if(d.startsWith("THE single visual acceptance pass")||d.startsWith("THE single visual acceptance"))return TR_AGENT_DESCS["judge"]}'
            'return d};'
        )
        pos_mht = js_content.find('function MHt(')
        if pos_mht != -1:
            js_content = js_content[:pos_mht] + subagent_helpers + js_content[pos_mht:]
            target_sub = f'children:e.description||d.formatMessage({{id:{bt}settings.subagents.noDescription{bt}}})'
            replacement_sub = f'children:_trAgentDesc(e)||d.formatMessage({{id:{bt}settings.subagents.noDescription{bt}}})'
            if target_sub in js_content:
                js_content = js_content.replace(target_sub, replacement_sub, 1)

    # Section titles helper and V7, m7 injection
    if "function _trSectionTitle(" not in js_content:
        pos_m7 = js_content.find("function m7(")
        if pos_m7 != -1:
            section_title_helper = (
                'const TR_SEC_TITLES={"Restore Legacy Sessions":"Eski Oturumları Geri Yükle",'
                '"Skill Creator":"Beceri Oluşturucu","ZCode Guide":"ZCode Rehberi",'
                '"Android Emulator":"Android Emülatörü","iOS Simulator":"iOS Simülatörü",'
                '"Document Skills":"Belge Becerileri","Browser Use":"Browser Use","Computer Use":"Bilgisayar Kontrolü"};'
                'function _trSectionTitle(n){return TR_SEC_TITLES[n]||n};'
            )
            js_content = js_content[:pos_m7] + section_title_helper + js_content[pos_m7:]
            target_m7 = 'function m7({count:e,hint:t,title:n}){'
            replacement_m7 = 'function m7({count:e,hint:t,title:n}){n=_trSectionTitle(n);'
            if target_m7 in js_content:
                js_content = js_content.replace(target_m7, replacement_m7, 1)
            target_v7 = 'function V7({actions:e,count:t,title:n}){'
            replacement_v7 = 'function V7({actions:e,count:t,title:n}){n=_trSectionTitle(n);'
            if target_v7 in js_content:
                js_content = js_content.replace(target_v7, replacement_v7, 1)

    # Skills and Commands helpers injection
    if "function _trSkillDesc(" not in js_content:
        skill_cmd_helpers = (
            'const TR_SKILL_DESCS={"restore-legacy-sessions":"ZCode\'un ~/.zcode/v2/sessions altındaki eski ACP dönemi ZCode oturumlarını yeni ZCode görev/oturum depolarına aktarması, incelemesi veya planlaması gerektiğinde kullanın. Eski sohbet geçmişini taşıma veya önceki oturumları geri yükleme sorularında tetiklenir.",'
            '"skill-creator":"Yeni beceriler oluşturun, mevcut becerileri düzenleyin ve ifadeleri iyileştirin. Sıfırdan SKILL.md yazarken, mevcut becerileri geliştirirken, tekrarlanan iş akışlarını yeniden kullanılabilir becerilere dönüştürürken veya beceri tetikleyicilerini giderirken kullanın.",'
            '"diagnosing-commands":"ZCode istemcisindeki özel eğik çizgi komutu (/komut) yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir komut eksik olduğunda, bir beceri/ajan tarafından geçersiz kılındığında, ayrıştırılamadığında, kapsamlarda yinelenen adlara sahip olduğunda veya çalıştırılamadığında geçerlidir.",'
            '"diagnosing-hooks":"ZCode istemcisindeki kanca (hook) yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir kanca tetiklenmediğinde, bir olay adı yanlış olduğunda, bir eşleştirici eşleşmediğinde, bir komut dosyası başarısız olduğunda veya kanca sıralaması/izinleri beklenmeyen davranışlara yol açtığında geçerlidir.",'
            '"diagnosing-mcp":"ZCode istemcisindeki MCP (Model Bağlam Protokolü) sunucu yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir MCP sunucusu bağlanmadığında, araçları eksik olduğunda, işlemi hata ile sonlandığında, aktarım protokolü (stdio veya SSE) yanlış yapılandırıldığında veya ortam değişkenleri hatalı olduğunda geçerlidir.",'
            '"diagnosing-plugins":"ZCode istemcisindeki eklenti ve mağaza sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir eklenti listelenmediğinde, mağaza ekleme veya eklenti yükleme başarısız olduğunda, bir eklenti komutu/becerisi/ajanı eksik olduğunda veya bir eklenti yapılandırması bozulduğunda geçerlidir.",'
            '"diagnosing-skills":"ZCode istemcisindeki beceri yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir beceri keşfedilmediğinde, yüklü olduğu halde otomatik tetiklenmediğinde, dosyaları eksik olduğunda, frontmatter ayrıştırma hataları verdiğinde veya kapsamlarda yinelenen adlara sahip olduğunda geçerlidir.",'
            '"zcode-configuration-guide":"ZCode istemcisinde uzantı kaynaklarını (MCP sunucuları, eğik çizgi komutları, beceriler, kancalar ve eklentiler) veya AGENTS.md gibi talimat dosyalarını yapılandırırken kullanın. Bir kullanıcı bu uzantı mekanizmalarının nasıl ekleneceğini, düzenleneceğini veya yapılandırılacağını sorduğunda geçerlidir.",'
            '"ios-dev":"ios-simulator MCP araçlarıyla iOS simülatör uygulamalarını derleyin, çalıştırın, denetleyin ve kolayca otomatikleştirin.",'
            '"android-emulator":"Android emülatörlerini yönetme, başlatma ve cihaz kontrolü için geliştirici araçları.",'
            '"android-dev":"android-emulator MCP araçlarıyla Android emülatör uygulamalarını derleyin, çalıştırın, denetleyin ve kolayca otomatikleştirin."};'
            'function _trSkillDesc(e){let n=(e&&(e.name||e.id))||"";let b=n.includes(":")?n.slice(n.indexOf(":")+1):n;'
            'if(TR_SKILL_DESCS[b])return TR_SKILL_DESCS[b];if(TR_SKILL_DESCS[n])return TR_SKILL_DESCS[n];'
            'let d=(e&&e.description)||"";if(typeof d==="string"){'
            'if(d.startsWith("Use when ZCode needs to inspect"))return TR_SKILL_DESCS["restore-legacy-sessions"];'
            'if(d.startsWith("Create new skills"))return TR_SKILL_DESCS["skill-creator"];'
            'if(d.startsWith("Use to diagnose and fix ZCode custom slash-command"))return TR_SKILL_DESCS["diagnosing-commands"];'
            'if(d.startsWith("Use to diagnose and fix ZCode hook configuration"))return TR_SKILL_DESCS["diagnosing-hooks"];'
            'if(d.startsWith("Use to diagnose and fix ZCode MCP"))return TR_SKILL_DESCS["diagnosing-mcp"];'
            'if(d.startsWith("Use to diagnose and fix ZCode plugin"))return TR_SKILL_DESCS["diagnosing-plugins"];'
            'if(d.startsWith("Use to diagnose and fix ZCode skill configuration"))return TR_SKILL_DESCS["diagnosing-skills"];'
            'if(d.startsWith("Use when configuring ZCode")&&d.includes("extension resources"))return TR_SKILL_DESCS["zcode-configuration-guide"];'
            'if(d.startsWith("Build, run, inspect, and lightly automate iOS"))return TR_SKILL_DESCS["ios-dev"];'
            'if(d.startsWith("Build, run, inspect, and lightly automate Android"))return TR_SKILL_DESCS["android-dev"]}'
            'return d};'
            'const TR_CMD_DESCS={"android-dev":"Android emülatör geliştirme döngüsünü başlatın.","/android-dev":"Android emülatör geliştirme döngüsünü başlatın.",'
            '"ios-dev":"iOS simülatör geliştirme döngüsünü başlatın.","/ios-dev":"iOS simülatör geliştirme döngüsünü başlatın.",'
            '"restore-legacy-sessions":"Eski bir ZCode oturumunu seçin ve geri yükleyin.","/restore-legacy-sessions":"Eski bir ZCode oturumunu seçin ve geri yükleyin."};'
            'function _trCommandDesc(e){let n=(e&&(e.name||e.id))||"";let b=n.startsWith("/")?n.slice(1):n;'
            'if(TR_CMD_DESCS[b])return TR_CMD_DESCS[b];if(TR_CMD_DESCS[n])return TR_CMD_DESCS[n];'
            'let d=(e&&e.description)||"";if(typeof d==="string"){'
            'if(d.startsWith("Start the Android emulator"))return TR_CMD_DESCS["android-dev"];'
            'if(d.startsWith("Start the iOS simulator"))return TR_CMD_DESCS["ios-dev"];'
            'if(d.startsWith("Select and restore a legacy"))return TR_CMD_DESCS["restore-legacy-sessions"]}'
            'return d};'
            'const TR_CMD_HINTS={"[goal or issue description]":"[hedef veya sorun açıklaması]","[agent/workspace/session filters]":"[ajan/çalışma alanı/oturum filtreleri]"};'
            'function _trCommandHint(h){if(!h||typeof h!=="string")return h;let t=h.trim();if(TR_CMD_HINTS[t])return TR_CMD_HINTS[t];'
            'if(t.includes("[goal or issue description]"))return t.replace("[goal or issue description]","[hedef veya sorun açıklaması]");'
            'if(t.includes("[agent/workspace/session filters]"))return t.replace("[agent/workspace/session filters]","[ajan/çalışma alanı/oturum filtreleri]");'
            'return h};'
        )
        pos_qut = js_content.find("function qUt(")
        if pos_qut != -1:
            js_content = js_content[:pos_qut] + skill_cmd_helpers + js_content[pos_qut:]
            target_skill_card = f'children:e.description||p.formatMessage({{id:{bt}settings.skills.noDescription{bt}}})'
            replacement_skill_card = f'children:_trSkillDesc(e)||p.formatMessage({{id:{bt}settings.skills.noDescription{bt}}})'
            if target_skill_card in js_content:
                js_content = js_content.replace(target_skill_card, replacement_skill_card, 1)

            target_skill_modal = f'children:Ae.description||p.formatMessage({{id:{bt}settings.skills.noDescription{bt}}})'
            replacement_skill_modal = f'children:_trSkillDesc(Ae)||p.formatMessage({{id:{bt}settings.skills.noDescription{bt}}})'
            if target_skill_modal in js_content:
                js_content = js_content.replace(target_skill_modal, replacement_skill_modal, 1)

            target_cmd_card = f'children:e.description||a.formatMessage({{id:{bt}settings.commands.noDescription{bt}}})'
            replacement_cmd_card = f'children:_trCommandDesc(e)||a.formatMessage({{id:{bt}settings.commands.noDescription{bt}}})'
            if target_cmd_card in js_content:
                js_content = js_content.replace(target_cmd_card, replacement_cmd_card, 1)

            target_cmd_hint = f'e.argumentHint?(0,$.jsx)(`span`,{{className:`text-ui-base text-foreground-subtlest`,children:e.argumentHint}}):null'
            replacement_cmd_hint = f'e.argumentHint?(0,$.jsx)(`span`,{{className:`text-ui-base text-foreground-subtlest`,children:_trCommandHint(e.argumentHint)}}):null'
            if target_cmd_hint in js_content:
                js_content = js_content.replace(target_cmd_hint, replacement_cmd_hint, 1)

    return js_content


def patch_usage_parts(js_content):
    js_content = js_content.replace('DateTimeFormat(e,', 'DateTimeFormat("tr-TR",')
    js_content = js_content.replace('NumberFormat(e,', 'NumberFormat("tr-TR",')
    js_content = js_content.replace('NumberFormat(e||void 0,', 'NumberFormat("tr-TR",')
    return js_content

def patch_main(js_content):
    js_content = js_content.replace("\\u8D44\\u6E90\\u7BA1\\u7406\\u5668", "Dosya Gezgini")
    js_content = js_content.replace("资源管理器", "Dosya Gezgini")
    return js_content

def patch_html(html_content):
    if "zcode-tr-dom-patch" in html_content:
        return html_content

    dom_script = r"""<script id="zcode-tr-dom-patch">
(function() {
  const DOM_MAP = {
    "Manage Modeller": "Modelleri Yönet",
    "Manage Models": "Modelleri Yönet",
    "Manage models": "Modelleri Yönet",
    "Selected Çalışma Alanları": "Seçili Çalışma Alanları",
    "Selected İşle": "Seçili Commit",
    "Connection Ayarlar": "Bağlantı Ayarları",
    "Görev title": "Görev Başlığı",
    "Görev name": "Görev Adı",
    "İstek description": "İstek Açıklaması",
    "This model does not accept image inputs. Send this request without images, or use a model that supports image input.": "Bu model görsel girişlerini desteklemiyor. Bu isteği görsel olmadan gönderin veya görsel desteği olan bir model kullanın.",
    "This model does not accept image inputs.": "Bu model görsel girişlerini desteklemiyor.",
    "Send this request without images, or use a model that supports image input.": "Bu isteği görsel olmadan gönderin veya görsel desteği olan bir model kullanın.",
    "Turn execution failed": "Tur yürütme başarısız oldu",
    "Computer Use": "Bilgisayar Kontrolü",
    "Parameters": "Parametreler",
    "Tool Call": "Araç Çağrısı",
    "Execution Details": "Yürütme Ayrıntıları",
    "Weekly Summary": "Haftalık Özet",
    "Error Fix": "Hata Düzeltme",
    "PPT Creation": "Sunum (PPT) Hazırlama",
    "Idle-time task": "Boş Zaman Görevi",
    "Idle-time Task": "Boş Zaman Görevi",
    "idle-time task": "Boş Zaman Görevi",
    "Idle-time tasks": "Boş Zaman Görevleri",
    "Idle-time Tasks": "Boş Zaman Görevleri",
    "Idle-time Görev": "Boş Zaman Görevi",
    "idle-time Görev": "Boş Zaman Görevi",
    "Morning dev brief": "Sabah Geliştirici Özeti",
    "Risk scan": "Risk Taraması",
    "Release brief": "Sürüm Özeti",
    "Documentation sync check": "Belge Senkronizasyon Kontrolü",
    "Oluştur Zamanlandı Görev": "Zamanlanmış Görev Oluştur",
    "Zamanlandı Görev template": "Zamanlanmış Görev Şablonları",
    "Zamanlandı Görev": "Zamanlanmış Görev",
    "Eklenti Marketplace": "Eklenti Mağazası",
    "Günlük At 10:00": "Her gün 10:00'da",
    "Haftalık olarak Fri'da, 16:00'de": "Haftalık olarak Cuma günü, 16:00'da",
    "Haftalık olarak Çar'da, 15:00'de": "Haftalık olarak Çarşamba günü, 15:00'te",
    "Personal plans": "Bireysel Planlar",
    "Team plans": "Ekip Planları",
    "Personal Plans": "Bireysel Planlar",
    "Team Plans": "Ekip Planları",
    "Monthly": "Aylık",
    "Quarterly -20%": "3 Aylık -%20",
    "Yearly -30%": "Yıllık -%30",
    "Quarterly": "3 Aylık",
    "Yearly": "Yıllık",
    "Subscribe": "Abone Ol",
    "Ended": "Sona Erdi",
    "Expired": "Süresi Doldu",
    "Ideal for getting started": "Başlangıç için ideal",
    "5-day free trial, including:": "5 günlük ücretsiz deneme, şunları içerir:",
    "5-day free trial": "5 günlük ücretsiz deneme",
    "Configure custom models with BYOK": "BYOK ile özel modelleri yapılandırın",
    "Occasional free token offers": "Dönemsel ücretsiz token teklifleri",
    "Weekend Build": "Hafta Sonu Derlemesi",
    "Global Build": "Küresel Derleme",
    "Lightweight repo iteration": "Hafif repo geliştirmesi",
    "Rolling access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere kesintisiz erişim",
    "Supports 20+ coding tools, including ZCode": "ZCode dahil 20+ kodlama aracını destekler",
    "ZCode-exclusive benefits:": "ZCode'a özel avantajlar:",
    "Idle-time tasks: 1/day Free token": "Boş zaman görevleri: Günde 1 Ücretsiz token",
    "Idle-time tasks: 3/day Free token": "Boş zaman görevleri: Günde 3 Ücretsiz token",
    "Idle-time tasks: 5/day Free token": "Boş zaman görevleri: Günde 5 Ücretsiz token",
    "Idle-time tasks: 1/day": "Boş zaman görevleri: Günde 1",
    "Idle-time tasks: 3/day": "Boş zaman görevleri: Günde 3",
    "Idle-time tasks: 5/day": "Boş zaman görevleri: Günde 5",
    "Idle-time tasks": "Boş zaman görevleri",
    "Free token": "Ücretsiz token",
    "free token": "ücretsiz token",
    "Reset the 5-hour quota during idle hours": "Boş zaman saatlerinde 5 saatlik kotayı sıfırlama",
    "ZCode MCP benefits": "ZCode MCP avantajları",
    "150% quota with a limited-time usage multiplier discount": "Sınırlı süreli kullanım çarpanı indirimiyle %150 kota",
    "Everything in Lite": "Lite'taki her şey dahil",
    "Everything in Pro": "Pro'daki her şey dahil",
    "Priority access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere öncelikli erişim",
    "Includes a curated selection of MCP tools": "Seçkin MCP araçları koleksiyonu içerir",
    "Faster generation speeds": "Daha yüksek üretim hızları",
    "Built for advanced users working on mid-to-large repos": "Orta ve büyük repolarda çalışan ileri düzey kullanıcılar için üretildi",
    "First access to the latest flagship models and features": "En yeni amiral gemisi modellere ve özelliklere ilk erişim",
    "Dedicated resources during peak times": "Yoğun saatlerde ayrılmış kaynaklar",
    "Code Review": "Kod İncelemesi",
    "Refactor": "Yeniden Düzenleme",
    "Explain Code": "Kodu Açıkla",
    "Generate Tests": "Test Üret",
    "Optimize": "Optimize Et",
    "General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks.": "Karmaşık soruları araştırmak, kod aramak ve çok adımlı görevleri yürütmek için genel amaçlı ajan.",
    "Read-only search agent for broad fan-out searches.": "Geniş kapsamlı aramalar için salt okunur arama ajanı.",
    "THE single visual acceptance pass for a rendered deliverable of these types only — pptx, docx, xlsx, pdf, poster, chart; for anything else, do not use it...": "Yalnızca pptx, docx, xlsx, pdf, poster ve grafik türündeki görsel çıktıların kabul incelemesi için tek yetkili görsel onay ajanı.",
    "Restore Legacy Sessions": "Eski Oturumları Geri Yükle",
    "Skill Creator": "Beceri Oluşturucu",
    "ZCode Guide": "ZCode Rehberi",
    "Android Emulator": "Android Emülatörü",
    "iOS Simulator": "iOS Simülatörü",
    "Document Skills": "Belge Becerileri",
    "Unified kullanıcı & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Unified user & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Unified seat & permission management": "Birleşik kullanıcı ve yetki yönetimi",
    "Team analytics & dashboard": "Ekip analizleri ve gösterge paneli",
    "Flexible usage billing": "Esnek kullanım faturalandırması",
    "Centralized billing & invoicing": "Merkezi faturalandırma ve fatura yönetimi",
    "Default data privacy": "Varsayılan veri gizliliği",
    "All Standard benefits": "Tüm Standart avantajları dahil",
    "Early access to new models & features": "Yeni modellere ve özelliklere erken erişim",
    "Priority resource allocation during peak hours": "Yoğun saatlerde öncelikli kaynak tahsisi",
    "per kullanıcı/ay": "/ kullanıcı / ay",
    "per user/month": "/ kullanıcı / ay",
    "per user / month": "/ kullanıcı / ay",
    "per seat/month": "/ kullanıcı / ay",
    "per seat / month": "/ kullanıcı / ay",
    "66,000 Credits / week": "Haftalık 66.000 Kredi",
    "155,000 Credits / week": "Haftalık 155.000 Kredi",
    "Credits / week": "Kredi / hafta",
    "Credits/week": "Kredi / hafta",
    "Start the Android emulator development loop.": "Android emülatör geliştirme döngüsünü başlatın.",
    "Start the iOS simulator development loop.": "iOS simülatör geliştirme döngüsünü başlatın.",
    "Select and restore a legacy ZCode session.": "Eski bir ZCode oturumunu seçin ve geri yükleyin.",
    "[goal or issue description]": "[hedef veya sorun açıklaması]",
    "[agent/workspace/session filters]": "[ajan/çalışma alanı/oturum filtreleri]"
  };

  const SORTED_DOM_KEYS = Object.keys(DOM_MAP).sort((a, b) => b.length - a.length);

  function translateNode(n) {
    if (!n) return;
    if (n.nodeType === 3) {
      let raw = n.nodeValue;
      if (!raw) return;
      let rawNorm = raw.replace(/\u00a0/g, " ");
      let clean = rawNorm.trim().replace(/\s+/g, " ");
      if (!clean) return;
      if (DOM_MAP[clean]) {
        let mLead = rawNorm.match(/^\s+/);
        let mTrail = rawNorm.match(/\s+$/);
        let lead = mLead ? mLead[0] : "";
        let trail = mTrail ? mTrail[0] : "";
        n.nodeValue = lead + DOM_MAP[clean] + trail;
        return;
      }
      let modified = rawNorm;
      for (const k of SORTED_DOM_KEYS) {
        if (modified.includes(k)) {
          modified = modified.replaceAll(k, DOM_MAP[k]);
        }
      }
      if (clean.startsWith("6x Lite usage") || clean.startsWith("6× Lite usage")) {
        modified = "6 kat Lite kullanımı + Tüm Lite avantajları";
      } else if (clean.startsWith("14x Lite usage") || clean.startsWith("14× Lite usage")) {
        modified = "14 kat Lite kullanımı + Tüm Lite avantajları";
      } else if (clean.startsWith("20x Lite usage") || clean.startsWith("20× Lite usage")) {
        modified = "20 kat Lite kullanımı + Tüm Pro avantajları";
      } else if (clean.startsWith("THE single visual acceptance pass") || clean.startsWith("THE single visual acceptance")) {
        modified = "Yalnızca pptx, docx, xlsx, pdf, poster ve grafik türündeki görsel çıktıların kabul incelemesi için tek yetkili görsel onay ajanı.";
      } else if (clean.startsWith("General-purpose agent")) {
        modified = "Karmaşık soruları araştırmak, kod aramak ve çok adımlı görevleri yürütmek için genel amaçlı ajan.";
      } else if (clean.startsWith("Read-only search agent")) {
        modified = "Geniş kapsamlı aramalar için salt okunur arama ajanı.";
      } else if (clean.startsWith("Use when ZCode needs to inspect")) {
        modified = "ZCode'un ~/.zcode/v2/sessions altındaki eski ACP dönemi ZCode oturumlarını yeni ZCode görev/oturum depolarına aktarması, incelemesi veya planlaması gerektiğinde kullanın. Eski sohbet geçmişini taşıma veya önceki oturumları geri yükleme sorularında tetiklenir.";
      } else if (clean.startsWith("Create new skills")) {
        modified = "Yeni beceriler oluşturun, mevcut becerileri düzenleyin ve ifadeleri iyileştirin. Sıfırdan SKILL.md yazarken, mevcut becerileri geliştirirken, tekrarlanan iş akışlarını yeniden kullanılabilir becerilere dönüştürürken veya beceri tetikleyicilerini giderirken kullanın.";
      } else if (clean.startsWith("Use to diagnose and fix ZCode custom slash-command")) {
        modified = "ZCode istemcisindeki özel eğik çizgi komutu (/komut) yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir komut eksik olduğunda, bir beceri/ajan tarafından geçersiz kılındığında, ayrıştırılamadığında, kapsamlarda yinelenen adlara sahip olduğunda veya çalıştırılamadığında geçerlidir.";
      } else if (clean.startsWith("Use to diagnose and fix ZCode hook configuration")) {
        modified = "ZCode istemcisindeki kanca (hook) yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir kanca tetiklenmediğinde, bir olay adı yanlış olduğunda, bir eşleştirici eşleşmediğinde, bir komut dosyası başarısız olduğunda veya kanca sıralaması/izinleri beklenmeyen davranışlara yol açtığında geçerlidir.";
      } else if (clean.startsWith("Use to diagnose and fix ZCode MCP")) {
        modified = "ZCode istemcisindeki MCP (Model Bağlam Protokolü) sunucu yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir MCP sunucusu bağlanmadığında, araçları eksik olduğunda, işlemi hata ile sonlandığında, aktarım protokolü (stdio veya SSE) yanlış yapılandırıldığında veya ortam değişkenleri hatalı olduğunda geçerlidir.";
      } else if (clean.startsWith("Use to diagnose and fix ZCode plugin")) {
        modified = "ZCode istemcisindeki eklenti ve mağaza sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir eklenti listelenmediğinde, mağaza ekleme veya eklenti yükleme başarısız olduğunda, bir eklenti komutu/becerisi/ajanı eksik olduğunda veya bir eklenti yapılandırması bozulduğunda geçerlidir.";
      } else if (clean.startsWith("Use to diagnose and fix ZCode skill configuration")) {
        modified = "ZCode istemcisindeki beceri yapılandırma sorunlarını teşhis etmek ve düzeltmek için kullanın. Bir beceri keşfedilmediğinde, yüklü olduğu halde otomatik tetiklenmediğinde, dosyaları eksik olduğunda, frontmatter ayrıştırma hataları verdiğinde veya kapsamlarda yinelenen adlara sahip olduğunda geçerlidir.";
      } else if (clean.startsWith("Use when configuring ZCode") && clean.includes("extension resources")) {
        modified = "ZCode istemcisinde uzantı kaynaklarını (MCP sunucuları, eğik çizgi komutları, beceriler, kancalar ve eklentiler) veya AGENTS.md gibi talimat dosyalarını yapılandırırken kullanın. Bir kullanıcı bu uzantı mekanizmalarının nasıl ekleneceğini, düzenleneceğini veya yapılandırılacağını sorduğunda geçerlidir.";
      } else if (clean.startsWith("Build, run, inspect, and lightly automate iOS")) {
        modified = "ios-simulator MCP araçlarıyla iOS simülatör uygulamalarını derleyin, çalıştırın, denetleyin ve kolayca otomatikleştirin.";
      } else if (clean.startsWith("Build, run, inspect, and lightly automate Android")) {
        modified = "android-emulator MCP araçlarıyla Android emülatör uygulamalarını derleyin, çalıştırın, denetleyin ve kolayca otomatikleştirin.";
      } else if (clean.startsWith("Save 10% annually")) {
        modified = clean.replace("Save 10% annually", "Yıllık %10 indirim").replace("From", "Başlangıç:").replace("/month", "/ ay").replace("/ay", "/ ay");
      } else if (clean.startsWith("Unified")) {
        modified = "Birleşik kullanıcı ve yetki yönetimi";
      }
      if (modified.includes("per kullanıcı/ay") || modified.includes("per user/month") || modified.includes("per seat/month")) {
        modified = modified.replace("per kullanıcı/ay", "/ kullanıcı / ay").replace("per user/month", "/ kullanıcı / ay").replace("per seat/month", "/ kullanıcı / ay");
      }
      if (modified.includes("Credits / week") || modified.includes("Credits/week")) {
        modified = modified.replace("Credits / week", "Kredi / hafta").replace("Credits/week", "Kredi / hafta");
      }
      if (modified !== raw) n.nodeValue = modified;
    } else if (n.nodeType === 1) {
      if (n.tagName === "SCRIPT" || n.tagName === "STYLE") return;
      if (n.placeholder && DOM_MAP[n.placeholder.trim()]) n.placeholder = DOM_MAP[n.placeholder.trim()];
      if (n.title && DOM_MAP[n.title.trim()]) n.title = DOM_MAP[n.title.trim()];
      if (n.getAttribute && n.getAttribute("aria-label")) {
        const aria = n.getAttribute("aria-label").trim();
        if (DOM_MAP[aria]) n.setAttribute("aria-label", DOM_MAP[aria]);
      }
      for (let c = n.firstChild; c; c = c.nextSibling) {
        translateNode(c);
      }
    }
  }

  if (document.body) translateNode(document.body);

  const obs = new MutationObserver(mutations => {
    for (const m of mutations) {
      if (m.type === "childList") {
        for (let i = 0; i < m.addedNodes.length; i++) {
          translateNode(m.addedNodes[i]);
        }
      } else if (m.type === "characterData") {
        translateNode(m.target);
      }
    }
  });

  obs.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true
  });
})();
</script>"""
    return html_content.replace("</body>", dom_script + "\n</body>")


def rebuild_asar(source_asar_path, dest_asar_path, modified_files_map):
    print("Rebuilding ASAR...")
    with open(source_asar_path, "rb") as f_src:
        header, base_offset, str_len = parse_asar_header(f_src)

        file_list = []
        def collect(node, parts):
            if "files" in node:
                for name, child in node["files"].items():
                    collect(child, parts + [name])
            else:
                p_str = "/".join(parts)
                file_list.append((p_str, parts, node))

        collect(header, [])

        sorted_files = []
        for p_str, parts, node in file_list:
            if "offset" in node:
                sorted_files.append((int(node["offset"]), p_str, parts, node))
        sorted_files.sort(key=lambda x: x[0])

        new_header = json.loads(json.dumps(header))
        new_payload = bytearray()
        current_offset = 0

        for orig_offset, p_str, parts, orig_node in sorted_files:
            h_node = find_node(new_header, parts)
            if p_str in modified_files_map:
                data = modified_files_map[p_str]
            else:
                data = extract_file(f_src, orig_node, base_offset)

            size = len(data)
            h_node["offset"] = str(current_offset)
            h_node["size"] = size
            new_payload.extend(data)
            current_offset += size

        new_json_str = json.dumps(new_header, separators=(",", ":"))
        new_json_bytes = new_json_str.encode("utf-8")

        pad = (4 - (len(new_json_bytes) % 4)) % 4
        padded_json_bytes = new_json_bytes + (b"\x00" * pad)
        padded_len = len(padded_json_bytes)
        raw_json_len = len(new_json_bytes)

        with open(dest_asar_path, "wb") as f_out:
            f_out.write(struct.pack("<IIII", 4, 8 + padded_len, 4 + padded_len, raw_json_len))
            f_out.write(padded_json_bytes)
            f_out.write(new_payload)

        print(f"ASAR rebuilt successfully: {dest_asar_path} ({os.path.getsize(dest_asar_path)} bytes)")

def main():
    print("Reading original ASAR and dictionary...")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        tr_dict = json.load(f)

    with open(ORIG_ASAR, "rb") as f_src:
        header, base_offset, str_len = parse_asar_header(f_src)
        targets = find_target_paths(header, f_src, base_offset)
        print("Dynamic targets identified:")
        for k, v in targets.items():
            print(f"  {k}: {'/'.join(v)}")

        intl_orig = extract_file(f_src, find_node(header, targets["intl"]), base_offset).decode("utf-8")
        styles_orig = extract_file(f_src, find_node(header, targets["styles"]), base_offset).decode("utf-8")
        usage_orig = extract_file(f_src, find_node(header, targets["usage_parts"]), base_offset).decode("utf-8")
        menu_orig = extract_file(f_src, find_node(header, targets["menu"]), base_offset).decode("utf-8")
        main_orig = extract_file(f_src, find_node(header, targets["main"]), base_offset).decode("utf-8")
        html_orig = extract_file(f_src, find_node(header, targets["html"]), base_offset).decode("utf-8")

    print("Applying patches in memory...")
    intl_patched = patch_intl(intl_orig, tr_dict)
    styles_patched = patch_styles(styles_orig)
    usage_patched = patch_usage_parts(usage_orig)
    menu_patched = patch_menu(menu_orig)
    main_patched = patch_main(main_orig)
    html_patched = patch_html(html_orig)

    modified_files = {
        "/".join(targets["intl"]): intl_patched.encode("utf-8"),
        "/".join(targets["styles"]): styles_patched.encode("utf-8"),
        "/".join(targets["usage_parts"]): usage_patched.encode("utf-8"),
        "/".join(targets["menu"]): menu_patched.encode("utf-8"),
        "/".join(targets["main"]): main_patched.encode("utf-8"),
        "/".join(targets["html"]): html_patched.encode("utf-8"),
    }

    rebuild_asar(ORIG_ASAR, PATCHED_ASAR, modified_files)

    print("\nVerifying rebuilt ASAR by reading back modified files...")
    with open(PATCHED_ASAR, "rb") as f_check:
        h_check, b_check, s_check = parse_asar_header(f_check)
        for k, v in targets.items():
            p_str = "/".join(v)
            node = find_node(h_check, v)
            assert node is not None, f"Node {p_str} not found in check!"
            data = extract_file(f_check, node, b_check)
            assert len(data) == len(modified_files[p_str]), f"Size mismatch for {p_str}"
            print(f"  Verified {k}: {len(data)} bytes")

    print("\n>>> REBUILD AND INTEGRITY VERIFICATION 100% SUCCESSFUL! <<<")

if __name__ == "__main__":
    main()
