# CYBER FRACTURE

Official Android releases from CYBER FRACTURE.

Add this repository in the F-Droid client:

```text
https://alex9001.github.io/cyber-fracture-fdroid/fdroid/repo
```

[Open the add-repository page and QR code](https://alex9001.github.io/cyber-fracture-fdroid/).
The QR and copy button include the signing fingerprint. Scan the QR from inside
F-Droid or Droid-ify, or use the Add to F-Droid button on your phone.

After adding, refresh repositories to load the **CYBER FRACTURE** name. The earlier
`/cyber-fracture-fdroid/repo` address also works. If a saved entry still has a
generic name, refresh it or correct its address to the one above; a manually
assigned custom name may need to be edited in the client.

F-Droid displays the repository signing fingerprint before you trust it. Compare
it with the fingerprint in [REPOSITORY-FINGERPRINT.txt](REPOSITORY-FINGERPRINT.txt).

## Maintainers

This is a signed binary repository. APK signing keys and the repository signing
key stay outside Git. To publish an APK, add its metadata under `fdroid/metadata/`,
copy the already signed APK into `fdroid/repo/`, run `scripts/update-repo`, then
commit and push the resulting `fdroid/repo/` directory. GitHub Pages deploys that
directory and a copy at the old `/repo` address. Deployment stages only public
repository files, never the private signing configuration or keys.

`repository.yml` controls the signed name, description, address, and categories.
`web/index.html` is the page template. The update script regenerates the page and
full-size QR after signing, so branding and scanning fixes survive future releases.
The F-Droid tooling image is pinned by digest.

Run `scripts/check-repo.py` in the F-Droid tooling container with either a local
repository directory or its public HTTPS URL to verify both index signatures,
the name, APK digests, and index diff digests. Decode `fdroid/repo/index.png` with
`zbarimg --quiet --raw` to check its fingerprint-bearing URL.

Use an APK signed by the same application key as its previous releases; otherwise
Android users must uninstall the old app before installing the update.
