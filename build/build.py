# -*- coding: utf-8 -*-
import re, os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"..","index.html")
H=open(os.path.join(HERE,"base.html"),encoding="utf-8").read(); V=106
IMGROOT=os.path.join(HERE,"..","images","projets")

def between(a,b,s=H): i=s.index(a); return s[i:s.index(b,i)]
def match_div(s,k):
    depth=0;p=k
    while p<len(s):
        if s.startswith('</div>',p):
            depth-=1
            if depth==0: return s[k:p+6]
            p+=6; continue
        if s.startswith('<div',p): depth+=1
        p+=1
    return s[k:]
def groups(section):
    out=[];i=0
    while True:
        k=section.find('<div class="group">',i)
        if k<0:break
        b=match_div(section,k); out.append(b); i=k+len(b)
    return out
def gt(g):
    m=re.search(r'<h3>(.*?)</h3>',g,re.S); return (m.group(1) if m else '')

pub=between('<!-- ============ PUBLICATIONS','<!-- ============ TALKS')
tal=between('<!-- ============ TALKS','<!-- ============ MEDIA')
med=between('<!-- ============ MEDIA','<!-- ============ CONTACT')
PUBG=groups(pub); TALG=groups(tal); MEDG=groups(med)
book=[g for g in PUBG if 'book chapters' in gt(g).lower()]
pub_nobook=[g for g in PUBG if g not in book]
thesis_card=match_div(H,H.index('<div class="card">',H.index('id="p-thesis"')))
banner=re.search(r'<img class="thesis-banner"[^>]*>',H).group(0).replace('images/banniere-memorial.jpg','images/banniere-memorial.jpg?v=%d'%V)
soutenance=re.search(r'<figure class="thesis-photo">.*?</figure>',H,re.S).group(0)
ritmea=re.sub(r'^<div class="panel active" id="p-postdoc">','',match_div(H,H.index('<div class="panel active" id="p-postdoc">')))[:-6]
# decompose thesis card into pieces for 2-col layout
th_h3=re.search(r'<h3>(.*?)</h3>',thesis_card,re.S).group(1)
th_sub=re.search(r'<p style="color:var\(--ink-faint\);font-size:15px;margin-top:-4px">.*?</p>',thesis_card,re.S).group(0)
th_jury=re.search(r'<div class="thesis-jury">.*?</div>',thesis_card,re.S).group(0)
_a=thesis_card.index(th_sub)+len(th_sub)
_b=thesis_card.index('<div class="thesis-jury">')
th_resume=thesis_card[_a:_b].strip()
# une ligne par point dans le sous-titre (ne pas couper « Defended… »)
th_sub=th_sub.replace(' · ','<br>')
# decompose RITMEA panel for the postdoc 2-col layout
rit_h3=re.search(r'<h3>(.*?)</h3>',ritmea,re.S).group(1)
rit_link=re.search(r'<a class="online".*?</a>',ritmea,re.S).group(0)
rit_body=re.findall(r'<p>.*?</p>',ritmea,re.S)[0]

# ---------- captions ----------
SRC={"own":("Source : A. Mallah","Source: A. Mallah"),
 "opendata":("Source : Open Data Paris &amp; A. Mallah","Source: Open Data Paris &amp; A. Mallah"),
 "apur":("Source : APUR &amp; A. Mallah","Source: APUR &amp; A. Mallah"),"none":None}
