# Frontend Dashboard - SoH Predictor

Dashboard web moderne pour la prédiction du SoH des batteries.

## 🎨 Technologies

- **HTML5** + **Tailwind CSS** : Interface responsive
- **JavaScript Vanilla** : Logique frontend
- **Chart.js** : Visualisations interactives
- **Google Fonts** : Orbitron + Inter

## 🚀 Déploiement sur Vercel

### Prérequis
- Compte Vercel (gratuit)
- GitHub repo

### Étapes :

1. **Pousser le code sur GitHub**
```bash
   git add frontend/
   git commit -m "Add frontend"
   git push
```

2. **Connecter à Vercel**
   - Aller sur https://vercel.com
   - Cliquer sur "New Project"
   - Importer votre repo GitHub
   - Root Directory : `frontend`
   - Framework Preset : Other
   - Cliquer sur "Deploy"

3. **URL publique**
```
   https://battery-soh.vercel.app
```

4. **Configurer l'API**
   - Ouvrir `app.js`
   - Ligne 2 : Remplacer `API_URL` par votre URL Hugging Face
```javascript
   const API_URL = 'https://ona6-battery-soh-api.hf.space';
```
   - Re-déployer

## 🎨 Design

### Couleurs (extraites du logo)
- **Bleu foncé** : `#1e40af` (Primary)
- **Vert** : `#10b981` (Secondary)
- **Jaune/Orange** : `#fbbf24` (Accent)
- **Bleu très foncé** : `#0f172a` (Dark)

### Polices
- **Orbitron** : Titres (style tech/futuriste)
- **Inter** : Texte (lisibilité)

## 📁 Fichiers
```
frontend/
├── index.html       # Page principale
├── app.js           # Logique JavaScript
├── logo.png         # Logo du projet
├── vercel.json      # Configuration Vercel
└── README.md        # Ce fichier
```

## 🧪 Test Local

1. Ouvrir `index.html` dans un navigateur
2. Tester l'upload CSV
3. (API non fonctionnelle en local, nécessite déploiement)

## 📱 Responsive

- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (320px - 767px)

## 🔗 Liens Utiles

- **Vercel Docs** : https://vercel.com/docs
- **Tailwind CSS** : https://tailwindcss.com
- **Chart.js** : https://www.chartjs.org