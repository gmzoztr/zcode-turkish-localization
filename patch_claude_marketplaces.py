# -*- coding: utf-8 -*-
"""
patch_claude_marketplaces.py
claude-plugins-official dizinindeki marketplace.json dosyalarını Türkçeleştirir.
Başlıkları (name, displayName) ASLA değiştirmez, sadece description ve description_i18n.tr alanlarını günceller.
"""

import os
import json
import sys

def patch_file(filepath, tr_dict):
    if not os.path.exists(filepath):
        print(f"[YOK] {filepath}")
        return 0

    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    updated_count = 0
    plugins = data.get("plugins", [])
    for pl in plugins:
        pname = pl.get("name")
        if pname in tr_dict:
            tr_desc = tr_dict[pname]
            # Başlıkları asla değiştirmiyoruz
            if pl.get("description") != tr_desc:
                pl["description"] = tr_desc
                if "description_i18n" not in pl or not isinstance(pl["description_i18n"], dict):
                    pl["description_i18n"] = {}
                pl["description_i18n"]["tr"] = tr_desc
                updated_count += 1

    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[TAMAMLANDI] {filepath} -> {updated_count}/{len(plugins)} eklenti açıklaması Türkçeleştirildi.")
    return updated_count

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tr_path = os.path.join(base_dir, "claude_plugins_tr.json")

    with open(tr_path, "r", encoding="utf-8") as f:
        tr_dict = json.load(f)

    targets = [
        r"C:\Users\Work-D\.zcode\cli\plugins\marketplaces\claude-plugins-official\marketplace.json",
        r"C:\Users\Work-D\.zcode\cli\plugins\marketplaces\claude-plugins-official\.claude-plugin\marketplace.json",
    ]

    for t in targets:
        patch_file(t, tr_dict)

if __name__ == "__main__":
    main()
