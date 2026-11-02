#!/usr/bin/env python3
"""Build the Kaplun Financial Group website.

Outputs:
  site/            deployable multi-page static site (upload this folder to any host)
  preview/index.html  single-file preview (hash routing, inlined CSS and logo)

Edit content below, then run:  python3 build.py
"""
import base64, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
PHONE = "253-335-9649"
PHONE_TEL = "+12533359649"
EMAIL = "info@kaplunfinancial.com"
CITY = "Tukwila, WA"
NAME = "Kaplun Financial Group"

NAV = [("index", "Home"), ("about", "About"), ("services", "Services"),
       ("industries", "Industries"), ("faq", "FAQ"), ("contact", "Contact")]

SERVICE_PAGES = [
    ("tax-preparation", "Tax Preparation", "Federal and state returns of every type, in all 50 states."),
    ("tax-planning", "Tax Planning", "Year-round strategy to lower what you owe."),
    ("business-formation", "Business Formation & Permits", "LLCs and corporations in any state, plus licenses and permits."),
    ("bookkeeping", "Bookkeeping & Quarterly Filings", "Clean books and on-time quarterly taxes, for businesses in every state."),
    ("commercial-insurance", "Commercial Insurance", "Coverage for Washington businesses."),
]

ICONS = {
    "tax-preparation": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h6"/>',
    "tax-planning": '<path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 15l4-4 3 3 5-6"/>',
    "business-formation": '<path d="M3 21h18"/><path d="M5 21V9l7-5 7 5v12"/><path d="M10 21v-6h4v6"/>',
    "bookkeeping": '<path d="M4 5h11a3 3 0 0 1 3 3v12H7a3 3 0 0 1-3-3z"/><path d="M8 9h6M8 13h6"/>',
    "commercial-insurance": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "restaurant": '<path d="M7 3v8a2 2 0 0 0 4 0V3M9 11v10"/><path d="M17 3c-2 0-3 2-3 5s1 4 3 4v9"/>',
    "car": '<path d="M5 17h14v-5l-2-5H7l-2 5z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
    "store": '<path d="M4 9l2-5h12l2 5"/><path d="M4 9h16v12H4z"/><path d="M10 21v-6h4v6"/>',
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
    "rocket": '<path d="M12 15l-3-3c1-5 4-8 9-9-1 5-4 8-9 9"/><path d="M9 12l-4 1-2 4 4-1M12 15l-1 4-4 2 1-4"/>',
    "building": '<path d="M4 21V5l8-2v18M12 9h8v12"/><path d="M8 8v1M8 12v1M8 16v1M16 13v1M16 17v1"/>',
}

def icon(key):
    return f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[key]}</svg>'

def card(title, text, ico=None, link=None):
    i = f'<div class="ico-wrap">{icon(ico)}</div>' if ico else ""
    l = f'<a class="more" href="{link}.html">Learn more &rarr;</a>' if link else ""
    return f'<div class="card">{i}<h3>{title}</h3><p>{text}</p>{l}</div>'

def checklist(items):
    return '<ul class="check">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def page_head(title, lead, crumb=None):
    c = f'<p class="crumb"><a href="services.html">Services</a> / {crumb}</p>' if crumb else ""
    return f'<section class="page-head"><div class="glow g1"></div><div class="gridbg"></div><div class="wrap">{c}<h1>{title}</h1><p class="lead">{lead}</p></div></section>'

def cta(title="Ready to get started?", text="Tell us what you need and we will get back to you quickly."):
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta"><div class="glow g1"></div><div class="cta-in"><h2>{title}</h2><p>{text}</p>
<div class="btns"><a class="btn white" href="contact.html">Book a consultation <span class="arr">&rarr;</span></a><a class="btn glass" href="tel:{PHONE_TEL}">Call {PHONE}</a></div></div></div></div></section>'''

SERVICE_ARGS = {}

def service_detail(slug, title, lead, intro, includes, who, faq=None):
    SERVICE_ARGS[slug] = (title, lead, intro, includes, who)
    other = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, _ in SERVICE_PAGES if s != slug)
    f = ""
    if faq:
        f = '<h2 style="margin-top:48px">Common questions</h2>' + "".join(
            f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    return page_head(title, lead, crumb=title) + f'''
