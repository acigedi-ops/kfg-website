# Unique layouts for About, Industries, FAQ, Contact and each service page.
# Executed inside build.py (shares its globals: PAGES, icon, cta, checklist, SERVICE_PAGES, SVC_FEATURES, FAQ_CATS, ...).

FAQ_BY_ID = {cid: (label, ic, qs) for cid, label, ic, qs in FAQ_CATS}

def head_split(title, lead, visual, crumb=None, kicker=None):
    c = f'<p class="crumb"><a href="services.html">Services</a> / {crumb}</p>' if crumb else ""
    k = f'<span class="pill-badge"><span class="dot"></span>{kicker}</span>' if kicker else ""
    if crumb and kicker: k = '<br>' + k
    return f'''<section class="page-head split-head"><div class="glow g1"></div><div class="gridbg"></div>
<div class="wrap ph-grid"><div>{c}{k}<h1>{title}</h1><p class="lead">{lead}</p>
<div class="btns"><a class="btn" href="contact.html">Book a consultation <span class="arr">&rarr;</span></a><a class="btn glass" href="tel:{PHONE_TEL}">Call {PHONE}</a></div></div>
<div class="ph-visual">{visual}</div></div></section>'''

def vcard(slug):
    _, _, _, (vt, rows) = SVC_FEATURES[slug]
    r = "".join(f'<div class="vrow"><span class="vk">{k}</span><span>{v}</span><span class="vchk"></span></div>' for k, v in rows)
    return f'<div class="vcard"><p class="vtitle">{vt}</p>{r}</div>'

def faq_list(items, cls=""):
    return f'<div class="qa {cls}">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

# ------------------------------------------------------------ service-specific sections
def sx_tax_prep():
    dates = [("Jan", "15", "Q4 estimated tax payment", "Prior year"),
             ("Mar", "15", "Partnerships (1065) and S corps (1120-S)", "Business"),
             ("Apr", "15", "Individuals (1040), C corps (1120) and Q1 estimate", "Main deadline"),
             ("Jun", "15", "Q2 estimated tax payment", "Estimate"),
             ("Sep", "15", "Q3 estimate and extended 1065 / 1120-S", "Extension"),
             ("Oct", "15", "Extended 1040 and 1120 returns", "Extension")]
    cells = "".join(f'<div class="cal{" hot" if t=="Main deadline" else ""}"><div class="cal-d"><span>{m}</span><strong>{d}</strong></div><div><em>{t}</em><p>{x}</p></div></div>' for m, d, x, t in dates)
    return f'''<section class="soft"><div class="wrap"><div class="sec-head"><span class="kicker">Key dates</span><h2>The federal tax calendar</h2>
<p class="lead">Typical deadlines for calendar-year filers. When a date falls on a weekend or holiday, it moves to the next business day. We track all of them for you.</p></div>
<div class="cal-grid">{cells}</div></div></section>'''

def sx_tax_planning():
    qs = [("Q1", "Jan to Mar", "Review last year, project this year, set estimated payments."),
          ("Q2", "Apr to Jun", "Check entity and owner pay. Consider an S corp election if it fits."),
          ("Q3", "Jul to Sep", "Mid-year true-up of income, expenses and estimates."),
          ("Q4", "Oct to Dec", "Year-end moves: purchases, retirement contributions, timing.")]
    nodes = "".join(f'<div class="tl-node"><span class="tl-dot">{q}</span><small>{w}</small><p>{t}</p></div>' for q, w, t in qs)
    return f'''<section class="dark-band"><div class="glow g1"></div><div class="wrap"><div class="sec-head"><span class="kicker dk">Year-round</span><h2>Your planning year with KFG</h2>
<p class="lead">Planning works because it happens before the year closes, not after.</p></div>
<p class="swipe-hint">Swipe to see more &rarr;</p><div class="timeline">{nodes}</div></div></section>'''

