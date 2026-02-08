# Maintainer: gomanager <gomanager@generated>
pkgname=htb-cli
pkgver=1.7.0
pkgrel=1
pkgdesc="Interact with Hackthebox using your terminal - Be faster and more competitive !"
arch=('x86_64' 'aarch64')
url="https://github.com/GoToolSharing/htb-cli"
license=('unknown')
depends=('glibc')
makedepends=('go' 'git')
source=("git+https://github.com/GoToolSharing/htb-cli.git#tag=v$pkgver")
sha256sums=('SKIP')

build() {
  cd "$pkgname" || exit
  go build \
    -trimpath \
    -mod=readonly \
    -modcacherw \
    -ldflags='-s -w' \
    -o $pkgname \
    .
}

package() {
  cd "$pkgname" || exit
  install -Dm 755 $pkgname -t "$pkgdir/usr/bin"
  install -Dm 644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname"
  install -Dm 644 README.md -t "$pkgdir/usr/share/doc/$pkgname"
}
