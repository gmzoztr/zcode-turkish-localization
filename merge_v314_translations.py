# -*- coding: utf-8 -*-
"""
merge_v314_translations.py
Merges all 756 new v3.14.0 translations and updater fixes into tr_dictionary_zcode.json.
"""

import json
import os
import sys

from v314_part1_onboarding_and_small import PART1_TR
from v314_part2_settings import PART2_TR
from v314_part3_workflows import PART3_TR
from v314_part4_chat_general import PART4_TR
from v314_part5_chat_toolcalls_1 import PART5_TR
from v314_part6_chat_toolcalls_2 import PART6_TR

DICT_PATH = "tr_dictionary_zcode.json"

with open(DICT_PATH, "r", encoding="utf-8") as f:
    tr_dict = json.load(f)

print(f"Original dictionary keys: {len(tr_dict)}")

all_new = {}
all_new.update(PART1_TR)
all_new.update(PART2_TR)
all_new.update(PART3_TR)
all_new.update(PART4_TR)
all_new.update(PART5_TR)
all_new.update(PART6_TR)

# Updater dialog fixes
all_new["updateDialog.downloadProgress"] = "İndirme İlerlemesi"
all_new["updateDialog.cancelDownload"] = "İndirmeyi İptal Et"
all_new["updateDialog.restartToUpdate"] = "Yeniden Başlat ve Güncelle"
all_new["updateDialog.downloadAndUpdate"] = "Güncellemeyi İndir"

# Merge
for k, v in all_new.items():
    tr_dict[k] = v

print(f"Total merged keys: {len(all_new)}")
print(f"Updated dictionary keys: {len(tr_dict)}")

with open(DICT_PATH, "w", encoding="utf-8") as f:
    json.dump(tr_dict, f, ensure_ascii=False, indent=2)

print("Saved updated tr_dictionary_zcode.json successfully.")
