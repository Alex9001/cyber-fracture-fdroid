# CYBER FRACTURE F-Droid Repository

Official Android releases from CYBER FRACTURE.

Add this repository in the F-Droid client:

```text
https://alex9001.github.io/cyber-fracture-fdroid/fdroid/repo
```

F-Droid displays the repository signing fingerprint before you trust it. Compare
it with the fingerprint in [REPOSITORY-FINGERPRINT.txt](REPOSITORY-FINGERPRINT.txt).

## Maintainers

This is a signed binary repository. APK signing keys and the repository signing
key stay outside Git. To publish an APK, add its metadata under `fdroid/metadata/`,
copy the already signed APK into `fdroid/repo/`, run `scripts/update-repo`, then
commit and push the resulting `fdroid/repo/` directory. GitHub Pages deploys that
directory.

Use an APK signed by the same application key as its previous releases; otherwise
Android users must uninstall the old app before installing the update.
