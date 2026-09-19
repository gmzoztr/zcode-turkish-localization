# -*- coding: utf-8 -*-
import os

with open(r"C:\Users\Work-D\ZCodeProject\tr_dict_b64.txt", "r", encoding="ascii") as f:
    b64 = f.read().strip()

with open(r"C:\Users\Work-D\ZCodeProject\claude_tr_b64.txt", "r", encoding="ascii") as f:
    claude_b64 = f.read().strip()

with open(r"C:\Users\Work-D\ZCodeProject\single_click_template.py", "r", encoding="utf-8") as f:
    template = f.read()

final = template.replace("__B64_DATA__", b64).replace("__CLAUDE_B64_DATA__", claude_b64)

target = r"C:\Users\Work-D\ZCodeProject\single_click_patcher.py"
with open(target, "w", encoding="utf-8") as f:
    f.write(final)

print("single_click_patcher.py generated successfully!")
print("Size:", os.path.getsize(target), "bytes")
