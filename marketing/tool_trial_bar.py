"""Add a dismissible "try it on your real records" bar to each free tool page.

The bar appears only after the visitor has used the tool (typed in a field or pressed a button),
so it follows the result instead of interrupting. python tool_trial_bar.py [--apply]
"""
import pathlib, sys

ROOT = pathlib.Path(r"C:\Users\17209\Projects")
PAGES = {
    "getsublimit.com/subcontracting-limit-calculator.html": dict(
        name="SubLimit", text="Track this for every contract and period from your own payment records.",
        trial="/start.html?utm_source=tool&utm_medium=bar", trial_label="Get SubLimit free for 30 days",
        store="9N6GJSH3J8BD", cid="sl-tool-bar", color="#173f2c"),
    "getleafledger.com/tobacco-rollforward-check.html": dict(
        name="LeafLedger", text="Run this for every product class and draft your TTB and FDA reports from your own records.",
        trial="https://license.getleafledger.com/trial", trial_label="Start the free 30-day trial",
        store="9NJJJJMSLD2W", cid="ll-tool-bar", color="#1d3b2a"),
    "getstockstart.com/pricebook-unit-cost-checker.html": dict(
        name="StockStart", text="Check a whole month of supplier invoices against your pricebook export.",
        trial="https://app.getstockstart.com/signup?utm_source=tool&utm_medium=bar", trial_label="Start the free 14-day trial",
        store="9PK7HXBCMQW8", cid="ss-tool-bar", color="#173f2c"),
    "getsaleledger.com/trust-account-check.html": dict(
        name="SaleLedger", text="Run this three-way check from your settlement export, QuickBooks file and bank statement every month.",
        trial="https://license.getsaleledger.com/trial", trial_label="Start the free 30-day trial",
        store="9N46593KX9HK", cid="sd-tool-bar", color="#1f2a24"),
}
MARK = "ppg-trial-bar"
TEMPLATE = """<div id="ppg-trial-bar" hidden style="position:fixed;left:12px;right:12px;bottom:12px;z-index:50;max-width:760px;margin:0 auto;background:{color};color:#fff;border-radius:12px;padding:14px 44px 14px 16px;box-shadow:0 6px 24px rgba(0,0,0,.25);font:15px/1.45 system-ui,sans-serif">
<button type="button" aria-label="Close" onclick="this.parentNode.hidden=true;try{{sessionStorage.setItem('ppgbar','x')}}catch(e){{}}" style="position:absolute;top:6px;right:8px;background:none;border:0;color:#fff;font-size:22px;cursor:pointer">&times;</button>
<strong>{text}</strong> No card needed.
<span style="display:inline-flex;flex-wrap:wrap;gap:10px;margin-top:8px;align-items:center"><a href="{trial}" style="background:#fff;color:{color};padding:8px 14px;border-radius:8px;font-weight:700;text-decoration:none">{trial_label}</a>
<a href="https://apps.microsoft.com/detail/{store}?mode=direct&cid={cid}" style="color:#fff">or get {name} from the Microsoft Store</a></span></div>
<script>(function(){{var b=document.getElementById('ppg-trial-bar');if(!b)return;var done=false;function used(){{try{{var k='pp_used_'+location.pathname;if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,'1');var u='';try{{u=(JSON.parse(localStorage.getItem('profitpin_lead')||'null')||{{}}).utm_source||''}}catch(e){{}}if(!/^(localhost|127\.)/.test(location.hostname))new Image().src='https://license.getsaleledger.com/growth/hit?'+new URLSearchParams({{s:location.hostname,p:'/tool-used'+location.pathname.replace(/\.html$/,''),f:'0',r:'',u:u,t:String(Date.now())}})}}catch(e){{}}}}function show(){{used();if(done)return;done=true;try{{if(sessionStorage.getItem('ppgbar'))return}}catch(e){{}}setTimeout(function(){{b.hidden=false}},2500)}}var m=document.querySelector('main')||document.body;var n=0;m.addEventListener('change',function(){{if(++n>=4)show()}});m.addEventListener('click',function(e){{if(e.target.closest('button'))show()}});}})();</script>
"""

apply = "--apply" in sys.argv
for rel, cfg in PAGES.items():
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    if MARK in t:
        print(rel, "already has the bar"); continue
    assert t.count("</body>") == 1, rel
    t = t.replace("</body>", TEMPLATE.format(**cfg) + "</body>")
    print(rel, "bar added" if apply else "would add bar")
    if apply:
        p.write_text(t, encoding="utf-8")
