# Site de recherche — Dr Alexandra Mallah

Site vitrine du profil de chercheuse d'Alexandra Mallah, géographe (postdoctorat UPHF — LARSH).

- **Site statique** : un seul fichier `index.html` (HTML/CSS/JS pur, aucune dépendance).
- **Bilingue** : anglais par défaut, bascule français.
- **Hébergement** : GitHub Pages.

## Mettre à jour le site

```bash
cd "/Users/alexandramallah/Documents/Site-Recherche"
git add index.html
git commit -m "description du changement"
git push origin main
```

Incrémenter le numéro de version dans le `<footer>` (`v1` → `v2` …) à chaque push, pour vérifier que la bonne version est en ligne. GitHub Pages se met à jour en ~1 à 2 minutes.