CAP={
"geographie-des-collages-contre-les-feminicides":("Géographie des collages contre les féminicides, de 2019 à 2024, à Paris","Geography of anti-femicide collages, 2019–2024 · Paris","own","2025"),
"visibilite-des-collages":("Niveau de visibilité des collages selon leur rue d'implantation, à Paris","Visibility of collages by street where posted · Paris","apur","2025"),
"part-des-collages-commemoratifs":("Part des collages commémoratifs dans le total, de 2019 à 2024, à Paris","Commemorative collages as a share of the total, 2019–2024 · Paris","own","2025"),
"evolution-mensuelle-des-collages":("Évolution de la production des collages, par mois, de 2019 à 2024, à Paris","Monthly evolution of collage production, 2019–2024 · Paris","own","2025"),
"quartier-folie-mericourt":("Les collages dans le quartier de la Folie-Méricourt, à Paris","Collages in the Folie-Méricourt district · Paris","own","2025"),
"distribution-collages-folie-mericourt":("Distribution des collages selon la fréquentation des rues","Distribution of collages by street footfall","apur","2024"),
"voies-feminines-selon-leur-date-de-bapteme":("Voies féminines selon leur date de baptême, à Paris","Streets named after women, by date of naming · Paris","opendata","2025"),
"production-des-odonymes-par-mandat":("Production des odonymes par mandat municipal, de 1983 à 2024, à Paris","Street-name creation by municipal term, 1983–2024 · Paris","opendata","2025"),
"evolution-des-odonymes-18602024":("Évolution de la production des odonymes, de 1860 à 2024, à Paris","Evolution of street-name creation, 1860–2024 · Paris","opendata","2025"),
"graphique-part-genre-selon-generique-apres-2001":("Part des odonymes selon le genre et le type de générique, après 2001, à Paris","Share of street names by gender and type of generic term, after 2001 · Paris","opendata","2025"),
"plaques-de-rue-boulevard-pereire":("Positionnement des plaques de rue au croisement du boulevard Pereire et de la rue Laugier, à Paris","Placement of street signs at boulevard Pereire × rue Laugier · Paris","own","2022"),
"schema-type-boulevard":("Schéma type d'un boulevard","Typical schema of a boulevard","none","2025"),
"schema-type-avenue":("Schéma type d'une avenue","Typical schema of an avenue","none","2025"),
"schema-type-allee":("Schéma type d'une allée","Typical schema of an allée","none","2025"),
"schema-type-promenade":("Schéma type d'une promenade","Typical schema of a promenade","none","2025"),
"schema-type-villa":("Schéma type d'une cité ou villa","Typical schema of a cité / villa","none","2025"),
"schema-type-passage-couvert":("Schéma type d'un passage couvert","Typical schema of a covered passage","none","2025"),
"organisation-des-marqueurs-memoriels-de-la-place-du-pantheon-selon-le-type-de-memoire-vehiculee":("Organisation des marqueurs mémoriels de la place du Panthéon selon le type de mémoire","Mapping the memorial markers of place du Panthéon by type of memory","own","2025"),
"synthese-des-geographies-des-memoires":("Synthèse des géographies des mémoires féminines et féministes, à Paris","Synthesis of women's and feminist memory geographies · Paris","opendata","2025"),
"construction-du-corpus-de-recherche":("Construction du corpus de recherche par affinages successifs","Building the research corpus through successive refinements","own","2025"),
"schemes-temporels-et-spatiaux":("Schèmes temporels et spatiaux qui régissent l'existence des écrits","Temporal and spatial schemes governing public writings","own","2025"),
"visibilite-des-ecritures-approche-temporelle":("La visibilité des écritures exposées selon une approche temporelle","The visibility of public writings through a temporal lens","own","2025"),
"panneaux-publicitaires":("Les panneaux publicitaires : espace de la page, écriture et hauteur d'affichage","Advertising panels: page space, writing and display height","own","2025"),
}
# documents affichés à leur hauteur naturelle (pas de cadre à ratio imposé)
NAT={"synthese-des-geographies-des-memoires"}
PHOTOS={
"rue-bouvier-janvier-2023":("Rue Bouvier, Paris · janvier 2023","Rue Bouvier, Paris · January 2023","2023"),
"rue-bouvier-janvier-2023-1":("Rue Bouvier, Paris · janvier 2023","Rue Bouvier, Paris · January 2023","2023"),
"rue-bouvier-janvier-2023-2":("Rue Bouvier, Paris · janvier 2023","Rue Bouvier, Paris · January 2023","2023"),
"rue-du-chevaleret-janvier-2024":("Rue du Chevaleret, Paris · janvier 2024","Rue du Chevaleret, Paris · January 2024","2024"),
"rue-du-chevaleret-janvier-2024-1":("Rue du Chevaleret, Paris · janvier 2024","Rue du Chevaleret, Paris · January 2024","2024"),
"rue-du-chevaleret-janvier-2024-2":("Rue du Chevaleret, Paris · janvier 2024","Rue du Chevaleret, Paris · January 2024","2024"),
}
def credit(year,src):
    s=SRC.get(src)
    base='<span class="credit">© Alexandra Mallah, %s</span>'%year
    if s: base+='<span class="credit credit-src"><span class="en">%s</span><span class="fr">%s</span></span>'%(s[1],s[0])
    return base
LIC='<a class="lic" href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" rel="noopener" aria-label="Licence Creative Commons Attribution - Pas d\'utilisation commerciale - Pas de modification 4.0">CC BY-NC-ND&nbsp;4.0</a>'
CITE=('<details class="cite"><summary><span class="en">How to cite these figures</span><span class="fr">Pour citer ces figures</span></summary>'
 '<p>Mallah Alexandra, 2025, <em>Géographie de l\'invisible. Les territoires de la mémoire des femmes</em>, '
 'Thèse de doctorat en géographie, EHESS, Paris, 528 p. · '
 '<a href="https://theses.fr/2025EHES0116" target="_blank" rel="noopener">theses.fr/2025EHES0116</a></p></details>')
MOIS_FR=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
MOIS_EN=["January","February","March","April","May","June","July","August","September","October","November","December"]
def session_cap(stem):
    p=stem.replace('session-','').split('-'); y,m,dd=int(p[0]),int(p[1]),int(p[2])
    return ("Session du %d %s %d"%(dd,MOIS_FR[m-1],y),"Session of %d %s %d"%(dd,MOIS_EN[m-1],y),"own","2025")

