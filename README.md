# 🤖 SaaS de Résumé Automatique

> Une application web minimaliste et performante pour générer des résumés concis de textes longs, propulsée par l'API Anthropic (Claude).

---

## 🏗️ Architecture

Le projet suit une séparation claire des responsabilités :

- **Backend** — API RESTful développée avec **FastAPI**, gérant la logique métier et la communication sécurisée avec l'IA.
- **Frontend** — Interface épurée permettant une interaction simple avec l'API, avec gestion d'état (chargement, erreurs).

---

## 🚀 Installation

### Prérequis

- Python **3.12+** (recommandé pour la compatibilité native des bibliothèques Rust/Pydantic)
- Une clé API **Anthropic**

### Étapes

**1. Configurer l'environnement virtuel**

```bash
# Création
python3 -m venv .venv

# Activation
source .venv/bin/activate
```

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Configurer les secrets**

Copiez le fichier d'exemple et renseignez vos variables :

```bash
cp .env.example .env
# Éditez .env et insérez votre ANTHROPIC_API_KEY et ALLOWED_ORIGINS
```

**4. Lancer le serveur**

```bash
uvicorn backend.main:app --reload
```

L'API est accessible sur `http://localhost:8000` et la documentation interactive sur `http://localhost:8000/docs`.

---

## 💡 Choix Techniques

| Technologie | Justification |
|---|---|
| **FastAPI** | Rapidité d'exécution, typage robuste via Pydantic, documentation interactive automatique (`/docs`) |
| **python-dotenv** | Isolation des variables d'environnement pour sécuriser la clé API |
| **`.gitignore`** | Protection des données sensibles hors du dépôt |
| **Gestion centralisée des erreurs** | Communication claire et cohérente entre le backend et le frontend |

---

## 🔒 Sécurité

- La clé API Anthropic n'est **jamais** exposée côté frontend.
- Les variables sensibles sont chargées exclusivement via `.env`, exclu du contrôle de version.
- Le CORS est restreint aux origines définies dans `ALLOWED_ORIGINS` (`.env`).

---

## 📋 Changelog

### v1.2.0
- **CI** — Ajout d'un workflow GitHub Actions Pylint sur chaque push vers `main`

### v1.1.0
- **Sécurité** — CORS restreint : `allow_origins=["*"]` remplacé par une liste configurable via la variable d'environnement `ALLOWED_ORIGINS`
- **Logs** — Ajout de logs détaillés à chaque requête (IP, taille du texte, modèle utilisé, durée de traitement, taille du résumé)
- **Repo** — Suppression de `.clinerules` et `.clineignore` du contrôle de version (configs personnelles)

### v1.0.0
- Version initiale : backend FastAPI + frontend HTML, résumé de texte via l'API Anthropic

---

> Projet développé avec une approche centrée sur la **maintenabilité** et les **bonnes pratiques** de développement logiciel.
