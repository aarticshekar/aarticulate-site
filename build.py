# aarticulate.co static build. python3 build.py -> out/
import os, re, html, json, shutil, glob, hashlib, markdown
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
OUT = 'out'; SITE = 'https://aarticulate.co'; E = html.escape
BRIEF = 'https://aarticshekar.substack.com/s/the-integration-layer'
LINKEDIN = 'https://www.linkedin.com/in/aarticshekar'
ESSAYS = 'https://www.aarti.blog/the-essays/'
CSS = open('style.css').read(); CSSV = hashlib.md5(CSS.encode()).hexdigest()[:8]
LENSES = [("The Integration Problem", "Why most revenue issues sit in the seams, not in a department."),
          ("The Handoff", "Where leads, deals and customers get dropped between teams."),
          ("The Tech Layer", "CRM and tools people still use after go-live."),
          ("The Transformation", "Changing how a revenue team works without breaking it."),
          ("The Operator's Mind", "How good RevOps people think in week one.")]
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# ---------- posts
POSTS = []
for f in glob.glob('posts/*.md'):
    raw = open(f).read(); head, body = raw.split('\n---\n', 1)
    meta = dict(l.split(': ', 1) for l in head.strip().split('\n'))
    faq = []
    if '\n=== FAQ\n' in body:
        body, fq = body.split('\n=== FAQ\n', 1)
        faq = [l.split('|', 1) for l in fq.strip().split('\n') if '|' in l]
    words = len(re.findall(r'\w+', body))
    POSTS.append(dict(meta, slug=os.path.basename(f)[:-3], body=body, faq=faq, mins=max(3, round(words / 230))))
POSTS = [p for p in POSTS if p.get('draft') != 'yes']
POSTS.sort(key=lambda p: int(p['order']))

def md(s): return markdown.markdown(s, extensions=['tables'])

