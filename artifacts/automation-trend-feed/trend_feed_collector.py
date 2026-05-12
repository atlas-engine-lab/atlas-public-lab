#!/usr/bin/env python3
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path

FEEDS = {
    "hn_frontpage": "https://hnrss.org/frontpage",
    "github_trending_python": "https://github.com/trending/python?since=daily",
}

OUT_DIR = Path('/home/stripes/.hermes/revenue-engine/data')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore')


def parse_hn_rss(xml_text: str):
    root = ET.fromstring(xml_text)
    titles = []
    for item in root.findall('.//item/title'):
        if item.text:
            titles.append(item.text.strip())
    return titles


def parse_github_trending(html: str):
    return re.findall(r'<h2[^>]*>\s*<a[^>]*>(.*?)</a>', html, flags=re.S)


def tokenize(lines):
    words = []
    for line in lines:
        line = re.sub(r'<[^>]+>', ' ', line)
        toks = re.findall(r"[A-Za-z][A-Za-z0-9\-\+]{2,}", line.lower())
        words.extend(toks)
    stop = {
        'the','and','for','with','from','that','this','your','you','are','not','how','why','what','when','new','using','into','over','under','best','more','than','one','two','three','about','their'
    }
    return [w for w in words if w not in stop]


def main():
    all_lines = []
    raw = {}

    hn_xml = fetch_text(FEEDS['hn_frontpage'])
    hn_titles = parse_hn_rss(hn_xml)
    raw['hn_frontpage_titles'] = hn_titles
    all_lines.extend(hn_titles)

    gh_html = fetch_text(FEEDS['github_trending_python'])
    gh_items = parse_github_trending(gh_html)
    gh_items = [re.sub(r'\s+', ' ', x).strip() for x in gh_items]
    raw['github_trending_python'] = gh_items
    all_lines.extend(gh_items)

    tokens = tokenize(all_lines)
    top = Counter(tokens).most_common(40)

    now = datetime.utcnow().strftime('%Y-%m-%d')
    payload = {
        'date_utc': now,
        'sources': list(FEEDS.keys()),
        'items_collected': len(all_lines),
        'top_terms': top,
        'sample_titles': all_lines[:20],
    }

    (OUT_DIR / f'trend_snapshot_{now}.json').write_text(json.dumps(payload, indent=2))
    (OUT_DIR / 'latest_trend_snapshot.json').write_text(json.dumps(payload, indent=2))

    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
