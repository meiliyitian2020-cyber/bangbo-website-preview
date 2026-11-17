"""Validate this isolated, vendored project without overwriting product copy."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'template/manifest.json').read_text('utf-8'))
assert hashlib.sha256((root/'template/index.html').read_bytes()).hexdigest()==manifest['sha256']
content=json.loads((root/'product-copy.json').read_text('utf-8'))
assert set(content)=={'en','zh','hi','id'}
for language,copy in content.items():
 assert len(copy['scenes'])==5 and copy['downloadText']
for name in ['logo.png','app-icon.png']:
 assert (root/'brand'/name).is_file()
print('Isolated template, brand assets and four-language copy verified.')