NAV = [("Writing", "/writing/"), ("About", "/about/"), ("The Integration Brief", "/the-integration-brief/")]
def head(title, desc, path, schema=(), noindex=False, img='/covers/og-home.jpg'):
    nav = ''.join(f'<a href="{u}"{" aria-current=page" if path.startswith(u) else ""}>{n}</a>' for n, u in NAV)
    sch = ''.join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schema)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{SITE}{path}">
{'<meta name="robots" content="noindex">' if noindex else ''}<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/s.css?v={CSSV}">{sch}</head><body>
<header class="top"><div class="wrap topin"><a class="logo" href="/">Aarticulate<span class="dot"></span></a><nav>{nav}</nav></div></header>'''
SIGN = f'''<section class="brief"><div class="wrap briefin"><div><p class="k">The Integration Brief</p><h2>One gap a week, named precisely, with what to do about it.</h2>
<p>For founders, revenue leaders and the partners who implement their systems. Free. Unsubscribe in one click.</p></div>
<a class="btn" href="{BRIEF}">Subscribe on Substack</a></div></section>'''
FOOT = SIGN + f'''<footer class="foot"><div class="wrap footin"><div><a class="logo" href="/">Aarticulate<span class="dot"></span></a>
<p>Aarticulate is part of The Ocean Life, a family of writing by Aarti Chandrseker.</p></div>
<div class="fl"><a href="{LINKEDIN}">LinkedIn</a><a href="{BRIEF}">Substack</a><a href="{ESSAYS}">Personal essays</a><a href="/start/">Start here</a><a href="/privacy/">Privacy</a></div></div>
<div class="wrap copy">&copy; Aarti Chandrseker 2026</div></footer></body></html>'''
STRIP = f'<a class="strip" href="{BRIEF}"><span class="sk">Free</span><span class="st">The Integration Brief: one gap a week between sales, marketing, CS and tech.</span><span class="sg">Subscribe &rarr;</span></a>'

URLS = []
def write(path, htmlstr):
    p = OUT + path + ('index.html' if path.endswith('/') else '')
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(htmlstr)
    if path.endswith('/'): URLS.append(path)

def card(p):
    return f'''<a class="card" href="/writing/{p["slug"]}/"><img src="/covers/{p["slug"]}.jpg" alt="" width="1600" height="900" loading="lazy"><span class="lens">{E(p["lens"])}</span><h3>{E(p["title"])}</h3><p>{E(p["desc"].split(". ")[0])}.</p><span class="meta">{p["mins"]} min read</span></a>'''

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
open(f'{OUT}/s.css', 'w').write(CSS); shutil.copytree('static/covers', f'{OUT}/covers')
open(f'{OUT}/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#1F5C63"/><text x="16" y="23" text-anchor="middle" font-family="Georgia,serif" font-size="20" fill="#F6F1EA">A</text><circle cx="25" cy="22" r="2.6" fill="#BE7C68"/></svg>')

person = {"@context": "https://schema.org", "@type": "Person", "name": "Aarti Chandrseker", "url": SITE, "jobTitle": "CRM Transformation and RevOps", "sameAs": [LINKEDIN]}


READ = [("Founders", "Your business works, but only when you're in the room. Your teams blame each other, and the tools you bought aren't helping.", ["integration-problem", "more-to-crm-than-data-logging"]),
        ("Revenue leaders", "You've inherited a CRM nobody trusts, a forecast nobody believes, and handoffs that leak.", ["customer-is-king", "your-client-isnt-difficult"]),
        ("Implementation partners", "You know the platform. It's the space between the platform and the people that keeps biting you.", ["your-client-isnt-difficult", "more-to-crm-than-data-logging"])]
BYSLUG = {p['slug']: p for p in POSTS}
def readers():
    out = []
    for n, d, sl in READ:
        links = ''.join(f'<a href="/writing/{x}/">{E(BYSLUG[x]["title"])} &rarr;</a>' for x in sl if x in BYSLUG)
        out.append(f'<div class="rd"><h3>{E(n)}</h3><p>{E(d)}</p><div class="rl">{links}</div></div>')
    return '<section class="wrap sec"><p class="k">Who I write for</p><h2 class="rh">Start with the path that sounds like you.</h2><div class="readers">' + ''.join(out) + '</div></section>'

# ---------- home
write('/', head("Aarticulate | Your revenue problem is an integration problem", "Aarti Chandrseker writes about the gaps between sales, marketing, customer success and technology, where revenue actually falls through.", '/', [person]) + f'''
<main><section class="hero"><div class="wrap"><p class="k">Aarticulate</p><h1>Your revenue problem is an <em>integration</em> problem.</h1>
<p class="lede">Sales blames marketing. Marketing blames the data. Customer success hears about churn last. I write about the gaps between your teams, because that's where revenue actually falls through.</p>
<div class="ctas"><a class="btn light" href="{BRIEF}">Get The Integration Brief</a><a class="btn ghost" href="/writing/">Read the writing</a></div></div></section>
<section class="wrap sec"><p class="k">Sound familiar?</p><div class="three">
<div class="q">The quarterly review turned into a blame session.</div><div class="q">You bought the tool. Six months later, the team is back in Excel.</div><div class="q">The business works, but only when you're in the room.</div></div>
<p class="after">If any of these landed, start with <a href="/writing/{POSTS[0]["slug"]}/">{E(POSTS[0]["title"])}</a></p></section>
{readers()}
<section class="wrap sec"><div class="sh"><h2>Latest writing</h2><a href="/writing/">All writing</a></div><div class="grid">{''.join(card(p) for p in POSTS[:3])}</div></section>
<section class="wrap sec"><p class="k">Five lenses I write through</p><div class="lenses">{''.join(f'<div><h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, d in LENSES)}</div></section>
<section class="proof"><div class="wrap"><p class="k">Proof, not enthusiasm</p><ul class="pl">
<li><b>60+</b><span>countries in a Salesforce Service Cloud transformation</span></li><li><b>200+</b><span>users on Sales and Marketing Cloud across APAC and MEA</span></li>
<li><b>40%</b><span>lift in MQL to SQL conversion, and in CRM engagement</span></li><li><b>20 to 30%</b><span>faster sales cycles across engagements</span></li>
<li><b>From scratch</b><span>APAC sales ops and an IMEA commercial function</span></li></ul></div></section></main>''' + FOOT)

# ---------- writing
used = [n for n, _ in LENSES if any(p['lens'] == n for p in POSTS)]
write('/writing/', head("Writing | Aarticulate", "Field notes from the space between sales, marketing, customer success and technology.", '/writing/') + f'''
<main class="wrap"><section class="intro"><h1>Writing</h1><p class="lede">Field notes from the space between your teams.</p>
<label class="vh" for="q">Search</label><input id="q" class="search" type="search" placeholder="Search the writing" autocomplete="off"><div class="filt" role="group" aria-label="Filter by lens"><button data-l="all" aria-pressed="true">All</button>{''.join(f'<button data-l="{slugify(n)}" aria-pressed="false">{E(n)}</button>' for n in used)}</div></section>
{STRIP}<div class="grid wl">{''.join(card(p).replace('class="card"', f'class="card" data-l="{slugify(p["lens"])}" data-t="{E((p["title"]+" "+p["desc"]+" "+p["lens"]).lower())}"') for p in POSTS)}</div>
<p class="more">More short pieces live in <a href="{BRIEF}">The Integration Layer on Substack</a>.</p></main>
<p class="none" hidden>Nothing yet on that. Try another word, or <a href="{BRIEF}">get The Integration Brief</a>.</p>
<script>let L='all';const q=document.getElementById('q');function f(){{const t=q.value.trim().toLowerCase();let n=0;document.querySelectorAll('.wl .card').forEach(c=>{{const ok=(L==='all'||c.dataset.l===L)&&(!t||c.dataset.t.includes(t));c.hidden=!ok;if(ok)n++}});document.querySelector('.none').hidden=n>0}}
q.oninput=f;document.querySelectorAll('.filt button').forEach(b=>b.onclick=()=>{{L=b.dataset.l;document.querySelectorAll('.filt button').forEach(x=>x.setAttribute('aria-pressed',x===b));f()}})</script>''' + FOOT)

# ---------- posts
for i, p in enumerate(POSTS):
    path = f'/writing/{p["slug"]}/'
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p['title'], "description": p['desc'], "author": person, "mainEntityOfPage": SITE + path}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    rel = [x for x in POSTS if x is not p][:2]
    faqh = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faq'])
    write(path, head(f"{p['seo']} | Aarticulate", p['desc'], path, [art, fq] if p['faq'] else [art], img=f"/covers/{p['slug']}.jpg") + f'''
<main class="wrap"><article class="post"><a class="back" href="/writing/">Writing</a><span class="lens">{E(p["lens"])} &middot; {p["mins"]} min read</span><h1>{E(p["title"])}</h1><p class="stand">{E(p["desc"])}</p><img class="cover" src="/covers/{p["slug"]}.jpg" alt="{E(p["title"])}" width="1600" height="900">{STRIP}
<div class="body">{md(p["body"])}</div>{f'<section class="faq"><h2>Questions people ask</h2>{faqh}</section>' if faqh else ''}
<p class="by">Written by <a href="/about/">Aarti Chandrseker</a>, who works on CRM transformation and RevOps.</p></article>
<section class="sec"><div class="sh"><h2>Read next</h2><a href="/writing/">All writing</a></div><div class="grid two">{''.join(card(x) for x in rel)}</div></section></main>''' + FOOT)

# ---------- simple pages
PAGES = {
'/about/': ("About | Aarticulate", "Aarti Chandrseker works on CRM transformation and RevOps, and writes about the gaps between teams.", f'''<p class="k">About</p><h1>I started out selling door to door.</h1>
<p class="lede">You learn fast that a no is usually a broken process, not a broken person.</p>
<p>From there I moved into recruitment and HR, then marketing, sales enablement and CRM, and finally RevOps. Different titles, the same job every time: getting sales, marketing, customer success and technology to work as one, and getting people who don't usually sit together into the same room until the work gets done.</p>
<p>The moment it clicked was a quarterly review. Sales blamed marketing. Marketing blamed the data. Customer success heard about churn last. Nobody was failing. The system between them was.</p>
<p>That's the work I care about: sales and marketing married to technology, done well enough that the customer feels it. Not more tools. Fewer gaps.</p>
<p>Along the way I built a commercial function across India, the Middle East and Africa at GlobalData, where I was named Employee of the Year. I worked on pipeline intelligence for IBM DACH, and led CRM transformation at VFS Global across 60+ countries. I'm a certified Salesforce Administrator, Business Analyst and Agentforce Specialist, based in Dubai.</p>
<h2>Who I write for</h2><p>Founders whose business only works when they're in the room. Revenue leaders inheriting a CRM nobody trusts. And the implementation partners who get handed both.</p>
<h2>Off the clock</h2><p>Aarticulate is part of The Ocean Life, a family of writing by Aarti Chandrseker. I also write personal essays on life, motherhood and becoming at <a href="{ESSAYS}">aarti.blog</a>.</p>
<p><a class="btn" href="{LINKEDIN}">Connect on LinkedIn</a></p>'''),
'/the-integration-brief/': ("The Integration Brief | Aarticulate", "One email a week. One gap between sales, marketing, customer success and tech, named precisely, with what to do about it.", f'''<p class="k">Newsletter</p><h1>The Integration Brief</h1>
<p class="lede">One email a week. One gap, named precisely, with what to do about it.</p>
<p>For founders, revenue leaders and the partners who implement their systems. You get one idea a week from the field, the piece behind it, and nothing to buy. Unsubscribe in one click.</p>
<p><a class="btn" href="{BRIEF}">Subscribe on Substack</a></p><p class="fine">It's free, and it lives in The Integration Layer section of my Substack.</p>'''),
'/start/': ("Start here | Aarticulate", "New here? Where to begin with Aarti Chandrseker's writing on RevOps, CRM and customer experience.", f'''<p class="k">Start here</p><h1>Hi, I'm Aarti.</h1>
<p class="lede">I work on CRM transformation and RevOps, and I write about the gaps between sales, marketing, customer success and tech.</p>
<div class="links">
<a href="/writing/{POSTS[0]["slug"]}/"><b>New here? Read this first</b><span>{E(POSTS[0]["title"])}</span></a>
<a href="{BRIEF}"><b>Get one gap a week</b><span>The Integration Brief, free on Substack</span></a>
<a href="/writing/"><b>Browse by problem</b><span>Handoffs, CRM adoption, discovery, customer experience</span></a>
<a href="{ESSAYS}"><b>Off the clock</b><span>Personal essays on life, motherhood and becoming, at aarti.blog</span></a>
<a href="{LINKEDIN}"><b>Say hello</b><span>Connect on LinkedIn</span></a></div>'''),
'/privacy/': ("Privacy | Aarticulate", "Privacy policy for aarticulate.co.", '''<h1>Privacy</h1><p>This site uses no advertising cookies and no tracking scripts.</p>
<p>If you subscribe to The Integration Brief, Substack holds your email address and uses it only to send the newsletter. Its own privacy policy applies.</p>
<p>If a page ever recommends a tool through an affiliate link, that page will say so.</p>'''),
}
for path, (t, d, b) in PAGES.items():
    write(path, head(t, d, path) + f'<main class="wrap"><div class="prose">{b}</div></main>' + (FOOT if path != '/start/' else FOOT.replace(SIGN, '')))
write('/404.html'.replace('.html', '/')[:-1] + '.html' if False else '/404/', head("Not found | Aarticulate", "Page not found.", '/404/', noindex=True) + '<main class="wrap"><div class="prose"><h1>That page has gone missing.</h1><p><a href="/writing/">Try the writing</a>.</p></div></main>' + FOOT)
URLS.remove('/404/'); shutil.copy(f'{OUT}/404/index.html', f'{OUT}/404.html')
open(f'{OUT}/robots.txt', 'w').write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc></url>' for u in URLS) + '</urlset>')
open(f'{OUT}/.htaccess', 'w').write("DirectoryIndex index.html\nErrorDocument 404 /404.html\n<IfModule mod_rewrite.c>\nRewriteEngine Off\n</IfModule>\n")
print(len(URLS), 'pages,', len(POSTS), 'posts')
