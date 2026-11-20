"""Put the two real next steps (free trial, Microsoft Store) at the very top of each product home page,
so a visitor sees them without scrolling. python home_action_strip.py [--apply]"""
import pathlib, sys
ROOT = pathlib.Path(r"C:\Users\17209\Projects")
SITES = {
    "getsublimit.com": dict(days=30, trial="/start.html?utm_source=home&utm_medium=strip", store="9N6GJSH3J8BD", cid="sl-home-strip", bg="#173f2c"),
    "getleafledger.com": dict(days=30, trial="https://license.getleafledger.com/trial", store="9NJJJJMSLD2W", cid="ll-home-strip", bg="#0b211b"),
    "getstockstart.com": dict(days=14, trial="https://app.getstockstart.com/signup?utm_source=home&utm_medium=strip", store="9PK7HXBCMQW8", cid="ss-home-strip", bg="#173f2c"),
    "getsaleledger.com": dict(days=30, trial="https://license.getsaleledger.com/trial", store="9N46593KX9HK", cid="sd-home-strip", bg="#1f2a24"),
}
MARK = "ppg-home-strip"
TEMPLATE = ('<div id="ppg-home-strip" style="background:{bg};color:#fff;font:600 15px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;'
            'padding:10px 16px;text-align:center;display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:center;align-items:center">'
            '<span>Free {days}-day trial. No card, no automatic charge.</span>'
            '<a href="{trial}" style="background:#fff;color:{bg};padding:7px 14px;border-radius:6px;text-decoration:none;font-weight:700">Start free trial</a>'
            '<a href="https://apps.microsoft.com/detail/{store}?mode=direct&amp;cid={cid}" style="color:#fff;text-decoration:underline;text-underline-offset:3px">or get it from the Microsoft Store</a></div>')
apply = "--apply" in sys.argv
for s, cfg in SITES.items():
    p = ROOT / s / "index.html"
    t = p.read_text(encoding="utf-8")
    if MARK in t:
        print(s, "already has the strip"); continue
    assert t.count("<body>") == 1, s
    t = t.replace("<body>", "<body>" + TEMPLATE.format(**cfg), 1)
    print(s, "strip added" if apply else "would add strip")
    if apply:
        p.write_text(t, encoding="utf-8", newline="")
