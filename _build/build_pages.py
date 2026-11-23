"""Builds Edel's industry pages (one folder per page, index.html inside).

Run from the site root:  python3 -I _build/build_pages.py
Header and footer come from chrome(); other pages copy the same markup.
"""
import html, json, os
from urllib.parse import quote

SITE = "https://edel-erp.github.io/"
WA = "251960369445"
e = html.escape

INDUSTRY_LINKS = [
    ("hotel-software-ethiopia", "Hotels", "Rooms, restaurant, stores"),
    ("beer-distribution-software-ethiopia", "Beer distribution", "Trucks, crates, cash"),
    ("tour-company-software-ethiopia", "Tours & travel", "Bookings, cars, drivers"),
    ("import-export-software-ethiopia", "Import & export", "Shipments, landed cost"),
    ("manufacturing-erp-ethiopia", "Manufacturing", "Recipes, runs, cost per unit"),
    ("farm-management-software-ethiopia", "Farms", "Fields, harvest, workers"),
]
FREE_LINKS = [
    ("e-invoicing-ethiopia", "E-invoicing guide"),
    ("e-invoicing-checker", "Does e-invoicing apply to me?"),
    ("vat-calculator-ethiopia", "VAT calculator (15%)"),
    ("invoice-template-ethiopia", "Free invoice template"),
]
WA_LINK = "https://wa.me/251960369445?text=Hello%20Edel%2C%20I%27d%20like%20to%20know%20more%20about%20e-invoicing%20for%20my%20business."
WA_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 20.5l1.4-4.2A8.5 8.5 0 1 1 8 19.3z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.6-2-1-1 .9a4.5 4.5 0 0 1-2.3-2.3l.9-1-1-2z"/></svg>'


def head(title, desc, path, ld):
    url = SITE + path + "/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Edel">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}edel-logo-web.png">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=Noto+Sans+Ethiopic:wght@400;600&display=swap">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>
'''


def chrome_top(current=""):
    def cur(p): return ' aria-current="page"' if p == current else ""
    return f'''<header class="site">
  <div class="wrap nav">
    <a href="../"><img src="../edel-logo-web-360.webp" srcset="../edel-logo-web-360.webp 360w, ../edel-logo-web.webp 720w" sizes="128px" width="720" height="338" alt="Edel: e-invoicing software for Ethiopia"></a>
    <nav aria-label="Main" id="main-nav">
      <a href="../e-invoicing-ethiopia/"{cur("e-invoicing-ethiopia")}>E-invoicing guide</a>
      <a href="../#erp">Industries</a>
      <a href="../e-invoicing-checker/"{cur("tools")}>Free tools</a>
      <a href="../#request">Contact</a>
      <a class="nav-call" href="tel:+251911251837">Call +251 911 251837</a>
    </nav>
    <a class="btn btn-dark" href="../#request">Request e-invoice</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
'''


def chrome_bottom():
    ind = "".join(f'<li><a href="../{p}/">{e(n)}</a></li>' for p, n, _ in INDUSTRY_LINKS)
    free = "".join(f'<li><a href="../{p}/">{e(n)}</a></li>' for p, n in FREE_LINKS)
    return f'''<div class="tibeb" aria-hidden="true"></div>
<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div><img src="../edel-logo-dark-360.webp" srcset="../edel-logo-dark-360.webp 360w, ../edel-logo-dark.webp 720w" sizes="90px" width="720" height="338" alt="Edel Trading PLC" loading="lazy"><p>E-invoicing and ERP for Ethiopian businesses, approved by the Ministry of Revenues. Built and supported in Addis Ababa.</p><p lang="am" style="font-family:'Noto Sans Ethiopic',var(--body);margin-top:8px">ኤሌክትሮኒክ ደረሰኝ እና ኢአርፒ ለኢትዮጵያ ንግዶች</p></div>
      <div><h4>Industries</h4><ul>{ind}</ul></div>
      <div><h4>Free tools and guides</h4><ul>{free}</ul></div>
      <div><h4>Contact</h4><ul><li><a href="tel:+251911251837">+251 911 251837</a></li><li><a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp +251 960 369445</a></li><li>Addis Ababa, Ethiopia</li><li><a href="../#request">Request e-invoice</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>© <span class="yr">2026</span> Edel Trading PLC</span><span lang="am">ግብር ይክፈሉ፣ ሀገር ይልማ።</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Message Edel on WhatsApp">{WA_SVG}</a>
