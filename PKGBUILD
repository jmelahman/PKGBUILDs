# Maintainer: Jamison Lahman <jamison+aur@lahman.dev>

pkgname=ibazel-bin
pkgver=0.25.3
pkgrel=1
pkgdesc='Tool for building Bazel targets when source files change.'
arch=('x86_64' 'aarch64')
license=('Apache')
url='https://github.com/bazelbuild/bazel-watcher'
conflicts=('ibazel' 'ibazel-git')
source=(
  "LICENSE-${pkgver}::https://raw.githubusercontent.com/bazelbuild/bazel-watcher/v${pkgver}/LICENSE"
)
source_x86_64+=(
  "${pkgname}-x86_64-${pkgver}::${url}/releases/download/v${pkgver}/${pkgname%-bin}_linux_amd64"
)
source_aarch64+=(
  "${pkgname}-aarch64-${pkgver}::${url}/releases/download/v${pkgver}/${pkgname%-bin}_linux_arm64"
)
sha256sums=('c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4')
sha256sums_x86_64=('d8e1ea02777670a095719ed3800e9bbf814269b05edf901992c1e7c5eca0e3b6')
sha256sums_aarch64=('3fa76bef2a1eac55975a0e6949c133d0a9898eb1e5425ce4f7df0289859f56c5')

package() {
  cd "${srcdir}" || exit

  # Install the license file
  install -D -m 0644 \
    "${source[0]%%::*}" \
    "${pkgdir}/usr/share/licenses/${pkgname%-bin}/LICENSE"

  # Install the binary
  install -D -m 0755 \
    "./${pkgname}-${CARCH}-${pkgver}" \
    "${pkgdir}/usr/bin/${pkgname%-bin}"
}