<section><div class="wrap detail"><div class="main-col">
<p class="intro">{intro}</p>
<h2>What's included</h2>{checklist(includes)}
<h2>Who it's for</h2><p>{who}</p>{f}
</div><aside class="side">
<div class="side-box dark"><h3>Talk to KFG</h3><p>Questions about {title.lower()}? Reach out and we will walk you through it.</p>
<p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><a class="btn" href="contact.html">Book a consultation</a></div>
<div class="side-box"><h3>Other services</h3><ul class="plain">{other}</ul></div>
</aside></div></section>''' + cta()

# ---------------------------------------------------------------- pages
PAGES = {}

PAGES["index"] = ("Tax, Bookkeeping & Business Services | Tukwila, WA & All 50 States", f"""
<section class="hero"><div class="glow g1"></div><div class="glow g2"></div><div class="gridbg"></div>
<div class="wrap hero-grid"><div class="hero-copy">
<span class="pill-badge"><span class="dot"></span>Based in {CITY} &middot; Serving all 50 states</span>
<h1>Taxes, business setup and books, <span class="grad">handled.</span></h1>
<p class="hero-lead">Kaplun Financial Group files every type of tax return, opens and licenses new companies, keeps your books and insures your business, all with one team. Based in {CITY} and working with clients in all 50 states.</p>
<div class="btns"><a class="btn" href="contact.html">Book a consultation <span class="arr">&rarr;</span></a><a class="btn glass" href="services.html">Explore services</a></div>
<div class="hero-tags"><span class="tag-us">All 50 states</span><span>1040</span><span>Schedule C</span><span>1065</span><span>S corp</span><span>C corp</span><span>LLC formation</span></div>
</div>
<div class="hero-visual" aria-hidden="true">
<div class="float-card fc-main">
 <div class="fc-head"><span class="fc-logo">KFG</span><div><strong>Client dashboard</strong><small>Everything in one place</small></div></div>
 <div class="fc-row"><span class="st ok"></span><div><strong>Tax return</strong><small>Prepared &amp; e-filed</small></div><em class="tag ok">Filed</em></div>
 <div class="fc-row"><span class="st ok"></span><div><strong>LLC formation</strong><small>State filing &amp; EIN</small></div><em class="tag ok">Approved</em></div>
 <div class="fc-row"><span class="st pend"></span><div><strong>Quarterly taxes</strong><small>Estimated payment</small></div><em class="tag pend">Scheduled</em></div>
 <div class="fc-row"><span class="st ok"></span><div><strong>Business insurance</strong><small>General liability</small></div><em class="tag ok">Active</em></div>
</div>
<div class="float-card fc-mini fm1"><span class="mini-ico">{icon("bookkeeping")}</span><div><small>Books</small><strong>Up to date</strong></div></div>
<div class="float-card fc-mini fm2"><span class="mini-ico">{icon("business-formation")}</span><div><small>Permits</small><strong>Restaurant license</strong></div></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head center"><span class="kicker">Services</span><h2>Everything your business needs, under one roof</h2>
<p class="lead">From a single 1040 to a multi-member partnership, from opening an LLC to insuring your storefront.</p></div>
<div class="bento">
<a class="tile tile-big" href="tax-preparation.html"><div class="tile-ico">{icon("tax-preparation")}</div><h3>Tax Preparation</h3><p>Federal and state returns of every type, for all 50 states.</p>
<div class="chips"><span>1040</span><span>Schedule C</span><span>1065</span><span>1120-S</span><span>1120</span></div><span class="tile-go">Learn more &rarr;</span></a>
<a class="tile" href="tax-planning.html"><div class="tile-ico">{icon("tax-planning")}</div><h3>Tax Planning</h3><p>Year-round strategy to lower what you owe.</p><span class="tile-go">Learn more &rarr;</span></a>
<a class="tile" href="business-formation.html"><div class="tile-ico">{icon("business-formation")}</div><h3>Business Formation &amp; Permits</h3><p>LLCs and corporations in any state, plus licenses and permits.</p><span class="tile-go">Learn more &rarr;</span></a>
<a class="tile" href="bookkeeping.html"><div class="tile-ico">{icon("bookkeeping")}</div><h3>Bookkeeping &amp; Quarterly Filings</h3><p>Clean books and on-time quarterly taxes, nationwide.</p><span class="tile-go">Learn more &rarr;</span></a>
<a class="tile" href="commercial-insurance.html"><div class="tile-ico">{icon("commercial-insurance")}</div><h3>Commercial Insurance</h3><p>Coverage that protects the business you built. Available for Washington businesses.</p><span class="tile-go">Learn more &rarr;</span></a>
</div></div></section>

<section class="reach"><div class="glow g1"></div><div class="wrap reach-grid">
<div><span class="kicker dk">Where we work</span><h2>Based in Tukwila. Working in all 50 states.</h2>
<p class="lead">Our office is in {CITY}, and our clients are everywhere. Wherever you live or do business, we can help.</p></div>
<div class="reach-list">
<div class="rl"><span class="rl-ico">{icon("tax-preparation")}</span><div><strong>Tax preparation &amp; planning</strong><small>Federal and state, all 50 states</small></div><em class="tag ok">Nationwide</em></div>
<div class="rl"><span class="rl-ico">{icon("business-formation")}</span><div><strong>LLC &amp; corporation filings</strong><small>Formed in any state</small></div><em class="tag ok">Nationwide</em></div>
<div class="rl"><span class="rl-ico">{icon("bookkeeping")}</span><div><strong>Bookkeeping &amp; quarterly filings</strong><small>For businesses in every state</small></div><em class="tag ok">Nationwide</em></div>
<div class="rl"><span class="rl-ico">{icon("commercial-insurance")}</span><div><strong>Commercial insurance</strong><small>For Washington businesses</small></div><em class="tag wa">Washington</em></div>
</div></div></section>

<section class="sec soft"><div class="wrap split">
<div><span class="kicker">Who we work with</span><h2>Built for people who run real businesses</h2>
<p class="lead">We know the permits, filings and tax rules that come with your industry, and we handle them before they become problems.</p>
<div class="btns"><a class="btn dark" href="industries.html">Industries we serve <span class="arr">&rarr;</span></a></div></div>
<div class="ind-grid">
<div class="ind"><span class="ind-ico">{icon("restaurant")}</span><strong>Restaurants</strong><small>Permits, books, quarterly filings</small></div>
<div class="ind"><span class="ind-ico">{icon("car")}</span><strong>Car dealerships</strong><small>Dealer licensing, entity setup</small></div>
<div class="ind"><span class="ind-ico">{icon("store")}</span><strong>Retail stores</strong><small>Registration, sales tax, insurance</small></div>
<div class="ind"><span class="ind-ico">{icon("rocket")}</span><strong>Startups</strong><small>The right structure from day one</small></div>
<div class="ind"><span class="ind-ico">{icon("building")}</span><strong>Corporations</strong><small>1065, 1120-S and 1120 returns</small></div>
<div class="ind"><span class="ind-ico">{icon("person")}</span><strong>Individuals</strong><small>1040 and Schedule C returns</small></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head center"><span class="kicker">How it works</span><h2>Getting started takes three steps</h2></div>
<p class="swipe-hint">Swipe to see more &rarr;</p><div class="steps">
<div class="step"><span class="step-n">1</span><h3>Reach out</h3><p>Call, email or send the form and tell us what you need.</p></div>
<div class="step"><span class="step-n">2</span><h3>Consultation</h3><p>We review your situation and explain your options and costs up front.</p></div>
<div class="step"><span class="step-n">3</span><h3>We handle it</h3><p>Returns filed, company formed, books in order and coverage in place.</p></div>
</div></div></section>""" + cta("Let's get your taxes and business in order."))

PAGES["about"] = ("About", page_head(f"About {NAME}", "A one-stop financial partner for individuals and business owners in Tukwila and the greater Seattle area.") + f'''
<section><div class="wrap cols">
<div><h2>Who we are</h2>
<p>{NAME} (KFG) brings tax preparation, tax planning, business formation, bookkeeping and commercial insurance together under one roof. Instead of juggling an accountant, a filing service, a bookkeeper and an insurance agent, our clients have one team that knows their whole picture.</p>
<p>We work with everyone from individuals filing a single 1040 to restaurants, car dealerships, retail stores and growing companies filing partnership and corporate returns.</p></div>
<div><h2>Our mission</h2>
<p>To take the stress out of taxes and business paperwork, so our clients can focus on running their lives and their businesses.</p>
<h2>What we value</h2>{checklist(["<strong>Clarity.</strong> Plain answers and upfront pricing.", "<strong>Accuracy.</strong> Every return and filing done right the first time.", "<strong>Responsiveness.</strong> Real people who pick up the phone.", "<strong>Long-term relationships.</strong> We are here every quarter, not just in April."])}</div>
</div></section>
<section class="alt"><div class="wrap"><h2>Why clients choose KFG</h2><div class="grid">''' +
card("Everything in one place", "Taxes, books, formation and insurance handled by one team, with no handoffs.", "building") +
card("Business know-how", "Hands-on experience with permits and licensing for restaurants, dealerships and retail.", "store") +
card("Proactive planning", "We look for savings all year so tax season holds no surprises.", "tax-planning") +
'</div></div></section>' + cta())

SVC_FEATURES = {
    "tax-preparation": ("Every return, done right and filed on time.",
        "Personal or corporate, simple or complex, in any of the 50 states: we prepare it carefully, find every deduction you are entitled to and e-file it on time.",
        ["All 50 states", "Form 1040", "Schedule C", "Form 1065", "Form 1120-S", "Form 1120", "Amended returns"],
        ("Returns we file", [("1040", "Individuals & families"), ("Sch C", "Self-employed"), ("1065", "Partnerships & LLCs"), ("1120-S", "S corporations"), ("1120", "C corporations")])),
    "tax-planning": ("Pay less tax, legally and predictably.",
        "We look at your income, entity and goals all year long, then build a plan that keeps more money in your pocket and keeps surprises out of April.",
        ["Tax projections", "LLC vs. S corp", "Owner pay strategy", "Estimated payments", "Deduction strategy"],
        ("Your plan covers", [("Q1", "Projection & estimates"), ("Q2", "Entity & pay review"), ("Q3", "Mid-year adjustments"), ("Q4", "Year-end moves")])),
    "business-formation": ("Open your company the right way from day one.",
        "LLCs, corporations, EINs, state registration and the licenses and permits your industry requires, in any of the 50 states.",
        ["Any state", "LLC formation", "Corporations & S corps", "EIN registration", "Business licenses", "Restaurant permits", "Dealer licensing"],
        ("Typical setup", [("01", "Choose the right structure"), ("02", "File with the state"), ("03", "Get your EIN"), ("04", "Licenses & permits"), ("05", "Open for business")])),
    "bookkeeping": ("Clean books and on-time quarterly filings.",
        "For businesses anywhere in the US, we keep your records accurate every month and handle quarterly filings and estimated payments, so tax season is easy and you always know your numbers.",
        ["All 50 states", "Monthly bookkeeping", "Reconciliations", "P&L and balance sheet", "Quarterly filings", "Books clean-up"],
        ("Every month you get", [("P&L", "Profit & loss statement"), ("BS", "Balance sheet"), ("REC", "Bank reconciliations"), ("QTR", "Quarterly filings on time")])),
    "commercial-insurance": ("Coverage that protects what you built.",
        "We help Washington businesses find commercial insurance that fits their industry, size and budget, and review existing policies to close the gaps.",
        ["Washington businesses", "General liability", "Commercial property", "Business owner's policy", "Commercial auto", "Umbrella"],
        ("Popular coverage", [("GL", "General liability"), ("PROP", "Commercial property"), ("BOP", "Business owner's policy"), ("AUTO", "Commercial auto"), ("UMB", "Umbrella coverage")])),
}

def svc_feature(i, slug, title):
    head, text, chips, (vt, rows) = SVC_FEATURES[slug]
    flip = " flip" if i % 2 else ""
    chip_html = "".join(f"<span>{c}</span>" for c in chips)
    row_html = "".join(f'<div class="vrow"><span class="vk">{k}</span><span>{v}</span><span class="vchk"></span></div>' for k, v in rows)
    return f'''<div class="feature{flip}" data-slug="{slug}">