def gallery(proj, sec_folder, order=None, ar=None):
    base=os.path.join(IMGROOT,proj,sec_folder) if sec_folder else os.path.join(IMGROOT,proj)
    if not os.path.isdir(base): return ""
    files=[f for f in os.listdir(base) if not f.startswith('.') and not f.startswith('acces') and not f.startswith('fond') and os.path.isfile(os.path.join(base,f))]
    stems={}
    for f in files:
        n,ext=os.path.splitext(f); ext=ext.lower()
        if n.endswith('-en'): lang='en'; key=n[:-3]
        elif n.endswith('-fr'): lang='fr'; key=n[:-3]
        else: lang='base'; key=n
        stems.setdefault(key,{})[lang]=(f,ext)
    keys=list(stems.keys())
    if order:
        keys.sort(key=lambda k:(order.index(k) if k in order else 999, k))
    rel="images/projets/%s/%s/"%(proj,sec_folder) if sec_folder else "images/projets/%s/"%proj
    figs=[]
    for k in keys:
        d=stems[k]; frf=d.get('fr') or d.get('base'); enf=d.get('en')
        ext=(frf or enf)[1]
        if ext in ('.jpg','.jpeg'):
            fr,en,yr=PHOTOS.get(k,(k.replace('-',' '),k.replace('-',' '),'2025'))
            f=(frf or enf)[0]
            figs.append('<figure class="doc"><img src="%s%s?v=%d" loading="lazy" draggable="false" alt="%s"><figcaption><span class="en">%s</span><span class="fr">%s</span><span class="credit">© Alexandra Mallah, %s</span>%s</figcaption></figure>'%(rel,f,V,en,en,fr,yr,LIC))
            continue
        if k.startswith('session-'): cfr,cen,src,yr=session_cap(k)
        else:
            c=CAP.get(k)
            if c: cfr,cen,src,yr=c
            else: cfr,cen,src,yr=(k.replace('-',' '),k.replace('-',' '),"own","2025")
        cap='<figcaption><span class="en">%s</span><span class="fr">%s</span>%s%s</figcaption>'%(cen,cfr,credit(yr,src),LIC)
        kl='schema paper'+(' schema-voie' if k.startswith('schema-type') else '')+(' fig-nat' if k in NAT else '')
        if frf and enf:
            figs.append('<figure class="%s"><img class="fr" src="%s%s?v=%d" loading="lazy" draggable="false" alt="%s"><img class="en" src="%s%s?v=%d" loading="lazy" draggable="false" alt="%s">%s</figure>'%(kl,rel,frf[0],V,cfr,rel,enf[0],V,cen,cap))
        else:
            f=(frf or enf)[0]
            figs.append('<figure class="%s"><img src="%s%s?v=%d" loading="lazy" draggable="false" alt="%s">%s</figure>'%(kl,rel,f,V,cfr,cap))
    style=' style="--fig-ar:%s"'%ar if ar else ''
    return '<div class="fig-grid doc-scroll"%s>%s</div>'%(style,''.join(figs))

# doctoral document sections
doc_secs=[("Section_collages","Collages","Collages"),("Section_odonymes","Odonymes / noms de rues","Street names / odonymy"),("Section_pantheon","Place du Panthéon","Place du Panthéon"),("Section_transversale","Transversal","Cross-cutting")]
def sec_block(proj,folder,labfr,laben,order=None,ar=None):
    g=gallery(proj,folder,order,ar)
    if not g: return ""
    return '<div class="fig-section"><h3 class="fig-h"><span class="en">%s</span><span class="fr">%s</span></h3>%s</div>'%(laben,labfr,g)

ORD_collages=["geographie-des-collages-contre-les-feminicides","visibilite-des-collages","part-des-collages-commemoratifs","evolution-mensuelle-des-collages","rue-bouvier-janvier-2023-1","rue-bouvier-janvier-2023-2","rue-du-chevaleret-janvier-2024","rue-du-chevaleret-janvier-2024-1"]
ORD_odo=["voies-feminines-selon-leur-date-de-bapteme","production-des-odonymes-par-mandat","evolution-des-odonymes-18602024","graphique-part-genre-selon-generique-apres-2001","schema-type-boulevard","schema-type-avenue","schema-type-promenade","schema-type-villa","plaques-de-rue-boulevard-pereire"]
ORD_tr=["construction-du-corpus-de-recherche","schemes-temporels-et-spatiaux","visibilite-des-ecritures-approche-temporelle","panneaux-publicitaires","synthese-des-geographies-des-memoires"]

doc_docs = CITE + sec_block("doctoral","section-collages","Collages féminicides","Feminicide collages",ORD_collages,ar="3/2")+sec_block("doctoral","section-odonymes","Odonymie","Odonymy",ORD_odo,ar="3/2")+sec_block("doctoral","section-pantheon","Place du Panthéon","Place du Panthéon",ar="3/4")+sec_block("doctoral","section-transversale","Documents transversaux","Cross-cutting documents",ORD_tr,ar="2/3")
ORD_master=["distribution-collages-folie-mericourt"]
master_docs = gallery("master","",ORD_master,ar="9/10")

