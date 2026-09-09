#!/usr/bin/env python3
"""Merge reviewable public branding into the private signing configuration."""
from pathlib import Path
import os
import yaml

root = Path(__file__).resolve().parent.parent
path = root / 'fdroid/config.yml'
config = yaml.safe_load(path.read_text())
public = yaml.safe_load((root / 'repository.yml').read_text())
allowed = {'repo_name', 'repo_description', 'repo_url', 'repo_icon', 'categories'}
if set(public) != allowed:
    raise SystemExit('Public configuration contains unexpected or missing fields')
config.update(public)
os.chmod(path, 0o600)
path.write_text(yaml.safe_dump(config, sort_keys=False))
