# -*- coding: utf-8 -*-
import os
import zlib
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dict_path = os.path.join(BASE_DIR, "tr_dictionary_zcode.json")
with open(dict_path, "rb") as f:
    raw_dict = f.read()
b64_dict = base64.b64encode(zlib.compress(raw_dict, 9)).decode("ascii")
with open(os.path.join(BASE_DIR, "tr_dict_b64.txt"), "w", encoding="ascii") as f:
    f.write(b64_dict)

claude_path = os.path.join(BASE_DIR, "claude_plugins_tr.json")
with open(claude_path, "rb") as f:
    raw_claude = f.read()
b64_claude = base64.b64encode(zlib.compress(raw_claude, 9)).decode("ascii")
with open(os.path.join(BASE_DIR, "claude_tr_b64.txt"), "w", encoding="ascii") as f:
    f.write(b64_claude)

template_path = os.path.join(BASE_DIR, "single_click_template.py")
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

final = template.replace("__B64_DATA__", b64_dict).replace("__CLAUDE_B64_DATA__", b64_claude)

target = os.path.join(BASE_DIR, "single_click_patcher.py")
with open(target, "w", encoding="utf-8") as f:
    f.write(final)

print("single_click_patcher.py generated successfully!")
print("Size:", os.path.getsize(target), "bytes")