OUTP=lambda gs: ''.join(gs)

# ---------- new body ----------
def L(en,fr): return '<span class="en">%s</span><span class="fr">%s</span>'%(en,fr)
DT=L("Geography of the invisible","Géographie de l'invisible")
MT=L("Appropriating public space","Appropriation de l'espace public")
PT=L("Cross-border mobilities","Mobilités transfrontalières")
def wm(pid,full=False,img="acces.jpg"): return '<div class="proj-wm%s" aria-hidden="true"><img src="images/projets/%s/%s?v=%d" alt=""></div>'%(' proj-wm-full' if full else '',pid,img,V)
def projnav(pv,pt,nv,nt):
    return ('<nav class="proj-nav" aria-label="Navigation entre projets">'
      '<a class="pn pn-prev" onclick="showView(\'%s\')" role="button" tabindex="0" aria-label="Projet précédent"><span class="pn-arr" aria-hidden="true">←</span><span class="pn-lab">%s</span></a>'
      '<a class="pn pn-next" onclick="showView(\'%s\')" role="button" tabindex="0" aria-label="Projet suivant"><span class="pn-arr" aria-hidden="true">→</span><span class="pn-lab">%s</span></a>'
      '</nav>')%(pv,pt,nv,nt)
body = '''
<!-- ============ PROJETS (landing) ============ -->
<section class="view active" id="view-projects">
  <div class="wrap">
    <p class="eyebrow">%s</p>
    <p class="proj-h">%s</p>
    <div class="proj-grid">
      <a class="proj-card" onclick="showView('proj-doctoral')" role="button" tabindex="0">
        <span class="proj-img"><img src="images/projets/doctoral/acces.jpg?v=%d" loading="lazy" draggable="false" alt="Géographie de l'invisible"></span>
        <span class="proj-cap"><span class="proj-role">%s</span><span class="proj-title">%s</span></span></a>
      <a class="proj-card" onclick="showView('proj-master')" role="button" tabindex="0">
        <span class="proj-img"><img src="images/projets/master/acces.jpg?v=%d" loading="lazy" draggable="false" alt="Appropriation de l'espace public"></span>
        <span class="proj-cap"><span class="proj-role">%s</span><span class="proj-title">%s</span></span></a>
      <a class="proj-card" onclick="showView('proj-postdoc')" role="button" tabindex="0">
        <span class="proj-img"><img src="images/projets/postdoc/acces.jpg?v=%d" loading="lazy" draggable="false" alt="Les mobilités transfrontalières franco-belges"></span>
        <span class="proj-cap"><span class="proj-role">%s</span><span class="proj-title">%s</span></span></a>
    </div>
  </div>
</section>
''' % (
 L("Geographer &amp; architect · Postdoctoral researcher","Géographe &amp; architecte · Postdoctorante"),
 L("Projects","Projets"),
 V, L("Doctoral project","Projet doctoral"), L("Geography of the invisible","Géographie de l'invisible"),
 V, L("Master's project","Projet de master"), L("Appropriating public space","Appropriation de l'espace public"),
 V, L("Postdoctoral project","Projet postdoctoral"), L("Cross-border mobilities","Les mobilités transfrontalières"),
)

# DOCTORAL
body += '''
<section class="view proj-view" id="view-proj-doctoral">
  <div class="wrap">
    <div class="proj-hero">%s<div class="proj-hero-in">
    <a class="proj-back" onclick="showView('projects')" role="button" tabindex="0">%s</a>
    <p class="proj-meta">%s</p>
    <div class="proj-cols">
      <div class="proj-info">
        <h1 class="proj-h1">%s</h1>
        <p class="proj-affil">%s</p>
        %s
        %s
      </div>
      <div class="proj-prod">
        <p class="proj-lbl">%s</p>
        <div class="proj-outputs">%s</div>
      </div>
      <div class="proj-right">
        <div class="proj-resume">%s</div>
        %s
      </div>
    </div>
    </div></div>
    <h2 class="proj-sec">%s</h2>
    %s
    %s
  </div>
</section>
''' % (wm('doctoral',full=True), L("← Projects","← Projets"),
 L("Doctoral project · 2021–2025","Projet doctoral · 2021–2025"),
 th_h3,
 L("2021–2025 · UMR Géographie-cités, EHESS","2021–2025 · UMR Géographie-cités, EHESS"),
 th_sub, th_jury,
 L("Outputs","Productions"), OUTP(pub_nobook),
 th_resume, soutenance,
 L("Graphic documents","Documents graphiques"), doc_docs,
 projnav('proj-postdoc',PT,'proj-master',MT))

