#!/usr/bin/env python3
"""Build the add-repository page and QR from the signed index, on every update."""
from pathlib import Path
import hashlib
import html
import json
import zipfile
import qrcode
from cryptography.hazmat.primitives.serialization import pkcs7, Encoding

root = Path(__file__).resolve().parent.parent
repo = root / 'fdroid/repo'
with zipfile.ZipFile(repo / 'index-v1.jar') as jar:
    index = json.loads(jar.read('index-v1.json'))
    signature = next(n for n in jar.namelist() if n.endswith('.RSA'))
    certs = pkcs7.load_der_pkcs7_certificates(jar.read(signature))
    if len(certs) != 1:
        raise SystemExit('Expected one repository signing certificate')
    fingerprint = hashlib.sha256(certs[0].public_bytes(Encoding.DER)).hexdigest().upper()
expected = 'B391053073F0F905594C914D4A63C9D1CDB673F00DDEEEA57CF7CF98480E1047'
if fingerprint != expected:
    raise SystemExit('Repository signing identity changed')
url = index['repo']['address']
link = url + '?fingerprint=' + fingerprint
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
qr.add_data(link)
qr.make(fit=True)
qr.make_image(fill_color='black', back_color='white').save(repo / 'index.png')
template = (root / 'web/index.html').read_text()
values = {
    'NAME': index['repo']['name'],
    'DESCRIPTION': index['repo']['description'],
    'URL': url,
    'ADD_LINK': 'https://fdroid.link/#' + link,
    'COPY_LINK': link,
    'FINGERPRINT': ':'.join(fingerprint[i:i + 2] for i in range(0, len(fingerprint), 2)),
}
for key, value in values.items():
    template = template.replace('{{' + key + '}}', html.escape(value, quote=True))
(repo / 'index.html').write_text(template)
print('Rendered repository page and fingerprint-bearing QR:', index['repo']['name'])
