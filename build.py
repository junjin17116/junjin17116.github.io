#!/usr/bin/env python3
"""Regenerate all six static pages: python3 build.py. No dependencies."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'site-data.json').read_text(encoding='utf-8'))
def e(s): return html.escape(str(s),quote=True)
def link(url,label): return f'<a href="{e(url)}">{e(label)}</a>'
NAV=[('index.html','Home'),('paper.html','Papers'),('paper_topic.html','Papers by topics'),('grants.html','Grants'),('group.html','Group'),('teaching.html','Teaching')]
def page(file,title,body):
    nav=''.join(f'<a href="{f}"'+(' aria-current="page"' if file==f else '')+f'>{t}</a>' for f,t in NAV)
    out=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Jun Jin (金君), School of Mathematical Sciences, Yangzhou University. Statistical machine learning, federated learning, distributed statistical inference, generative modelling, and image and spatiotemporal data analysis."><meta name="theme-color" content="#527bbd"><title>{e(title)} | Jun Jin</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><div class="layout"><aside class="menu"><div class="menu-name">{e(D['name'])}</div><nav aria-label="Main navigation">{nav}</nav><div class="menu-note">金君<br>Yangzhou University</div></aside><main class="content" id="main"><div class="toptitle"><h1>{e(title)}</h1></div>{body}<footer class="footer">Page updated {e(D['updated'])}. &nbsp; {link(D['official_homepage'],'Official faculty profile')} · {link(D['github'],'GitHub')}</footer></main></div></body></html>
'''
    (ROOT/file).write_text(out,encoding='utf-8')
def pubs(items, prefix=''):
    entries=[]
    for p in items:
        meta=f'{p["venue"]}, {p["year"]}' + (f', {p["volume"]}' if p['volume'] else '') + '.'
        links=link('https://doi.org/'+p['doi'],'DOI: '+p['doi']) if p['doi'] else ''
        link_html=f'<div class="publication-links">{links}</div>' if links else ''
        entries.append(f'<li id="{e(prefix+p["id"])}"><div class="publication-title">{e(p["title"])}</div><div class="authors">{e(p["authors"]).replace("Jun Jin", "<strong>Jun Jin</strong>").replace("金君", "<strong>金君</strong>")}</div><div class="publication-meta">{e(meta)}</div>{link_html}</li>')
    return '<ul class="publications">'+''.join(entries)+'</ul>'
interest='<ul class="interest-list">'+''.join(f'<li>{link("paper_topic.html#"+x["id"],x["en"])} <span lang="zh-CN">· {e(x["cn"])}</span></li>' for x in D['interests'])+'</ul>'
home=f'''<section class="intro" aria-label="Profile"><img class="portrait" src="{e(D['portrait'])}" alt="Portrait of Jun Jin" width="350" height="421"><div><p>My name is Jun Jin (金君). I am a lecturer and master's supervisor at the School of Mathematical Sciences, Yangzhou University.</p><p lang="zh-CN">扬州大学数学科学学院 · 讲师 · 硕士生导师</p><p>E-mail: {link('mailto:'+D['email'],D['email'])}<br>{link(D['official_homepage'],'Yangzhou University faculty profile')}<br>{link(D['github'],'GitHub')}</p><p>Office: {e(D['office'])}</p><h2>Research interests</h2><p>My research interests include:</p>{interest}<div class="invite"><p>I welcome inquiries about graduate study and research collaboration in statistics and machine learning.</p><p lang="zh-CN">欢迎对统计学与机器学习感兴趣的同学交流，也欢迎开展科研合作。</p></div></div></section>'''
for key,label in [('education','Education'),('experience','Experience')]:
    home+=f'<h2>{label}</h2>'+''.join(f'<p><strong>{e(x["institution"])}</strong><br>{e(x["detail"])}</p>' for x in D[key])
home+='<h2>Research overview</h2><p>My research spans statistical machine learning, federated learning, distributed statistical inference, generative modelling, and image and spatiotemporal data analysis.</p><h2>Academic service</h2><p>Reviewer for '+', '.join(e(x) for x in D['service'])+', among other journals.</p>'
if D['news']: home+='<h2>News</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in D['news'])+'</ul>'
page('index.html',D['name']+' ['+D['name_cn']+']',home)
papers='<p class="quiet">* Corresponding author · # Student author</p>'
for year in sorted({p['year'] for p in D['publications'] if not 2017 <= p['year'] <= 2020},reverse=True):
    papers+=f'<h2>{year}</h2>'+pubs([p for p in D['publications'] if p['year']==year])
early=sorted([p for p in D['publications'] if 2017 <= p['year'] <= 2020],key=lambda p:p['year'],reverse=True)
if early:
    papers+='<h2>2017–2020</h2>'+pubs(early)
page('paper.html','Selected publications',papers)
topics='<div class="topic-links">'+''.join(link('#'+x['id'],x['en']) for x in D['interests'])+link('#nonparametric','Nonparametric and robust regression')+'</div>'
for x in D['interests']:
    topics+=f'<section class="topic-section" id="{e(x["id"])}"><h2>{e(x["en"])}</h2><p lang="zh-CN">{e(x["cn"])}</p><p>{e(x["description"])}</p>'
    selected=[p for p in D['publications'] if x['id'] in p['topics']]
    if selected: topics+=pubs(selected, x['id']+'-')
    topics+='</section>'
topics+='<section id="nonparametric"><h2>Nonparametric and robust regression</h2>'+pubs([p for p in D['publications'] if 'nonparametric' in p['topics'] or 'robust' in p['topics']], 'nonparametric-')+'</section>'
topics+='<section id="clustering"><h2>Clustering and applied statistical modelling</h2>'+pubs([p for p in D['publications'] if 'clustering' in p['topics']], 'clustering-')+'</section>'
topics+='<section id="applications"><h2>Applied statistics and interdisciplinary research</h2>'+pubs([p for p in D['publications'] if 'applications' in p['topics']], 'applications-')+'</section>'
page('paper_topic.html','Publications and research by topics',topics)
grants='<p>My research focuses on statistical machine learning, federated learning, distributed statistical inference, generative modelling, and image and spatiotemporal data analysis.</p>'
if D['grants']: grants+='<h2>Research grants</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in D['grants'])+'</ul>'
grants+='<h2>Funding information</h2><p>For current research grant details, please refer to my '+link(D['official_homepage'],'official faculty profile')+'.</p><h2>Research collaboration</h2><p>I welcome collaboration in statistical machine learning, federated learning, distributed statistical inference, generative modelling, and image and spatiotemporal data analysis.</p><p>Contact: '+link('mailto:'+D['email'],D['email'])+'</p>'
page('grants.html','Grants',grants)
group='<h2>Graduate supervision</h2><p>I supervise master\'s students at the School of Mathematical Sciences, Yangzhou University.</p><p lang="zh-CN">欢迎对统计学理论、统计计算、机器学习和空间与图像数据分析感兴趣的同学联系交流。</p><h2>Research areas</h2>'+interest
if D['students']: group+='<h2>Current students · 在读学生</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in D['students'])+'</ul>'
group+='<h2>Contact</h2><p>For supervision and research inquiries, please email '+link('mailto:'+D['email'],D['email'])+'.</p><p>'+link(D['official_homepage'],'Official faculty profile and supervision information')+'</p>'
page('group.html','Group',group)
teaching='<h2>Teaching and learning</h2><p>My teaching and academic interests centre on statistical modelling, regression analysis, statistical inference, and statistical learning.</p><h2>Regression analysis</h2><p>Topics include least-squares estimation, projection matrices, analysis of variance, coefficient tests, model diagnostics, and prediction.</p>'
if D['courses']: teaching+='<h2>Courses</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in D['courses'])+'</ul>'
teaching+='<h2>Course information</h2><p>For formal course listings and current teaching arrangements, please see my '+link(D['official_homepage'],'official faculty profile')+'.</p><p>For academic questions, contact '+link('mailto:'+D['email'],D['email'])+'.</p>'
page('teaching.html','Teaching',teaching)
print('Generated 6 static pages.')
