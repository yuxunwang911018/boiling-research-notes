"""Check generated pages, links, accessibility basics and asset integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'dist'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.headings = []
        self.errors = []
        self.lang = None
        self.images = 0
        self.tables = 0
        self.captions = 0
        self.mains = 0

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'main':
            self.mains += 1
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'img':
            self.images += 1
            if not attrs.get('alt'):
                self.errors.append('Image missing meaningful alt')
        if tag == 'table':
            self.tables += 1
        if tag == 'caption':
            self.captions += 1
        if tag == 'th' and attrs.get('scope') not in ('col', 'row'):
            self.errors.append('Table header missing scope')
        for key in ('href', 'src', 'data-poster', 'data-animation'):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    errors = []
    pages = {}
    for path in sorted(SITE.glob('*.html')):
        page = Page(path)
        raw = path.read_text(encoding='utf-8')
        page.feed(raw)
        if page.lang != 'zh-Hant':
            errors.append(f'{path.name}: missing zh-Hant language')
        if page.headings.count(1) != 1 or page.mains != 1:
            errors.append(f'{path.name}: expected one h1 and main')
        for prev, current in zip(page.headings, page.headings[1:]):
            if current > prev + 1:
                errors.append(f'{path.name}: skipped heading level')
        if len(set(page.ids)) != len(page.ids):
            errors.append(f'{path.name}: duplicate ids')
        if page.tables != page.captions:
            errors.append(f'{path.name}: table missing caption')
        if re.search(r'\{\{\w+\}\}|/Users/|review-materials/', raw):
            errors.append(f'{path.name}: unfilled template or local-only path')
        errors += [f'{path.name}: {e}' for e in page.errors]
        pages[path.resolve()] = page
    if not pages:
        errors.append('No pages were built')

    checked = 0
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                if url.scheme not in ('https', 'mailto'):
                    errors.append(f'{path.name}: unexpected URL scheme: {href}')
                continue
            if url.path.startswith('/'):
                errors.append(f'{path.name}: root path breaks repository hosting: {href}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target != SITE.resolve() and SITE.resolve() not in target.parents:
                errors.append(f'{path.name}: path outside website: {href}')
            elif not target.is_file():
                errors.append(f'{path.name}: broken link: {href}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.name}: broken anchor: {href}')
            checked += 1

    manifest = json.loads((ROOT / 'docs/asset-manifest.json').read_text(encoding='utf-8'))
    known = set()
    for asset in manifest['assets']:
        known.add(asset['local_path'])
        for base in (ROOT, SITE):
            path = base / asset['local_path']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
                errors.append(f'Asset changed or missing: {path}')
    case_files = sorted((ROOT / 'content/cases').glob('*.json'))
    for file in case_files:
        case = json.loads(file.read_text(encoding='utf-8'))
        output = SITE / (case['slug'] + '.html')
        if output.resolve() not in pages:
            errors.append(f'Case not generated: {file.name}')
            continue
        for anchor in ('question', 'conditions', 'method', 'results', 'limitations', 'sources'):
            if anchor not in pages[output.resolve()].ids:
                errors.append(f'{file.name}: missing mandatory section {anchor}')
        for medium in case['media']:
            for field in ('poster', 'animation'):
                if medium[field] not in known:
                    errors.append(f'Untracked case asset: {medium[field]}')
        for path in pages:
            if case['slug'] + '.html' not in pages[path].links:
                errors.append(f'{path.name}: case missing from navigation')

    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} pages, {len(case_files)} cases, {checked} relative links/media references, {len(known)} original asset hashes.')
    print('PASS: six sections per case; one h1/main; image alt; table captions and header scope; portable relative paths.')


if __name__ == '__main__':
    main()
