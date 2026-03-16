#!/usr/bin/env python

# Original: https://gitlab.com/myriacore/pandoc-kroki-filter
# Author:   MyriaCore
# Patched:  MiDES - Download SVGs with proper User-Agent header (avoids HTTP 403)
#           and convert to PDF via rsvg-convert for crisp vector graphics in LaTeX.
#           Mermaid uses PNG instead of SVG because its HTML <foreignObject> text
#           labels are not supported by rsvg-convert or LaTeX.
#           Includes rate-limiting, content-hash caching, and error handling.

import sys
import os
import base64
import hashlib
import zlib
import time
import subprocess
import tempfile
import urllib.request

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_caption

DIAGRAM_TYPES = ['blockdiag', 'bpmn', 'bytefield', 'seqdiag', 'actdiag',
                 'nwdiag', 'packetdiag', 'rackdiag', 'c4plantuml', 'ditaa',
                 'erd', 'excalidraw', 'graphviz', 'mermaid', 'nomnoml',
                 'plantuml', 'svgbob', 'umlet', 'vega', 'vegalite', 'wavedrom']
DIAGRAM_SYNONYMNS = {'dot': 'graphviz', 'c4': 'c4plantuml'}
AVAILABLE_DIAGRAMS = DIAGRAM_TYPES + list(DIAGRAM_SYNONYMNS.keys())

DIAGRAM_BLACKLIST = list(filter(
  lambda d: d in AVAILABLE_DIAGRAMS,
  os.environ.get('KROKI_DIAGRAM_BLACKLIST', '').split(',')
))

KROKI_SERVER = os.environ.get('KROKI_SERVER', 'https://kroki.io/')
KROKI_SERVER = KROKI_SERVER[:-1] if KROKI_SERVER[-1] == '/' else KROKI_SERVER

KROKI_DELAY = float(os.environ.get('KROKI_DELAY', '1'))

# Diagram types that use PNG instead of SVG->PDF conversion.
# Mermaid uses HTML <foreignObject> for text labels in SVG, which neither
# rsvg-convert nor LaTeX can render, resulting in missing text.
# PNG is rendered server-side with a full browser, so text is preserved.
KROKI_PNG_TYPES = set(
    os.environ.get('KROKI_PNG_TYPES', 'mermaid').split(',')
)

_output_dir = os.environ.get('KROKI_OUTPUT_DIR', tempfile.mkdtemp(prefix='kroki-'))
_request_count = 0


def download_image(url, output_path, accept='image/png'):
    """Download an image directly from kroki."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'pandoc-kroki-filter/1.0',
        'Accept': accept,
    })
    resp = urllib.request.urlopen(req, timeout=30)
    data = resp.read()
    with open(output_path, 'wb') as f:
        f.write(data)
    return len(data)


def download_and_convert(url, pdf_path):
    """Download SVG from kroki and convert to PDF via rsvg-convert."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'pandoc-kroki-filter/1.0',
        'Accept': 'image/svg+xml',
    })
    resp = urllib.request.urlopen(req, timeout=30)
    svg_data = resp.read()

    svg_path = pdf_path.replace('.pdf', '.svg')
    with open(svg_path, 'wb') as f:
        f.write(svg_data)

    subprocess.run(
        ['rsvg-convert', '-f', 'pdf', '-o', pdf_path, svg_path],
        check=True, capture_output=True,
    )
    os.remove(svg_path)
    return len(svg_data)


def kroki(key, value, format_, _):
    global _request_count
    if key == 'CodeBlock':
        [[ident, classes, keyvals], content] = value
        diagram_classes = list(set(AVAILABLE_DIAGRAMS) & set(classes))
        if len(diagram_classes) == 1 and diagram_classes[0] not in DIAGRAM_BLACKLIST:
            caption, typef, keyvals = get_caption(keyvals)

            if diagram_classes[0] in DIAGRAM_SYNONYMNS.keys():
                diagram_type = DIAGRAM_SYNONYMNS[diagram_classes[0]]
            else:
                diagram_type = diagram_classes[0]

            # Rate-limit
            if _request_count > 0:
                time.sleep(KROKI_DELAY)
            _request_count += 1

            encoded = base64.urlsafe_b64encode(
                zlib.compress(content.encode('utf-8'), 9)
            ).decode()

            content_hash = hashlib.sha1(content.encode('utf-8')).hexdigest()[:12]

            # Use PNG for diagram types with SVG text rendering issues
            if diagram_type in KROKI_PNG_TYPES:
                url = f'{KROKI_SERVER}/{diagram_type}/png/{encoded}'
                filename = f'kroki_{content_hash}.png'
                filepath = os.path.join(_output_dir, filename)
                try:
                    size = download_image(url, filepath, 'image/png')
                    sys.stderr.write(f'[kroki] {_request_count}: {diagram_type} -> {filename} ({size} bytes PNG)\n')
                    return Para([Image([ident, [], keyvals], caption, [filepath, typef])])
                except Exception as e:
                    sys.stderr.write(f'[kroki] {_request_count}: ERROR {diagram_type} - {e}\n')
                    return None

            url = f'{KROKI_SERVER}/{diagram_type}/svg/{encoded}'
            filename = f'kroki_{content_hash}.pdf'
            filepath = os.path.join(_output_dir, filename)

            try:
                svg_size = download_and_convert(url, filepath)
                sys.stderr.write(f'[kroki] {_request_count}: {diagram_type} -> {filename} ({svg_size} bytes SVG)\n')
                return Para([Image([ident, [], keyvals], caption, [filepath, typef])])
            except Exception as e:
                sys.stderr.write(f'[kroki] {_request_count}: ERROR {diagram_type} - {e}\n')
                return None


def main():
    toJSONFilter(kroki)

if __name__ == "__main__":
    main()
