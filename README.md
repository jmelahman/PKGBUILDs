# PKGBUILDs

## Adding a new package

```shell
git subtree add --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```

## Pushing changes

```shell
git subtree push --prefix=$PACKAGE ssh://aur@aur.archlinux.org/$PACKAGE.git master
```