# MASTER
master_desc_fr="Réalisé à l'EHESS sous la direction de Claudia Damasceno Fonseca, ce mémoire de master analyse l'appropriation de l'espace public parisien par le mouvement <em>Collages Féminicides Paris</em>. En portant les violences sexistes et sexuelles sur les murs de la ville, ces messages éphémères rendent visible un problème souvent invisibilisé. À partir d'une enquête de terrain (observation, participation observante, cartographie des sessions de collage), le travail interroge la répartition spatiale des activités militantes, la conquête de légitimité dans l'espace public, la réception par les passant·es, et le rôle du mur comme support à la frontière entre espace public et privé. L'analyse procède par un emboîtement des échelles — du mur à la rue, puis à la ville."
master_desc_en="Carried out at the EHESS under the supervision of Claudia Damasceno Fonseca, this master's thesis analyses how the <em>Collages Féminicides Paris</em> movement appropriates Parisian public space. By bringing gender-based and sexual violence onto the city's walls, these ephemeral messages make visible an often-invisibilised issue. Drawing on fieldwork (observation, observant participation, mapping of pasting sessions), it examines the spatial distribution of activist practices, the struggle for legitimacy in public space, passers-by's reception, and the role of the wall at the boundary between public and private space. The analysis unfolds through a nesting of scales — from the wall to the street, then to the city."
body += '''
<section class="view proj-view" id="view-proj-master">
  <div class="wrap">
    <div class="proj-hero">%s<div class="proj-hero-in">
    <a class="proj-back" onclick="showView('projects')" role="button" tabindex="0">%s</a>
    <p class="proj-meta">%s</p>
    <div class="proj-cols">
      <div class="proj-info">
        <h1 class="proj-h1"><em>L'appropriation de l'espace public par les mouvements sociaux féministes : le cas de Collages Féminicides Paris</em></h1>
        <p class="proj-affil">%s</p>
      </div>
      <div class="proj-prod">
        <p class="proj-lbl">%s</p>
        <div class="proj-outputs">%s</div>
      </div>
      <div class="proj-right">
        <div class="proj-resume"><p>%s</p></div>
      </div>
    </div>
    </div></div>
    <h2 class="proj-sec">%s</h2>
    %s
    %s
  </div>
</section>
''' % (wm('master',img='fond.jpg'), L("← Projects","← Projets"),
 L("Master's project · 2020–2021","Projet de master · 2020–2021"),
 L("Master Territoires, espaces et sociétés<br>EHESS, 2020–2021<br>supervised by Claudia Damasceno Fonseca","Master Territoires, espaces et sociétés<br>EHESS, 2020–2021<br>dir. Claudia Damasceno Fonseca"),
 L("Outputs","Productions"), OUTP(book),
 L(master_desc_en,master_desc_fr),
 L("Graphic documents","Documents graphiques"),
 CITE+'<div class="fig-section"><h3 class="fig-h">%s</h3>%s</div>'%(L("Maps","Cartographies"),master_docs),
 projnav('proj-doctoral',DT,'proj-postdoc',PT))

# POSTDOC
body += '''
<section class="view proj-view" id="view-proj-postdoc">
  <div class="wrap">
    <div class="proj-hero">%s<div class="proj-hero-in">
    <a class="proj-back" onclick="showView('projects')" role="button" tabindex="0">%s</a>
    <p class="proj-meta">%s</p>
    <div class="proj-cols">
      <div class="proj-info">
        <h1 class="proj-h1">%s</h1>
        <p class="proj-affil">%s</p>
      </div>
      <div class="proj-prod">
        <p class="proj-lbl">%s</p>
        <p class="proj-soon">%s</p>
      </div>
      <div class="proj-right">
        <div class="proj-resume">%s</div>
        <p style="margin-top:12px">%s</p>
      </div>
    </div>
    %s
    <p class="proj-copy">© 2026 Alexandra Mallah<span class="foot-lic"><span class="en">Figures licensed under </span><span class="fr">Figures sous licence </span><a class="lic-inline" href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" rel="noopener">CC BY-NC-ND&nbsp;4.0</a></span></p>
    </div></div>
  </div>
</section>
''' % (wm('postdoc',full=True), L("← Projects","← Projets"),
 L("Postdoctoral project · 2026–present","Projet postdoctoral · 2026–présent"),
 rit_h3,
 L("Since 2026 · LARSH, UPHF · RITMEA project<br>in collaboration with Thomas Pfirsch and Guillaume Schmitt","2026–présent · LARSH, UPHF · projet RITMEA<br>en collaboration avec Thomas Pfirsch et Guillaume Schmitt"),
 L("Outputs","Productions"),
 L("Outputs and graphic documents to come.","Productions et documents graphiques à venir."),
 rit_body, rit_link,
 projnav('proj-master',MT,'proj-doctoral',DT))

# CV
body += '''
<section class="view" id="view-cv">
  <div class="wrap">
    <div class="cv-head">
      <h2><span class="en">Curriculum vit&aelig;</span><span class="fr">Curriculum vit&aelig;</span></h2>
      <a class="docs-jump" href="cv-alexandra-mallah.pdf" target="_blank" rel="noopener">%s <span aria-hidden="true">↓</span></a>
    </div>
    <p class="cv-cat">%s</p>
    %s
    <p class="cv-cat">%s</p>
    %s
    <p class="cv-cat">%s</p>
    %s
  </div>
</section>
''' % (L("Download CV","Télécharger le CV"),
 L("Publications","Publications"), OUTP(PUBG),
 L("Talks","Communications"), OUTP(TALG),
 L("In the media","Médias"), OUTP(MEDG))

