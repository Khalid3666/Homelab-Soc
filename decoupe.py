#!/usr/bin/env python3
"""Découpe le rapport Markdown en respectant la hiérarchie titres / sous-sections.

Usage (à la racine du projet, à côté de test.md et de son dossier media/) :
    python decoupe.py test.md

Hiérarchie :
  - chaque « # »  (grand titre)  devient une SECTION : un dossier NN-slug/
    son texte d'introduction va dans l'index.md de ce dossier ;
  - chaque « ## » (sous-section) devient une PAGE dans ce dossier : NN-slug.md.
Dans le menu du site, les sous-sections apparaissent ainsi en retrait, sous leur
grand titre (voir les options navigation.* ajoutées dans mkdocs.yml).

Détails :
  - l'ordre est conservé par un préfixe numérique (01-, 02-…), sur les dossiers
    comme sur les pages ;
  - le titre long d'origine est gardé tel quel en haut de chaque page (« # … ») ;
  - le dossier media/ est copié dans docs/media/, et les liens d'image sont
    ajustés selon la profondeur du fichier pour rester valides.
"""
import re
import shutil
import sys
import unicodedata
from pathlib import Path

DOCS = Path("docs")


def slug(titre):
    """« Wazuh Security Assessment configuration. » -> « wazuh-security-assessment »."""
    sans_accent = "".join(
        c for c in unicodedata.normalize("NFKD", titre) if not unicodedata.combining(c)
    )
    mots = re.sub(r"[^a-z0-9]+", "-", sans_accent.lower()).strip("-").split("-")
    return "-".join(mots[:5]) or "section"  # 5 mots max pour un nom court


def analyser(texte):
    """Renvoie (avant, sections) où :
      avant    = lignes situées avant le premier « # »
      sections = [{titre, intro, pages:[(titre, lignes)]}] (une entrée par « # »)."""
    avant, sections = [], []
    cible = avant
    dans_code = False
    for ligne in texte.splitlines():
        if ligne.startswith("```"):
            dans_code = not dans_code
        m = None if dans_code else re.match(r"^(#{1,2})\s+(.*)$", ligne)
        if m and len(m.group(1)) == 1:                      # grand titre « # »
            sections.append({"titre": m.group(2).strip(), "intro": [], "pages": []})
            cible = sections[-1]["intro"]
        elif m:                                             # sous-section « ## »
            if not sections:  # un « ## » sans « # » au-dessus : on crée une section d'accueil
                sections.append({"titre": "Documentation", "intro": [], "pages": []})
            sections[-1]["pages"].append([m.group(2).strip(), []])
            cible = sections[-1]["pages"][-1][1]
        else:
            cible.append(ligne)
    return avant, sections


def ajuster_images(texte, profondeur):
    """Réécrit « media/x.png » en « ../media/x.png » selon la profondeur du fichier."""
    if profondeur == 0:
        return texte
    prefixe = "../" * profondeur
    return re.sub(r'(src="|\]\()(?:\.\./)*media/', rf"\1{prefixe}media/", texte)


def ecrire(chemin, titre, lignes):
    corps = ajuster_images("\n".join(lignes).strip("\n"), len(chemin.relative_to(DOCS).parts) - 1)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(f"# {titre}\n\n{corps}\n", encoding="utf-8")
    print(f"  {chemin.relative_to(DOCS).as_posix()}   (titre : {titre})")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage : python decoupe.py test.md")
    source = Path(sys.argv[1])
    avant, sections = analyser(source.read_text(encoding="utf-8"))

    DOCS.mkdir(exist_ok=True)

    # Texte avant le premier « # » (learning paths, idées) -> page d'accueil.
    if any(l.strip() for l in avant):
        ecrire(DOCS / "index.md", "Accueil", avant)

    for n, section in enumerate(sections, start=1):
        dossier = DOCS / f"{n:02d}-{slug(section['titre'])}"
        ecrire(dossier / "index.md", section["titre"], section["intro"])  # le grand titre
        for m, (titre, lignes) in enumerate(section["pages"], start=1):    # ses sous-sections
            ecrire(dossier / f"{m:02d}-{slug(titre)}.md", titre, lignes)

    media = source.parent / "media"
    if media.is_dir():
        shutil.rmtree(DOCS / "media", ignore_errors=True)
        shutil.copytree(media, DOCS / "media")
        print(f"  dossier media/ copié dans {DOCS / 'media'}")

    print(f"\n{len(sections)} section(s) écrite(s) dans {DOCS}/")


if __name__ == "__main__":
    main()
