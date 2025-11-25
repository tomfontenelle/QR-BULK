# QR-BULK - Générateur de QR Codes en masse

Générateur de QR codes pour des références (exemple: E10000, E10001, etc.)

## Fonctionnalités

- Génération de QR codes à partir de références textuelles
- Génération en masse à partir d'un fichier CSV ou d'une liste
- Personnalisation de la taille et du niveau de correction d'erreur
- Export en SVG (format vectoriel, qualité infinie) avec nom de fichier basé sur la référence
- Support des URL personnalisées

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Générer un QR code unique

```bash
python qr_generator.py --reference E10000
```

### Générer plusieurs QR codes à partir d'un fichier

Créez un fichier `references.txt` avec une référence par ligne:
```
E10000
E10001
E10002
```

Puis lancez:
```bash
python qr_generator.py --file references.txt
```

### Générer des QR codes qui pointent vers une URL

```bash
python qr_generator.py --reference E10000 --url "https://monsite.com/produit/"
```

Cela créera un QR code qui pointe vers `https://monsite.com/produit/E10000`

### Options avancées

```bash
python qr_generator.py --reference E10000 \
  --size 10 \
  --border 2 \
  --error-correction H \
  --output-dir ./qrcodes
```

#### Paramètres disponibles:

- `--reference` : Référence unique (ex: E10000)
- `--file` : Fichier contenant une liste de références
- `--url` : URL de base pour construire l'URL complète
- `--size` : Taille du QR code (défaut: 10)
- `--border` : Taille de la bordure (défaut: 4)
- `--error-correction` : Niveau de correction d'erreur (L, M, Q, H)
- `--output-dir` : Dossier de sortie (défaut: ./QR CODE GENERE)

## Structure des fichiers générés

Les QR codes sont sauvegardés dans le dossier `QR CODE GENERE/` avec le nom:
```
<reference>.svg
```

Exemple: `E10000.svg`

## Exemples

### Exemple 1: Générer un QR code simple
```bash
python qr_generator.py --reference E10000
```
Génère un QR code contenant le texte "E10000"

### Exemple 2: Générer des QR codes pour un catalogue de produits
```bash
python qr_generator.py --file produits.txt --url "https://catalogue.entreprise.com/produit/"
```
Chaque QR code pointera vers une URL unique basée sur la référence

### Exemple 3: Générer des QR codes haute qualité
```bash
python qr_generator.py --file references.txt --size 15 --error-correction H
```

## Licence

MIT
