# PKGBUILDs

[![Test status](https://github.com/jmelahman/pkgbuilds/actions/workflows/test.yml/badge.svg)](https://github.com/jmelahman/pkgbuilds/actions)

## Managing packages

Each package is managed as a git [subtree](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging#_subtree_merge).
Changes are automatically pushed upstream on commit.

### Adding a new package

```shell
git subtree add --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```

## Running tests

As recommended by the [Arch Wiki](https://wiki.archlinux.org/title/PKGBUILD), `namcap` and
`shellcheck` are configured to check the PKGBUILDs.

Each can be ran with the following commands,

```shell
./shellcheck
```

```shell
./namcap
```
