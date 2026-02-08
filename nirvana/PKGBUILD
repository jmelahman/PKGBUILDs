# Maintainer: gomanager <gomanager@generated>
pkgname=nirvana
pkgver=0.3.1
pkgrel=1
pkgdesc="Golang Restful API Framework for Productivity"
arch=('x86_64' 'aarch64')
url="https://github.com/caicloud/nirvana"
license=('unknown')
depends=('glibc')
makedepends=('go' 'git')
source=("git+https://github.com/caicloud/nirvana.git#tag=v$pkgver")
sha256sums=('SKIP')

build() {
  cd "$pkgname" || exit
  go build \
    -trimpath \
    -mod=readonly \
    -modcacherw \
    -ldflags='-s -w' \
    -o $pkgname \
    ./cmd/nirvana
}

package() {
  cd "$pkgname" || exit
  install -Dm 755 $pkgname -t "$pkgdir/usr/bin"
  install -Dm 644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname"
  install -Dm 644 README.md -t "$pkgdir/usr/share/doc/$pkgname"
}
