#!/usr/bin/env python3
"""Verify published index signatures, branding and file integrity using F-Droid."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import urllib.request
from fdroidserver import common, index

common.read_config()
fingerprint = 'B391053073F0F905594C914D4A63C9D1CDB673F00DDEEEA57CF7CF98480E1047'
address = 'https://alex9001.github.io/cyber-fracture-fdroid/fdroid/repo'
origin = sys.argv[1].rstrip('/')
with tempfile.TemporaryDirectory(prefix='check-cyber-fracture-') as directory:
    def fetch(name):
        path = Path(directory) / Path(name).name
        if origin.startswith('https://') or origin.startswith('http://'):
            with urllib.request.urlopen(origin + '/' + name, timeout=30) as response:
                path.write_bytes(response.read())
        else:
            path.write_bytes((Path(origin) / name).read_bytes())
        return path

    v1, _, _ = index.get_index_from_jar(str(fetch('index-v1.jar')), fingerprint, allow_deprecated=True)
    entry, _, _ = index.get_index_from_jar(str(fetch('entry.jar')), fingerprint)
    content = fetch(entry['index']['name'].lstrip('/')).read_bytes()
    assert len(content) == entry['index']['size'], 'Index size mismatch'
    assert hashlib.sha256(content).hexdigest() == entry['index']['sha256'], 'Index digest mismatch'
    v2 = json.loads(content)
    assert v1['repo']['name'] == v2['repo']['name']['en-US'] == 'CYBER FRACTURE'
    assert v1['repo']['address'] == v2['repo']['address'] == address
    for app_id, app in v2['packages'].items():
        for version in app['versions'].values():
            file = version['file']
            payload = fetch(file['name'].lstrip('/')).read_bytes()
            assert len(payload) == file['size'], 'APK size mismatch'
            assert hashlib.sha256(payload).hexdigest() == file['sha256'], 'APK digest mismatch'
        print('Verified application:', app_id)
    for diff in entry.get('diffs', {}).values():
        payload = fetch(diff['name'].lstrip('/')).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == diff['sha256'], 'Diff digest mismatch'
    print('PASS: v1/v2 signatures, CYBER FRACTURE name, address, APKs and diffs:', origin)
