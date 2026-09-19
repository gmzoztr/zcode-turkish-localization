# -*- coding: utf-8 -*-
"""
analyze_zcode_update.py
ZCode güncellendiğinde yeni app.asar dosyasını inceler:
- Sürüm numarasını tespit eder
- Yeni eklenen veya değişen metinleri bulur
- Çeviri sözlüğümüzdeki eksikleri raporlar
"""

import os
import sys
import json
import struct
import re

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"C:\Users\Work-D\ZCodeProject"
ZCODE_RESOURCES = r"C:\Program Files\ZCode\resources"
CURRENT_ASAR = os.path.join(ZCODE_RESOURCES, "app.asar")
DICT_PATH = os.path.join(BASE_DIR, "tr_dictionary_zcode.json")

def parse_asar_header(f):
    header_raw = f.read(16)
    u1, str_len, u2, json_len = struct.unpack("<IIII", header_raw)
    json_bytes = f.read(json_len)
    header = json.loads(json_bytes.decode("utf-8"))
    base_offset = 8 + str_len
    return header, base_offset

def extract_file(f_src, node, base_offset):
    offset = int(node["offset"])
    size = int(node["size"])
    f_src.seek(base_offset + offset)
    return f_src.read(size)

def find_node(header_json, path_parts):
    node = header_json
    for part in path_parts:
        if "files" not in node or part not in node["files"]:
            return None
        node = node["files"][part]
    return node

def main():
    print("=" * 60)
    print("ZCode Güncelleme Analiz Aracı")
    print("=" * 60)

    if not os.path.exists(CURRENT_ASAR):
        print(f"[-] Hata: {CURRENT_ASAR} bulunamadı!")
        return

    with open(CURRENT_ASAR, "rb") as f:
        header, base_offset = parse_asar_header(f)

        # 1. package.json sürüm tespiti
        pkg_node = find_node(header, ["package.json"])
        if pkg_node:
            pkg_data = json.loads(extract_file(f, pkg_node, base_offset).decode("utf-8"))
            print(f"[+] ZCode Sürümü: {pkg_data.get('version', 'Bilinmiyor')}")
            print(f"[+] Paket Adı: {pkg_data.get('name', 'Bilinmiyor')}")

        # 2. IntlProvider dosyasını bul
        renderer_assets = header.get("files", {}).get("out", {}).get("files", {}).get("renderer", {}).get("files", {}).get("assets", {}).get("files", {})
        intl_file = None
        styles_file = None
        for fname, fnode in renderer_assets.items():
            if fname.startswith("IntlProvider-") and fname.endswith(".js"):
                intl_file = fname
            elif fname.startswith("styles-") and fname.endswith(".js"):
                styles_file = fname

        print(f"[+] IntlProvider Dosyası: {intl_file}")
        print(f"[+] Styles Dosyası: {styles_file}")

        # 3. IntlProvider içindeki İngilizce/Çince stringleri incele
        if intl_file:
            intl_content = extract_file(f, renderer_assets[intl_file], base_offset).decode("utf-8", errors="ignore")
            # tr-TR eklenmiş mi kontrol et
            is_patched = '"tr-TR"' in intl_content or 'tr-TR' in intl_content
            print(f"[+] Canlı ASAR Durumu: {'YAMALI (Bizim Türkçe Sürüm)' if is_patched else 'ORİJİNAL / YENİ GÜNCELLEME'}")

            # Sözlük ile karşılaştır
            if os.path.exists(DICT_PATH):
                with open(DICT_PATH, "r", encoding="utf-8") as df:
                    tr_dict = json.load(df)

                # Anahtarları yakala (e.g., "key":"value")
                matches = re.findall(r'"([^"\\]{2,60})":\s*"([^"\\]{1,200})"', intl_content)
                new_candidates = []
                for k, v in matches:
                    if k not in tr_dict and not k.startswith("http") and not k.startswith("/") and len(k) > 3:
                        new_candidates.append((k, v))

                print(f"[+] Sözlükteki Toplam Anahtar: {len(tr_dict)}")
                print(f"[+] Olası Yeni/Eksik Anahtarlar: {len(new_candidates)}")
                if new_candidates:
                    print("--- İlk 10 Yeni Anahtar ---")
                    for k, v in new_candidates[:10]:
                        print(f"  {k} => {v}")

    print("=" * 60)
    print("Analiz tamamlandı.")

if __name__ == "__main__":
    main()