# ---------- splice ----------
start=H.index('<section class="view active" id="view-home">')
endm=H.index('<!-- ============ CONTACT ============ -->')
H = H[:start] + body.strip() + "\n\n" + H[endm:]

# nav
oldnav=match_div(H,H.index('<nav class="menu" id="menu">')) if False else None
nav_re=re.search(r'<nav class="menu" id="menu">.*?</nav>',H,re.S)
newnav='''<nav class="menu" id="menu">
      <a data-view="projects" class="active" onclick="showView('projects')"><span class="en">Projects</span><span class="fr">Projets</span></a>
      <a data-view="cv" onclick="showView('cv')">CV</a>
      <a data-view="contact" onclick="showView('contact')">Contact</a>
      <button class="lang-btn" id="langBtn" onclick="toggleLang()">FR</button>
    </nav>'''
H=H[:nav_re.start()]+newnav+H[nav_re.end():]

# JS: default reveal + nav active for subpages + lightbox scope
H=H.replace("applyReveal(document.getElementById('view-home'));","applyReveal(document.getElementById('view-projects'));")
H=H.replace("document.querySelectorAll('.menu a').forEach(a=>a.classList.toggle('active', a.getAttribute('data-view')===v));",
            "var navkey=v.indexOf('proj-')===0?'projects':v;document.querySelectorAll('.menu a').forEach(a=>a.classList.toggle('active', a.getAttribute('data-view')===navkey));")
H=H.replace("var scope=img.closest('.doc-scroll');","var scope=img.closest('.fig-grid, .doc-scroll');")
# logo -> page Projets (la vue home n'existe plus)
H=H.replace("showView('home')","showView('projects')")
# animation d'entrée des vues sans transform (sinon la section devient le bloc
# contenant des flèches fixes et casse leur centrage vertical)
H=H.replace('@keyframes viewIn{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}','@keyframes viewIn{from{opacity:0}to{opacity:1}}')
# mention de licence (CC BY-NC-ND 4.0) au pied de page
H=H.replace('<footer>© 2026 Alexandra Mallah</footer>','<footer>© 2026 Alexandra Mallah<span class="foot-lic"><span class="en">Figures licensed under </span><span class="fr">Figures sous licence </span>'+LIC+'</span></footer>')
# entrée « thèse » des productions : ne garder que la publication officielle
H=H.replace(' · Supervised by Nicolas Verdier · Defended 14 November 2025.','.')
H=H.replace(' · Direction : Nicolas Verdier · Soutenue le 14 novembre 2025.','.')
# retirer l'eyebrow "Contact" + "résumé accepté" du colloque
H=H.replace('<p class="eyebrow">Contact</p>','')
H=H.replace('Montpellier — abstract accepted.','Montpellier.').replace('Montpellier — résumé accepté.','Montpellier.')

