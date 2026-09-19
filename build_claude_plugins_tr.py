# -*- coding: utf-8 -*-
"""
build_claude_plugins_tr.py
Birleştirir, doğrular ve claude_plugins_tr.json dosyasını üretir.
"""

import os
import json
import sys

from tr_part1 import PART1
from tr_part2 import PART2
from tr_part3 import PART3
from tr_part4 import PART4
from tr_part5 import PART5
from tr_part6 import PART6

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    en_path = os.path.join(base_dir, "claude_plugins_en.json")
    tr_path = os.path.join(base_dir, "claude_plugins_tr.json")

    with open(en_path, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    merged = {}
    parts = [PART1, PART2, PART3, PART4, PART5, PART6]
    for p in parts:
        merged.update(p)

    print(f"Toplam İngilizce Eklenti Sayısı: {len(en_data)}")
    print(f"Toplam Türkçe Çevrilen Eklenti: {len(merged)}")

    # Eksik olan anahtarları kontrol et
    missing_keys = set(en_data.keys()) - set(merged.keys())
    if missing_keys:
        print(f"[UYARI] Eksik anahtarlar ({len(missing_keys)} adet): {missing_keys}")
    else:
        print("[BAŞARILI] 291 eklentinin tamamı eksiksiz çevrildi!")

    extra_keys = set(merged.keys()) - set(en_data.keys())
    if extra_keys:
        print(f"[UYARI] Fazla anahtarlar ({len(extra_keys)} adet): {extra_keys}")

    # Boş veya hatalı karakter kontrolü
    for k, v in merged.items():
        if not v or not v.strip():
            print(f"[HATA] Boş çeviri: {k}")
        if "\ufffd" in v:
            print(f"[HATA] Bozuk karakter (ufffd): {k}")

    with open(tr_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"[KAYDEDİLDİ] {tr_path} (Boyut: {os.path.getsize(tr_path)} bayt)")

if __name__ == "__main__":
    main()
