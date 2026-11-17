"""Tag every Microsoft Store link with a per-page campaign id and add a Store block to content pages.

python store_links.py [--apply]
"""
import re, sys, pathlib

ROOT = pathlib.Path(r"C:\Users\17209\Projects")
SITES = {
    "getsublimit.com": ("sl", "9N6GJSH3J8BD", "SubLimit"),
    "getleafledger.com": ("ll", "9NJJJJMSLD2W", "LeafLedger"),
    "getstockstart.com": ("ss", "9PK7HXBCMQW8", "StockStart"),
    "getsaleledger.com": ("sd", "9N46593KX9HK", "SaleLedger"),
}
SKIP = {"404", "licenses", "privacy", "refunds", "terms", "welcome"}
APPLY = "--apply" in sys.argv

BLOCK = ('<aside class="ms-store-cta" style="margin:40px 0 8px;padding:20px 22px;border:1px solid rgba(127,127,127,.35);'
         'border-radius:10px;display:flex;flex-wrap:wrap;gap:16px;align-items:center">'
         '<a href="https://apps.microsoft.com/detail/{id}?mode=direct&cid={cid}" rel="noopener">'
         '<img src="https://get.microsoft.com/images/en-us%20dark.svg" width="180" alt="Get {name} from the Microsoft Store"></a>'
         '<p style="margin:0;flex:1 1 260px">{name} is in the Microsoft Store. Microsoft checks and signs Store apps, '
         'so Windows installs it without an unknown-publisher warning.</p></aside>')

for site, (pre, sid, name) in SITES.items():
    for f in sorted((ROOT / site).glob("*.html")):
        if f.stem in SKIP and f.stem != "welcome" or f.name.startswith("google"):
            continue
        text = f.read_text(encoding="utf-8")
        cid = f"{pre}-{f.stem}"
        new = re.sub(r"(apps\.microsoft\.com/detail/[0-9A-Z]{12}\?mode=direct)(?!&cid)", rf"\1&cid={cid}", text)
        added = False
        anchor = "</main>" if "</main>" in new else "<footer"
        if "ms-store-cta" not in new and "vinext.navigationRuntime" not in new and f.stem not in SKIP \
                and f.stem != "index" and anchor in new and "apps.microsoft.com" not in text:
            blk = BLOCK.format(id=sid, cid=cid, name=name)
            if anchor == "<footer":
                blk = '<div class="wrap">' + blk + '</div>\n'
            new = new.replace(anchor, blk + anchor, 1)
            added = True
        if new != text:
            print(f"{site}/{f.name}: links tagged={len(re.findall('&cid=', new)) - len(re.findall('&cid=', text))} block={added}")
            if APPLY:
                f.write_text(new, encoding="utf-8")
