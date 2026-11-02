# Growth layer: technical SEO, local SEO, free tools and lead magnets.
# Executed inside build.py after pages_unique.py (shares its globals: PAGES, NAV, icon, cta, checklist, FAQ_CATS, ...).
import json, html as _html

SITE_URL = "https://kaplunfinancial.com"   # live domain (GitHub Pages); change here if it differs
HOURS = "Mon&ndash;Fri, 9am&ndash;6pm"
HOURS_PLAIN = "Mon-Fri, 9am-6pm"
# Where lead forms submit. Paste a Formspree/Basin/Netlify endpoint here when hosting is chosen.
FORM_ACTION = f"mailto:{EMAIL}"
FORM_ATTRS = ' method="post" enctype="text/plain"' if FORM_ACTION.startswith("mailto:") else ' method="post"'

NAV.insert(1, ("tools", "Free tools"))

# ============================================================ 1. TECHNICAL SEO
# Unique <title> and meta description per page (titles under ~60 chars, descriptions under ~160).
META = {
 "index": ("Tax Preparation, Bookkeeping & LLC Formation | Tukwila, WA | KFG",
           "Kaplun Financial Group in Tukwila, WA: tax returns, tax planning, LLC formation and bookkeeping in all 50 states, plus commercial insurance in Washington."),
 "about": ("About Kaplun Financial Group | Tukwila, WA",
           "One team for your taxes, business filings, books and insurance. Learn how Kaplun Financial Group in Tukwila, WA works with clients in all 50 states."),
 "services": ("Tax, Bookkeeping, Formation & Insurance Services | KFG",
           "Tax preparation, tax planning, LLC and corporation formation, bookkeeping, quarterly filings and Washington commercial insurance from one team."),
 "tax-preparation": ("Tax Preparation: 1040, Schedule C, 1065, 1120-S, 1120 | KFG",
           "Individual and business tax returns for all 50 states: 1040, Schedule C, 1065, 1120-S and 1120, plus extensions, amendments and IRS notice help."),
 "tax-planning": ("Small Business & Individual Tax Planning | Kaplun Financial",
           "Year-round tax planning to lower what you owe: entity and S corp strategy, estimated payments, retirement and deduction planning. All 50 states."),
 "business-formation": ("LLC & Corporation Formation, EIN & Permits | Kaplun Financial",
           "Form an LLC, S corp or C corp in any state, get your EIN, and handle restaurant, dealership and retail licenses and permits with KFG."),
 "bookkeeping": ("Bookkeeping & Quarterly Tax Filings for Small Business | KFG",
           "Monthly bookkeeping, reconciliations, financial reports and on-time quarterly filings for small businesses in all 50 states."),
 "commercial-insurance": ("Commercial Insurance for Washington Businesses | KFG",
           "General liability, commercial property, auto and business owner's policies for Washington businesses, from the team that already knows your books."),
 "industries": ("Accounting for Restaurants, Dealerships & Retail | KFG",
           "Taxes, permits, bookkeeping and insurance for restaurants, car dealerships, retail stores, startups and corporations, in all 50 states."),
 "faq": ("Tax, LLC & Bookkeeping Questions Answered | KFG FAQ",
           "Answers to common questions about tax returns, deadlines, LLCs, S corps, bookkeeping, quarterly taxes and Washington business insurance."),
 "contact": ("Contact Kaplun Financial Group | 253-335-9649 | Tukwila, WA",
           "Call 253-335-9649 or send a message to book a consultation. Open Mon-Fri 9am-6pm. Based in Tukwila, WA, serving all 50 states."),
}

def page_title(slug, title):
    return _html.unescape(META[slug][0]) if slug in META else f"{_html.unescape(title)} | {NAME}"

def _strip(s):
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

ORG = {
 "@type": ["AccountingService", "InsuranceAgency"], "@id": SITE_URL + "/#business",
 "name": NAME, "alternateName": "KFG", "url": SITE_URL + "/",
 "logo": SITE_URL + "/img/kfg-logo.png", "image": SITE_URL + "/img/og-image.png",
 "telephone": PHONE_TEL, "email": EMAIL,
 "address": {"@type": "PostalAddress", "addressLocality": "Tukwila", "addressRegion": "WA", "addressCountry": "US"},
 "areaServed": [{"@type": "Country", "name": "United States"}, {"@type": "State", "name": "Washington"}],
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
 "knowsAbout": ["Tax preparation", "Tax planning", "LLC formation", "Bookkeeping", "Quarterly estimated taxes", "Commercial insurance"],
}

def _ld(obj):
    obj = dict(obj); obj.setdefault("@context", "https://schema.org")
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

PAGE_SCHEMA = {}      # slug -> list of extra JSON-LD objects (filled below)
CRUMBS = {}           # slug -> [(name, slug), ...]

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": _strip(q),
            "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}} for q, a in items]}

PAGE_SCHEMA["faq"] = [faq_schema([qa for *_, qs in FAQ_CATS for qa in qs])]
for s, t, d in SERVICE_PAGES:
    PAGE_SCHEMA[s] = [{"@type": "Service", "name": _strip(t), "description": d, "provider": {"@id": SITE_URL + "/#business"},
                       "areaServed": {"@type": "State", "name": "Washington"} if s == "commercial-insurance" else {"@type": "Country", "name": "United States"}},
                      faq_schema(FAQ_BY_ID[SVC_EXTRA[s][1]][2][:5])]
    CRUMBS[s] = [("Services", "services"), (_strip(t), s)]

def seo_head(slug, title):
    t = page_title(slug, title)
    desc = META.get(slug, (None, None))[1] or META["index"][1]
    path = "/" if slug == "index" else f"/{slug}.html"
    url = SITE_URL + path
    ld = [ORG if slug in ("index", "contact", "about") or slug.startswith("tax-services-") or slug == "areas" else {"@type": "AccountingService", "@id": SITE_URL + "/#business", "name": NAME, "url": SITE_URL + "/"}]
    ld.append({"@type": "WebPage", "name": t, "url": url, "description": _html.unescape(desc), "isPartOf": {"@type": "WebSite", "name": NAME, "url": SITE_URL + "/"}})
    if slug != "index":
        trail = [("Home", "index")] + CRUMBS.get(slug, [(_strip(title), slug)])
        ld.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                   "item": SITE_URL + ("/" if s == "index" else f"/{s}.html")} for i, (n, s) in enumerate(trail)]})
    ld += PAGE_SCHEMA.get(slug, [])
    e = lambda s: _html.escape(_html.unescape(s), quote=True)
    return f'''<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#060A13">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/img/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(t)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE_URL}/img/og-image.png">
<meta name="geo.region" content="US-WA"><meta name="geo.placename" content="Tukwila">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png"><link rel="apple-touch-icon" href="img/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
''' + "\n".join(_ld(x) for x in ld)