# CSS additions before </style>
css='''
  /* ---- pied de page collé en bas (sticky footer) ---- */
  body{min-height:100vh;display:flex;flex-direction:column}
  footer{margin-top:auto}
  .view.active{flex:1 0 auto}
  /* postdoc : le hero (et son filigrane) remplit tout l'écran */
  #view-proj-postdoc.active{display:flex;flex-direction:column}
  #view-proj-postdoc.active>.wrap{flex:1 0 auto;display:flex;flex-direction:column}
  #view-proj-postdoc .proj-hero{flex:1 0 auto;display:flex;flex-direction:column}
  #view-proj-postdoc .proj-hero-in{flex:1 0 auto;display:flex;flex-direction:column}
  #view-proj-postdoc{padding-top:0;padding-bottom:0}
  #view-proj-postdoc .proj-hero-in{padding:54px 0 26px}
  #view-proj-postdoc .proj-copy{margin-top:auto}
  #view-proj-postdoc .proj-copy{text-align:center;color:var(--ink-faint);font-size:13.5px;margin:auto 0 0}
  body:has(#view-proj-postdoc.active)>footer{display:none}
  /* ---- Refonte projets ---- */
  .proj-h{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin:42px 0 16px}
  .proj-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .proj-card{display:block;position:relative;overflow:hidden;border-radius:6px;cursor:pointer;text-decoration:none;background:var(--surface);border:1px solid var(--line)}
  .proj-img{display:block;aspect-ratio:4/5;overflow:hidden;background:var(--line-soft)}
  .proj-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .55s cubic-bezier(.2,.6,.2,1)}
  .proj-card:hover .proj-img img{transform:scale(1.05)}
  .proj-ph{display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 40% 35%,#f1e6d3,#e3d3b4);color:var(--gold-soft);font-family:var(--serif);font-style:italic;font-size:15px}
  .proj-cap{position:absolute;left:0;right:0;bottom:0;padding:34px 16px 14px;background:linear-gradient(to top,rgba(28,22,14,.82),rgba(28,22,14,.25),rgba(28,22,14,0));color:#fff;pointer-events:none}
  .proj-role{display:block;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.9;margin-bottom:4px}
  .proj-title{display:block;font-family:var(--serif);font-size:19px;line-height:1.12;font-weight:500}
  .proj-back{display:inline-block;font-size:13px;letter-spacing:.04em;color:var(--gold);margin-bottom:20px;cursor:pointer}
  .proj-back:hover{text-decoration:underline}
  .proj-meta{font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-faint);margin:0 0 22px}
  .proj-cols{display:grid;grid-template-columns:0.92fr 1.12fr;column-gap:46px;align-items:start;grid-template-areas:"info resume" "prod resume"}
  .proj-info{grid-area:info;min-width:0}
  .proj-prod{grid-area:prod;min-width:0;margin-top:10px}
  .proj-right{grid-area:resume;min-width:0}
  .proj-h1{font-family:var(--serif);font-weight:400;font-size:27px;line-height:1.18;margin:0 0 14px;color:var(--ink)}
  .proj-affil{font-size:13px;letter-spacing:.04em;color:var(--gold);margin:0 0 16px;font-weight:500}
  .proj-info .thesis-jury{margin-top:18px;font-size:12.5px;line-height:1.5;color:var(--ink-faint)}
  .proj-info .thesis-jury p{margin:0 0 8px}
  .proj-lbl{font-size:13.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:30px 0 14px}
  .proj-soon{color:var(--ink-faint);font-style:italic;font-size:14.5px;margin:6px 0 0}
  .proj-outputs .group{margin:0 0 18px}
  .proj-outputs .src,.proj-outputs .t{text-align:justify;-webkit-hyphens:none;hyphens:none}
  .eyebrow{font-size:14px;letter-spacing:.14em}
  .cv-head{display:flex;align-items:baseline;justify-content:space-between;gap:24px;flex-wrap:wrap;margin:0 0 30px}
  .cv-head h2{margin:0}
  .proj-nav .pn{position:fixed;top:50%;transform:translateY(-50%);z-index:30;display:flex;align-items:center;gap:12px;text-decoration:none;cursor:pointer}
  .proj-nav .pn-prev{left:22px}
  .proj-nav .pn-next{right:22px;flex-direction:row-reverse}
  .proj-nav .pn-arr{display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:rgba(250,250,248,.74);color:var(--gold);font-size:19px;transition:background .2s,color .2s,border-color .2s}
  .proj-nav .pn:hover .pn-arr{background:var(--gold);color:#fff;border-color:var(--gold)}
  .proj-nav .pn-lab{font-family:var(--serif);font-style:italic;font-size:15px;color:var(--ink-soft);max-width:0;opacity:0;overflow:hidden;white-space:nowrap;transition:max-width .3s,opacity .3s}
  .proj-nav .pn:hover .pn-lab{max-width:240px;opacity:1}
  @media(max-width:980px){.proj-nav .pn-lab{display:none}.proj-nav .pn-arr{width:40px;height:40px;font-size:17px}.proj-nav .pn-prev{left:10px}.proj-nav .pn-next{right:10px}}
  @media(max-width:560px){.proj-nav{display:none}}
  .fig-grid .schema.schema-voie{background:#fff}
  .fig-grid .schema.schema-voie img{aspect-ratio:1260/1630;object-fit:contain;object-position:center;background:#fff}
  .fig-grid figcaption .credit{display:block}
  .fig-grid figcaption .credit-src{display:block;margin-top:1px}
  .proj-view{position:relative;overflow-x:clip}
  .proj-hero{position:relative}
  .proj-hero-in{position:relative;z-index:1}
  .proj-wm{position:absolute;top:0;left:50%;width:100vw;transform:translateX(-50%);z-index:0;pointer-events:none;opacity:.22;-webkit-mask-image:linear-gradient(to bottom,transparent,#000 9%,#000 62%,transparent);mask-image:linear-gradient(to bottom,transparent,#000 9%,#000 62%,transparent)}
  .proj-wm img{display:block;width:100%;height:auto;filter:grayscale(.2)}
  .proj-wm-full{top:0;bottom:0;-webkit-mask-image:linear-gradient(to bottom,transparent,#000 24%);mask-image:linear-gradient(to bottom,transparent,#000 24%)}
  .proj-wm-full img{height:100%;object-fit:cover;object-position:center}
  .proj-outputs .entry{border-bottom:none}
  #view-proj-master .proj-wm{height:62vh;opacity:.2}
  #view-proj-master .proj-wm img{height:100%;object-fit:cover;object-position:center center}
  .proj-right .proj-resume p{font-size:15.5px;line-height:1.62;margin:0 0 15px;text-align:justify;-webkit-hyphens:none;hyphens:none}
  .proj-right .thesis-photo{margin-top:8px}
  .proj-info>p[style]{font-size:13.5px;line-height:1.5}
  .proj-sec{margin-top:48px;font-weight:300}
  @media(max-width:820px){.proj-cols{grid-template-columns:1fr;column-gap:0;row-gap:6px;grid-template-areas:"info" "resume" "prod"}.proj-h1{font-size:23px}.proj-prod{margin-top:22px}}
  .fig-section{margin:0 0 34px}
  .fig-h{font-family:var(--serif);font-weight:400;font-size:18px;margin:26px 0 16px;padding-bottom:7px;border-bottom:1px solid var(--line);letter-spacing:.01em}
  .fig-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(225px,1fr));gap:18px;max-height:none;overflow:visible;align-items:stretch}
  .fig-grid .schema, .fig-grid .doc{width:100%;margin:0;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}
  .fig-grid .schema img, .fig-grid .doc img{width:100%;height:auto;aspect-ratio:var(--fig-ar,3/2);object-fit:contain;object-position:center;background:#fff;box-sizing:border-box}
  .fig-grid .fig-nat img{aspect-ratio:auto;object-fit:fill;height:auto}
  .fig-grid figcaption{padding:11px 14px 13px;border-top:1px solid var(--line-soft);font-size:13px;line-height:1.42}
  .fig-grid figcaption .lic{display:inline-block;margin-top:6px;font-size:9.5px;letter-spacing:.05em;color:var(--ink-faint);text-decoration:none;opacity:.7}
  .fig-grid figcaption .lic:hover{color:var(--gold);opacity:1}
  .lb-cap .lic{display:block;font-family:var(--sans);font-size:11.5px;color:#bcae99;margin-top:3px;letter-spacing:0;opacity:1;text-decoration:none}
  .lb-cap .lic:hover{color:#d8cdb6}
  .foot-lic{display:block;margin-top:5px;font-size:12px;color:var(--ink-faint)}
  .foot-lic a{color:inherit;font:inherit;text-decoration:underline}
  .foot-lic a:hover{opacity:.7}
  .cite{margin:2px 0 26px}
  .cite summary{cursor:pointer;display:inline-block;font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--gold);list-style:none}
  .cite summary::-webkit-details-marker{display:none}
  .cite summary::after{content:' →'}
  .cite[open] summary::after{content:' ↓'}
  .cite p{margin:11px 0 0;font-size:13.5px;line-height:1.55;color:var(--ink-soft);max-width:680px}
  .cite a{color:var(--gold);text-decoration:none}
  .cite a:hover{text-decoration:underline}
  .cv-cat{font-family:var(--serif);font-weight:500;font-size:23px;color:var(--ink);margin:40px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--gold-soft)}
  @media(max-width:760px){.proj-grid{grid-template-columns:1fr 1fr;gap:12px}}
  @media(max-width:480px){.proj-grid{grid-template-columns:1fr}}
'''
H=H.replace("</style>",css+"</style>",1)

