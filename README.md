# Site personnel — Dr Alexandra Mallah

Site vitrine académique (géographe & architecte, postdoctorante UPHF).
En ligne : **https://alexandramallah.github.io/**
Dépôt GitHub Pages : `github.com/AlexandraMallah/alexandramallah.github.io` (branche `main`, build auto ~1 min).

> ⚠️ **Ne pas éditer `index.html` à la main.** Le fichier est **généré**. Toutes les
> modifications passent par `build/build.py`.

---

## 1. Architecture

- **Site mono-fichier** : tout est dans `index.html` (HTML + CSS + JS inline, sans framework).
- 3 « vues » basculées en JS par `showView(v)` :
  - `view-projects` (accueil, vignettes des 3 projets) · `view-proj-doctoral` · `view-proj-master` · `view-proj-postdoc` · `view-cv` · `view-contact`.
- Bilingue **EN (défaut) / FR** : classe sur `<body>` (`lang-en` / `lang-fr`) + spans `.en` / `.fr` masqués par CSS. Bouton `FR`/`EN` = `toggleLang()`.
- Anti-cache : numéro de build `?v=N` sur toutes les images + `version.json`.

### Pages projet
2 colonnes (`grid-template-areas`) : à gauche infos + productions, à droite résumé justifié ; documents graphiques en dessous ; **filigrane** (image en fond du « hero ») ; **flèches latérales ← →** (fixes, mi-hauteur) pour naviguer entre projets ; pied de page collé en bas.

---

## 2. Construire & déployer

```bash
cd "Site-Recherche"

# 1. éditer build/build.py (et/ou les images)
#    → incrémenter le numéro de version :  V=104  (en haut de build.py)

# 2. régénérer index.html
python3 build/build.py            # écrit ../index.html depuis build/base.html

# 3. mettre version.json au MÊME numéro
printf '{"build": 104}\n' > version.json

# 4. publier
git add -A && git commit -m "v104 : ..." && git push

# 5. vérifier la mise en ligne (~1 min)
curl -s "https://alexandramallah.github.io/version.json?cb=$RANDOM"
```

**Le numéro de version est à 3 endroits, tous pilotés par `V=` dans build.py** :
`var BUILD = N`, la pastille `vN` en bas, et les `?v=N`. **Seul `version.json` est à mettre à jour à la main** (étape 3) pour qu'il corresponde.

Dépendances : `python3` (génération HTML, aucune lib) ; `pypdfium2` + `Pillow` uniquement pour re-rendre des images.

---

## 3. Fonctionnement de `build/build.py`

1. Lit **`build/base.html`** = instantané du site *avant* la refonte (ancienne structure, sert de réservoir : groupes publications/communications/médias, carte thèse, panneau RITMEA, pied de page, lightbox, menu…).
2. **Extrait** des morceaux de `base.html` (publications, communications, médias, résumé de thèse, jury, sous-titre, panneau RITMEA…).
3. **Reconstruit** le `<body>` (accueil + 3 pages projet + CV) et le **splice** à la place de l'ancien contenu.
4. Génère les **galeries de documents** en scannant `images/projets/<projet>/<section>/`.
5. Applique le **thème** par `H.replace(...)` en fin de script (palette froide + police Spectral — voir §5).
6. Écrit **`index.html`**.

Points d'entrée utiles dans `build.py` :
- `CAP` : légendes FR/EN + source + année de chaque document.
- `SRC` : libellés de source (`own`, `opendata`, `apur`).
- `ORD_collages / ORD_odo / ORD_tr` : ordre d'affichage des documents par section.
- `NAT` : documents affichés à leur **hauteur naturelle** (pas de cadre à ratio imposé).
- `ar="3/2"` etc. passé à `sec_block` : **ratio du cadre** d'une section (alignement des vignettes).
- `wm(pid, full=, img=)` : filigrane d'une page projet.
- `projnav(...)` : flèches latérales de navigation.
- `CITE` : bloc « Pour citer ces figures » (réf. de thèse).
- `LIC` : badge de licence CC.

---

## 4. Images

```
images/projets/
  doctoral/  acces.jpg + section-collages/ section-odonymes/ section-pantheon/ section-transversale/
  master/    acces.jpg (vignette + filigrane) + session-*.png + distribution-…png  (fond.jpg = non utilisé)
  postdoc/   acces.jpg
```
- **Vignette d'accueil** d'un projet = `acces.jpg`.
- **Filigrane** d'une page projet = même `acces.jpg` (postdoc plein écran ; master = bandeau centré ; doctoral = bandeau).
- **Documents graphiques** : versions web **haute résolution (~2400 px)** re-rendues depuis les **originaux vectoriels** (PDF / .ai) situés dans
  `~/Documents/Claude/Site_web/Projet_Geographie_de_l_invisible/Documents_graphiques/` et `…/Projet_appropriation_de_l_espace_public/Documents_graphiques/`.
- **Re-rendre** un document en HD : `pypdfium2` → `page.render(scale=cible/max(w,h), fill_color=(255,255,255,255))`. Suffixes `-fr` / `-en` pour les paires bilingues ; sans suffixe = version unique.

---

## 5. Identité visuelle

- **Palette « Albâtre & ardoise »** (froide) : fond `#f4f3ef`, encre `#292d31`, accent bleu-pétrole `#3e5c66`. Appliquée par `H.replace` en fin de build (l'ancienne palette beige/or est encore dans `base.html`).
- **Polices** : titres **Spectral** (`--serif`), corps **Archivo** (`--sans`) — Google Fonts.
- Résumés **justifiés, sans césure**.

---

## 6. Licence des figures

**CC BY-NC-ND 4.0** (figures © Alexandra Mallah). Affichée : mention en **pied de page** · **badge** sous chaque figure · bloc dépliable **« Pour citer ces figures → »** (doctoral + master) renvoyant à :
*Mallah Alexandra, 2025, Géographie de l'invisible. Les territoires de la mémoire des femmes, Thèse de doctorat en géographie, EHESS, Paris, 528 p.* — theses.fr/2025EHES0116

---

## 7. Pièges / à savoir

- **Tout passe par `build.py`** : modifier `index.html` directement = écrasé au prochain build.
- `build/base.html` ne change **que** pour des contenus non pilotés par build.py (texte RITMEA, entrées de publications/communications). Sinon, préférer un `H.replace` dans build.py (plus traçable).
- **Échappements Python** : ne jamais écrire `\00a0` dans une chaîne normale (= octet nul). Utiliser une vraie espace, `\\00a0`, ou une chaîne brute.
- `version.json` à **synchroniser manuellement** avec `V`.
- Pastille `vN` en bas à droite = version réellement servie.
- Aperçu local : `python3 -m http.server` ; si le bac à sable bloque la lecture du dossier, servir depuis une copie dans `/tmp`.

---

## 8. État actuel (v103)

Refonte 3 onglets · palette froide + Spectral · filigranes par projet · navigation latérale · documents HD alignés et légendés (sources / dates / licence) · bloc « Pour citer » · licence CC · pied de page collé.

**Option jamais tranchée** : appliquer le « plein écran » du postdoc à la **page thèse** (actuellement en `cover` qui remplit le hero) — à décider si on veut uniformiser.

*(Projet distinct, autre dépôt : « Mon-Tableau-de-Vie » — ne pas confondre.)*