BRAND_FILES = ["favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "favicon.ico", "og-image.png"]

def make_brand_images(out_img):
    """Copy the favicon set + social share image from img/brand/ (generated once, committed, so CI needs no Pillow)."""
    src = os.path.join(ROOT, "img", "brand")
    if not all(os.path.exists(os.path.join(src, f)) for f in BRAND_FILES):
        os.makedirs(src, exist_ok=True); draw_brand_images(src)
    for f in BRAND_FILES:
        shutil.copy(os.path.join(src, f), os.path.join(os.path.dirname(out_img) if f == "favicon.ico" else out_img, f))

def draw_brand_images(out_img):
    """Draw favicons + 1200x630 share image from the brand colors (needs Pillow and Inter fonts)."""
    from PIL import Image, ImageDraw, ImageFont
    bold = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
    def mark(size):
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * .22), fill=(6, 10, 19, 255))
        f = ImageFont.truetype(bold, int(size * .38)); w = d.textlength("KFG", font=f)
        d.text(((size - w) / 2, size * .26), "KFG", font=f, fill=(255, 255, 255, 255))
        d.rounded_rectangle([size * .2, size * .74, size * .8, size * .80], radius=int(size * .03), fill=(59, 125, 216, 255))
        return im
    mark(32).save(os.path.join(out_img, "favicon-32.png"))
    mark(180).save(os.path.join(out_img, "apple-touch-icon.png"))
    mark(192).save(os.path.join(out_img, "icon-192.png")); mark(512).save(os.path.join(out_img, "icon-512.png"))
    mark(64).save(os.path.join(out_img, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    og = Image.new("RGB", (1200, 630), (6, 10, 19)); d = ImageDraw.Draw(og)
    for r in range(420, 0, -6):  # soft blue glow
        a = int(70 * (1 - r / 420)); d.ellipse([1000 - r, -120 - r, 1000 + r, -120 + r], fill=(6 + a // 3, 10 + a // 2, 19 + a))
    logo = Image.open(os.path.join(ROOT, "img", "kfg-logo-dark-bg.png")).convert("RGBA"); logo.thumbnail((300, 200))
    og.paste(logo, (80, 70), logo)
    f1 = ImageFont.truetype(bold, 64); f2 = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 30)
    d.text((80, 300), "Taxes, business setup", font=f1, fill="white"); d.text((80, 375), "and books, handled.", font=f1, fill=(124, 196, 255))
    d.text((80, 485), "Tukwila, WA  ·  Serving all 50 states  ·  253-335-9649", font=f2, fill=(154, 166, 184))
    og.save(os.path.join(out_img, "og-image.png"), optimize=True)

def write_seo_files(out):
    urls = ["/" if s == "index" else f"/{s}.html" for s in PAGES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = "1.0" if u == "/" else ("0.9" if any(u == f"/{s}.html" for s, _, _ in SERVICE_PAGES) else "0.7")
        sm += f"  <url><loc>{SITE_URL}{u}</loc><priority>{pr}</priority></url>\n"
    open(os.path.join(out, "sitemap.xml"), "w").write(sm + "</urlset>\n")
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(out, "site.webmanifest"), "w").write(json.dumps({"name": NAME, "short_name": "KFG", "start_url": "/", "display": "standalone",
        "background_color": "#060A13", "theme_color": "#060A13",
        "icons": [{"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))

# ============================================================ shared lead form
def lead_box(source, title="Want a pro to check your numbers?", text="Send us your details and we will review your situation with you. No obligation.", button="Get my free review"):
    return f'''<form class="c-form lead-form" action="{FORM_ACTION}"{FORM_ATTRS}><h2>{title}</h2><p class="muted">{text}</p>
<input type="hidden" name="source" value="{source}">
<div class="row2"><div><label>Name</label><input name="name" required autocomplete="name"></div><div><label>Phone</label><input name="phone" type="tel" autocomplete="tel"></div></div>
<div><label>Email</label><input name="email" type="email" required autocomplete="email"></div>
<button class="btn" type="submit">{button} <span class="arr">&rarr;</span></button><p class="form-note" hidden></p>
<p class="lf-fine">Or call <a href="tel:{PHONE_TEL}">{PHONE}</a>, {HOURS}.</p></form>'''

# ============================================================ 3. TOOLS & LEAD MAGNETS
TOOLS = [
 ("s-corp-calculator", "S Corp Tax Savings Calculator", "rocket", "See roughly how much an S corp election could save you, including the QBI deduction."),
 ("estimated-tax-calculator", "Quarterly Estimated Tax Calculator", "tax-planning", "Estimate your quarterly IRS payments if you are self-employed or own a business."),
 ("business-structure-quiz", "Which Business Structure Fits? Quiz", "business-formation", "Answer three questions to see whether an LLC, S corp, multi-member LLC or C corp fits."),
 ("tax-document-checklist", "Tax Document Checklist", "tax-preparation", "A printable list of everything to gather before your personal or business return."),
]
META.update({
 "tools": ("Free Tax Calculators & Small Business Tools | KFG",
           "Free S corp savings calculator, quarterly estimated tax calculator, business structure quiz and printable tax document checklist."),
 "s-corp-calculator": ("S Corp Tax Savings Calculator (2026) | Kaplun Financial",
           "Free S corp calculator: compare total tax as a standard LLC vs an S corp with 2026 rates, including the Section 199A QBI deduction."),
 "estimated-tax-calculator": ("Quarterly Estimated Tax Calculator 2026 | Kaplun Financial",
           "Estimate your 2026 quarterly estimated tax payments for self-employment income, with federal brackets, SE tax and due dates."),
 "business-structure-quiz": ("LLC vs S Corp vs C Corp Quiz: Which Fits You? | KFG",
           "Answer three quick questions to see which business structure may fit you best: single-member LLC, S corp, multi-member LLC or C corp."),
 "tax-document-checklist": ("Tax Document Checklist: What to Bring (Printable) | KFG",
           "Printable checklist of documents for your personal or business tax return: W-2s, 1099s, deductions, business records and more."),
})
TOOL_SLUGS = [s for s, *_ in TOOLS]
for s, t, _, _ in TOOLS:
    CRUMBS[s] = [("Free tools", "tools"), (t, s)]

def vis_card(title, rows):
    r = "".join(f'<div class="vrow"><span class="vk">{k}</span><span>{v}</span><span class="vchk"></span></div>' for k, v in rows)
    return f'<div class="vcard"><p class="vtitle">{title}</p>{r}</div>'

TOOL_VIS = {
 "S Corp Tax Savings Calculator": vis_card("Example: $100k profit, $50k salary, married", [("LLC", "Total federal tax $19,465"), ("S corp", "Total federal tax $13,761"), ("Saved", "About $5,700 a year")]),
 "Quarterly Estimated Tax Calculator": vis_card("2026 estimated tax due dates", [("Q1", "April 15, 2026"), ("Q2", "June 15, 2026"), ("Q3", "September 15, 2026"), ("Q4", "January 15, 2027")]),
 "Which business structure fits you?": vis_card("Possible results", [("LLC", "Single-member LLC"), ("S corp", "LLC taxed as an S corp"), ("2+", "Multi-member LLC"), ("C corp", "C corporation")]),
 "Tax document checklist": vis_card("5 sections, 35 items", [("ID", "Everyone on the return"), ("1099", "Income forms"), ("1098", "Deductions &amp; credits"), ("Sch C", "Self-employed"), ("K-1", "Partnerships &amp; corporations")]),
}

PERKS = [("100% free", "No sign-up, no email required to use it"), ("Updated for 2026", "Current IRS brackets, limits and dates"), ("Private", "Your numbers stay in your browser")]
def perks_strip():
    ic = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>'
    return '<section class="perks-sec"><div class="wrap"><div class="perks">' + "".join(f'<div class="perk"><span class="perk-ico">{ic}</span><div><strong>{t}</strong><span>{d}</span></div></div>' for t, d in PERKS) + '</div></div></section>'

def tool_head(title, lead, kicker="Free tool"):
    vis = TOOL_VIS.get(title, "")
    return f'''<section class="page-head split-head"><div class="glow g1"></div><div class="gridbg"></div>
<div class="wrap ph-grid"><div><p class="crumb"><a href="tools.html">Free tools</a> / {title}</p><span class="pill-badge"><span class="dot"></span>{kicker}</span><h1>{title}</h1><p class="lead">{lead}</p>
<div class="btns"><a class="btn" href="#start">Start now <span class="arr">&darr;</span></a><a class="btn glass" href="tel:{PHONE_TEL}">Ask a pro: {PHONE}</a></div></div>
<div class="ph-visual">{vis}</div></div></section>''' + perks_strip()

DISCLAIM = '<p class="tool-fine">Estimates for general information only, not tax advice. Your actual numbers depend on your full situation.</p>'

def tools_hub():
    cards = "".join(f'<a class="tool-card" href="{s}.html"><span class="tc-ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><span class="more">Open tool &rarr;</span></a>' for s, t, ic, d in TOOLS)
    return page_head("Free tax and business tools", "Quick calculators and checklists our clients use. Free, no sign-up needed. When you want a professional to look at your numbers, we're one call away.") + f'''
<section><div class="wrap"><div class="tool-grid">{cards}</div></div></section>''' + cta("Want real numbers, not estimates?", "Book a consultation and we'll run your actual situation.")

def scorp_page():
    return tool_head("S Corp Tax Savings Calculator", "If your business makes a solid profit, electing S corp status can cut your total tax. Compare a standard LLC with an S corp using 2026 federal rates, including the Section 199A (QBI) deduction.") + f"""
<section id="start"><div class="wrap tool-wrap"><div class="tool-in">
<div class="row2"><div><label for="sc-status">Filing status</label><select id="sc-status"><option value="s">Single</option><option value="m">Married filing jointly</option></select></div>
<div><label for="sc-type">Type of business</label><select id="sc-type"><option value="n">Standard business</option><option value="sstb">Professional service (SSTB)</option></select></div></div>
<div><label for="sc-profit">Expected net business profit for the year</label><input id="sc-profit" type="number" inputmode="numeric" min="0" step="1000" value="100000"></div>
<div><label for="sc-salary">Reasonable salary you would pay yourself</label><input id="sc-salary" type="number" inputmode="numeric" min="0" step="1000" value="50000"><small>The IRS requires S corp owners who work in the business to take a reasonable salary.</small></div>
<div><label for="sc-other">Other taxable income (spouse wages, interest, etc.)</label><input id="sc-other" type="number" inputmode="numeric" min="0" step="1000" value="0"></div>
<small>Professional services (SSTB) include accounting, consulting, law, health, financial services and similar fields. Their QBI deduction phases out at higher incomes.</small>
{DISCLAIM}</div>
<div class="tool-out"><div class="glow g1"></div><p class="to-k">Estimated yearly savings</p><p class="to-big" id="sc-save">$0</p>
<p class="to-k sm">Standard LLC</p>
<div class="to-rows"><div><span>Self-employment tax</span><strong id="sc-se">$0</strong></div>
<div><span>Federal income tax <em class="to-sub" id="sc-q1"></em></span><strong id="sc-it1">$0</strong></div>
<div class="tot"><span>Total</span><strong id="sc-t1">$0</strong></div></div>
<p class="to-k sm">S corporation</p>
<div class="to-rows"><div><span>Payroll taxes on salary</span><strong id="sc-fica">$0</strong></div>
<div><span>Federal income tax <em class="to-sub" id="sc-q2"></em></span><strong id="sc-it2">$0</strong></div>
<div class="tot"><span>Total</span><strong id="sc-t2">$0</strong></div></div>
<p class="to-msg" id="sc-msg"></p><p class="to-note"><strong>Keep in mind:</strong> an S corp costs more to run than a standard LLC (payroll service, a separate business tax return, state fees and state unemployment tax). The savings shown are before those costs.</p><a class="btn" href="contact.html">Talk to us about an S corp <span class="arr">&rarr;</span></a></div></div></section>
<section class="soft"><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">How it works</span><h2>What this calculator counts</h2></div>
<div class="prose-sm"><p><strong>Standard LLC:</strong> 15.3% self-employment tax on 92.35% of profit (Social Security up to the 2026 wage base of $184,500, Medicare on all of it, plus the 0.9% additional Medicare tax above $200,000 single / $250,000 joint). Half of the self-employment tax is deducted before income tax.</p>
<p><strong>S corp:</strong> employee and employer Social Security and Medicare on your salary only, the 0.9% additional Medicare tax where it applies, and federal unemployment tax (FUTA) on the first $7,000. The employer share is deducted from the business profit that passes through to you.</p>
<p><strong>Section 199A (QBI) deduction:</strong> up to 20% of qualified business income, limited to 20% of taxable income. In an S corp your salary is not QBI, so the deduction is usually smaller. Above $201,775 taxable income ($403,550 joint) the deduction is limited by W-2 wages, and for professional service businesses it phases out over the next $75,000 ($150,000 joint).</p>
<p>Federal income tax uses 2026 brackets and the standard deduction. Not included: the extra cost of running an S corp, itemized deductions, credits, health insurance and retirement contributions, and state income tax. Washington has no personal income tax, but other states treat S corps differently.</p></div></div></section>
<section><div class="wrap narrow">{lead_box("S corp calculator", "Is an S corp right for you?", "Send us your details and we will check the numbers for your business before you elect.")}</div></section>
<script>(function(){{var SS=184500,$=function(i){{return document.getElementById(i)}},m=function(n){{return '$'+Math.round(n).toLocaleString('en-US')}};
var B={{s:{{sd:16100,th:201775,ph:75000,am:200000,b:[[12400,.10],[50400,.12],[105700,.22],[201775,.24],[256225,.32],[640600,.35],[1e15,.37]]}},m:{{sd:32200,th:403550,ph:150000,am:250000,b:[[24800,.10],[100800,.12],[211400,.22],[403550,.24],[512450,.32],[768700,.35],[1e15,.37]]}}}};
function tax(x,b){{var t=0,lo=0;for(var i=0;i<b.length;i++){{var hi=b[i][0];if(x>lo)t+=(Math.min(x,hi)-lo)*b[i][1];lo=hi}}return t}}
function qbi(q,w2,ti,F,sstb){{q=Math.max(0,q);var d;if(ti<=F.th)d=.2*q;else{{var f=Math.min(1,(ti-F.th)/F.ph),ap=sstb?1-f:1;var t=.2*q*ap,wl=.5*w2*ap;d=f>=1?Math.min(t,wl):(wl<t?t-f*(t-wl):t);}}return Math.max(0,Math.min(d,.2*Math.max(0,ti)))}}
function run(){{var F=B[$('sc-status').value],sstb=$('sc-type').value==='sstb',p=Math.max(0,+$('sc-profit').value||0),s=Math.max(0,+$('sc-salary').value||0),o=Math.max(0,+$('sc-other').value||0);if(s>p)s=p;
var nb=p*0.9235,se=Math.min(nb,SS)*0.124+nb*0.029+Math.max(0,nb-F.am)*0.009;var ti1=Math.max(0,p+o-se/2-F.sd);var q1=qbi(p-se/2,0,ti1,F,sstb);var it1=tax(ti1-q1,F.b),t1=se+it1;
var er=Math.min(s,SS)*0.062+s*0.0145,ee=Math.min(s,SS)*0.062+s*0.0145+Math.max(0,s-F.am)*0.009,futa=Math.min(s,7000)*0.006;var k1=p-s-er-futa;
var ti2=Math.max(0,s+k1+o-F.sd);var q2=qbi(k1,s,ti2,F,sstb);var it2=tax(ti2-q2,F.b),t2=er+ee+futa+it2,v=t1-t2;
$('sc-se').textContent=m(se);$('sc-it1').textContent=m(it1);$('sc-q1').textContent='after '+m(q1)+' QBI deduction';$('sc-t1').textContent=m(t1);
$('sc-fica').textContent=m(er+ee+futa);$('sc-it2').textContent=m(it2);$('sc-q2').textContent='after '+m(q2)+' QBI deduction';$('sc-t2').textContent=m(t2);
$('sc-save').textContent=v>0?m(v):'$0';
$('sc-msg').textContent=v>=2000?'Worth looking into: an S corp could save you money.':v>0?'Savings look small. It may not be worth the extra work yet.':'At these numbers an S corp likely costs more than it saves.';}}
['sc-status','sc-type','sc-profit','sc-salary','sc-other'].forEach(function(i){{$(i).addEventListener('input',run)}});run();}})();</script>""" + cta()

def esttax_page():
    return tool_head("Quarterly Estimated Tax Calculator", "Self-employed or own a pass-through business? Estimate what you may owe the IRS for 2026 and what each quarterly payment should be.") + f'''
<section id="start"><div class="wrap tool-wrap"><div class="tool-in">
<div><label for="et-status">Filing status</label><select id="et-status"><option value="s">Single</option><option value="m">Married filing jointly</option></select></div>
<div><label for="et-profit">Expected net self-employment profit for 2026</label><input id="et-profit" type="number" inputmode="numeric" min="0" step="1000" value="80000"></div>
<div><label for="et-other">Other income (W-2 wages, interest, etc.)</label><input id="et-other" type="number" inputmode="numeric" min="0" step="1000" value="0"></div>
<div><label for="et-wh">Federal tax already withheld from paychecks this year</label><input id="et-wh" type="number" inputmode="numeric" min="0" step="100" value="0"></div>
{DISCLAIM}</div>
<div class="tool-out"><div class="glow g1"></div><p class="to-k">Estimated payment per quarter</p><p class="to-big" id="et-q">$0</p>
<div class="to-rows"><div><span>Federal income tax</span><strong id="et-it">$0</strong></div><div><span>Self-employment tax</span><strong id="et-se">$0</strong></div>
<div><span>Less withholding</span><strong id="et-w">$0</strong></div><div class="tot"><span>Total for the year</span><strong id="et-tot">$0</strong></div></div>
<p class="to-k sm">2026 due dates</p><div class="to-dates"><span>Apr 15, 2026</span><span>Jun 15, 2026</span><span>Sep 15, 2026</span><span>Jan 15, 2027</span></div>
<a class="btn" href="bookkeeping.html">Let us handle your quarterly filings <span class="arr">&rarr;</span></a></div></div></section>
<section class="soft"><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">How it works</span><h2>What this calculator assumes</h2></div>
<div class="prose-sm"><p>It uses the 2026 federal tax brackets and standard deduction ($16,100 single, $32,200 married filing jointly), adds 15.3% self-employment tax on 92.35% of your profit, and deducts half of that self-employment tax from income, the way your return does.</p>
<p>It does not include the qualified business income deduction, itemized deductions, credits or state taxes, so your real bill may be lower. Paying at least 100% of last year's tax (110% if your income was over $150,000) in four equal payments generally protects you from underpayment penalties.</p></div></div></section>
<section><div class="wrap narrow">{lead_box("Estimated tax calculator", "Never miss a quarterly payment again", "We calculate and schedule your quarterly payments as part of bookkeeping. Send your details and we will reach out.", "Set up my quarterly taxes")}</div></section>
<script>(function(){{var SS=184500,$=function(i){{return document.getElementById(i)}},m=function(n){{return '$'+Math.round(n).toLocaleString('en-US')}};
var B={{s:{{sd:16100,b:[[12400,.10],[50400,.12],[105700,.22],[201775,.24],[256225,.32],[640600,.35],[1e15,.37]]}},m:{{sd:32200,b:[[24800,.10],[100800,.12],[211400,.22],[403550,.24],[512450,.32],[768700,.35],[1e15,.37]]}}}};
function tax(x,b){{var t=0,lo=0;for(var i=0;i<b.length;i++){{var hi=b[i][0];if(x>lo)t+=(Math.min(x,hi)-lo)*b[i][1];lo=hi}}return t}}
function run(){{var st=$('et-status').value,p=+$('et-profit').value||0,o=+$('et-other').value||0,w=+$('et-wh').value||0;var base=Math.max(0,p)*0.9235,ssRoom=Math.max(0,SS-o);
var se=Math.min(base,ssRoom)*0.124+base*0.029;var ti=Math.max(0,p+o-se/2-B[st].sd);var it=tax(ti,B[st].b);var tot=Math.max(0,it+se-w);
$('et-it').textContent=m(it);$('et-se').textContent=m(se);$('et-w').textContent=(w>0?'-':'')+m(w);$('et-tot').textContent=m(tot);$('et-q').textContent=m(tot/4);}}
['et-status','et-profit','et-other','et-wh'].forEach(function(i){{$(i).addEventListener('input',run)}});run();}})();</script>''' + cta()

QUIZ = [
 ("owners", "How many people will own the business?", [("1", "Just me (or me and my spouse)"), ("2", "Two or more partners")]),
 ("profit", "What yearly profit do you expect once you're up and running?", [("lo", "Under $40,000"), ("mid", "$40,000 to $80,000"), ("hi", "Over $80,000")]),
 ("investors", "Do you plan to raise money from outside investors?", [("no", "No, I'll fund it myself or with loans"), ("yes", "Yes, I want investors or venture capital")]),
]
def quiz_page():
    qs = "".join(f'<fieldset class="qz-q" data-q="{k}"><legend><span class="qz-n">{i+1}</span>{q}</legend><div class="pick">' +
                 "".join(f'<label class="pk"><input type="radio" name="qz-{k}" value="{v}"><span>{l}</span></label>' for v, l in opts) + '</div></fieldset>'
                 for i, (k, q, opts) in enumerate(QUIZ))
    return tool_head("Which business structure fits you?", "Answer three quick questions to see which structure may fit: single-member LLC, S corp, multi-member LLC or C corp. Takes under a minute.", "Free quiz") + f'''
<section id="start"><div class="wrap tool-wrap"><div class="tool-in qz">{qs}{DISCLAIM.replace("tax advice", "legal or tax advice")}</div>
<div class="tool-out" id="qz-out"><div class="glow g1"></div><p class="to-k">Your likely fit</p><p class="to-big sm" id="qz-r">Answer the questions</p><p class="to-msg" id="qz-why">Your result will appear here as you answer.</p>
<div class="to-rows" id="qz-forms" hidden><div><span>Tax return you would file</span><strong id="qz-f">&nbsp;</strong></div></div>
<a class="btn" href="business-formation.html">Form your company with KFG <span class="arr">&rarr;</span></a></div></div></section>
<section><div class="wrap narrow">{lead_box("Business structure quiz", "Get a second opinion on your structure", "We will look at your plans and confirm the right structure before you file anything.", "Review my structure")}</div></section>
<script>(function(){{var R={{
sp:["Single-member LLC","Simple and protected: profit goes on your personal return, and the LLC keeps business debts and lawsuits separate from your personal assets. As profit grows, you can elect S corp tax status without forming a new company.","Schedule C on your 1040"],
llcs:["LLC now, S corp election soon","Start as an LLC. As profit grows past roughly $40,000 to $60,000, electing S corp tax status can start saving self-employment tax. Try our S corp calculator to check.","Schedule C now, Form 1120-S later"],
s:["LLC taxed as an S corporation","With this level of profit, an S corp election often saves thousands in self-employment tax. You pay yourself a reasonable salary and take the rest as distributions.","Form 1120-S plus payroll"],
p:["Multi-member LLC (partnership)","With partners, a multi-member LLC is flexible and protects each owner. It files a partnership return and each owner gets a K-1. Higher-profit partnerships can also elect S corp status.","Form 1065, K-1s to owners"],
c:["C corporation","Investors and venture capital funds usually expect a C corporation. It pays its own corporate tax and makes it easy to issue shares and stock options.","Form 1120"]}};
var $=function(i){{return document.getElementById(i)}};function v(k){{var e=document.querySelector('input[name="qz-'+k+'"]:checked');return e?e.value:null}}
function run(){{var o=v('owners'),p=v('profit'),i=v('investors');var n=[o,p,i].filter(Boolean).length;if(n<3){{$('qz-r').textContent=n?'Keep going ('+n+' of 3)':'Answer the questions';return}}
var k=i==='yes'?'c':o==='2'?'p':p==='hi'?'s':p==='mid'?'llcs':'sp';$('qz-r').textContent=R[k][0];$('qz-why').textContent=R[k][1];$('qz-f').textContent=R[k][2];$('qz-forms').hidden=false;
if(window.innerWidth<1040)$('qz-out').scrollIntoView({{behavior:'smooth',block:'start'}});}}
document.querySelectorAll('.qz input').forEach(function(e){{e.addEventListener('change',run)}});}})();</script>''' + cta()

CHECK = [
 ("Everyone", ["Photo ID for you (and your spouse, if filing jointly)", "Social Security numbers and birth dates for everyone on the return", "Last year's federal and state tax returns", "Bank account and routing number for your refund or payment", "IRS or state letters you received this year", "Identity Protection PIN, if the IRS issued you one"]),
 ("Income", ["W-2s from every employer", "1099-NEC and 1099-K for freelance, gig or app income", "1099-INT and 1099-DIV for interest and dividends", "1099-B or brokerage statements for stock and crypto sales", "1099-R for retirement distributions and SSA-1099 for Social Security", "K-1s from partnerships, S corps or trusts", "Rental income and expenses", "1099-G for unemployment or state refunds"]),
 ("Deductions & credits", ["Form 1098 mortgage interest and property tax bills", "Charitable donation receipts", "Childcare provider name, address, tax ID and amount paid", "Form 1098-T tuition and 1098-E student loan interest", "Form 1095-A if you bought insurance through the marketplace", "IRA, HSA and retirement contribution statements", "Energy-efficient home improvement or EV purchase receipts"]),
 ("Self-employed & small business", ["Income records: invoices, deposits, 1099s you received", "Expense records or a profit and loss report", "Business mileage log and vehicle details", "Home office square footage and home expenses", "Receipts for equipment and other large purchases", "Estimated tax payments you made this year, with dates", "1099s you issued to contractors"]),
 ("Partnerships & corporations", ["Year-end profit and loss statement and balance sheet", "Bank and credit card statements for December", "Payroll reports (W-2s, W-3, 941s, state filings)", "Loan statements showing interest paid and balances", "Fixed asset list with purchases and sales this year", "Owner contributions, distributions and ownership changes", "Prior-year business return and depreciation schedules"]),
]
def checklist_page():
    cols = "".join(f'<div class="ck-col"><h2 class="h-sm">{h}</h2><ul class="ck">' + "".join(f'<li><label><input type="checkbox"><span>{x}</span></label></li>' for x in items) + '</ul></div>' for h, items in CHECK)
    return tool_head("Tax document checklist", "Everything to gather before your personal or business tax return, in one printable list. Check items off as you go, then print it or save it as a PDF.", "Free printable") + f'''
<section id="start"><div class="wrap"><div class="ck-bar"><button class="btn" type="button" onclick="window.print()">Print or save as PDF</button><span class="muted">Tip: on your phone, use Share &rarr; Print to save a PDF.</span></div>
<div class="ck-grid">{cols}</div></div></section>
<section class="soft no-print"><div class="wrap narrow">{lead_box("Tax document checklist", "Send me my personalized checklist", "Tell us a little about you and we will email a checklist tailored to your return, plus a reminder before the deadline.", "Email my checklist")}</div></section>''' + cta()

PAGES["tools"] = ("Free tools", tools_hub())
PAGES["s-corp-calculator"] = ("S Corp Tax Savings Calculator", scorp_page())
PAGES["estimated-tax-calculator"] = ("Quarterly Estimated Tax Calculator", esttax_page())
PAGES["business-structure-quiz"] = ("Business Structure Quiz", quiz_page())
PAGES["tax-document-checklist"] = ("Tax Document Checklist", checklist_page())

# ---- richer tool pages: how-to steps, FAQs, related service and tools
TOOL_EXTRA = {
 "s-corp-calculator": (
  [("Enter your profit", "Use your expected net profit for the year, after business expenses."), ("Set a reasonable salary", "What you'd pay someone else to do your job. The IRS expects it to be realistic."), ("Compare the totals", "See total federal tax as a standard LLC and as an S corp, side by side.")],
  [("What counts as a reasonable salary?", "Roughly what you would pay someone else to do the work you do, based on your duties, hours, experience and industry. Setting it too low to save payroll tax is a common audit trigger, so we help clients set and document a defensible number."),
   ("When do I have to elect S corp status?", "File Form 2553 within 2 months and 15 days of the start of the tax year you want it to apply to. For most businesses that means by March 15. If you missed it, the IRS often grants late election relief, and we can file for it."),
   ("Do I need to form a new company?", "No. Your existing LLC simply elects to be taxed as an S corporation. It keeps the same name, EIN and liability protection; only the way it's taxed changes."),
   ("Why does the QBI deduction get smaller with an S corp?", "The Section 199A deduction is 20% of qualified business income, and the salary you pay yourself is not QBI. So moving profit into salary trims the deduction a little. The calculator includes this.")],
  "tax-planning", "Want a full S corp analysis, including your state, health insurance and retirement plan? That's part of our tax planning."),
 "estimated-tax-calculator": (
  [("Pick your filing status", "Single or married filing jointly."), ("Enter your income", "Your expected self-employment profit, other income and any tax withheld from paychecks."), ("Pay each quarter", "Pay the quarterly amount by each due date through IRS Direct Pay or your IRS online account.")],
  [("Who has to pay estimated taxes?", "Generally anyone who expects to owe $1,000 or more for the year after withholding and credits. That includes most self-employed people, freelancers, gig workers and business owners whose pay isn't withheld."),
   ("What happens if I miss a payment?", "The IRS charges an underpayment penalty, figured separately for each quarter, much like interest. Paying late is still better than not paying; the penalty stops growing once the payment is made."),
   ("How can I avoid the penalty?", "Pay at least 90% of this year's tax, or 100% of last year's tax (110% if last year's adjusted gross income was over $150,000), spread over the four due dates."),
   ("How do I make the payments?", "Online through IRS Direct Pay, EFTPS or your IRS online account, or by mail with a Form 1040-ES voucher. Our bookkeeping clients get the amounts and reminders from us each quarter.")],
  "bookkeeping", "Let us calculate and schedule your quarterly payments every quarter as part of bookkeeping."),
 "business-structure-quiz": (
  [("Answer three questions", "Owners, expected profit and whether you'll raise money from investors."), ("See your likely fit", "Get a recommended structure and the tax return it files."), ("Confirm with us", "We review your plans and form the company in any state.")],
  [("Can I change my structure later?", "Yes. Many owners start as an LLC and elect S corp taxation once profits grow, without forming a new company. Converting to a C corporation later is also possible, though it takes more paperwork."),
   ("Why not just operate under my own name?", "Without an entity, you are personally on the hook for business debts and lawsuits. An LLC is inexpensive to form, separates business from personal assets and makes banking and bookkeeping cleaner, which is why we recommend it as the starting point."),
   ("Do I need an operating agreement?", "Washington doesn't require you to file one, but every LLC should have one. It sets out ownership, decision-making and what happens if an owner leaves, and banks often ask for it. We prepare it as part of formation."),
   ("Can a multi-member LLC be an S corp?", "Yes, as long as every owner is an eligible shareholder (generally US citizens or residents), there are no more than 100 owners and profits are split by ownership percentage.")],
  "business-formation", "We form LLCs and corporations in all 50 states, get your EIN and handle licenses and permits."),
 "tax-document-checklist": (
  [("Check what applies", "Go section by section and tick off what you already have."), ("Print or save", "Save it as a PDF or print it to keep track as forms arrive."), ("Book your appointment", "Bring or send everything and we take it from there.")],
  [("When will I have all my forms?", "Employers and most payers must send W-2s and 1099-NEC forms by January 31. Brokerage 1099s often arrive in mid-February, and corrected forms can come as late as March, so it pays to wait until you have everything."),
   ("What if a form is missing?", "Don't guess. We can pull your IRS wage and income transcript to see what was reported under your Social Security number, or contact the payer for a copy."),
   ("Do I need receipts for every expense?", "You need records that support each deduction: receipts, invoices, bank or card statements and a mileage log for vehicle use. Keep them at least three years after filing."),
   ("Can you prepare my return if I'm not in Washington?", "Yes. We prepare federal and state returns for all 50 states. You send documents electronically and we meet by phone or video.")],
  "tax-preparation", "We prepare individual and business returns of every type, federal and state, in all 50 states."),
}
SVC_TITLE = {s: t for s, t, _ in SERVICE_PAGES}

def tool_extras(slug):
    steps, faqs, svc, pitch = TOOL_EXTRA[slug]
    st = "".join(f'<div class="step"><span class="step-n">{i+1}</span><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(steps))
    rel = "".join(f'<a class="tool-card" href="{s}.html"><span class="tc-ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><span class="more">Open tool &rarr;</span></a>' for s, t, ic, d in TOOLS if s != slug)
    return f'''<section class="no-print"><div class="wrap"><div class="sec-head"><span class="kicker">How to use it</span><h2>Three steps, about a minute</h2></div>
<p class="swipe-hint">Swipe to see more &rarr;</p><div class="steps">{st}</div></div></section>
<section class="soft no-print"><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Questions</span><h2>Common questions</h2><p class="lead">Straight answers from our team.</p><a class="more" href="faq.html">See all FAQs &rarr;</a></div>{faq_list(faqs)}</div></section>
<section class="no-print"><div class="wrap"><a class="svc-band" href="{svc}.html"><span class="tc-ico">{icon(svc)}</span><div><small>Related service</small><strong>{SVC_TITLE[svc]}</strong><p>{pitch}</p></div><span class="btn small">Learn more <span class="arr">&rarr;</span></span></a>
<p class="os-label rel-label">More free tools</p><div class="tool-grid three">{rel}</div></div></section>'''

for slug in TOOL_EXTRA:
    t, b = PAGES[slug]
    marker = '<section class="soft no-print"><div class="wrap narrow">' if slug == "tax-document-checklist" else '<section><div class="wrap narrow">'
    assert b.count(marker) == 1, slug
    PAGES[slug] = (t, b.replace(marker, tool_extras(slug) + marker.replace('class="soft no-print"', 'class="no-print"')))
    PAGE_SCHEMA.setdefault(slug, []).append(faq_schema(TOOL_EXTRA[slug][1]))

HUB_FAQ = [("Are the tools really free?", "Yes. There's no sign-up and no email required. Use them as often as you like."),
           ("Do you save the numbers I enter?", "No. The calculators run entirely in your browser, and nothing is sent to us unless you choose to fill out a form."),
           ("Is this tax advice?", "No. The tools give estimates for general information. Your actual tax depends on your full situation, which is what a consultation is for."),
           ("How current are the numbers?", "The calculators use 2026 federal tax brackets, standard deductions and the Social Security wage base. We update them every January.")]
def tools_hub2():
    cards = "".join(f'<a class="tool-card" href="{s}.html"><span class="tc-ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><span class="more">Open tool &rarr;</span></a>' for s, t, ic, d in TOOLS)
    vis = vis_card("Free tools", [("S corp", "Savings calculator"), ("1040-ES", "Quarterly tax calculator"), ("LLC", "Business structure quiz"), ("List", "Tax document checklist")])
    who = [("Freelancers &amp; gig workers", "Estimate quarterly payments and get your documents together.", "person"),
           ("Growing small businesses", "See whether an S corp election would pay off this year.", "tax-planning"),
           ("New business owners", "Find the right structure before you file anything.", "rocket")]
    wc = "".join(f'<div class="card"><div class="ico-wrap">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></div>' for t, d, ic in who)
    return f'''<section class="page-head split-head"><div class="glow g1"></div><div class="gridbg"></div>
<div class="wrap ph-grid"><div><span class="pill-badge"><span class="dot"></span>Free, no sign-up</span><h1>Free tax and business tools</h1>
<p class="lead">Calculators, a quiz and a printable checklist built by our team. Run the numbers yourself, then call us when you want a professional to look at your situation.</p>
<div class="btns"><a class="btn" href="#tool-list">See the tools <span class="arr">&darr;</span></a><a class="btn glass" href="tel:{PHONE_TEL}">Call {PHONE}</a></div></div>
<div class="ph-visual">{vis}</div></div></section>''' + perks_strip() + f'''
<section id="tool-list"><div class="wrap"><div class="sec-head"><span class="kicker">Tools</span><h2>Pick a tool</h2></div><div class="tool-grid">{cards}</div></div></section>
<section class="soft"><div class="wrap"><div class="sec-head"><span class="kicker">Who they're for</span><h2>Built for people who run their own business</h2></div><div class="grid g3">{wc}</div></div></section>
<section><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Questions</span><h2>About these tools</h2></div>{faq_list(HUB_FAQ)}</div></section>''' + cta("Want real numbers, not estimates?", "Book a consultation and we'll run your actual situation.")
PAGES["tools"] = ("Free tools", tools_hub2())
PAGE_SCHEMA["tools"] = [faq_schema(HUB_FAQ)]

PAGE_SCHEMA["s-corp-calculator"] = [{"@type": "WebApplication", "name": "S Corp Tax Savings Calculator", "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
PAGE_SCHEMA["estimated-tax-calculator"] = [{"@type": "WebApplication", "name": "Quarterly Estimated Tax Calculator", "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]

# promote tools from home and the matching service pages
def tool_promo(slug, line):
    s, t, ic, d = next(x for x in TOOLS if x[0] == slug)
    return f'<section class="promo-sec"><div class="wrap"><a class="tool-promo" href="{s}.html"><span class="tc-ico">{icon(ic)}</span><div><small>Free tool</small><strong>{t}</strong><p>{line}</p></div><span class="tile-go">&rarr;</span></a></div></section>'

PROMO = {"tax-preparation": ("tax-document-checklist", "Print the list of documents to gather before your appointment."),
         "tax-planning": ("s-corp-calculator", "See how much an S corp election could save you this year."),
         "business-formation": ("business-structure-quiz", "Not sure which structure to form? Take the 4-question quiz."),
         "bookkeeping": ("estimated-tax-calculator", "Estimate your quarterly IRS payments in under a minute.")}
for s, (tool, line) in PROMO.items():
    t, b = PAGES[s]; PAGES[s] = (t, b.replace('<section class="other-sec">', tool_promo(tool, line) + '<section class="other-sec">', 1))

def home_tools_band():
    cards = "".join(f'<a class="tool-card" href="{s}.html"><span class="tc-ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></a>' for s, t, ic, d in TOOLS)
    return f'''<section class="soft"><div class="wrap"><div class="sec-head"><span class="kicker">Free tools</span><h2>Run the numbers yourself</h2>
<p class="lead">Free calculators and checklists, no sign-up needed.</p></div><div class="tool-grid">{cards}</div></div></section>'''

# ============================================================ 2. LOCAL SEO
# Each page has its own local copy (no copy-paste doorway pages).
CITIES = [
 ("tukwila", "Tukwila", "Our office is here in Tukwila, so local clients can meet with us in person by appointment.",
  "Tukwila is home to the Southcenter shopping district and a dense mix of retailers, restaurants, auto businesses and service companies along the I-5 and I-405 corridor. Many of our clients run businesses within a few miles of our office.",
  ["Retail and restaurant sales tax reporting to the Washington Department of Revenue", "Washington B&O tax returns, monthly, quarterly or annual", "City business license endorsements through the state Business Licensing Service", "Bookkeeping and payroll records for busy storefronts", "Commercial property and liability coverage for Southcenter-area shops"],
  [("Can I meet with you in person?", "Yes. Our office is in Tukwila and we meet with clients in person by appointment, Monday to Friday, 9am to 6pm. We also work by phone, email and video if that's easier."),
   ("Do Tukwila businesses need a city business license?", "Most businesses operating in Tukwila need a city business license endorsement in addition to their Washington state business license. We can set up both and track the renewals for you.")],
  ["seattle", "renton", "kent", "burien", "seatac"]),
 ("seattle", "Seattle", "We work with Seattle individuals, freelancers and small businesses from our nearby Tukwila office.",
  "Seattle businesses deal with more local tax rules than most of the state. On top of Washington's B&O and sales tax, the City of Seattle has its own business license tax and business license requirements, and larger employers may owe the city's payroll expense tax.",
  ["Seattle business license tax certificate and city B&O filings", "Washington B&O, sales and use tax returns", "Returns for tech contractors, gig workers and consultants", "S corp planning for high-earning self-employed professionals", "Restaurant and retail permits, books and quarterly filings"],
  [("Do I file a Seattle city tax return in addition to state taxes?", "Many Seattle businesses do. The city has its own business license tax, separate from Washington's B&O tax. Whether you owe it, and how often you file, depends on your income and activities. We figure that out and handle both."),
   ("Do I have to come to Tukwila?", "No. Most Seattle clients work with us by phone, email and video. If you'd like to meet in person, our Tukwila office is a short drive away.")],
  ["tukwila", "bellevue", "burien", "renton"]),
 ("renton", "Renton", "Renton is right next door to our Tukwila office.",
  "Renton's economy mixes aerospace, healthcare, retail around The Landing and a growing number of contractors and home-based businesses. We help Renton residents with their personal returns and Renton business owners with everything from forming an LLC to keeping the books.",
  ["Personal returns for aerospace, healthcare and tech employees", "LLC formation and licensing for contractors and trades", "Quarterly estimated taxes for self-employed residents", "Bookkeeping and Washington B&O filings for small businesses", "Commercial auto and liability coverage for contractors"],
  [("Can you help me start a contracting business in Renton?", "Yes. We form the company, get your EIN and Washington business license, set up bookkeeping and quarterly filings, and can quote general liability and commercial auto coverage. Contractor registration with L&I is a separate step we'll walk you through."),
   ("I work at a large employer but have a side business. Can you help?", "Yes. We combine your W-2 income and side business on one return, track deductible expenses and set up estimated payments so you don't get a surprise bill.")],
  ["tukwila", "kent", "seattle", "bellevue"]),
 ("kent", "Kent", "We serve Kent businesses and families from our office just north in Tukwila.",
  "The Kent Valley is one of the largest warehouse, distribution and manufacturing areas on the West Coast. That means lots of trucking, logistics, wholesale and industrial businesses, along with family-owned restaurants and shops downtown and on the East Hill.",
  ["Returns for owner-operators and trucking companies", "Bookkeeping for wholesale, distribution and manufacturing businesses", "Fuel, mileage and equipment depreciation tracking", "Entity setup and S corp planning for growing companies", "Commercial auto and property coverage"],
  [("Do you work with truck drivers and owner-operators?", "Yes. We prepare returns for owner-operators and trucking companies, track mileage, per diem and equipment depreciation, and keep quarterly payments on schedule."),
   ("Can you take over my books mid-year?", "Yes. We'll catch up the months that are behind, reconcile your accounts and keep you current from there.")],
  ["tukwila", "renton", "federal-way", "seatac"]),
 ("burien", "Burien", "Burien is a few minutes west of our Tukwila office.",
  "Burien's downtown is full of independent restaurants, salons, shops and service businesses, many of them family run. We help owners keep their sales tax, B&O filings and books in order, and help families with straightforward and not-so-straightforward personal returns.",
  ["Sales tax and B&O returns for restaurants and shops", "Bookkeeping that keeps up with cash and card sales", "Family returns with dependents, education and childcare credits", "LLC formation and city licensing for new storefronts", "Business owner's policies for small shops"],
  [("I'm opening a restaurant in Burien. Where do I start?", "Start with structure and licensing: we form your LLC, get your EIN and state business license, and help with the permits a restaurant needs. Then we set up books and sales tax filing before your first day open."),
   ("Do you prepare family tax returns too?", "Yes. We prepare individual and family returns of every type, including dependents, credits, rental income and self-employment.")],
  ["tukwila", "seatac", "seattle", "federal-way"]),
 ("seatac", "SeaTac", "SeaTac borders Tukwila, a few minutes from our office.",
  "With the airport at its center, SeaTac has a large concentration of hotels, parking, transportation, food service and travel businesses. The city also has its own higher minimum wage for many hospitality and transportation employers, which affects payroll and bookkeeping.",
  ["Payroll-aware bookkeeping for hospitality and transportation businesses", "Returns for rideshare, delivery and airport-area drivers", "Sales and lodging-related tax reporting", "Entity and license setup for new travel-related businesses", "Commercial auto and liability coverage"],
  [("I drive for rideshare and delivery apps. Can you help?", "Yes. We report your 1099-K and 1099-NEC income, claim mileage and other deductions, and set up quarterly estimated payments so you stay ahead of the IRS."),
   ("Does SeaTac's minimum wage affect my business?", "It can, if you're a covered hospitality or transportation employer. We keep your books and payroll records accurate so your labor costs and filings line up.")],
  ["tukwila", "burien", "kent", "federal-way"]),
 ("federal-way", "Federal Way", "We serve Federal Way clients from our Tukwila office, about 20 minutes up I-5.",
  "Federal Way is home to a diverse community of small business owners in retail, restaurants, home services, healthcare and real estate. We help them form their companies, file their taxes and keep clean books, and we prepare personal returns for families across the city.",
  ["Returns for real estate agents and rental property owners", "Home services and contractor bookkeeping", "LLC and S corp setup for growing businesses", "Washington B&O and sales tax filings", "Commercial insurance for storefronts and service vans"],
  [("I own rental property. Can you handle that on my return?", "Yes. We report rental income and expenses, calculate depreciation and help you keep the records you need, whether you own one unit or several."),
   ("Can we work together without meeting in person?", "Absolutely. Most clients send documents by email and meet with us by phone or video. In-person meetings at our Tukwila office are available by appointment.")],
  ["kent", "tukwila", "seatac", "burien"]),
 ("bellevue", "Bellevue", "We work with Bellevue clients by phone, email and video, with in-person meetings available at our Tukwila office.",
  "Bellevue is a hub for technology, professional services and consulting. The city has its own business license and B&O tax, so Bellevue businesses often file at both the city and state level. Many residents also have stock compensation and side businesses that make their personal returns more complex.",
  ["Bellevue city business license and B&O filings", "Returns with RSUs, stock options and brokerage sales", "Washington capital gains tax review for large sales", "S corp and tax planning for consultants and contractors", "Bookkeeping for professional services firms"],
  [("Do Bellevue businesses pay a city B&O tax?", "Bellevue has its own business and occupation tax and business license, separate from the state. Small businesses may fall under a threshold, so we check what applies to you and handle the filings."),
   ("My return has RSUs and stock sales. Can you prepare it?", "Yes. We reconcile your brokerage forms with your W-2 so stock compensation isn't taxed twice, and review whether Washington's capital gains tax applies.")],
  ["seattle", "renton", "tukwila"]),
]
CITY_BY = {c[0]: c for c in CITIES}

def city_page(c):
    k, name, close, intro, needs, faqs, near = c
    svc = "".join(f'<a class="tool-card" href="{s}.html"><span class="tc-ico">{icon(s)}</span><h3>{t}</h3><p>{d}</p></a>' for s, t, d in SERVICE_PAGES)
    nl = "".join(f'<a class="area-chip" href="tax-services-{n}-wa.html">{CITY_BY[n][1]}</a>' for n in near)
    return f'''<section class="page-head"><div class="glow g1"></div><div class="gridbg"></div><div class="wrap">
<p class="crumb"><a href="areas.html">Areas we serve</a> / {name}, WA</p><span class="pill-badge"><span class="dot"></span>{close}</span>
<h1>Tax, bookkeeping and business services in {name}, WA</h1><p class="lead">Tax preparation, tax planning, LLC formation, bookkeeping and commercial insurance for {name} individuals and businesses.</p>
<div class="btns"><a class="btn" href="contact.html">Book a consultation <span class="arr">&rarr;</span></a><a class="btn glass" href="tel:{PHONE_TEL}">Call {PHONE}</a></div></div></section>
<section><div class="wrap split-top"><div><span class="kicker">Local know-how</span><h2>Working with {name} clients</h2><p class="intro big">{intro}</p>
<div class="who"><strong>Hours</strong><p>{HOURS}. In person by appointment in Tukwila, or by phone, email and video.</p></div></div>
<div><h2 class="h-sm">What {name} clients ask us for</h2>{checklist(needs)}</div></div></section>
<section class="soft"><div class="wrap"><div class="sec-head"><span class="kicker">Services</span><h2>Everything under one roof</h2><p class="lead">Taxes, formation and bookkeeping in all 50 states. Commercial insurance for Washington businesses, including {name}.</p></div>
<div class="tool-grid five">{svc}</div></div></section>
<section><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Questions</span><h2>{name} clients often ask</h2><a class="more" href="faq.html">See all FAQs &rarr;</a></div>{faq_list(faqs)}</div></section>
<section class="soft"><div class="wrap"><p class="os-label">Nearby areas we serve</p><div class="area-row">{nl}<a class="area-chip" href="areas.html">All areas</a></div></div></section>''' + cta(f"Let's talk about your taxes and business in {name}.")

def areas_page():
    chips = "".join(f'<a class="area-card" href="tax-services-{k}-wa.html"><strong>{n}, WA</strong><span>{cl}</span></a>' for k, n, cl, *_ in CITIES)
    return page_head("Areas we serve", f"Our office is in Tukwila, WA. We meet local clients in person and work with clients in every state by phone, email and video. {HOURS}.") + f'''
<section><div class="wrap"><div class="sec-head"><span class="kicker">South King County and the Seattle area</span><h2>Washington communities we serve</h2>
<p class="lead">Every service, including commercial insurance, is available across Washington.</p></div><div class="area-grid">{chips}</div></div></section>
<section class="dark-band"><div class="glow g1"></div><div class="wrap split"><div><span class="kicker dk">Nationwide</span><h2>Clients in all 50 states</h2></div>
<p class="lead">Tax preparation and planning, LLC and corporation filings, and bookkeeping are available everywhere in the US. You send documents securely, we meet by phone or video, and you sign electronically. Commercial insurance is available for Washington businesses only.</p></div></section>''' + cta()

for c in CITIES:
    slug = f"tax-services-{c[0]}-wa"
    PAGES[slug] = (f"{c[1]}, WA", city_page(c))
    META[slug] = (f"Tax Preparation & Bookkeeping in {c[1]}, WA | KFG",
                  f"Tax preparation, LLC formation, bookkeeping and business insurance for {c[1]}, WA individuals and businesses. Call 253-335-9649, {HOURS_PLAIN}.")
    CRUMBS[slug] = [("Areas we serve", "areas"), (f"{c[1]}, WA", slug)]
    PAGE_SCHEMA[slug] = [faq_schema(c[5]), {"@type": "Service", "name": f"Tax and bookkeeping services in {c[1]}, WA", "provider": {"@id": SITE_URL + "/#business"},
                         "areaServed": {"@type": "City", "name": c[1], "containedInPlace": {"@type": "State", "name": "Washington"}}}]
PAGES["areas"] = ("Areas we serve", areas_page())
META["areas"] = ("Areas We Serve: Tukwila, Seattle & All 50 States | KFG",
                 "Kaplun Financial Group serves Tukwila, Seattle, Renton, Kent, Burien, SeaTac, Federal Way, Bellevue and clients in all 50 states.")
ORG["areaServed"] += [{"@type": "City", "name": c[1]} for c in CITIES]

# hours everywhere "By appointment" was used
for k in list(PAGES):
    t, b = PAGES[k]; PAGES[k] = (t, b.replace("By appointment", HOURS))

# home: tools band before the closing call to action
t, b = PAGES["index"]; i = b.rfind('<section class="cta-sec">')
PAGES["index"] = (t, b[:i] + home_tools_band() + b[i:])

# 404 page (site only, not in sitemap)
NOT_FOUND = page_head("Page not found", "The page you're looking for has moved or doesn't exist.") + '''<section><div class="wrap"><div class="btns"><a class="btn" href="index.html">Go to the home page <span class="arr">&rarr;</span></a><a class="btn outline" href="services.html">See our services</a><a class="btn outline" href="contact.html">Contact us</a></div></div></section>'''
