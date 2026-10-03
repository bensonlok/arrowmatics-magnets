#!/usr/bin/env python3
"""Swap the WhatsApp/mobile number everywhere in one go.
Usage: python3 scripts/swap_whatsapp.py 60122112522 60196626522
(digits only, country code first; display forms '+60 12-211 2522' are derived for Malaysian mobiles)
Review `git diff` afterwards. Run only after the owner confirms the number."""
import sys, os, re
old, new = sys.argv[1], sys.argv[2]
def disp(d):  # 60122112522 -> +60 12-211 2522
    return "+%s %s-%s %s" % (d[:2], d[2:4], d[4:7], d[7:])
pairs = [(old, new), ("+" + old, "+" + new), (disp(old), disp(new))]
root = os.path.join(os.path.dirname(__file__), "..")
n = 0
for dp, dn, fn in os.walk(root):
    if any(x in dp for x in (".git", "node_modules")): continue
    for f in fn:
        if not f.endswith((".html", ".md", ".txt", ".js", ".py", ".json", ".toml")) or f == "swap_whatsapp.py": continue
        p = os.path.join(dp, f)
        s = open(p, errors="ignore").read(); o = s
        for a, b in pairs: s = s.replace(a, b)
        if s != o: open(p, "w").write(s); n += 1; print("updated", os.path.relpath(p, root))
print(n, "files updated")
