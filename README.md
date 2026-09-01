# PKGBUILDs

[![Test status](https://github.com/jmelahman/pkgbuilds/actions/workflows/test.yml/badge.svg)](https://github.com/jmelahman/pkgbuilds/actions)

## Managing packages

Each package is managed as a git [subtree](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging#_subtree_merge).
Changes are automatically pushed to the AUR on commits to master.

[nvchecker](https://github.com/lilydjwg/nvchecker) is used to check upstream repositories for new versions nightly.
Pull requests to update versions are generated at midnight (PST).

### Adding a new package

```shell
git subtree add --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```

Add the package to `nvchecker.toml` for nightly version checks.
Verify the package will build in CI,

```shell
prek run --stage manual --files $PACKAGE/PKGBUILD
```

The build runs `makepkg -s` on the host, so it asks for a sudo password only
when a dependency is missing. CI runs the same hook inside an
`archlinux:base-devel` container, as a build user with passwordless
`sudo pacman`.

## Running tests

As recommended by the [Arch Wiki](https://wiki.archlinux.org/title/PKGBUILD), `shellcheck` is
configured to check the PKGBUILDs, along with
[pkglint](https://github.com/jmelahman/pkglint) for source-integrity, hermeticity, and
correctness checks.

Both can be ran over the whole tree with,

```shell
prek run --all-files
```

The builds are opt-in (`stages: [manual]`) and are not part of that run.