# ===== Theme « Albâtre & ardoise » : titres Spectral + palette froide =====
H=H.replace('Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500',
            'Spectral:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500')
H=H.replace("--serif:'Fraunces', Georgia, serif","--serif:'Spectral', Georgia, serif")
# palette : warm beige/gold -> cool albatre/slate/petrol
H=H.replace('--bg:#f7f2ea','--bg:#f4f3ef')
H=H.replace('--surface:#fffdf8','--surface:#fafaf8').replace('#fffdf8','#fafaf8')
H=H.replace('--ink:#3d342a','--ink:#292d31')
H=H.replace('--ink-soft:#7a6a55','--ink-soft:#565b61')
H=H.replace('--ink-faint:#a4967f','--ink-faint:#8c9097')
H=H.replace('#8a6d3b','#3e5c66')   # gold -> petrol (accent), 2 occurrences
H=H.replace('--gold-soft:#b89b6a','--gold-soft:#7c97a0')
H=H.replace('--line:#e7ddcc','--line:#e1e0da')
H=H.replace('--line-soft:#efe7d8','--line-soft:#ecebe6')
H=H.replace('rgba(247,242,234,.9)','rgba(244,243,239,.9)')   # sticky header bg
H=H.replace('rgba(28,22,14,','rgba(25,28,31,')               # card overlay -> slate
H=H.replace('#f1e6d3,#e3d3b4','#e8e7e2,#d2d6d9')             # placeholder gradient -> cool
H=H.replace('#f1e6d3,#e0cdab','#e8e7e2,#cfd3d6')            # decorative blob -> cool
# widen content a touch (more horizontal room)
H=H.replace('--maxw:920px','--maxw:1040px')
# version bump
H=re.sub(r'var BUILD = \d+;','var BUILD = %d;'%V,H)
H=re.sub(r'<div class="ver" id="ver">v\d+</div>','<div class="ver" id="ver">v%d</div>'%V,H)
open(OUT,"w",encoding="utf-8").write(H)
print("OK written. length",len(H))