def sx_formation():
    steps = [("Pick your structure", "LLC, corporation or S corp, chosen around your taxes and goals."),
             ("File with the state", "Formation documents with the Secretary of State in any of the 50 states, plus a registered agent."),
             ("Get your EIN", "Your federal tax ID from the IRS, needed for banking and payroll."),
             ("Register and license", "State and local business licenses and tax registrations wherever you operate."),
             ("Industry permits", "Health permits, liquor licenses, dealer licenses and more, as your business requires."),
             ("Stay compliant", "Annual reports, renewals and tax registrations tracked for you.")]
    st = "".join(f'<li><span class="sn">{i+1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(steps))
    return f'''<section class="soft"><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Step by step</span><h2>From idea to open for business</h2>
<p class="lead">We handle each step in the right order, so you are not stuck waiting on one office because another step came first.</p></div>
<p class="swipe-hint">Swipe to see more &rarr;</p><ol class="stepper">{st}</ol></div></section>'''

def sx_bookkeeping():
    bars = [("Jan", 52), ("Feb", 61), ("Mar", 58), ("Apr", 72), ("May", 80), ("Jun", 76)]
    b = "".join(f'<div class="bar"><span style="height:{h}%"></span><small>{m}</small></div>' for m, h in bars)
    return f'''<section class="soft"><div class="wrap split"><div><span class="kicker">What you get</span><h2>Know your numbers every month</h2>
<p class="lead">Each month your books are reconciled and you receive clear reports, so you can make decisions with real numbers instead of guesses.</p>
<ul class="mini-list"><li>Profit &amp; loss statement</li><li>Balance sheet</li><li>Bank and card reconciliations</li><li>Quarterly filing reminders</li></ul></div>
<div class="report"><div class="rep-head"><div><small>Sample report</small><strong>Profit &amp; Loss</strong></div><span class="tag ok">Reconciled</span></div>
<div class="bars">{b}</div>
<div class="rep-rows"><div><span>Revenue</span><strong class="up">Trending up</strong></div><div><span>Expenses</span><strong>Categorized</strong></div><div><span>Quarterly taxes</span><strong>Filed on time</strong></div></div>
<p class="rep-note">Illustration only.</p></div></div></section>'''

def sx_insurance():
    cols = ["Restaurants", "Dealerships", "Retail", "Offices"]
    rows = [("General liability", "1111"), ("Commercial property", "1111"), ("Business owner's policy", "1012"),
            ("Commercial auto", "0100"), ("Liquor liability", "2000"), ("Garage / dealer coverage", "0100"),
            ("Professional liability", "0002"), ("Umbrella", "2222")]
    sym = {"1": '<span class="m yes" title="Common"></span>', "2": '<span class="m maybe" title="Often"></span>', "0": '<span class="m no"></span>'}
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join(f'<tr><th scope="row">{r}</th>' + "".join(f"<td>{sym[x]}</td>" for x in v) + "</tr>" for r, v in rows)
    return f'''<section class="soft"><div class="wrap"><div class="sec-head"><span class="kicker">Coverage guide</span><h2>What businesses like yours usually carry</h2>
<p class="lead">For Washington businesses. A starting point, not a quote. Every business is different, so we review your situation before recommending coverage.</p></div>
<div class="matrix-wrap"><table class="matrix"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>
<div class="legend"><span><span class="m yes"></span>Common</span><span><span class="m maybe"></span>Often needed</span></div></div></section>'''

SVC_EXTRA = {"tax-preparation": (sx_tax_prep, "individual"), "tax-planning": (sx_tax_planning, "planning"),
             "business-formation": (sx_formation, "formation"), "bookkeeping": (sx_bookkeeping, "bookkeeping"),
             "commercial-insurance": (sx_insurance, "insurance")}

def service_page(slug):
    title, lead, intro, includes, who = SERVICE_ARGS[slug]
    fn, fcat = SVC_EXTRA[slug]
    flabel, _, fqs = FAQ_BY_ID[fcat]
    other = "".join(f'<a class="os" href="{s}.html">{icon(s)}<span>{t}</span></a>' for s, t, _ in SERVICE_PAGES if s != slug)
    where = "Available for Washington businesses" if slug == "commercial-insurance" else f"Available in all 50 states &middot; Based in {CITY}"
    return head_split(title, lead, vcard(slug), crumb=title, kicker=where) + f'''
<section><div class="wrap split-top"><div><span class="kicker">Overview</span><p class="intro big">{intro}</p>
<div class="who"><strong>Who it's for</strong><p>{who}</p></div></div>
<div><h2 class="h-sm">What's included</h2>{checklist(includes)}</div></div></section>''' + fn() + f'''
<section><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Questions</span><h2>{flabel}: common questions</h2>
<p class="lead">Quick answers to what clients ask us most.</p><a class="more" href="faq.html">See all FAQs &rarr;</a></div>
{faq_list(fqs[:5])}</div></section>
<section class="other-sec"><div class="wrap"><p class="os-label">Explore other services</p><div class="os-row">{other}</div></div></section>''' + cta()

for s, _, _ in SERVICE_PAGES:
    PAGES[s] = (PAGES[s][0], service_page(s))

# ------------------------------------------------------------ industries explorer
INDUSTRIES = [
 ("restaurants", "Restaurants & food service", "restaurant",
  "From your first health permit to your hundredth payroll, we keep your restaurant compliant and profitable.",
  {"Taxes": ["Business returns for your entity", "Sales tax on food and drinks", "State and local business taxes", "Tip reporting guidance"],
   "Licensing": ["State and city business licenses", "Food establishment permit", "Liquor license applications", "Renewals tracked"],
   "Bookkeeping": ["Monthly books and reconciliations", "Food and labor cost tracking", "Quarterly filings"],
   "Insurance": ["General liability", "Property and equipment", "Liquor liability", "Business interruption"]}),
 ("dealerships", "Car dealerships", "car",
  "Dealer licensing, entity setup, clean books and the coverage a lot full of vehicles needs.",
  {"Taxes": ["Corporate and partnership returns", "Sales tax on vehicle sales", "State and local business taxes", "Owner tax planning"],
   "Licensing": ["Entity formation", "Dealer license support with your state", "Surety bond coordination", "State and city licenses"],
   "Bookkeeping": ["Inventory and floor plan tracking", "Deal-by-deal records", "Monthly reporting"],
   "Insurance": ["Garage and dealer coverage", "Commercial auto", "General liability", "Property coverage"]}),
 ("retail", "Retail stores", "store",
  "Registration, sales tax and storefront protection, so you can focus on customers.",
  {"Taxes": ["Business returns", "Sales tax collection and filing", "State and local business taxes", "Inventory and cost of goods"],
   "Licensing": ["Business entity setup", "State business license and reseller permit", "City license", "Annual reports"],
   "Bookkeeping": ["Monthly books", "Sales and inventory reconciliation", "Quarterly filings"],
   "Insurance": ["Business owner's policy", "General liability", "Property and inventory", "Commercial umbrella"]}),
 ("startups", "Startups & new businesses", "rocket",
  "Start right: the correct structure, every filing, and a plan for your first tax year.",
  {"Taxes": ["Choosing how you are taxed", "First-year tax planning", "Estimated payments setup", "S corp election review"],
   "Licensing": ["LLC or corporation formation", "EIN registration", "State and city licenses", "Industry permits"],
   "Bookkeeping": ["Books set up from day one", "Software setup", "Monthly reporting"],
   "Insurance": ["General liability", "Coverage required by landlords and clients", "Policy reviews as you grow"]}),
 ("corporations", "Partnerships & corporations", "building",
  "Multi-owner businesses need returns, K-1s and planning that all line up. We make sure they do.",
  {"Taxes": ["Form 1065 partnership returns", "Form 1120-S and 1120 returns", "K-1s for every owner", "Owner compensation planning"],
   "Licensing": ["Annual reports", "Ownership changes and amendments", "New locations and licenses"],
   "Bookkeeping": ["Monthly books and statements", "Owner distributions tracking", "Year-end close"],
   "Insurance": ["General liability", "Property", "Professional liability", "Umbrella"]}),
 ("individuals", "Self-employed & individuals", "person",
  "Freelancers, gig workers and families: accurate returns and fewer surprises.",
  {"Taxes": ["Form 1040 returns", "Schedule C for the self-employed", "Prior-year and amended returns", "IRS letter help"],
   "Licensing": ["Forming an LLC when it makes sense", "Business license if you need one"],
   "Bookkeeping": ["Simple expense tracking", "Mileage and deduction records", "Quarterly estimate reminders"],
   "Insurance": ["Coverage for your side business", "Policy reviews"]}),
]
COL_ICON = {"Taxes": "tax-preparation", "Licensing": "business-formation", "Bookkeeping": "bookkeeping", "Insurance": "commercial-insurance"}

def industries_page():
    tabs = "".join(f'<button class="ind-tab{" on" if i==0 else ""}" data-ind="{k}">{icon(ic)}<span>{n}</span></button>' for i, (k, n, ic, _, _) in enumerate(INDUSTRIES))
    panels = ""
    for i, (k, n, ic, tag, cols) in enumerate(INDUSTRIES):
        cc = "".join(f'<div class="ind-col"><div class="ic-h"><span class="mini">{icon(COL_ICON[c])}</span><strong>{c}</strong></div><ul>' + "".join(f"<li>{x}</li>" for x in items) + '</ul></div>' for c, items in cols.items())
        panels += f'''<div class="ind-panel" data-ind="{k}"{"" if i==0 else " hidden"}><div class="ip-head"><span class="ip-ico">{icon(ic)}</span><div><h2>{n}</h2><p>{tag}</p></div></div>
<div class="ind-cols">{cc}</div><p class="ind-note">Taxes, formation and bookkeeping are available in all 50 states. Commercial insurance is available for Washington businesses.</p><div class="ip-foot"><span>Run a {n.split(" &")[0].lower().rstrip("s")} business?</span><a class="btn" href="contact.html">Talk to KFG <span class="arr">&rarr;</span></a></div></div>'''
    icons = "".join(f'<span class="orb o{i}">{icon(ic)}</span>' for i, (_, _, ic, _, _) in enumerate(INDUSTRIES))
    js = """<script>document.querySelectorAll('.ind-explorer').forEach(function(w){var t=w.querySelectorAll('.ind-tab');t.forEach(function(b){b.addEventListener('click',function(){t.forEach(function(x){x.classList.toggle('on',x===b)});
w.querySelectorAll('.ind-panel').forEach(function(p){p.hidden=p.dataset.ind!==b.dataset.ind});if(window.innerWidth<1040){var p=w.querySelector('.ind-panel:not([hidden])');if(p){var y=p.getBoundingClientRect().top+window.scrollY-80;window.scrollTo({top:y,behavior:'smooth'});}}});});});</script>"""
    return head_split("Industries we serve", "Every industry has its own permits, tax rules and risks. Pick yours to see exactly how KFG helps, wherever in the US you operate.",
                      f'<div class="orbit">{icons}<span class="orb-core">KFG</span></div>', kicker="Serving businesses in all 50 states") + f'''
<section><div class="wrap"><div class="ind-explorer"><p class="ind-pick">Choose your industry</p><div class="ind-tabs" role="tablist">{tabs}</div><div class="ind-panels">{panels}</div></div></div></section>
<section class="dark-band"><div class="glow g1"></div><div class="wrap split"><div><span class="kicker dk">Don't see yours?</span><h2>We work with businesses of every kind</h2></div>
<p class="lead">Contractors, salons, transportation companies, professional services and more. If you run a business, we can handle your taxes, filings, books and coverage.</p></div></section>''' + js + cta("Let's talk about your business.")

PAGES["industries"] = ("Industries", industries_page())

# ------------------------------------------------------------ FAQ: sidebar layout
def faq_page2():
    total = sum(len(q) for *_, q in FAQ_CATS)
    side_cats = f'<button class="fc on" data-cat="all"><span class="fc-i">{icon("rocket")}</span><span>All questions</span><em>{total}</em></button>' + "".join(
        f'<button class="fc" data-cat="{cid}"><span class="fc-i">{icon(ic)}</span><span>{label}</span><em>{len(qs)}</em></button>' for cid, label, ic, qs in FAQ_CATS)
    groups = ""
    for cid, label, ic, qs in FAQ_CATS:
        items = "".join(f'<details data-cat="{cid}"><summary><span class="qn">{i+1:02d}</span><span class="qt">{q}</span></summary><div class="qa-a"><p>{a}</p></div></details>' for i, (q, a) in enumerate(qs))
        groups += f'<div class="fgroup" data-cat="{cid}"><div class="fg-head"><span class="ico-wrap">{icon(ic)}</span><div><h2>{label}</h2><small>{len(qs)} questions</small></div></div>{items}</div>'
    js = """<script>(function(){document.querySelectorAll('.faq2').forEach(function(w){
var q=w.querySelector('.f-search input'),btns=w.querySelectorAll('.fc'),cat='all',cnt=w.querySelector('.f-count'),empty=w.querySelector('.faq-empty');
function run(){var t=(q.value||'').toLowerCase().trim(),n=0;
w.querySelectorAll('.fgroup').forEach(function(g){var vis=0,okCat=cat==='all'||g.dataset.cat===cat;
g.querySelectorAll('details').forEach(function(d){var ok=okCat&&(!t||d.textContent.toLowerCase().indexOf(t)>-1);d.hidden=!ok;if(ok)vis++;if(t)d.open=ok;});
g.hidden=!vis;n+=vis;});cnt.textContent=n+(n===1?' result':' results');empty.hidden=n>0;}
btns.forEach(function(b){b.addEventListener('click',function(){btns.forEach(function(x){x.classList.toggle('on',x===b)});cat=b.dataset.cat;run();
var m=w.querySelector('.f-main');if(window.innerWidth<1040&&m)m.scrollIntoView({behavior:'smooth',block:'start'});});});
q.addEventListener('input',run);run();});})();</script>"""
    head = f'''<section class="page-head faq-head"><div class="glow g1"></div><div class="gridbg"></div><div class="wrap fh-in">
<span class="pill-badge"><span class="dot"></span>{total} answers, 7 topics</span><h1>How can we help?</h1>
<p class="lead">Search our answers on taxes, business licensing, bookkeeping and commercial insurance.</p>
<div class="f-search big"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><label for="faq-q" class="sr">Search questions</label><input id="faq-q" type="search" placeholder="Try: LLC, extension, sales tax, liability" autocomplete="off" form="none"><span class="f-count"></span></div>
</div></section>'''
    # search box lives in the head; wrap head + body in one .faq2 container so the script can find both
    return f'''<div class="faq2">{head}<section class="faq-body"><div class="wrap faq-layout">
<aside class="f-side"><p class="f-side-t">Topics</p><div class="f-cats">{side_cats}</div>
<div class="f-help"><h3>Still have a question?</h3><p>Call or send us a message and a real person will answer.</p><a class="btn" href="contact.html">Ask KFG</a><a class="f-tel" href="tel:{PHONE_TEL}">{PHONE}</a></div></aside>
<div class="f-main">{groups}<div class="faq-empty" hidden>No questions match your search. Try another word, or <a href="contact.html">ask us directly</a>.</div>
<p class="faq-note">These answers are general information, not tax, legal or insurance advice for your specific situation. Rules and deadlines can change, so contact us about your situation.</p></div>
</div></section></div>''' + js

PAGES["faq"] = ("FAQ", faq_page2())

# ------------------------------------------------------------ About
def about_page():
    usual = "".join(f'<div class="prov">{icon(ic)}<span>{t}</span></div>' for ic, t in [("tax-preparation", "Tax preparer"), ("bookkeeping", "Bookkeeper"), ("business-formation", "Filing service"), ("commercial-insurance", "Insurance agent")])
    vals = [("Clarity", "Plain answers and upfront pricing, before any work begins."), ("Accuracy", "Every return and filing done right the first time."),
            ("Responsiveness", "Real people who pick up the phone and answer emails."), ("Long-term", "Here every quarter, not just in April.")]
    v = "".join(f'<div class="val"><span class="val-n">{i+1:02d}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(vals))
    visual = f'<div class="about-logo"><img src="LOGO_DARK" alt="" class="al-img"><div class="al-tags"><span>Tax</span><span>Formation</span><span>Books</span><span>Insurance</span></div></div>'
    return head_split(f"About {NAME}", f"A one-stop financial partner for individuals and business owners. Based in {CITY}, serving clients in all 50 states.", visual, kicker="Who we are") + f'''
<section><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Our story</span><h2>One team that knows your whole picture</h2></div>
<div class="prose"><p class="intro big">{NAME} brings tax preparation, tax planning, business formation, bookkeeping and commercial insurance together under one roof.</p>
<p>Most business owners juggle an accountant, a filing service, a bookkeeper and an insurance agent who never talk to each other. Things fall through the cracks: a missed quarterly filing, a license that lapsed, a policy that no longer fits.</p>
<p>We built KFG so our clients have one relationship instead. Our office is in Tukwila, Washington, and we work with clients across all 50 states, from individuals filing a single 1040 to restaurants, car dealerships, retail stores and growing companies filing partnership and corporate returns.</p></div></div></section>
<section class="soft"><div class="wrap"><div class="sec-head center"><span class="kicker">The difference</span><h2>Four providers, or one KFG</h2></div>
<div class="compare"><div class="cmp usual"><p class="cmp-t">The usual way</p><div class="provs">{usual}</div>
<ul class="xlist"><li>Four relationships to manage</li><li>Your information repeated four times</li><li>No one sees the full picture</li></ul></div>
<div class="cmp-vs">vs</div>
<div class="cmp kfg"><div class="glow g1"></div><p class="cmp-t">The KFG way</p><div class="kfg-one"><span class="fc-logo">KFG</span><div><strong>One team</strong><small>Taxes, filings, books and coverage</small></div></div>
<ul class="vlist"><li>One point of contact</li><li>Books feed taxes, taxes shape planning</li><li>Deadlines tracked in one place</li></ul></div></div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="kicker">What we value</span><h2>How we work</h2></div><p class="swipe-hint">Swipe to see more &rarr;</p><div class="vals">{v}</div></div></section>''' + cta()

PAGES["about"] = ("About", about_page())

# ------------------------------------------------------------ Contact
def contact_page():
    wq = FAQ_BY_ID["working"][2]
    pick = [q for q in wq if q[0].startswith(("How do I get started", "How much", "Do you work with new"))]
    return f'''<section class="page-head contact-head"><div class="glow g1"></div><div class="gridbg"></div><div class="wrap"><span class="pill-badge"><span class="dot"></span>We usually reply quickly</span>
<h1>Let's talk</h1><p class="lead">Tell us what you need. Taxes, a new company, your books or insurance, we will point you in the right direction.</p></div></section>
<section class="contact-sec"><div class="wrap contact-grid">
<div class="c-panel"><div class="glow g1"></div><div class="c-in"><h2>Reach us directly</h2>
<a class="c-row" href="tel:{PHONE_TEL}"><span class="c-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></span><div><small>Phone</small><strong>{PHONE}</strong></div></a>
<a class="c-row" href="mailto:{EMAIL}"><span class="c-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span><div><small>Email</small><strong>{EMAIL}</strong></div></a>
<div class="c-row"><span class="c-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span><div><small>Location</small><strong>{CITY}</strong><small class="c-sub">Serving clients in all 50 states</small></div></div>
<div class="c-row"><span class="c-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><div><small>Hours</small><strong>Mon&ndash;Fri, 9am&ndash;6pm</strong></div></div>
<p class="c-next-t">What happens next</p><ol class="c-next"><li>We review your message</li><li>We reach out to schedule a consultation</li><li>You get a clear plan and upfront pricing</li></ol></div></div>
<form id="contact-form" class="c-form" action="mailto:{EMAIL}" method="post" enctype="text/plain"><h2>Send a message</h2>
<div><label>I need help with</label><div class="pick">''' + "".join(f'<label class="pk"><input type="checkbox" name="service" value="{t}"><span>{t}</span></label>' for t in ["Tax preparation", "Tax planning", "Business formation", "Permits &amp; licenses", "Bookkeeping", "Commercial insurance"]) + f'''</div></div>
<div class="row2"><div><label for="n">Name</label><input id="n" name="name" required></div><div><label for="p">Phone</label><input id="p" name="phone" type="tel"></div></div>
<div><label for="e">Email</label><input id="e" name="email" type="email" required></div>
<div><label for="m">How can we help?</label><textarea id="m" name="message" rows="5" required placeholder="A few details about your situation"></textarea></div>
<button class="btn" type="submit">Send message <span class="arr">&rarr;</span></button><p id="form-note" class="form-note" hidden></p></form>
</div></section>
<section class="soft"><div class="wrap split-top"><div class="sticky-copy"><span class="kicker">Before you reach out</span><h2>Good to know</h2><a class="more" href="faq.html">See all FAQs &rarr;</a></div>{faq_list(pick)}</div></section>'''

PAGES["contact"] = ("Contact", contact_page())