<div class="f-copy"><div class="f-top"><span class="tile-ico">{icon(slug)}</span><span class="f-num">0{i+1} / 05</span></div>
<h3 class="f-eyebrow">{title}</h3><h2>{head}</h2><p class="lead">{text}</p>
<div class="chips light">{chip_html}</div>
<div class="btns"><a class="btn" href="{slug}.html">Learn more <span class="arr">&rarr;</span></a><a class="btn outline" href="contact.html">Get a quote</a></div></div>
<div class="f-visual"><div class="glow g1"></div><div class="vcard"><p class="vtitle">{vt}</p>{row_html}</div></div>
</div>'''

PAGES["services"] = ("Services", page_head("Services built for individuals and businesses", f"Based in {CITY}, serving clients in all 50 states. Taxes, company formation and bookkeeping anywhere in the US, plus commercial insurance for Washington businesses.") +
'<section class="svc-jump-sec"><div class="wrap"><nav class="svc-jump" aria-label="Jump to a service">' + "".join(
    f'<a href="{s}.html" data-jump="{s}">{icon(s)}<span>{t}</span></a>' for s, t, _ in SERVICE_PAGES) + '</nav></div></section>' +
'<section class="features-sec"><div class="wrap">' + "".join(svc_feature(i, s, t) for i, (s, t, _) in enumerate(SERVICE_PAGES)) + '</div></section>' +
'''<section class="soft"><div class="wrap"><div class="sec-head center"><span class="kicker">Why one firm</span><h2>Better together</h2>
<p class="lead">When the same team does your taxes, books, filings and insurance, nothing gets lost between providers.</p></div>
<p class="swipe-hint">Swipe to see more &rarr;</p><div class="steps">
<div class="step"><span class="step-n">1</span><h3>One point of contact</h3><p>No more chasing an accountant, a bookkeeper and an agent separately.</p></div>
<div class="step"><span class="step-n">2</span><h3>Your whole picture</h3><p>Your books feed your taxes, your taxes shape your plan, and your plan informs your coverage.</p></div>
<div class="step"><span class="step-n">3</span><h3>Here all year</h3><p>Quarterly filings, planning check-ins and fast answers whenever you need them.</p></div>
</div></div></section>''' + cta("Not sure which service you need?", "Tell us about your situation and we will point you in the right direction.") + """<script>document.querySelectorAll('[data-jump]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
var p=a.closest('main');var t=p.querySelector('.feature[data-slug="'+a.dataset.jump+'"]');if(t)t.scrollIntoView({behavior:'smooth',block:'start'});
a.parentNode.querySelectorAll('a').forEach(function(x){x.classList.remove('on')});a.classList.add('on');});});</script>""")

PAGES["tax-preparation"] = ("Tax Preparation", service_detail("tax-preparation", "Tax Preparation",
    "Individual and business tax returns of every type, federal and state, for clients in all 50 states.",
    "Whether you are filing a personal return or a corporate one, KFG prepares it carefully, looks for every deduction you are entitled to, and files it on time. We prepare federal returns and state returns for all 50 states. Basically, if it is a tax return, we do it.",
    ["<strong>State returns</strong> for all 50 states",
     "<strong>Form 1040</strong> individual and family returns",
     "<strong>Schedule C</strong> for self-employed, freelancers and sole proprietors",
     "<strong>Form 1065</strong> partnerships and multi-member LLCs",
     "<strong>Form 1120-S</strong> S corporations",
     "<strong>Form 1120</strong> C corporations",
     "Extensions, amended returns and prior-year filings",
     "Help responding to IRS and state notices"],
    "Individuals, families, gig workers, sole proprietors, partnerships and corporations of any size, in any state.",
    [("What do I need to bring?", "Your income documents (W-2s, 1099s, K-1s), last year's return, and records of deductible expenses. We will send a checklist when you book."),
     ("Can you file a return I missed from a prior year?", "Yes. We prepare prior-year and amended returns and can help you get caught up.")]))

PAGES["tax-planning"] = ("Tax Planning", service_detail("tax-planning", "Tax Planning",
    "Year-round strategy that lowers your tax bill and keeps surprises out of April, for clients in all 50 states.",
    "The best time to save on taxes is before the year ends. We review your income, business structure and goals, then build a plan to reduce what you owe legally and predictably.",
    ["Year-round tax projections",
     "Entity selection, such as LLC vs. S corp election",
     "Owner compensation and distribution planning",
     "Estimated quarterly payment planning",
     "Deduction and expense strategy",
     "Planning around major life and business changes"],
    "Business owners, self-employed professionals and individuals with growing or changing income."))

PAGES["business-formation"] = ("Business Formation & Permits", service_detail("business-formation", "Business Formation & Permits",
    "Open your company the right way in any of the 50 states, with the right structure, filings, licenses and permits.",
    "Starting a business comes with a lot of paperwork. KFG handles the filings and licensing so you can open your doors with confidence, whether you are launching a restaurant, a car dealership, a retail store or any other company.",
    ["LLC formation and filings in all 50 states",
     "Corporation and S corporation setup",
     "EIN (federal tax ID) registration",
     "State business registration and registered agent setup",
     "Business licenses and permits",
     "Permits for restaurants, car dealerships, retail stores and more",
     "Annual reports and ongoing compliance"],
    "New business owners and existing businesses that are expanding, restructuring or adding locations."))

PAGES["bookkeeping"] = ("Bookkeeping & Quarterly Filings", service_detail("bookkeeping", "Bookkeeping & Quarterly Filings",
    "Clean, current books and quarterly tax filings handled on time, for businesses in all 50 states.",
    "Good books make everything easier, from tax season to getting a loan. We keep your records accurate and up to date, and handle quarterly tax filings so nothing slips through the cracks.",
    ["Monthly bookkeeping and reconciliations",
     "Profit and loss statements and balance sheets",
     "Quarterly tax filings",
     "Estimated quarterly tax payments",
     "Year-end books ready for your tax return",
     "Clean-up of past-due or messy books"],
    "Small and mid-size businesses, restaurants, retailers and self-employed professionals who want their numbers handled."))

PAGES["commercial-insurance"] = ("Commercial Insurance", service_detail("commercial-insurance", "Commercial Insurance",
    "Coverage that protects the business you built, for Washington businesses.",
    "Every business faces risk. KFG helps Washington companies find commercial insurance that fits their industry, size and budget, and because we already know your business, we can match coverage to what you actually need.",
    ["General liability",
     "Commercial property",
     "Business owner's policies (BOP)",
     "Commercial auto",
     "Professional liability and umbrella policies",
     "Guidance on Washington L&I workers' comp for employers",
     "Coverage reviews for existing policies"],
    "Washington restaurants, dealerships, retail stores, contractors and companies of all sizes. Commercial insurance is currently offered for Washington businesses only."))

PAGES["industries"] = ("Industries", page_head("Industries we serve", "We know the filings, permits and tax rules that come with your type of business.") +
'<section><div class="wrap"><div class="grid">' +
card("Restaurants &amp; food service", "Health and business permits, entity setup, bookkeeping, quarterly filings and coverage for your kitchen and staff.", "restaurant") +
card("Car dealerships", "Dealer licensing, business formation, books, tax returns and commercial auto and liability coverage.", "car") +
card("Retail stores", "Business registration and licenses, sales and quarterly taxes, bookkeeping and storefront insurance.", "store") +
card("Startups &amp; new businesses", "Choosing the right structure, opening your LLC or corporation, and getting set up correctly from day one.", "rocket") +
card("Partnerships &amp; corporations", "1065, 1120-S and 1120 returns, owner planning and year-round compliance.", "building") +
card("Self-employed &amp; individuals", "1040 and Schedule C returns, estimated payments and personal tax planning.", "person") +
'</div></div></section>' + cta("Don't see your industry?", "We work with businesses of all kinds. Get in touch and tell us about yours."))

from faq_data import FAQ_CATS

def faq_page():
    total = sum(len(q) for *_, q in FAQ_CATS)
    search = '<div class="faq-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><label for="faq-q" class="sr">Search questions</label><input id="faq-q" type="search" placeholder="Search questions, e.g. LLC, extension, sales tax" autocomplete="off"></div>'
    cats = f'<div class="faq-cats" role="tablist"><button class="on" data-cat="all">All <em>{total}</em></button>' + "".join(
        f'<button data-cat="{cid}">{label} <em>{len(qs)}</em></button>' for cid, label, _, qs in FAQ_CATS) + '</div>'
    groups = "".join(
        f'<div class="faq-group" data-cat="{cid}"><h3><span class="ico-wrap">{icon(ic)}</span>{label}</h3>' +
        "".join(f'<details data-cat="{cid}"><summary>{q}</summary><p>{ans}</p></details>' for q, ans in qs) + '</div>'
        for cid, label, ic, qs in FAQ_CATS)
    js = """<script>(function(){document.querySelectorAll('.faq-wrap').forEach(function(w){
var q=w.querySelector('#faq-q'),btns=w.querySelectorAll('.faq-cats button'),cat='all',cnt=w.querySelector('.faq-count'),empty=w.querySelector('.faq-empty');
function run(){var t=(q.value||'').toLowerCase().trim(),n=0;
w.querySelectorAll('.faq-group').forEach(function(g){var vis=0;var okCat=cat==='all'||g.dataset.cat===cat;
g.querySelectorAll('details').forEach(function(d){var ok=okCat&&(!t||d.textContent.toLowerCase().indexOf(t)>-1);d.hidden=!ok;if(ok){vis++;if(t)d.open=true;}else if(t){d.open=false;}});
g.hidden=!vis;n+=vis;});cnt.textContent=n+(n===1?' question':' questions');empty.hidden=n>0;}
btns.forEach(function(b){b.addEventListener('click',function(){btns.forEach(function(x){x.classList.remove('on')});b.classList.add('on');cat=b.dataset.cat;run();});});
q.addEventListener('input',run);run();});})();</script>"""
    return (page_head("Frequently asked questions", f"{total} answers about taxes, business formation and licensing, bookkeeping and commercial insurance. Search or filter by topic.") +
        '<section><div class="wrap narrow faq-wrap"><div class="faq-tools">' + search + cats + '<span class="faq-count"></span></div>' + groups +
        '<div class="faq-empty" hidden>No questions match your search. Try another word, or <a href="contact.html">ask us directly</a>.</div>' +
        '<p class="faq-note">These answers are general information, not tax, legal or insurance advice for your specific situation. Deadlines and rules can change. Contact us for advice about your situation.</p>' +
        '</div></section>' + js + cta("Didn't find your answer?", "Ask us directly. We are happy to help."))

PAGES["faq"] = ("FAQ", faq_page())

PAGES["contact"] = ("Contact", page_head("Contact us", "Tell us what you need and we will get back to you quickly.") + f'''
<section><div class="wrap cols">
<div><h2>Send a message</h2>
<form id="contact-form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
<div class="row2"><div><label for="n">Name</label><input id="n" name="name" required></div>
<div><label for="p">Phone</label><input id="p" name="phone" type="tel"></div></div>
<div><label for="e">Email</label><input id="e" name="email" type="email" required></div>
<div><label for="s">I need help with</label><select id="s" name="service">
<option>Tax preparation</option><option>Tax planning</option><option>Business formation &amp; permits</option>
<option>Bookkeeping &amp; quarterly filings</option><option>Commercial insurance</option><option>Something else</option></select></div>
<div><label for="m">Message</label><textarea id="m" name="message" rows="5" required></textarea></div>
<button class="btn" type="submit">Send message</button>
<p id="form-note" class="form-note" hidden></p>
</form></div>
<div><h2>Reach us directly</h2>
<div class="contact-item">{icon("person")}<div><strong>Phone</strong><br><a href="tel:{PHONE_TEL}">{PHONE}</a></div></div>
<div class="contact-item"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg><div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="contact-item"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><div><strong>Location</strong><br>{CITY}<br><span class="muted">Serving the greater Seattle area</span></div></div>
<div class="contact-item"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><div><strong>Hours</strong><br>Mon&ndash;Fri, 9am&ndash;6pm</div></div>
</div></div></section>''')

exec(open(os.path.join(ROOT, "pages_unique.py")).read())
exec(open(os.path.join(ROOT, "growth.py")).read())

# ---------------------------------------------------------------- layout
CSS = open(os.path.join(ROOT, "src", "styles.css")).read()
import hashlib
CSS_VER = hashlib.md5(CSS.encode()).hexdigest()[:8]  # cache-buster: browsers fetch new CSS after every change

def nav_html(active):
    items = ""
    for slug, label in NAV:
        cls = ' class="active"' if slug == active or (label == "Services" and active in [s for s, _, _ in SERVICE_PAGES]) else ""
        items += f'<li><a href="{slug}.html"{cls}>{label}</a></li>'
    return items

def layout(slug, title, body, logo_src, css_tag, logo_dark_src):
    t = f"{NAME} | {title}" if slug != "index" else f"{NAME} | {title}"
    svc_links = "".join(f'<li><a href="{s}.html">{t2}</a></li>' for s, t2, _ in SERVICE_PAGES)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{seo_head(slug, title)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{css_tag}</head><body>
<header><div class="wrap nav"><a class="logo" href="index.html"><img src="{logo_dark_src}" alt="{NAME}" width="71" height="46"></a>
<button class="menu-btn" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button><ul class="menu">{nav_html(slug)}<li class="menu-cta"><a class="btn" href="contact.html">Book a consultation</a><a class="menu-tel" href="tel:{PHONE_TEL}">{PHONE}</a></li></ul>
<a class="btn small nav-cta" href="contact.html">Book a consultation</a></div></header>
<main>{body}</main>
<div class="mobile-bar"><a class="mb-call" href="tel:{PHONE_TEL}">Call</a><a class="mb-book" href="contact.html">Book a consultation</a></div>
<footer><div class="wrap foot-grid">
<div><img class="foot-logo" src="{logo_dark_src}" alt="{NAME}" width="460" height="297" loading="lazy"><p>{NAME}<br>Based in {CITY}. Taxes, business formation and bookkeeping in all 50 states. Commercial insurance for Washington businesses.</p></div>
<div><h4>Services</h4><ul class="plain">{svc_links}</ul></div>
<div><h4>Company</h4><ul class="plain"><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="tools.html">Free tools</a></li><li><a href="areas.html">Areas we serve</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li></ul></div>
<div><h4>Contact</h4><p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>{CITY}<br>{HOURS}<br>Serving all 50 states</p></div>
</div><div class="wrap copy">&copy; <span class="year"></span> {NAME}. All rights reserved.</div></footer>
'''

