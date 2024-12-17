# Maintainer: Jamison Lahman <jamison@lahman.dev>

pkgname=work
pkgver=1.0.9
pkgrel=1
pkgdesc='A stupid simple time tracker.'
arch=('i686' 'x86_64' 'aarch64')
url='https://github.com/jmelahman/work'
license=('MIT')
makedepends=('go' 'git')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('52f6f4f99d9e9747308710cfe7b5bb4c0dcc38269e3194318fc7df1ff4463cde')

build() {
    cd "$srcdir/$pkgname-$pkgver" || exit
    commit="$(git rev-parse HEAD)"
    go build -ldflags="-X main.version=v$pkgver -X main.commit=$commit -s -w" -o "$pkgname"
}

package() {
    cd "$srcdir/$pkgname-$pkgver" || exit
    install -Dm755 "$pkgname" "$pkgdir/usr/bin/$pkgname"
}
