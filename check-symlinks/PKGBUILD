# Maintainer: Jamison Lahman <jamison+aur@lahman.dev>
# Contributor:

pkgname=check-symlinks
pkgver=0.4.2
pkgrel=1
pkgdesc='Check for broken symlinks'
arch=('x86_64')
url='https://github.com/jmelahman/check-symlinks'
license=('MIT')
depends=('gcc-libs')
makedepends=('git' 'rust')
_commit='20c9a595ead56fb701182ed31c8ce120f7c3c9bb'
source=("$pkgname::git+$url.git#commit=$_commit")
md5sums=('SKIP')

pkgver() {
  cd "$pkgname" || exit

  git describe --tags | sed 's/^v//'
}

prepare() {
  cd "$pkgname" || exit

  # download dependencies
  cargo fetch --locked --target "$CARCH-unknown-linux-gnu"
}

build() {
  cd "$pkgname" || exit

  cargo build --frozen --release
}

package() {
  cd "$pkgname" || exit

  # binary
  install -vDm755 -t "$pkgdir/usr/bin" "target/release/$pkgname"

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