SITE_JS = '''<script>

(function(){document.querySelectorAll('.hero-lines').forEach(function(c){var x=c.getContext('2d');function d(){var r=c.parentNode.getBoundingClientRect();if(!r.width)return;var dpr=window.devicePixelRatio||1;c.width=r.width*dpr;c.height=r.height*dpr;x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,r.width,r.height);
x.lineWidth=1;for(var i=0;i<22;i++){var off=i*34;x.strokeStyle='rgba(91,150,235,'+(0.05+0.18*(1-i/22))+')';x.beginPath();x.moveTo(r.width*0.52-off,r.height+20);x.lineTo(r.width*0.80-off*0.15,r.height*0.18+i*6);x.lineTo(r.width+40,r.height*0.48+i*14);x.stroke();}}
d();window.addEventListener('resize',d);c._draw=d;});})();
document.querySelector('.menu-btn').addEventListener('click',function(){var o=document.body.classList.toggle('nav-open');this.setAttribute('aria-expanded',o)});
document.querySelectorAll('.year').forEach(e=>e.textContent=new Date().getFullYear());
</script></body></html>'''

def build_site():
    out = os.path.join(ROOT, "site")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, "img"))
    for f in ["kfg-logo.png", "kfg-logo-dark-bg.png"]:
        shutil.copy(os.path.join(ROOT, "img", f), os.path.join(out, "img", f))
    open(os.path.join(out, "styles.css"), "w").write(CSS)
    for slug, (title, body) in PAGES.items():
        body = body.replace('src="LOGO_DARK"', 'src="img/kfg-logo-dark-bg.png"')
        html = layout(slug, title, body, "img/kfg-logo.png", f'<link rel="stylesheet" href="styles.css?v={CSS_VER}">', "img/kfg-logo-dark-bg.png") + SITE_JS
        open(os.path.join(out, f"{slug}.html"), "w").write(html)
    nf = layout("404", "Page not found", NOT_FOUND, "img/kfg-logo.png", f'<link rel="stylesheet" href="styles.css?v={CSS_VER}">', "img/kfg-logo-dark-bg.png") + SITE_JS
    nf = nf.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')
    nf = re.sub(r'(href|src)="(?!https?:|tel:|mailto:|#|/)([^"]+)"', r'\1="/\2"', nf)  # 404 can be served at any path
    open(os.path.join(out, "404.html"), "w").write(nf)
    make_brand_images(os.path.join(out, "img"))
    write_seo_files(out)

