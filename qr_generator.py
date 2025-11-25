#!/usr/bin/env python3
"""
QR-BULK - Générateur de QR Codes en masse
Génère des QR codes à partir de références textuelles
"""

import argparse
import os
import sys
from pathlib import Path
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def create_qr_code(data, output_path, size=10, border=4, error_correction='M'):
    """
    Crée un QR code et le sauvegarde

    Args:
        data: Contenu du QR code (texte ou URL)
        output_path: Chemin de sortie pour l'image PNG
        size: Taille du QR code (1-40, défaut: 10)
        border: Taille de la bordure en modules (défaut: 4)
        error_correction: Niveau de correction d'erreur (L, M, Q, H)
    """
    # Mapping des niveaux de correction d'erreur
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # ~7% de correction
        'M': qrcode.constants.ERROR_CORRECT_M,  # ~15% de correction
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25% de correction
        'H': qrcode.constants.ERROR_CORRECT_H,  # ~30% de correction
    }

    # Créer l'objet QR code
    qr = qrcode.QRCode(
        version=1,  # Taille du QR code (1 = 21x21, augmente automatiquement si nécessaire)
        error_correction=error_levels.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_M),
        box_size=size,
        border=border,
    )

    # Ajouter les données
    qr.add_data(data)
    qr.make(fit=True)

    # Créer l'image
    img = qr.make_image(fill_color="black", back_color="white")

    # Sauvegarder
    img.save(output_path)
    print(f"✓ QR code créé: {output_path}")


def generate_from_reference(reference, url_base=None, output_dir="QR CODE GENERE", **kwargs):
    """
    Génère un QR code à partir d'une référence

    Args:
        reference: La référence (ex: E10000)
        url_base: URL de base optionnelle
        output_dir: Dossier de sortie
        **kwargs: Options supplémentaires (size, border, error_correction)
    """
    # Construire les données du QR code
    if url_base:
        # Supprimer le slash final de l'URL si présent
        url_base = url_base.rstrip('/')
        data = f"{url_base}/{reference}"
    else:
        data = reference

    # Créer le dossier de sortie s'il n'existe pas
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Construire le chemin de sortie
    output_path = os.path.join(output_dir, f"{reference}.png")

    # Générer le QR code
    create_qr_code(data, output_path, **kwargs)

    return output_path


def generate_from_file(file_path, url_base=None, output_dir="QR CODE GENERE", **kwargs):
    """
    Génère des QR codes à partir d'un fichier de références

    Args:
        file_path: Chemin vers le fichier contenant les références
        url_base: URL de base optionnelle
        output_dir: Dossier de sortie
        **kwargs: Options supplémentaires (size, border, error_correction)
    """
    if not os.path.exists(file_path):
        print(f"❌ Erreur: Le fichier {file_path} n'existe pas")
        sys.exit(1)

    print(f"📖 Lecture du fichier: {file_path}")

    with open(file_path, 'r') as f:
        references = [line.strip() for line in f if line.strip()]

    print(f"📊 {len(references)} référence(s) trouvée(s)")
    print()

    generated = []
    for i, reference in enumerate(references, 1):
        print(f"[{i}/{len(references)}] Génération pour: {reference}")
        try:
            output_path = generate_from_reference(reference, url_base, output_dir, **kwargs)
            generated.append(output_path)
        except Exception as e:
            print(f"❌ Erreur lors de la génération pour {reference}: {e}")

    print()
    print(f"✅ {len(generated)}/{len(references)} QR code(s) générés avec succès")
    print(f"📁 Dossier de sortie: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Générateur de QR codes pour références",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s --reference E10000
  %(prog)s --reference E10000 --url "https://monsite.com/produit/"
  %(prog)s --file references.txt
  %(prog)s --file references.txt --url "https://catalogue.com/item/" --size 15
        """
    )

    # Arguments principaux
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--reference', '-r',
                       help='Référence unique (ex: E10000)')
    group.add_argument('--file', '-f',
                       help='Fichier contenant une liste de références (une par ligne)')

    # Options
    parser.add_argument('--url', '-u',
                        help='URL de base (ex: https://monsite.com/produit/)')
    parser.add_argument('--output-dir', '-o',
                        default='QR CODE GENERE',
                        help='Dossier de sortie (défaut: QR CODE GENERE)')
    parser.add_argument('--size', '-s',
                        type=int,
                        default=10,
                        help='Taille du QR code (défaut: 10)')
    parser.add_argument('--border', '-b',
                        type=int,
                        default=4,
                        help='Taille de la bordure (défaut: 4)')
    parser.add_argument('--error-correction', '-e',
                        choices=['L', 'M', 'Q', 'H'],
                        default='M',
                        help='Niveau de correction d\'erreur (défaut: M)')

    args = parser.parse_args()

    # Préparer les options
    options = {
        'size': args.size,
        'border': args.border,
        'error_correction': args.error_correction
    }

    print("=" * 60)
    print("QR-BULK - Générateur de QR Codes")
    print("=" * 60)
    print()

    if args.reference:
        # Génération d'une seule référence
        print(f"🎯 Mode: Référence unique")
        print(f"📝 Référence: {args.reference}")
        if args.url:
            print(f"🔗 URL de base: {args.url}")
        print()

        generate_from_reference(
            args.reference,
            url_base=args.url,
            output_dir=args.output_dir,
            **options
        )
    else:
        # Génération à partir d'un fichier
        print(f"🎯 Mode: Fichier de références")
        if args.url:
            print(f"🔗 URL de base: {args.url}")
        print()

        generate_from_file(
            args.file,
            url_base=args.url,
            output_dir=args.output_dir,
            **options
        )


if __name__ == "__main__":
    main()
