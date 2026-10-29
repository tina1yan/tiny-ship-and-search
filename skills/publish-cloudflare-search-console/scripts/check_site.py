#!/usr/bin/env python3
"""Read-only public release checks; does not verify Search Console ownership."""
import argparse
import json
from pathlib import Path
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('base_url')
p.add_argument('--verification-file', type=Path)
a = p.parse_args()
base = a.base_url.rstrip('/')
if urllib.parse.urlsplit(base).scheme != 'https':
    p.error('Use the canonical HTTPS origin.')
origin = urllib.parse.urlsplit(base)
if origin.path or origin.query or origin.fragment:
    p.error('Use the site origin without a path, query or fragment.')

class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlsplit(newurl)
        if target.scheme != 'https' or target.netloc != origin.netloc:
            raise ValueError('Unexpected cross-origin or non-HTTPS redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

opener = urllib.request.build_opener(SameOriginRedirect())

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'SiteReleaseCheck/1.0'})
    with opener.open(req, timeout=20) as r:
        return r.status, r.geturl(), r.headers.get('Content-Type', ''), r.read()

report = {'base_url': base, 'checks': [], 'search_console': 'not checked', 'indexing': 'not checked'}
try:
    status, url, mime, robots = get(base + '/robots.txt')
    lines = robots.decode().splitlines()
    sitemaps = [line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('sitemap:')]
    report['checks'].append({'route': '/robots.txt', 'status': status, 'sitemaps': sitemaps})
    if not sitemaps:
        raise ValueError('robots.txt has no sitemap declaration')
    for sitemap in sitemaps:
        if urllib.parse.urlsplit(sitemap).netloc != origin.netloc:
            raise ValueError('Review cross-origin sitemap before following it')
        status, url, mime, content = get(sitemap)
        root = ET.fromstring(content)
        urls = [el.text for el in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if not urls:
            raise ValueError('Expected a URL sitemap with at least one page')
        report['checks'].append({'route': sitemap, 'status': status, 'url_count': len(urls), 'checked': min(50, len(urls)), 'skipped': max(0, len(urls)-50)})
        for target in urls[:50]:
            parsed = urllib.parse.urlsplit(target)
            if parsed.scheme != 'https' or parsed.netloc != origin.netloc:
                raise ValueError('Review non-canonical sitemap URL: ' + target)
            status, final, mime, body = get(target)
            report['checks'].append({'route': target, 'status': status, 'final_url': final, 'content_type': mime, 'bytes': len(body)})
    if a.verification_file:
        status, final, mime, body = get(base + '/' + a.verification_file.name)
        if final != base + '/' + a.verification_file.name:
            raise ValueError('Verification file unexpectedly redirects')
        if body != a.verification_file.read_bytes():
            raise ValueError('Verification file differs from supplied bytes')
        report['checks'].append({'verification_file': a.verification_file.name, 'exact_bytes': True, 'status': status})
    report['result'] = 'public checks passed; manually review robots rules and page metadata'
except Exception as e:
    report['result'] = 'failed'
    report['error'] = str(e)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1)
print(json.dumps(report, ensure_ascii=False, indent=2))