<script>document.querySelectorAll(".yr").forEach(function (el) {{ el.textContent = new Date().getFullYear(); }});
(function () {{
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) {{
    var bar = document.createElement("div"); bar.className = "scroll-bar"; bar.setAttribute("aria-hidden", "true"); document.body.appendChild(bar);
    var tick = false;
    window.addEventListener("scroll", function () {{
      if (tick) return; tick = true;
      requestAnimationFrame(function () {{ var h = document.documentElement.scrollHeight - innerHeight; bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, scrollY / h) : 0) + ")"; tick = false; }});
    }}, {{ passive: true }});
  }}
}})();
(function () {{
  document.documentElement.classList.add("js");
  var els = document.querySelectorAll(".band h2, .band p.intro, .features li, .reasons > div, .demo-box, .faq details, .related a, .cta-band, .card");
  if (!("IntersectionObserver" in window) || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
  els.forEach(function (el, i) {{ el.classList.add("rv"); el.style.transitionDelay = (i % 4) * 60 + "ms"; }});
  var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }} }}); }}, {{ threshold: 0.1 }});
  els.forEach(function (el) {{ io.observe(el); }});
}})();
(function () {{
  var b = document.querySelector(".menu-btn"), n = document.getElementById("main-nav");
  if (!b || !n) return;
  function set(open) {{ n.classList.toggle("open", open); b.setAttribute("aria-expanded", open); b.setAttribute("aria-label", open ? "Close menu" : "Open menu"); }}
  b.addEventListener("click", function () {{ set(!n.classList.contains("open")); }});
  n.addEventListener("click", function (e) {{ if (e.target.closest("a")) set(false); }});
  document.addEventListener("keydown", function (e) {{ if (e.key === "Escape") set(false); }});
}})();</script>
'''


# ------------------------------------------------------------------ industries
TYPES = {'hotel': 'Hotel', 'beer': 'Beer distribution', 'tours': 'Tours & travel', 'import': 'Import & export', 'manufacturing': 'Manufacturing', 'farms': 'Farm'}

PAGES = [
 dict(path="hotel-software-ethiopia", demo="hotel", name="Hotels", live=True,
  title="Hotel Management Software in Ethiopia | Edel ERP",
  desc="Hotel and lodge software for Ethiopia: rooms, front desk, restaurant and bar, stores and daily reports, with Ministry of Revenues approved e-invoices. Amharic and English.",
  h1="Hotel management software for Ethiopian hotels and lodges",
  am="የሆቴል እና ሎጅ ማኔጅመንት ሶፍትዌር",
  lede="Run rooms, front desk, restaurant, bar and stores in one system. Every bill is a registered e-invoice, and the owner sees the day's income, profit and rooms tonight from anywhere.",
  intro="Hotels lose money in the gaps: a room checked out but not billed, drinks served but not rung up, stock issued to the kitchen with no record. Edel closes those gaps by putting the front desk, the restaurant till and every store on the same system.",
  feats=[("Rooms and front desk", "Bookings, check-in, check-out and room status on one screen."),
         ("Online bookings", "Rooms and rates stay in sync with booking sites and your own website."),
         ("Online payment", "Guests pay by telebirr, CBE Birr, card or bank transfer."),
         ("Restaurant and bar", "Waiter orders go straight to the kitchen screen; bills can go to the guest's room."),
         ("Kitchen, bar and housekeeping stores", "Each department requests stock and records exactly what it used."),
         ("Daily reporting", "Sales, guests, purchases and cash for every day, matched to your fiscal Z-reports."),
         ("Guest QR in every room", "Guests register themselves and message the hotel from their phone."),
         ("Staff and payroll", "Fingerprint attendance and Ethiopian payroll, ready to send to the bank.")],
  demo_points=["Check a guest out and watch income rise", "Ring up a restaurant sale with telebirr", "Approve an expense and see profit change"],
  faq=[("Can Edel handle both the hotel and its restaurant?", "Yes. Rooms, the restaurant and bar till, and the stores are one system, so a meal can be charged to a room and every sale shows in the same daily report."),
       ("Does it work with booking sites?", "Yes. Room availability and rates can be kept in sync with booking sites and with your own website, so you don't sell the same room twice."),
       ("Can I see my hotel's numbers when I'm away?", "Yes. The owner sees income, profit, rooms tonight and money received on the phone, every day, from anywhere.")]),
 dict(path="beer-distribution-software-ethiopia", demo="beer", name="Beer distribution", live=True,
  title="Beer Distribution Software in Ethiopia | Edel ERP",
  desc="Software for beverage and beer distributors in Ethiopia: truck sales, crates and empties, seller cash, brewery targets and stock, with registered e-invoices.",
  h1="Beer and beverage distribution software for Ethiopia",
  am="የቢራ እና መጠጥ አከፋፋይ ሶፍትዌር",
  lede="Every truck, crate, seller and Birr accounted for, every day. Edel tracks what leaves the warehouse, what each truck sells, which empties come back and whether the cash reached the bank.",
  intro="In distribution, profit disappears quietly: a few crates short on a truck, empties left with customers, cash that stays with a seller for days. Edel follows the beer from the brewery to the outlet and the money back to the bank, so the owner can see the gap the same day.",
  feats=[("Daily sales per truck", "Each truck's load, sales, returns and cash recorded every day."),
         ("Bottles and crates", "Know how many empties sit with each customer, truck and store."),
         ("Seller cash and deposits", "See what each seller owes and when the cash reached the bank."),
         ("Brewery purchases and targets", "Track orders, credits, and monthly and quarterly brewery targets."),
         ("Warehouse stock and counts", "Receive from the brewery, load trucks and count stock, with losses in Birr."),
         ("Bank matching", "Import bank statements and match every deposit and payment."),
         ("Purchase taxes worked out", "Ethiopian withholding and purchase taxes calculated on every purchase."),
         ("Owner dashboard", "Profit, stock losses, targets and an outlet map on one screen.")],
  demo_points=["Record a sale to an outlet with empties returned", "Load a truck from the warehouse", "Count stock and see the loss in Birr"],
  faq=[("Can Edel track empty crates and bottles?", "Yes. Empties going out with each sale and coming back are recorded per customer, truck and store, so you always know how many are outside."),
       ("How do I know each seller handed in the cash?", "Each truck's sales and the seller's bank deposits are recorded, and the owner sees what each seller still holds."),
       ("Does it follow brewery targets?", "Yes. Purchases from the brewery are tracked against monthly and quarterly targets, with progress on the owner's dashboard.")]),
 dict(path="tour-company-software-ethiopia", demo="tours", name="Tours & travel", live=True,
  title="Tour Company & Car Rental Software in Ethiopia | Edel ERP",
  desc="Software for tour operators and car rental companies in Ethiopia: bookings, dispatch, cars, drivers, fuel, per diem and profit per trip, with registered e-invoices.",
  h1="Software for tour companies and car rental in Ethiopia",
  am="የጉብኝት እና የመኪና ኪራይ ድርጅት ሶፍትዌር",
  lede="Every booking, car, driver and litre of fuel, with the profit of each trip. Edel takes the booking, dispatches the car, records the kilometres and fuel, and shows the owner what each car really earns.",
  intro="A tour company can be busy every day and still not know which car or route makes money. Edel puts bookings, dispatch, fuel and driver per diem together, so revenue and cost meet on every trip.",
  feats=[("Tour bookings", "Tours, airport shuttles and company trips with route, passengers, guide and agreed rate."),
         ("Deposits and credit", "Take a deposit, confirm with payment, or put an agency or company on credit."),
         ("Dispatch board", "Assign the car and driver, then record km out and km back for every trip."),
         ("Fuel barrels", "Every litre drawn for each car, so fuel used per trip is known."),
         ("Profit per car, driver and route", "Revenue, fuel, repairs and per diem for each, with cost per km."),
         ("Driver per diem", "Approved by the manager, and counted as a cost only once it is actually paid."),
         ("Papers and alerts", "Registration and insurance expiry reminders, and an alert when a car is out too long."),
         ("Owner dashboard", "Revenue, costs, profit and trips against last week, from your phone anywhere.")],
  demo_points=["Book a tour and confirm it with payment", "Dispatch a car and bring it back with fuel", "See profit by car, driver and route"],
  faq=[("Can I see profit per car?", "Yes. Revenue from each trip and the fuel, repairs and per diem for that car come together, with cost per kilometre."),
       ("Does it handle airport shuttles as well as tours?", "Yes. Tours, airport shuttles and company use are all booking types, each with its own reporting."),
       ("Will I know when a car's papers expire?", "Yes. Registration and insurance dates are tracked, with reminders before they expire.")]),
 dict(path="import-export-software-ethiopia", demo="import", name="Import & export", live=False,
  title="Import & Export Software in Ethiopia: Landed Cost, LC, Customs | Edel ERP",
  desc="ERP for Ethiopian importers and exporters: landed cost with customs duty, excise, VAT and surtax, letters of credit, foreign currency, Djibouti transit and stock.",
  h1="Import and export software for Ethiopian traders",
  am="የአስመጪ እና ላኪ ድርጅቶች ሶፍትዌር",
  lede="Know the true landed cost of every container, from Djibouti to your warehouse shelf. Edel follows each shipment, works out the import taxes in the right order, and prices stock at what it really cost.",
  intro="An importer who prices goods on the invoice price alone is often selling at a loss once duty, surtax, clearing and transport are added. Edel builds the landed cost of every shipment line by line, and keeps your books in Birr and in foreign currency.",
  feats=[("Landed cost per shipment", "Freight, insurance, duty, excise, VAT, surtax and withholding added to every load."),
         ("Import taxes in the right order", "Each tax worked out in Ethiopia's order, on top of the one before."),
         ("Letters of credit", "Follow each LC from opening to settlement, with fees and expiry alerts."),
         ("Foreign currency control", "Track foreign currency balances and rates, so imports match the currency you hold."),
         ("Djibouti transit", "Follow each container from the port to clearance, with the bill of lading attached."),
         ("Stock by shipment", "Know what each shipment brought in, at what cost, and where it is stored."),
         ("Export payment follow-up", "See every export payment and get warned before it is overdue."),
         ("Books in Birr and foreign currency", "Exchange gains and losses shown per shipment.")],
  demo_points=["Work out a container's landed cost, tax by tax", "Move a shipment from Djibouti to your warehouse", "Sell imported stock and see the real margin"],
  faq=[("How does Edel work out landed cost?", "It adds freight and insurance to the goods value, then customs duty, excise, VAT, surtax and withholding in order, plus clearing, transport and port charges. VAT and withholding are shown separately because they can be claimed back."),
       ("Can it follow letters of credit?", "Yes. Each LC is tracked from opening to settlement, with its fees, amendments and expiry date."),
       ("Does it keep books in foreign currency?", "Yes. Purchases are recorded in the supplier's currency and in Birr, with exchange gains and losses per shipment.")]),
 dict(path="manufacturing-erp-ethiopia", demo="manufacturing", name="Manufacturing", live=False,
  title="Manufacturing ERP in Ethiopia: Production, Recipes, Cost per Unit | Edel",
  desc="Manufacturing ERP for Ethiopian factories: recipes and bills of materials, production orders, raw material stock, waste, quality checks, power-cut downtime and true cost per unit.",
  h1="Manufacturing ERP for Ethiopian factories",
  am="ለኢትዮጵያ ፋብሪካዎች የምርት ማኔጅመንት ሶፍትዌር",
  lede="Know what every product really costs and where material is lost. Edel turns raw materials into finished goods through recipes, records waste and machine stops, and shows the true cost per unit.",
  intro="Factories often find out about losses at the end of the month, when stock doesn't match. Edel records each production run as it happens: what went in, what came out, what was scrapped and how long the line stood still.",
  feats=[("Recipes and bills of materials", "Set exactly what goes into each product, so every batch uses the right amounts."),
         ("Production orders", "Plan and track each run from raw material to finished goods, including stoppages."),
         ("Raw material stock", "See what you hold, what each run used, and when imported inputs need reordering."),
         ("True cost per product", "Materials, labour, power, waste and excise in the cost of every unit."),
         ("Waste and scrap", "Record losses and rejects per run, and see where material disappears."),
         ("Batch tracing", "Trace any product back to its raw material lots, and recall only what's affected."),
         ("Quality checks", "Test materials and products at set points, and block failed lots from sale."),
         ("Machines and power cuts", "Log servicing, breakdowns and power-cut downtime, so plans match reality.")],
  demo_points=["Record a production run and watch materials drop", "Log a power cut on a line", "See the cost of one pack, ingredient by ingredient"],
  faq=[("Can Edel tell me my cost per unit?", "Yes. Each product's recipe adds up materials and packaging, and labour, power and overhead are added on top, so you see the true cost of one unit."),
       ("Can it record power cuts?", "Yes. Downtime is logged per line, split into power cuts and breakdowns, so production plans reflect what the factory can really make."),
       ("Can I trace a batch back to its raw materials?", "Yes. Each finished batch keeps the lots of raw material it used, so a problem can be traced and only the affected batches recalled.")]),
 dict(path="farm-management-software-ethiopia", demo="farms", name="Farms", live=False,
  title="Farm Management Software in Ethiopia: Fields, Harvest, Workers | Edel",
  desc="Farm management software for commercial farms in Ethiopia: fields and blocks, crop cycles, harvest, inputs, seasonal workers and wages, cost per hectare, sales and traceability.",
  h1="Farm management software for commercial farms in Ethiopia",
  am="ለንግድ እርሻዎች የእርሻ ማኔጅመንት ሶፍትዌር",
  lede="From field and herd to market: one system for your costs, workers, harvests and sales. Edel shows what each block costs and yields, pays seasonal crews, and traces every lot back to where it grew.",
  intro="On a farm, costs are spread over months and fields, and harvest-time crews change every day. Edel charges every input and every day of labour to the block that used it, so the owner sees cost and yield per hectare, not just a total.",
  feats=[("Plot and herd records", "Every field, block, animal and flock on file, with its size, location and history."),
         ("Crops and harvests", "Follow each planting from sowing to harvest, with yield per field and season."),
         ("Inputs and their cost", "Seed, fertiliser, chemicals and feed charged to the field or herd that used them."),
         ("Seasonal workers", "Daily attendance and pay for casual and harvest crews."),
         ("Cost per hectare or animal", "See what each hectare, animal or batch cost and earned."),
         ("Tractors, pumps and trucks", "Fuel, repairs and service dates against the work each machine did."),
         ("Sales and export", "Sales to buyers, the commodity exchange and exporters, with stock and payments linked."),
         ("Traceability", "Trace each lot back to its plot, and keep buyer and certification records ready.")],
  demo_points=["Record a harvest weigh-in from a block", "Pay today's crews by telebirr", "Sell a lot and see which block it came from"],
  faq=[("Can I see cost per hectare?", "Yes. Inputs and labour are charged to the block that used them, so each block shows its cost, yield and cost per hectare."),
       ("Can it pay seasonal workers?", "Yes. Crews are marked present each day, assigned to a block, and paid in cash, telebirr or by bank."),
       ("Can buyers trace a lot back to the farm?", "Yes. Each lot keeps the block, crop and harvest date it came from, ready for buyers and certification.")]),
]


def industry_page(p):
    url = SITE + p["path"] + "/"
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Edel", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]},
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"Edel ERP for {p['name'].lower()}",
         "applicationCategory": "BusinessApplication", "operatingSystem": "Web browser", "description": p["desc"], "url": url,
         "inLanguage": ["en", "am"], "areaServed": {"@type": "Country", "name": "Ethiopia"},
         "publisher": {"@type": "Organization", "name": "Edel Trading PLC", "url": SITE}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    feats = "\n".join(f'          <li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in p["feats"])
    pts = "".join(f"<li>{e(x)}</li>" for x in p["demo_points"])
    faq = "\n".join(f'        <details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(p["faq"]))
    related = "".join(f'<a href="../{path}/">{e(n)}<small>{e(sub)}</small></a>' for path, n, sub in INDUSTRY_LINKS if path != p["path"])
    tag = '<span class="kicker live">● In use today at Ethiopian businesses</span>' if p["live"] else '<span class="kicker">Set up for your business</span>'
    wa_text = f"Hello Edel, I'd like to know more about Edel for {p['name'].lower()}."
    return head(p["title"], p["desc"], p["path"], ld) + chrome_top() + f'''<main>
  <div class="wrap crumbs"><a href="../">Edel</a><span>›</span><a href="../#erp">Industries</a><span>›</span>{e(p["name"])}</div>
  <section class="page-hero">
    <div class="wrap">
      {tag}
      <h1>{e(p["h1"])}</h1>
      <p class="am" lang="am">{e(p["am"])}</p>
      <p class="lede">{e(p["lede"])}</p>
      <div class="btns">
        <a class="btn btn-gold" href="../demo/{p["demo"]}.html">Try the free demo →</a>
        <a class="btn btn-line" href="https://wa.me/{WA}?text={quote(wa_text)}" target="_blank" rel="noopener">Ask on WhatsApp</a>
      </div>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">
      <h2>What Edel does for {e(p["name"].lower())}</h2>
      <p class="intro">{e(p["intro"])}</p>
      <ol class="features">
{feats}
      </ol>
    </div>
  </section>

  <section class="band dark">
    <div class="wrap">
      <h2>Why owners choose Edel</h2>
      <p class="intro">One system, approved for Ethiopian e-invoicing, that you can follow from anywhere.</p>
      <div class="reasons">
        <div><b>E-invoices approved by the Ministry</b><span>Every sale is a registered e-invoice with an official number and QR code.</span></div>
        <div><b>Follow your business from anywhere</b><span>See today's sales, cash and stock on your phone, wherever you are in the world.</span></div>
        <div><b>Set up and supported in Ethiopia</b><span>We set it up, train your staff and support you in Amharic and English.</span></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="demo-box">
        <div>
          <h2>Try it yourself, free</h2>
          <p>The demo runs with example data, right in your browser. No sign-up.</p>
          <ul>{pts}</ul>
        </div>
        <div class="btns"><a class="btn btn-gold" href="../demo/{p["demo"]}.html">Open the {e(p["name"].lower())} demo →</a></div>
      </div>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap narrow">
      <h2>Questions</h2>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>Other industries</h2>
      <div class="related">{related}</div>
      <div class="cta-band" style="margin-top:40px">
        <h2>Get Edel for your business</h2>
        <p>Send us your details and our team will call you to arrange a demo, in Amharic or English.</p>
        <div class="btns"><a class="btn btn-gold" href="../?type={quote(TYPES[p["demo"]])}#request">Request e-invoice</a><a class="btn btn-line" style="color:#fff;border-color:#55575C" href="https://wa.me/{WA}?text={quote(wa_text)}" target="_blank" rel="noopener">WhatsApp us</a></div>
      </div>
    </div>
  </section>
</main>
''' + chrome_bottom() + "</body>\n</html>\n"


if __name__ == "__main__":
    for p in PAGES:
        os.makedirs(p["path"], exist_ok=True)
        with open(os.path.join(p["path"], "index.html"), "w", encoding="utf-8") as f:
            f.write(industry_page(p))
        print("wrote", p["path"])