def build_preview():
    """Single HTML file: every page is a <div data-page>, links become #hash routes."""
    b64 = lambda f: "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "img", f), "rb").read()).decode()
    logo, logo_dark = "LOGO_LIGHT", "LOGO_DARK"
    pages_html = ""
    shell = None
    for slug, (title, body) in PAGES.items():
        full = layout(slug, title, body, logo, f"<style>{CSS}</style>", logo_dark)
        head, rest = full.split("<body>", 1)
        if shell is None:
            shell = head
        rest = re.sub(r'href="#(start|tool-list)"', r'href="javascript:void(0)" data-scroll="\1"', rest)
        rest = re.sub(r'href="([a-z-]+)\.html"', lambda m: f'href="#{"home" if m.group(1)=="index" else m.group(1)}"', rest)
        pid = "home" if slug == "index" else slug
        pages_html += f'<div class="pv-page" data-page="{pid}" data-title="{_html.escape(page_title(slug, title), quote=True)}" hidden>{rest}</div>\n'
    js = '''<script>
function show(){var id=(location.hash||'#home').slice(1);var pg=document.querySelector('[data-page="'+id+'"]')||document.querySelector('[data-page="home"]');
document.querySelectorAll('.pv-page').forEach(function(p){p.hidden=p!==pg});document.title=pg.dataset.title;window.scrollTo({top:0,behavior:'instant'});}
window.addEventListener('hashchange',show);show(); (function(){document.querySelectorAll('.hero-lines').forEach(function(c){var x=c.getContext('2d');function d(){var r=c.parentNode.getBoundingClientRect();if(!r.width)return;var dpr=window.devicePixelRatio||1;c.width=r.width*dpr;c.height=r.height*dpr;x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,r.width,r.height); x.lineWidth=1;for(var i=0;i<22;i++){var off=i*34;x.strokeStyle='rgba(91,150,235,'+(0.05+0.18*(1-i/22))+')';x.beginPath();x.moveTo(r.width*0.52-off,r.height+20);x.lineTo(r.width*0.80-off*0.15,r.height*0.18+i*6);x.lineTo(r.width+40,r.height*0.48+i*14);x.stroke();}} d();window.addEventListener('resize',d);c._draw=d;});})(); window.addEventListener('hashchange',function(){document.querySelectorAll('.hero-lines').forEach(function(c){c._draw&&c._draw()})});
document.addEventListener('click',function(e){var j=e.target.closest('[data-scroll]');if(j){var t=j.closest('.pv-page').querySelector('#'+j.dataset.scroll);if(t)t.scrollIntoView({behavior:'smooth'});return;}var b=e.target.closest('.menu-btn');if(b){var o=document.body.classList.toggle('nav-open');b.setAttribute('aria-expanded',o);}
if(e.target.closest('.menu a')){document.body.classList.remove('nav-open');}});
document.querySelectorAll('.year').forEach(function(e){e.textContent=new Date().getFullYear()});
document.querySelectorAll('form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.form-note');
n.hidden=false;n.textContent='Preview only: this form is not connected yet. It will deliver messages to info@kaplunfinancial.com once the site is live.';});});
</script></body></html>'''
    os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
    html = shell + "<body>\n" + pages_html + js
    # inline each logo once, reuse via CSS vars to keep file small
    html = html.replace('<img src="LOGO_DARK"', '<img class="logo-src" src="' + b64("kfg-logo-dark-bg.png") + '"', 1)
    html = html.replace('src="LOGO_DARK"', 'src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" data-logo="dark"')
    html = html.replace("</body></html>", "<script>var D=document.querySelector('.logo-src').src;document.querySelectorAll('[data-logo]').forEach(function(i){i.src=D});</script></body></html>")
    open(os.path.join(ROOT, "preview", "index.html"), "w").write(html)

if __name__ == "__main__":
    build_site()
    build_preview()
    print("built", len(PAGES), "pages")
