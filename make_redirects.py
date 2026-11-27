"""Writes one redirect page per docs page, plus a 404.html that redirects any other path.
Run by ReadTheDocs (see .readthedocs.yaml)."""
import sys
from html import escape
from pathlib import Path

NEW_BASE = 'https://www.otree.org/docs/en/latest/'

PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>oTree documentation has moved</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({url_js} + location.hash);</script>
</head><body>
<p>The oTree documentation has moved to <a href="{url}">{url}</a>.</p>
</body></html>
"""

# Any URL RTD can't find (old pages, other versions): /<lang>/<version>/<path> -> same <path>
NOT_FOUND = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>oTree documentation has moved</title>
<script>
  var parts = location.pathname.split('/').filter(Boolean);
  var rest = parts.slice(2).join('/') || 'index.html';
  location.replace('{base}' + rest + location.hash);
</script>
</head><body>
<p>The oTree documentation has moved to <a href="{base}index.html">{base}index.html</a>.</p>
</body></html>
"""


def main(out_dir):
    out = Path(out_dir)
    pages = Path(__file__).with_name('pages.txt').read_text().split()
    for page in pages:
        url = NEW_BASE + page
        dest = out / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(PAGE.format(url=escape(url), url_js=repr(url)))
    (out / '404.html').write_text(NOT_FOUND.replace('{base}', NEW_BASE))
    print(f'wrote {len(pages)} redirect pages + 404.html')


main(sys.argv[1])
