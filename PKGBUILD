# Maintainer: Jamison Lahman <jamison+aur@lahman.dev>
# Contributor:

pkgname=release-tag
_pkgname=tag
pkgver=0.2.2
pkgrel=1
pkgdesc='Automatically create semantic version git tags.'
arch=('i686' 'x86_64' 'aarch64')
url='https://github.com/jmelahman/tag'
license=('MIT')
makedepends=('go' 'git')
_commit='85b6904a136347cb2bea40eff89aa18c24eac7ff'
source=("${_pkgname}::git+$url.git#commit=$_commit")
md5sums=('SKIP')

pkgver() {
  cd "${_pkgname}" || exit

  git describe --tags | sed 's/^v//'
}

build() {
  cd "${_pkgname}" || exit

  go build -ldflags="-X main.version=v$pkgver -X main.commit=$_commit -s -w" -o "${_pkgname}"
}

package() {
  cd "${_pkgname}" || exit

  install -Dm755 "${_pkgname}" "$pkgdir/usr/bin/${_pkgname}"
}
