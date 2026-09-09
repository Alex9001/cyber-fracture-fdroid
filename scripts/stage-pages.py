#!/usr/bin/env python3
"""Publish only repository files, plus an alias for the original /repo address."""
from pathlib import Path
import shutil
import sys

root = Path(__file__).resolve().parent.parent
destination = Path(sys.argv[1]).resolve()
# Never overwrite a directory: use a new, empty staging path for each deployment.
destination.mkdir(parents=True, exist_ok=False)
source = root / 'fdroid/repo'
for path in ('fdroid/repo', 'repo'):
    shutil.copytree(source, destination / path, ignore=shutil.ignore_patterns('status'))
shutil.copyfile(source / 'index.html', destination / 'index.html')
shutil.copyfile(source / 'index.html', destination / 'fdroid/index.html')
shutil.copyfile(root / 'REPOSITORY-FINGERPRINT.txt', destination / 'REPOSITORY-FINGERPRINT.txt')
(destination / '.nojekyll').touch()
print('Staged canonical repository and legacy /repo alias in', destination)
