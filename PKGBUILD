# Maintainer: Spyro24 <minerpi16@gmail.com>
pkgname=ustoat
pkgver=0.3.4
pkgrel=1
pkgdesc="UStoat — A custom stoat client writen in python with the use of pygame-ce"
url="https://github.com/Spyro24/UStoat"
license=(GPL)
arch=(x86_64)
depends=(python python-pip)
makedepends=(git imagemagick)
optdepends=()
provides=()
conflicts=()
replaces=()
source=("git+https://github.com/Spyro24/UStoat.git")
sha512sums=('SKIP')

build() {
  cd "$srcdir/UStoat" || return 1
  return 0
}

package() {
  cd "$srcdir/UStoat" || return 1

  # Install Python requirements (if present)
  if [[ -f requirements.txt ]]; then
    python -m pip install --no-deps --root="$pkgdir" --prefix=/usr -r requirements.txt
  fi

  # Install the package itself
  python -m pip install --no-deps --root="$pkgdir" --prefix=/usr .

  # License (if present)
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE" || true

  # Copy repository files into /usr/lib/$pkgname so desktop wrapper can run main.pyw
  appdir="$pkgdir/usr/lib/$pkgname"
  mkdir -p "$appdir"
  cp -a "$srcdir/UStoat/." "$appdir/"

  # Wrapper executable
  install -Dm755 /dev/null "$pkgdir/usr/bin/$pkgname"
  cat > "$pkgdir/usr/bin/$pkgname" <<'EOF'
#!/bin/sh
exec python /usr/lib/ustoat/main.pyw "$@"
EOF

  # Desktop file
  install -d "$pkgdir/usr/share/applications"
  cat > "$pkgdir/usr/share/applications/$pkgname.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=UStoat
Comment=UStoat Client
Exec=/usr/bin/ustoat
Icon=ustoat
Terminal=false
Categories=Utility;
EOF

  # Install icon: res/icons/app_icon_x384.png -> hicolor 256x256 and 48x48
  if [[ -f "$srcdir/UStoat/res/icons/app_icon_x384.png" ]]; then
    install -d "$pkgdir/usr/share/icons/hicolor/256x256/apps"
    install -d "$pkgdir/usr/share/icons/hicolor/48x48/apps"
    if command -v convert >/dev/null 2>&1; then
      convert "$srcdir/UStoat/res/icons/app_icon_x384.png" -resize 256x256 "$pkgdir/usr/share/icons/hicolor/256x256/apps/$pkgname.png"
      convert "$srcdir/UStoat/res/icons/app_icon_x384.png" -resize 48x48 "$pkgdir/usr/share/icons/hicolor/48x48/apps/$pkgname.png"
    else
      cp "$srcdir/UStoat/res/icons/app_icon_x384.png" "$pkgdir/usr/share/icons/hicolor/256x256/apps/$pkgname.png"
      cp "$srcdir/UStoat/res/icons/app_icon_x384.png" "$pkgdir/usr/share/icons/hicolor/48x48/apps/$pkgname.png"
    fi
  fi
}
