"""Bundle current gallery images and SVG plans into one portable ZIP folder."""
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'public' / 'floor-plan'

def build():
    destination = SITE / 'downloads' / 'dream-house.zip'
    destination.parent.mkdir(exist_ok=True)
    files = [(p, f'floor-plans/{p.name}') for p in sorted(SITE.glob('*.svg'))]
    exterior = (SITE / 'exterior.html').read_text()
    current = sorted(set(re.findall(r'src="(exterior/[^"<>]+\.webp)"', exterior)))
    files.extend((SITE / name, name) for name in current)
    files.extend((p, f'interior/{p.name}') for p in sorted((SITE / 'interior').glob('*.webp')))
    with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
        for source, relative in files:
            archive.write(source, f'dream-house/{relative}')
        archive.writestr('dream-house/README.txt',
            'Dream House\n\nFloor plans: scalable SVG drawings.\n'
            'Exterior and interior: current WebP images.\n'
            'Images are conceptual studies; use the drawings for plan dimensions.\n')
    print(f'{destination}: {len(files)} images and plans')

if __name__ == '__main__':
    build()
