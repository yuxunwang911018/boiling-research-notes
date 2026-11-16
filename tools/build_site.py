"""Build the research notebook using Python 3's standard library."""
from pathlib import Path
from html import escape
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'


def e(value):
    return escape(str(value), quote=True)


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def render(name, **values):
    text = (ROOT / 'templates' / name).read_text(encoding='utf-8')
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    remaining = re.findall(r'\{\{\w+\}\}', text)
    if remaining:
        raise ValueError(f'Unfilled template fields: {remaining}')
    return text


def validate_case(case, path):
    required = {'slug', 'order', 'label', 'title', 'summary', 'version', 'updated',
                'question', 'conditions', 'methods', 'metrics', 'interpretation',
                'acceptance', 'limitations', 'media', 'sources'}
    if required - case.keys():
        raise ValueError(f'{path.name}: missing {required - case.keys()}')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', case['slug']) or case['slug'] != path.stem:
        raise ValueError(f'{path.name}: invalid slug')
    if case['slug'] in {'index', 'methods', 'rules'}:
        raise ValueError('Case slug conflicts with a fixed page')
    if type(case['order']) is not int or case['order'] < 1:
        raise ValueError('Case order must be a positive integer')
    for name in ('conditions', 'methods', 'metrics', 'limitations', 'media', 'sources'):
        if not case[name]:
            raise ValueError(f'{path.name}: {name} must not be empty')
    for metric in case['metrics']:
        for field in ('label', 'model', 'baseline', 'unit', 'aggregation'):
            if field not in metric:
                raise ValueError(f'Metric missing {field}')
        for field in ('model', 'baseline'):
            if type(metric[field]) not in (float, int):
                raise ValueError(f'Metric {field} must be a number')
    ids = [s['id'] for s in case['sources']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source ids')
    for medium in case['media']:
        if medium['source_id'] not in ids:
            raise ValueError('Media source is not declared')
        for field in ('poster', 'animation'):
            p = (ROOT / medium[field]).resolve()
            if ROOT / 'assets' not in p.parents or not p.is_file():
                raise ValueError(f'Invalid asset: {medium[field]}')


def main():
    cases = []
    for path in sorted((ROOT / 'content/cases').glob('*.json')):
        case = json.loads(path.read_text(encoding='utf-8'))
        validate_case(case, path)
        cases.append(case)
    cases.sort(key=lambda c: (c['order'], c['slug']))
    if not cases:
        raise ValueError('At least one case is required')
    if len({c['order'] for c in cases}) != len(cases):
        raise ValueError('Case order must be unique')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for folder in ('assets', 'styles', 'scripts'):
        shutil.copytree(ROOT / folder, OUT / folder, ignore=shutil.ignore_patterns('.gitkeep'))
    shutil.copyfile(ROOT / 'AGENTS.md', OUT / 'AGENTS.md')
    shutil.copyfile(ROOT / 'content/cases' / (cases[0]['slug'] + '.json'), OUT / 'case-template.json')
    (OUT / '.nojekyll').touch()

    def page(filename, title, description, body):
        links = [('index.html', '首頁'), ('methods.html', '研究方法')]
        links += [(c['slug'] + '.html', c['label']) for c in cases]
        links += [('rules.html', '協作規則')]
        nav = ''.join(f'<a href="{e(href)}"' + (' aria-current="page"' if href == filename else '') + f'>{e(label)}</a>' for href, label in links)
        (OUT / filename).write_text(render('base.html', title=e(title), description=e(description), navigation=nav, content=body), encoding='utf-8')

    home = load('content/pages/home.json')
    cards = []
    for i, case in enumerate(cases, 1):
        cards.append(f'''<a class="case-card" href="{e(case['slug'])}.html"><div class="case-card-copy"><span class="case-number">{i:02d} / {e(case['label'])}</span><h3>{e(case['title'])}</h3><p>{e(case['summary'])}</p><div class="case-card-footer"><span>{e(case['version'])}</span><span>閱讀筆記 ↗</span></div></div><div class="case-thumbnail"><img src="{e(case['media'][1]['poster'] if len(case['media']) > 1 else case['media'][0]['poster'])}" alt="{e(case['label'])} 氣相場比較預覽" loading="lazy" width="765" height="750"></div></a>''')
    concepts = ''.join(f'<div><span class="concept-number">{e(c["number"])}</span><h3>{e(c["title"])}</h3><p>{e(c["text"])}</p></div>' for c in home['concepts'])
    page('index.html', '首頁', home['intro'], render('home.html', eyebrow=e(home['eyebrow']), headline=e(home['title']).replace('\n', '<br>'), intro=e(home['intro']), question=e(home['question']), answer=e(home['answer']), case_cards=''.join(cards), concepts=concepts))

    methods = load('content/pages/methods.json')
    steps = ''.join(f'<div id="step-{i}" class="workflow-step"><span class="step-number">{i:02d}</span><div><h2>{e(s["title"])}</h2><p>{e(s["text"])}</p></div></div>' for i, s in enumerate(methods['steps'], 1))
    glossary = ''.join(f'<details><summary>{e(g["term"])}<span aria-hidden="true">＋</span></summary><p>{e(g["definition"])}</p></details>' for g in methods['glossary'])
    source_list = ''.join(f'<li><strong>{e(s["title"])}</strong><code>{e(s["path"])}</code></li>' for s in methods['sources'])
    page('methods.html', '研究方法', methods['intro'], render('methods.html', heading=e(methods['title']), intro=e(methods['intro']), steps=steps, glossary=glossary, sources=source_list))

    for i, case in enumerate(cases):
        conditions = ''.join(f'<div><dt>{e(c["label"])}</dt><dd>{e(c["value"])}</dd></div>' for c in case['conditions'])
        metrics = ''.join(f'<tr><th scope="row">{e(m["label"])}</th><td>{m["model"]:.6f}</td><td>{m["baseline"]:.6f}</td><td>{e(m["unit"])}</td><td>{e(m["aggregation"])}</td></tr>' for m in case['metrics'])
        tabs = []
        for j, m in enumerate(case['media']):
            attrs = ' '.join(f'data-{key}="{e(m[key])}"' for key in ('poster', 'animation', 'alt', 'caption'))
            tabs.append(f'<button type="button" class="media-choice" aria-pressed="{"true" if j == 0 else "false"}" {attrs}>{e(m["label"])}</button>')
        first = case['media'][0]
        media = f'''<figure class="media-viewer"><div class="media-toolbar"><div class="media-choices" role="group" aria-label="選擇物理場">{''.join(tabs)}</div><span class="media-status" role="status">靜態快照</span></div><div class="media-canvas"><img class="field-image" src="{e(first['poster'])}" alt="{e(first['alt'])}" width="765" height="750" loading="lazy"></div><div class="media-controls"><button type="button" class="play-button" aria-pressed="false">播放動畫 <span aria-hidden="true">▷</span></button><a class="original-link" href="{e(first['poster'])}" target="_blank" rel="noopener">開啟完整圖像 ↗</a></div><figcaption class="media-caption">{e(first['caption'])}</figcaption></figure>'''
        sources = ''.join(f'<li id="source-{e(s["id"])}"><strong>{e(s["title"])}</strong><code>{e(s["path"])}</code></li>' for s in case['sources'])
        others = [c for c in cases if c['slug'] != case['slug']]
        next_link = f'<a class="button outline" href="{e(others[0]["slug"])}.html">{e(others[0]["label"])} 案例 →</a>' if others else '<a class="button outline" href="methods.html">閱讀研究方法 →</a>'
        page(case['slug'] + '.html', case['label'] + ' 研究案例', case['summary'], render('case.html', label=e(case['label']), number=f'{i + 1:02d}', version=e(case['version']), heading=e(case['title']), summary=e(case['summary']), updated=e(case['updated']), question=e(case['question']), conditions=conditions, methods=''.join(f'<li>{e(m)}</li>' for m in case['methods']), media=media, metrics=metrics, interpretation=e(case['interpretation']), automatic=e(case['acceptance']['automatic']), stage=e(case['acceptance']['stage']), limitations=''.join(f'<li>{e(l)}</li>' for l in case['limitations']), sources=sources, next_case=next_link))
    page('rules.html', '協作規則', '以 AGENTS.md、共同內容格式與可追溯來源，讓 AI 持續新增研究筆記。', render('rules.html'))
    print(f'Built {len(cases) + 3} HTML pages from {len(cases)} case files → {OUT}')


if __name__ == '__main__':
    main()
