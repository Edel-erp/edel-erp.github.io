"""Builds Edel's three free tool pages (one folder each, index.html inside).

Run from the site root:  python3 -I _build/build_tools.py
Header, footer and <head> come from build_pages.py so every page matches.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import head, chrome_top, chrome_bottom, WA, SITE, e  # noqa: E402

TOOLS = [
    ("vat-calculator-ethiopia", "VAT calculator (15%)", "Add or remove 15% VAT in Birr"),
    ("invoice-template-ethiopia", "Free invoice template", "Fill in, print or save as PDF"),
    ("e-invoicing-checker", "Does e-invoicing apply to me?", "Check in 30 seconds"),
]

ETH_JS = r'''
  var ETH_MONTHS = ["መስከረም", "ጥቅምት", "ኅዳር", "ታኅሣሥ", "ጥር", "የካቲት", "መጋቢት", "ሚያዝያ", "ግንቦት", "ሰኔ", "ሐምሌ", "ነሐሴ", "ጳጉሜ"];
  function toEthiopian(d) {
    var jdn = Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000) + 2440588, E = 1723856;
    var r = (jdn - E) % 1461, n = (r % 365) + 365 * Math.floor(r / 1460);
    return { y: 4 * Math.floor((jdn - E) / 1461) + Math.floor(r / 365) - Math.floor(r / 1460), m: Math.floor(n / 30) + 1, d: (n % 30) + 1 };
  }
  function ethStr(d) { var t = toEthiopian(d); return ETH_MONTHS[t.m - 1] + " " + t.d + "፣ " + t.y; }
'''

COMMON_JS = r'''
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function birr(n, dec) { dec = dec == null ? 2 : dec; return "ETB " + (isFinite(n) ? n : 0).toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec }); }
  function num(v) { var t = String(v).replace(/[,\s]/g, ""); if (t === "") return 0; var x = Number(t); return isFinite(x) && x >= 0 ? x : NaN; }
  function ok(x) { return isFinite(x) ? x : 0; }
  document.addEventListener("input", function (ev) {
    var el = ev.target; if (!el.matches || !el.matches('input[inputmode="decimal"]')) return;
    var bad = isNaN(num(el.value)); el.classList.toggle("bad", bad); el.setAttribute("aria-invalid", bad ? "true" : "false");
  });
'''


BAD_CSS = "input.bad { border-color: #B3261E; background: #FBE7E5; } input.bad:focus { outline-color: #B3261E; }"

def ld_for(path, name, desc, faq):
    url = SITE + path + "/"
    return [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Edel", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Free tools", "item": SITE + "e-invoicing-checker/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "url": url, "description": desc,
         "applicationCategory": "BusinessApplication", "operatingSystem": "Web browser", "isAccessibleForFree": True,
         "inLanguage": ["en", "am"], "areaServed": {"@type": "Country", "name": "Ethiopia"},
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ETB"},
         "publisher": {"@type": "Organization", "name": "Edel Trading PLC", "url": SITE}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]


def page(path, crumb, title, desc, h1, am, lede, style, body, script, faq):
    style = style + BAD_CSS
    faq_html = "\n".join(f'        <details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>'
                         for i, (q, a) in enumerate(faq))
    others = "".join(f'<a href="../{p}/">{e(n)}<small>{e(s)}</small></a>' for p, n, s in TOOLS if p != path)
    others += '<a href="../e-invoicing-ethiopia/">E-invoicing guide<small>How it works, in plain words</small></a>'
    h = head(title, desc, path, ld_for(path, crumb, desc, faq))
    h = h.replace("</head>", f"<style>\n{style}\n</style>\n</head>", 1)
    return h + chrome_top("tools") + f'''<main>
  <div class="wrap crumbs no-print"><a href="../">Edel</a><span>›</span>Free tools<span>›</span>{e(crumb)}</div>
  <section class="page-hero no-print">
    <div class="wrap">
      <span class="kicker">Free tool · no sign-up</span>
      <h1>{e(h1)}</h1>
      <p class="am" lang="am">{e(am)}</p>
      <p class="lede">{e(lede)}</p>
    </div>
  </section>
{body}
  <section class="band soft no-print">
    <div class="wrap narrow">
      <h2>Questions</h2>
      <div class="faq">
{faq_html}
      </div>
    </div>
  </section>

  <section class="band no-print">
    <div class="wrap">
      <h2>More free tools</h2>
      <div class="related">{others}</div>
      <div class="cta-band" style="margin-top:40px">
        <h2>Need registered e-invoices?</h2>
        <p>Edel issues e-invoices approved by the Ministry of Revenues, with an official number and QR code on every sale. We set it up and train your staff.</p>
        <div class="btns"><a class="btn btn-gold" href="../#request">Request e-invoice</a><a class="btn btn-line" style="color:#fff;border-color:#55575C" href="https://wa.me/251960369445?text=Hello%20Edel%2C%20I%27d%20like%20to%20know%20more%20about%20e-invoicing%20for%20my%20business." target="_blank" rel="noopener">WhatsApp us</a></div>
      </div>
    </div>
  </section>
</main>
''' + chrome_bottom() + f"<script>\n(function () {{\n{script}\n}})();\n</script>\n</body>\n</html>\n"


# ------------------------------------------------------------------ 1. VAT calculator
VAT_STYLE = '''
.calc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items: start; }
@media (max-width: 820px) { .calc-grid { grid-template-columns: 1fr; } }
.seg { display: inline-flex; background: var(--soft); border: 1px solid var(--line); border-radius: 999px; padding: 4px; gap: 4px; max-width: 100%; }
@media (max-width: 480px) { .seg { display: flex; } .seg button { flex: 1; padding: 9px 8px; font-size: 13.5px; line-height: 1.2; } }
.seg button { border: 0; background: none; padding: 10px 14px; border-radius: 999px; font: 600 15px var(--body); color: var(--muted); cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--black); color: #fff; }
.big-in { font-size: 24px; font-weight: 700; padding: 14px 16px; }
.result { background: var(--black); color: #fff; border-radius: 16px; padding: 20px; display: grid; gap: 10px; }
.result .row { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; border-bottom: 1px solid #2A2C30; font-variant-numeric: tabular-nums; }
.result .row:last-of-type { border-bottom: 0; }
.result .row span { color: #B9BBBF; }
.result .total b { color: var(--gold); font-family: var(--display); font-size: 24px; }
.copy { justify-self: start; border: 1px solid #55575C; background: transparent; color: #fff; border-radius: 999px; padding: 8px 14px; font: 600 14px var(--body); cursor: pointer; }
.items { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.items th { text-align: left; font-size: 13px; color: var(--muted); font-weight: 600; padding: 6px 4px; }
.items td { padding: 4px; vertical-align: middle; }
.items td.n { text-align: right; white-space: nowrap; }
.items input { padding: 9px 10px; }
.items .del { border: 0; background: var(--soft); border-radius: 8px; width: 34px; height: 34px; cursor: pointer; font-size: 18px; color: var(--muted); }
.add-row { margin-top: 10px; border: 1.5px dashed var(--line); background: none; border-radius: 10px; padding: 10px 14px; font: 600 15px var(--body); cursor: pointer; width: 100%; }
.sum { margin-top: 14px; display: grid; gap: 6px; font-variant-numeric: tabular-nums; }
.sum div { display: flex; justify-content: space-between; gap: 10px; }
.sum b { white-space: nowrap; }
.sum .grand { font-weight: 700; font-size: 19px; border-top: 1px solid var(--line); padding-top: 8px; }
.items .q { width: 64px; } .items .p { width: 110px; }
@media (max-width: 520px) {
  .items thead { display: none; }
  .items, .items tbody { display: block; }
  .items tr { display: grid; grid-template-columns: 1fr 1fr 1.2fr 34px; gap: 6px; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--line); }
  .items td { padding: 0; min-width: 0; }
  .items td.desc { grid-column: 1 / -1; }
  .items .q, .items .p { width: 100%; }
  .items td.n { font-size: 14px; }
}
'''
VAT_BODY = '''  <section class="band" style="padding-top:8px">
    <div class="wrap calc-grid">
      <div class="card" style="display:grid;gap:16px">
        <h2 style="font-size:24px">One amount</h2>
        <div class="seg" role="group" aria-label="What do you want to do?">
          <button type="button" aria-pressed="true" data-mode="add">Add VAT to price</button>
          <button type="button" aria-pressed="false" data-mode="remove">Remove VAT from total</button>
        </div>
        <div class="field"><label for="amt" id="amt-label">Price before VAT (ETB)</label>
          <input id="amt" class="big-in" inputmode="decimal" autocomplete="off" placeholder="e.g. 2,000" value="2000"></div>
        <div class="result" aria-live="polite">
          <div class="row"><span>Price before VAT</span><b id="r-net">ETB 0.00</b></div>
          <div class="row"><span>VAT 15%</span><b id="r-vat">ETB 0.00</b></div>
          <div class="row total"><span>Total with VAT</span><b id="r-gross">ETB 0.00</b></div>
          <button type="button" class="copy" id="copy">Copy result</button>
        </div>
        <p class="note">VAT-registered businesses charge 15% VAT. Check exemptions for your goods with the Ministry of Revenues.</p>
      </div>
      <div class="card">
        <h2 style="font-size:24px;margin-bottom:10px">Several items</h2>
        <table class="items">
          <thead><tr><th class="desc">Item</th><th>Qty</th><th>Unit price</th><th class="n">Amount</th><th><span class="sr" style="position:absolute;left:-9999px">Remove</span></th></tr></thead>
          <tbody id="rows"></tbody>
        </table>
        <button type="button" class="add-row" id="add">+ Add item</button>
        <div class="sum" aria-live="polite">
          <div><span>Subtotal (before VAT)</span><b id="s-net">ETB 0.00</b></div>
          <div><span>VAT 15%</span><b id="s-vat">ETB 0.00</b></div>
          <div class="grand"><span>Total with VAT</span><b id="s-gross">ETB 0.00</b></div>
        </div>
      </div>
    </div>
  </section>
'''
VAT_JS = COMMON_JS + r'''
  var VAT = 0.15, mode = "add", amt = document.getElementById("amt");
  function round2(x) { return Math.round(x * 100) / 100; }
  function calc() {
    var v = ok(num(amt.value)), net, vat, gross;
    if (mode === "add") { net = v; vat = round2(v * VAT); gross = round2(net + vat); }
    else { gross = v; net = round2(v / (1 + VAT)); vat = round2(gross - net); }
    document.getElementById("r-net").textContent = birr(net);
    document.getElementById("r-vat").textContent = birr(vat);
    document.getElementById("r-gross").textContent = birr(gross);
    return { net: net, vat: vat, gross: gross };
  }
  document.querySelectorAll("[data-mode]").forEach(function (b) {
    b.addEventListener("click", function () {
      mode = b.dataset.mode;
      document.querySelectorAll("[data-mode]").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      document.getElementById("amt-label").textContent = mode === "add" ? "Price before VAT (ETB)" : "Total with VAT (ETB)";
      calc();
    });
  });
  amt.addEventListener("input", calc);
  document.getElementById("copy").addEventListener("click", function (ev) {
    var r = calc(), btn = ev.currentTarget;
    var t = "Price before VAT: " + birr(r.net) + "\nVAT 15%: " + birr(r.vat) + "\nTotal with VAT: " + birr(r.gross);
    var done = function () { btn.textContent = "Copied ✓"; setTimeout(function () { btn.textContent = "Copy result"; }, 1800); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () { btn.textContent = "Copy not allowed"; });
    else btn.textContent = "Copy not allowed";
  });
  calc();

  var rows = document.getElementById("rows");
  function addRow(d, q, p) {
    var tr = document.createElement("tr");
    tr.innerHTML = '<td class="desc"><input aria-label="Item" placeholder="Item" value="' + esc(d || "") + '"></td>' +
      '<td><input class="q" aria-label="Quantity" inputmode="decimal" value="' + esc(q == null ? 1 : q) + '"></td>' +
      '<td><input class="p" aria-label="Unit price" inputmode="decimal" value="' + esc(p == null ? "" : p) + '"></td>' +
      '<td class="n" data-amt>ETB 0.00</td><td><button type="button" class="del" aria-label="Remove item">×</button></td>';
    rows.appendChild(tr); sum();
  }
  function sum() {
    var net = 0;
    rows.querySelectorAll("tr").forEach(function (tr) {
      var ins = tr.querySelectorAll("input"), a = round2(ok(num(ins[1].value)) * ok(num(ins[2].value)));
      tr.querySelector("[data-amt]").textContent = birr(a); net += a;
    });
    net = round2(net); var vat = round2(net * VAT);
    document.getElementById("s-net").textContent = birr(net);
    document.getElementById("s-vat").textContent = birr(vat);
    document.getElementById("s-gross").textContent = birr(net + vat);
  }
  rows.addEventListener("input", sum);
  rows.addEventListener("click", function (ev) { var b = ev.target.closest(".del"); if (b) { b.closest("tr").remove(); sum(); } });
  document.getElementById("add").addEventListener("click", function () { addRow("", 1, ""); });
  addRow("Teff flour 25kg", 4, 3250); addRow("Sunflower oil 5L", 6, 1180);
'''
VAT_FAQ = [
    ("How do I calculate 15% VAT in Ethiopia?", "Multiply the price before VAT by 0.15 to get the VAT, then add it to the price. For example, ETB 2,000 + 15% VAT (ETB 300) = ETB 2,300."),
    ("How do I remove VAT from a total?", "Divide the total by 1.15 to get the price before VAT. The difference is the VAT. For example, ETB 1,150 ÷ 1.15 = ETB 1,000, so the VAT is ETB 150."),
    ("Does every business charge VAT?", "VAT-registered businesses charge 15% VAT. Some goods and services are exempt, and businesses that are not VAT-registered pay turnover tax instead. Check your situation with the Ministry of Revenues."),
]

# ------------------------------------------------------------------ 2. Invoice template
INV_STYLE = '''
.inv-grid { display: grid; grid-template-columns: 1fr 1.05fr; gap: 18px; align-items: start; }
@media (max-width: 900px) { .inv-grid { grid-template-columns: 1fr; } }
.banner { background: var(--gold-soft); border: 1px solid #EADFBF; border-radius: 14px; padding: 14px 16px; font-size: 15px; margin-bottom: 18px; }
.banner a { font-weight: 700; }
fieldset { border: 1px solid var(--line); border-radius: 14px; padding: 14px; display: grid; gap: 10px; margin: 0; }
legend { font-weight: 700; padding: 0 6px; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 480px) { .two { grid-template-columns: 1fr; } }
.irow { display: grid; grid-template-columns: 1fr 60px 100px 34px; gap: 6px; align-items: center; }
.irow .del { border: 0; background: var(--soft); border-radius: 8px; height: 38px; cursor: pointer; font-size: 18px; color: var(--muted); }
.add-row { border: 1.5px dashed var(--line); background: none; border-radius: 10px; padding: 10px; font: 600 15px var(--body); cursor: pointer; }
.check { display: flex; gap: 8px; align-items: center; font-weight: 600; }
.check input { width: auto; }
.preview-wrap { position: sticky; top: 92px; display: grid; gap: 12px; }
.invoice { background: #fff; border: 1px solid var(--line); border-top: 6px solid var(--gold); border-radius: 10px; padding: 24px; font-size: 14px; box-shadow: 0 30px 60px -30px rgba(14,15,16,.35); overflow-wrap: anywhere; }
.invoice .top { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.invoice h2 { font-size: 22px; margin: 0 0 2px; }
.invoice .muted { color: var(--muted); }
.invoice table { width: 100%; border-collapse: collapse; margin-top: 16px; font-variant-numeric: tabular-nums; }
.invoice th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); border-bottom: 1.5px solid var(--ink); padding: 6px 4px; }
.invoice td { padding: 7px 4px; border-bottom: 1px solid #EEECE6; }
.invoice .n { text-align: right; white-space: nowrap; }
.invoice .tot { margin-top: 12px; margin-left: auto; width: min(280px, 100%); display: grid; gap: 4px; font-variant-numeric: tabular-nums; }
.invoice .tot div { display: flex; justify-content: space-between; }
.invoice .tot .grand { font-weight: 700; font-size: 17px; border-top: 1.5px solid var(--ink); padding-top: 6px; }
.invoice .plain { margin-top: 18px; font-size: 11.5px; color: var(--muted); border-top: 1px dashed var(--line); padding-top: 8px; }
@media print {
  body * { visibility: hidden !important; }
  #invoice, #invoice * { visibility: visible !important; }
  #invoice { position: absolute; left: 0; top: 0; width: 100%; box-shadow: none; border: 0; border-top: 6px solid #D3A628; }
  .page-hero, .crumbs { display: none !important; }
}
'''
INV_BODY = '''  <section class="band" style="padding-top:8px">
    <div class="wrap">
      <div class="banner no-print">This is a plain invoice, not a registered e-invoice. Registered e-invoices with an official number and QR code come from an approved system like Edel. <a href="../#request">Request e-invoice →</a></div>
      <div class="inv-grid">
        <form class="card no-print" id="inv-form" style="display:grid;gap:14px" onsubmit="return false">
          <fieldset><legend>Your business (seller)</legend>
            <div class="field"><label for="s-name">Business name</label><input id="s-name" value="Abyssinia Grocers PLC"></div>
            <div class="two"><div class="field"><label for="s-tin">TIN</label><input id="s-tin" inputmode="numeric" value="0012345678"></div>
            <div class="field"><label for="s-phone">Phone</label><input id="s-phone" value="+251 911 000000"></div></div>
            <div class="field"><label for="s-addr">Address</label><input id="s-addr" value="Bole, Addis Ababa"></div>
          </fieldset>
          <fieldset><legend>Customer (buyer)</legend>
            <div class="two"><div class="field"><label for="b-name">Customer name</label><input id="b-name" value="Meskerem Trading PLC"></div>
            <div class="field"><label for="b-tin">Customer TIN</label><input id="b-tin" inputmode="numeric" value=""></div></div>
          </fieldset>
          <fieldset><legend>Invoice</legend>
            <div class="two"><div class="field"><label for="i-no">Invoice number</label><input id="i-no" value="INV-0001"></div>
            <div class="field"><label for="i-date">Date</label><input id="i-date" type="date"></div></div>
            <div id="items" style="display:grid;gap:6px"></div>
            <button type="button" class="add-row" id="add">+ Add item</button>
            <label class="check" for="vat-on"><input type="checkbox" id="vat-on" checked> Add VAT 15%</label>
            <div class="field"><label for="i-notes">Notes</label><textarea id="i-notes" rows="2">Payment within 15 days. Thank you for your business.</textarea></div>
          </fieldset>
        </form>
        <div class="preview-wrap">
          <article class="invoice" id="invoice" aria-label="Invoice preview"></article>
          <div class="btns no-print"><button type="button" class="btn btn-gold" id="print">Print or save as PDF</button></div>
          <p class="note no-print">Tip: in the print window, choose "Save as PDF" to send it by email or Telegram.</p>
        </div>
      </div>
    </div>
  </section>
'''
INV_JS = COMMON_JS + ETH_JS + r'''
  var $ = function (id) { return document.getElementById(id); };
  var items = $("items");
  var d0 = new Date(); $("i-date").value = d0.getFullYear() + "-" + String(d0.getMonth() + 1).padStart(2, "0") + "-" + String(d0.getDate()).padStart(2, "0");
  function addItem(d, q, p) {
    var row = document.createElement("div"); row.className = "irow";
    row.innerHTML = '<input aria-label="Item description" placeholder="Item" value="' + esc(d || "") + '">' +
      '<input aria-label="Quantity" inputmode="decimal" value="' + esc(q == null ? 1 : q) + '">' +
      '<input aria-label="Unit price" inputmode="decimal" placeholder="Price" value="' + esc(p == null ? "" : p) + '">' +
      '<button type="button" class="del" aria-label="Remove item">×</button>';
    items.appendChild(row); render();
  }
  function render() {
    var lines = [], net = 0;
    items.querySelectorAll(".irow").forEach(function (r) {
      var i = r.querySelectorAll("input"), q = ok(num(i[1].value)), p = ok(num(i[2].value)), a = Math.round(q * p * 100) / 100;
      if (i[0].value.trim() || a) { lines.push({ d: i[0].value, q: q, p: p, a: a }); net += a; }
    });
    net = Math.round(net * 100) / 100;
    var vatOn = $("vat-on").checked, vat = vatOn ? Math.round(net * 15) / 100 : 0;
    var dt = $("i-date").value ? new Date($("i-date").value + "T12:00:00") : new Date();
    var greg = dt.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
    var plain = function (n) { return n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
    $("invoice").innerHTML =
      '<div class="top"><div><h2>' + esc($("s-name").value || "Your business") + '</h2><div class="muted">' + esc($("s-addr").value) +
      (($("s-phone").value) ? '<br>' + esc($("s-phone").value) : "") + (($("s-tin").value) ? '<br>TIN ' + esc($("s-tin").value) : "") + '</div></div>' +
      '<div style="text-align:right"><b style="font-size:18px">' + (vatOn ? "TAX INVOICE" : "INVOICE") + '</b><div class="muted">No ' + esc($("i-no").value) +
      '<br>' + esc(ethStr(dt)) + ' ዓ.ም<br>' + esc(greg) + '</div></div></div>' +
      '<div style="margin-top:16px"><span class="muted">Bill to</span><br><b>' + esc($("b-name").value || "Customer") + '</b>' +
      (($("b-tin").value) ? '<br><span class="muted">TIN ' + esc($("b-tin").value) + '</span>' : "") + '</div>' +
      '<table><thead><tr><th>Item</th><th class="n">Qty</th><th class="n">Unit price</th><th class="n">Amount</th></tr></thead><tbody>' +
      (lines.length ? lines.map(function (l) { return '<tr><td>' + esc(l.d) + '</td><td class="n">' + esc(l.q) + '</td><td class="n">' + plain(l.p) + '</td><td class="n">' + plain(l.a) + '</td></tr>'; }).join("")
        : '<tr><td colspan="4" class="muted">Add items on the left.</td></tr>') +
      '</tbody></table><div class="tot"><div><span>Subtotal</span><span>' + plain(net) + '</span></div>' +
      (vatOn ? '<div><span>VAT 15%</span><span>' + plain(vat) + '</span></div>' : "") +
      '<div class="grand"><span>TOTAL ETB</span><span>' + plain(net + vat) + '</span></div></div>' +
      (($("i-notes").value.trim()) ? '<p style="margin-top:14px">' + esc($("i-notes").value).replace(/\n/g, "<br>") + '</p>' : "") +
      '<div class="plain">Plain invoice made with the free Edel template. Not a registered e-invoice.</div>';
  }
  $("inv-form").addEventListener("input", render);
  $("inv-form").addEventListener("change", render);
  items.addEventListener("click", function (ev) { var b = ev.target.closest(".del"); if (b) { b.closest(".irow").remove(); render(); } });
  $("add").addEventListener("click", function () { addItem("", 1, ""); });
  $("print").addEventListener("click", function () { window.print(); });
  addItem("Teff flour, 25kg bag", 20, 3250); addItem("Sunflower oil, 5L", 36, 1180);
'''
INV_FAQ = [
    ("Is this invoice valid for the Ministry of Revenues?", "It is a plain invoice. Businesses that must use electronic invoicing need registered e-invoices from an approved system, which carry an official number and QR code. Edel issues those."),
    ("What should an invoice in Ethiopia show?", "At least the seller's name, address and TIN, the buyer's name (and TIN for business customers), an invoice number, the date, each item with quantity and price, and the VAT if you are VAT-registered."),
    ("How do I save it as a PDF?", "Press 'Print or save as PDF', then choose 'Save as PDF' as the printer. You can then send it by email, WhatsApp or Telegram."),
]

# ------------------------------------------------------------------ 3. E-invoicing checker
CHK_STYLE = '''
.quiz { max-width: 720px; margin: 0 auto; }
.prog { height: 8px; background: var(--soft); border-radius: 999px; overflow: hidden; margin-bottom: 18px; }
.prog i { display: block; height: 100%; background: var(--gold); transition: width .3s ease; }
.qnum { font-size: 13px; font-weight: 700; color: var(--gold-deep); letter-spacing: .06em; text-transform: uppercase; }
.quiz h2 { font-size: clamp(22px, 3vw, 30px); margin: 6px 0 16px; }
.opts { display: grid; gap: 10px; }
.opts.grid2 { grid-template-columns: 1fr 1fr; }
@media (max-width: 520px) { .opts.grid2 { grid-template-columns: 1fr; } }
.opts button { text-align: left; border: 1.5px solid var(--line); background: var(--glass), #121214; color: var(--ink); border-radius: 14px; padding: 15px 16px; font: 600 16px var(--body); cursor: pointer; display: flex; justify-content: space-between; gap: 10px; transition: border-color .15s, transform .15s; }
.opts button:hover, .opts button:focus-visible { border-color: var(--gold); transform: translateY(-1px); outline: none; }
.opts button span { color: var(--gold-deep); }
.back { margin-top: 14px; border: 0; background: none; color: var(--muted); font: 600 14px var(--body); cursor: pointer; padding: 6px 0; }
.res { display: grid; gap: 16px; }
.res .pill { justify-self: start; background: var(--black); color: #fff; border-radius: 999px; padding: 6px 12px; font-weight: 700; font-size: 14px; }
.res .timing { background: var(--gold-soft); border: 1px solid #EADFBF; border-radius: 14px; padding: 16px; }
.res ul { padding-left: 20px; display: grid; gap: 6px; }
.res .disclaimer { font-size: 14px; color: var(--muted); border-left: 3px solid var(--gold); padding-left: 10px; }
'''
CHK_BODY = '''  <section class="band" style="padding-top:8px">
    <div class="wrap">
      <div class="card quiz" id="quiz" aria-live="polite"></div>
    </div>
  </section>
'''
CHK_JS = COMMON_JS + r'''
  var WA = "''' + WA + r'''";
  var Q = [
    { k: "vat", q: "Is your business VAT-registered?", o: [["Yes, we charge 15% VAT", "yes"], ["No, we pay turnover tax", "no"], ["Not sure", "unsure"]] },
    { k: "now", q: "How do you invoice today?", o: [["Cash register machine", "crm"], ["Paper receipt books", "paper"], ["Accounting software or Excel", "software"]] },
    { k: "br", q: "How many branches do you have?", o: [["One", "1"], ["2 to 5", "few"], ["More than 5", "many"]] },
    { k: "type", q: "What kind of business is it?", grid: true, o: [["Hotel or lodge", "hotel"], ["Beer or beverage distribution", "beer"], ["Tours and car rental", "tours"], ["Import or export", "import"], ["Manufacturing", "manufacturing"], ["Farm", "farms"], ["Shop or supermarket", "shop"], ["Restaurant or café", "restaurant"], ["Other", "other"]] }
  ];
  var NO_DEMO = { shop: true, other: true };
  var DEMO = { hotel: "hotel", restaurant: "hotel", beer: "beer", tours: "tours", import: "import", shop: "import", manufacturing: "manufacturing", farms: "farms", other: "hotel" };
  var quiz = document.getElementById("quiz"), A = {};
  function label(i, v) { var o = Q[i].o.filter(function (x) { return x[1] === v; })[0]; return o ? o[0] : v; }
  function step(i) {
    var pct = Math.round(i / Q.length * 100);
    if (i >= Q.length) return result();
    var q = Q[i];
    quiz.innerHTML = '<div class="prog" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><i style="width:' + pct + '%"></i></div>' +
      '<div class="qnum">Question ' + (i + 1) + ' of ' + Q.length + '</div><h2>' + esc(q.q) + '</h2>' +
      '<div class="opts' + (q.grid ? " grid2" : "") + '">' + q.o.map(function (o) { return '<button type="button" data-v="' + esc(o[1]) + '">' + esc(o[0]) + '<span aria-hidden="true">→</span></button>'; }).join("") + '</div>' +
      (i > 0 ? '<button type="button" class="back" id="back">← Back</button>' : "");
    quiz.querySelectorAll("[data-v]").forEach(function (b) { b.addEventListener("click", function () { A[q.k] = b.dataset.v; step(i + 1); }); });
    var bk = document.getElementById("back"); if (bk) bk.addEventListener("click", function () { step(i - 1); });
    var first = quiz.querySelector("[data-v]"); if (first && i > 0) first.focus({ preventScroll: true });
  }
  function result() {
    var rollout = "The Ministry of Revenues is rolling out electronic invoicing in phases, starting with larger and VAT-registered taxpayers.";
    var timing = A.vat === "yes" ? "As a VAT-registered business, you are likely in an early phase."
      : A.vat === "no" ? "As a turnover tax payer, you are likely in a later phase, so there is time to prepare."
      : "Check your TIN registration to see whether you are VAT-registered; we can help you confirm it.";
    var erp = A.br !== "1" || A.now === "software";
    var product = erp ? "Edel ERP" : "Edel E-Invoice";
    var why = erp ? (A.br !== "1" ? "With several branches, one system for invoices, stock and accounts saves the most time." : "You already use software, so moving your books into Edel avoids entering every sale twice.")
      : "A single branch can start with registered invoicing and add accounting later.";
    var prep = ["Your TIN certificate and trade licence", A.br === "1" ? "Your shop or office address" : "A list of branches with their addresses",
      A.now === "crm" ? "Your items and prices, and your cash register's last Z-report" : A.now === "paper" ? "Your items and prices, from a recent receipt book" : "An export of your items, prices and customers from your software"];
    var msg = "Hello Edel, I used the e-invoicing checker.\nVAT-registered: " + label(0, A.vat) + "\nInvoicing today: " + label(1, A.now) +
      "\nBranches: " + label(2, A.br) + "\nBusiness type: " + label(3, A.type) + "\nSuggested: " + product;
    quiz.innerHTML = '<div class="prog"><i style="width:100%"></i></div><div class="res">' +
      '<span class="pill">Suggested setup: ' + esc(product) + '</span>' +
      '<h2 style="margin:0">Your result</h2>' +
      '<div class="timing"><p>' + esc(rollout) + '</p><p style="margin-top:8px"><b>' + esc(timing) + '</b></p></div>' +
      '<div><h3 style="font-size:19px;margin-bottom:8px">What to prepare</h3><ul>' + prep.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + '</ul></div>' +
      '<div><h3 style="font-size:19px;margin-bottom:6px">Why ' + esc(product) + '</h3><p>' + esc(why) + '</p></div>' +
      '<div class="btns"><a class="btn btn-gold" href="https://wa.me/' + WA + '?text=' + encodeURIComponent(msg) + '" target="_blank" rel="noopener" id="wa">Send my answers on WhatsApp</a>' +
      (NO_DEMO[A.type || "other"] ? '<a class="btn btn-line" href="../" id="demo">See a registered invoice</a></div>' : '<a class="btn btn-line" href="../demo/' + DEMO[A.type] + '.html" id="demo">See the demo for my industry</a></div>') +
      '<p class="disclaimer">This is general guidance, not legal advice. Confirm your phase with the Ministry of Revenues.</p>' +
      '<button type="button" class="back" id="again">↺ Start again</button></div>';
    document.getElementById("again").addEventListener("click", function () { A = {}; step(0); });
  }
  step(0);
'''
CHK_FAQ = [
    ("Does e-invoicing apply to my business?", "The Ministry of Revenues is rolling out electronic invoicing in phases, starting with larger and VAT-registered taxpayers. Others follow in later phases. Use the checker above, and confirm your phase with the Ministry of Revenues."),
    ("What do I need to prepare?", "Your TIN certificate and trade licence, the addresses of your branches, and your list of items and prices. If you use a cash register or software, its reports make setup faster."),
    ("Can I keep my current cash register or receipt books?", "Registered e-invoices must come from an approved system. Edel runs in a web browser on the computers, tablets and phones you already have, and can print on your existing receipt printer."),
]

PAGES = [
    dict(path="vat-calculator-ethiopia", crumb="VAT calculator",
         title="VAT Calculator Ethiopia (15%): Add or Remove VAT in Birr | Edel",
         desc="Free 15% VAT calculator for Ethiopia. Add VAT to a price or remove it from a total, in Birr, and add up several items with VAT. No sign-up.",
         h1="VAT calculator for Ethiopia (15%)", am="የተጨማሪ እሴት ታክስ (ተ.እ.ታ) 15% ማስያ",
         lede="Add 15% VAT to a price, or take it out of a total, instantly in Birr. Add up several items below.",
         style=VAT_STYLE, body=VAT_BODY, script=VAT_JS, faq=VAT_FAQ),
    dict(path="invoice-template-ethiopia", crumb="Invoice template",
         title="Free Invoice Template for Ethiopian Businesses (Birr, VAT, TIN) | Edel",
         desc="Free invoice template for Ethiopia: seller and buyer TIN, Ethiopian and Gregorian date, items in Birr, 15% VAT. Fill it in, then print or save as PDF.",
         h1="Free invoice template for Ethiopian businesses", am="ለኢትዮጵያ ንግዶች ነፃ የደረሰኝ ቅፅ",
         lede="Fill in your details and items. The invoice updates as you type, with the Ethiopian and Gregorian date, then print it or save it as a PDF.",
         style=INV_STYLE, body=INV_BODY, script=INV_JS, faq=INV_FAQ),
    dict(path="e-invoicing-checker", crumb="E-invoicing checker",
         title="Does E-Invoicing Apply to My Business? Free Ethiopia Checker | Edel",
         desc="Answer 4 quick questions to see what Ethiopia's electronic invoicing rollout likely means for your business, what to prepare, and which setup fits.",
         h1="Does e-invoicing apply to my business?", am="ኤሌክትሮኒክ ደረሰኝ ንግዴን ይመለከታል? በ30 ሰከንድ ያረጋግጡ",
         lede="Check in 30 seconds. Answer four questions and see what electronic invoicing likely means for you and what to prepare.",
         style=CHK_STYLE, body=CHK_BODY, script=CHK_JS, faq=CHK_FAQ),
]

if __name__ == "__main__":
    for p in PAGES:
        os.makedirs(p["path"], exist_ok=True)
        with open(os.path.join(p["path"], "index.html"), "w", encoding="utf-8") as f:
            f.write(page(**p))
        print("wrote", p["path"])
