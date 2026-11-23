"""Builds the e-invoicing guide page: e-invoicing-ethiopia/index.html.

Run from the site root:  python3 -I _build/build_guide.py
Header and footer come from build_pages.py so every page matches.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from urllib.parse import quote
from build_pages import head, chrome_top, chrome_bottom, WA, SITE, e, INDUSTRY_LINKS

PATH = "e-invoicing-ethiopia"
URL = SITE + PATH + "/"
TITLE = "E-Invoicing in Ethiopia: A Plain Guide for Business Owners | Edel"
DESC = ("What e-invoicing in Ethiopia means for your business: how invoices are registered with the "
        "Ministry of Revenues, what changes at the till, what to prepare, and how Edel sets it up for you.")
H1 = "E-invoicing in Ethiopia: a plain guide for business owners"

FAQ = [
    ("Do I need to buy a new machine?",
     "No. Edel runs in a web browser on the computer, tablet or phone you already have."),
    ("Can I keep my receipt printer?",
     "Yes. You can connect your existing receipt printer and keep printing receipts for your customers."),
    ("What happens when a customer returns something?",
     "You issue a credit note. It is registered like an invoice, so the refund is on record and your sales stay correct."),
    ("Can I issue invoices in Amharic?",
     "Edel works in Amharic and English, and invoices can show their labels in both languages."),
    ("What does the QR code do?",
     "Anyone can scan the QR code on the invoice to check that it was registered with the Ministry of Revenues. It is your customer's proof that the invoice is genuine."),
    ("How much does Edel cost?",
     "Edel has monthly or yearly plans in Birr, based on the number of branches. Send us your details and we will give you a quote for your business."),
]

TOC = [
    ("what-is", "What is e-invoicing in Ethiopia?"),
    ("till", "What changes at the till"),
    ("who", "Who has to switch, and when"),
    ("prepare", "What you need to prepare"),
    ("offline", "When the internet or power goes down"),
    ("edel", "How Edel helps"),
    ("faq", "Questions"),
]

ld = [
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Edel", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "E-invoicing guide", "item": URL}]},
    {"@context": "https://schema.org", "@type": "Article", "headline": H1, "description": DESC,
     "inLanguage": "en", "url": URL, "mainEntityOfPage": URL, "dateModified": "2026-11-23",
     "image": SITE + "edel-logo-web.png",
     "author": {"@type": "Organization", "name": "Edel Trading PLC", "url": SITE},
     "publisher": {"@type": "Organization", "name": "Edel Trading PLC", "url": SITE,
                   "logo": {"@type": "ImageObject", "url": SITE + "edel-logo-web.png"}}},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]

toc = "".join(f'<li><a href="#{a}">{e(t)}</a></li>' for a, t in TOC)
faq = "\n".join(f'        <details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>'
                for i, (q, a) in enumerate(FAQ))
industries = "".join(f'<a href="../{p}/">{e(n)}<small>{e(sub)}</small></a>' for p, n, sub in INDUSTRY_LINKS)
wa_text = quote("Hello Edel, I read your e-invoicing guide and I'd like to get e-invoicing for my business.")

body = f'''<style>main [id] {{ scroll-margin-top: 96px; }} html {{ scroll-behavior: smooth; }} @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}</style>
<main>
  <div class="wrap crumbs"><a href="../">Edel</a><span>›</span>E-invoicing guide</div>
  <section class="page-hero">
    <div class="wrap">
      <span class="kicker">Guide · updated November 2026</span>
      <h1>{e(H1)}</h1>
      <p class="am" lang="am">ኤሌክትሮኒክ ደረሰኝ በኢትዮጵያ፦ ለንግድ ባለቤቶች ቀላል መመሪያ</p>
      <p class="lede">Your sale goes to the Ministry of Revenues automatically. The invoice comes back with an official number and a QR code. Here is what that means for your business, in plain words.</p>
      <div class="btns">
        <a class="btn btn-gold" href="../e-invoicing-checker/">Does it apply to me? Check now →</a>
        <a class="btn btn-line" href="../#request">Request e-invoice</a>
      </div>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap narrow">
      <div class="card">
        <h2 style="font-size:20px;margin-bottom:8px">On this page</h2>
        <ol class="prose" style="margin:0">{toc}</ol>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap narrow prose">
      <h2 id="what-is">What is e-invoicing in Ethiopia?</h2>
      <p>With electronic invoicing, each sale is sent to the Ministry of Revenues system as it happens.</p>
      <p>The invoice comes back with an official number and a QR code. Anyone can scan that code to check the invoice is genuine.</p>
      <p>For you, it means every sale is on record the moment it happens. For your customer, it means proof that the invoice is real.</p>

      <h2 id="till">What changes at the till</h2>
      <p>Only one step changes. Scanning items, taking cash or a transfer and printing the receipt stay the same.</p>
      <ul>
        <li><b>Before the receipt is handed over,</b> the sale is sent to the Ministry and registered.</li>
        <li><b>Your customer sees</b> an official invoice number and a QR code on every receipt.</li>
        <li><b>Refunds and corrections</b> are done with a credit note, which is registered too.</li>
      </ul>
      <p>One tip: train your cashiers on refunds and credit notes before you start. Corrections are where most early mistakes happen.</p>

      <h2 id="who">Who has to switch, and when</h2>
      <p>The Ministry of Revenues is rolling out electronic invoicing in phases, starting with larger and VAT-registered taxpayers.</p>
      <p>Not sure where your business stands? <a href="../e-invoicing-checker/">Answer three questions</a> and we'll tell you what e-invoicing likely means for you.</p>

      <h2 id="prepare">What you need to prepare</h2>
      <p>Getting ready is mostly about having your details in order. Before you start, gather:</p>
      <ol>
        <li>Your <b>TIN certificate</b> and <b>trade licence</b>.</li>
        <li>A <b>list of your branches</b> with their addresses.</li>
        <li>A <b>clean item list</b> with prices, and which items carry VAT at 15%.</li>
        <li>Which <b>device each branch will use</b>: the computer, tablet or phone you already have.</li>
        <li>Who will <b>issue invoices</b>, and who is allowed to <b>correct them</b>.</li>
      </ol>
      <p>Need a quick VAT figure while you clean up your prices? Use our <a href="../vat-calculator-ethiopia/">free VAT calculator</a>.</p>

      <h2 id="offline">When the internet or power goes down</h2>
      <p>With Edel, you keep selling. Invoices are stored safely and registered with the Ministry as soon as the connection is back.</p>
      <p>Your queue keeps moving, and nothing is lost.</p>

      <h2 id="edel">How Edel helps</h2>
      <p>Edel is approved by the Ministry of Revenues. We do the setup work so you can keep running your business:</p>
      <ul>
        <li>We <b>set up</b> the system and <b>register your branches</b>.</li>
        <li>We <b>import your items and customers</b>.</li>
        <li>We <b>train your staff</b>, and support you in <b>Amharic and English</b>.</li>
        <li>You <b>follow your business from anywhere</b>: today's sales, cash and stock on your phone.</li>
      </ul>
      <p>Want to see it working? <a href="../demo/hotel.html">Try the hotel demo</a>. It uses example data, runs in your browser, and needs no sign-up.</p>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">
      <h2>E-invoicing and ERP for your industry</h2>
      <p class="intro">Edel connects your e-invoices to the rest of your business: stock, purchasing, payroll and reports.</p>
      <div class="related">{industries}</div>
    </div>
  </section>

  <section class="band">
    <div class="wrap narrow">
      <h2 id="faq">Questions</h2>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="card" style="margin-bottom:24px">
        <h2 style="font-size:22px;margin-bottom:6px">Free tools</h2>
        <p class="note" style="margin-bottom:14px">Small helpers for Ethiopian businesses. Free, no sign-up.</p>
        <div class="related">
          <a href="../vat-calculator-ethiopia/">VAT calculator (15%)<small>Add or remove VAT in seconds</small></a>
          <a href="../invoice-template-ethiopia/">Free invoice template<small>Fill in, print or save as PDF</small></a>
          <a href="../e-invoicing-checker/">Does e-invoicing apply to me?<small>Three questions, one answer</small></a>
        </div>
      </div>
      <div class="cta-band">
        <h2>Get e-invoicing for your business</h2>
        <p>Send us your details and our team will call you to arrange setup, in Amharic or English.</p>
        <div class="btns"><a class="btn btn-gold" href="../#request">Request e-invoice</a><a class="btn btn-line" style="color:#fff;border-color:#55575C" href="https://wa.me/{WA}?text={wa_text}" target="_blank" rel="noopener">WhatsApp us</a></div>
      </div>
    </div>
  </section>
</main>
'''

if __name__ == "__main__":
    os.makedirs(PATH, exist_ok=True)
    with open(os.path.join(PATH, "index.html"), "w", encoding="utf-8") as f:
        f.write(head(TITLE, DESC, PATH, ld) + chrome_top(current=PATH) + body + chrome_bottom() + "</body>\n</html>\n")
    print("wrote", PATH)
