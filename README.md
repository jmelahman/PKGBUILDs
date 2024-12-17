# PKGBUILDs

[![Test status](https://github.com/jmelahman/pkgbuilds/actions/workflows/test.yml/badge.svg)](https://github.com/jmelahman/pkgbuilds/actions)

## Managing packages

### Adding a new package

```shell
git subtree add --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```

### Updating a package

```shell
git subtree push --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```

## Running tests

All that is required to run tests is [docker](https://docs.docker.com/engine).
As recommended by the [Arch Wiki](https://wiki.archlinux.org/title/PKGBUILD), `namcap` and
`shellcheck` are configured to check the `PKGBUILD`s.

Each can be ran respectively,

```shell
./shellcheck
```

```shell
./namcap
```
