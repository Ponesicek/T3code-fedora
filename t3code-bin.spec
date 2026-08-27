%global upstream_version 0.0.35
%global upstream_tag v%{upstream_version}
%global source0_sha256 97564d89bdb2d1b45f2fb1916183f39d4a384349dec788d5fb6fb2c643ae0794
%global source1_sha256 935d8f2af0c703f9c39517ee57cc4930b19d02d533be930b63f0e82f93614b43

Name:           t3code-bin
Version:        0.0.35
Release:        1%{?dist}
Summary:        GUI for coding agents (upstream binary package)

License:        MIT
URL:            https://github.com/pingdotgg/t3code
Source0:        %{url}/releases/download/%{upstream_tag}/T3-Code-%{upstream_version}-x86_64.AppImage
Source1:        https://raw.githubusercontent.com/pingdotgg/t3code/%{upstream_tag}/LICENSE
ExclusiveArch:  x86_64
BuildRequires:  coreutils
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       bash
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       libdrm
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libxkbcommon
Requires:       libXrandr
Requires:       libxcb
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils
Requires:       zlib-ng-compat
Provides:       t3code = %{version}-%{release}
Conflicts:      t3code-nightly-bin

# Keep the prebuilt, upstream-tested Electron payload intact.
%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_prefix}/lib/%{name}/.*$
%global __provides_exclude_from ^%{_prefix}/lib/%{name}/.*$

%description
T3 Code is a desktop control surface for coding agents. This package verifies
and repackages the x86_64 AppImage published with the corresponding upstream
stable release. It does not download or execute code during installation.


%prep
echo "%{source0_sha256}  %{SOURCE0}" | sha256sum --check --strict -
echo "%{source1_sha256}  %{SOURCE1}" | sha256sum --check --strict -
chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract >/dev/null
test -x squashfs-root/t3code
test -d squashfs-root/usr/share/icons/hicolor


%build
# The application is built and published by upstream.


%install
install -d %{buildroot}%{_prefix}/lib/%{name}
cp -a squashfs-root/. %{buildroot}%{_prefix}/lib/%{name}/
chmod -R a+rX %{buildroot}%{_prefix}/lib/%{name}

install -Dpm 0755 /dev/stdin %{buildroot}%{_bindir}/t3code <<'EOF'
#!/usr/bin/bash
set -euo pipefail

appdir='/usr/lib/t3code-bin'
export APPDIR="$appdir"

if [[ -z "${CODEX_CLI_PATH-}" ]] && command -v codex >/dev/null 2>&1; then
  export CODEX_CLI_PATH="$(command -v codex)"
fi

export PATH="$appdir:$appdir/usr/bin:$appdir/usr/sbin:$PATH"
export XDG_DATA_DIRS="$appdir/usr/share${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}"
export GSETTINGS_SCHEMA_DIR="$appdir/usr/share/glib-2.0/schemas${GSETTINGS_SCHEMA_DIR:+:$GSETTINGS_SCHEMA_DIR}"

exec "$appdir/t3code" "$@"
EOF

install -d %{buildroot}%{_datadir}/icons
cp -a squashfs-root/usr/share/icons/hicolor %{buildroot}%{_datadir}/icons/

install -Dpm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/com.t3tools.t3code.desktop <<'EOF'
[Desktop Entry]
Name=T3 Code
Comment=GUI for coding agents
Exec=t3code %U
Terminal=false
Type=Application
Icon=t3code
StartupWMClass=t3code
Categories=Development;
MimeType=x-scheme-handler/t3code;x-scheme-handler/t3code-dev;
EOF

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE


%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/t3code
%{_prefix}/lib/%{name}/
%{_datadir}/applications/com.t3tools.t3code.desktop
%{_datadir}/icons/hicolor/*/apps/t3code.png


%changelog
* Thu Aug 27 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.35-1
- Package upstream T3 Code 0.0.35 binary release
* Wed Aug 26 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34-1
- Package upstream T3 Code 0.0.34 binary release
* Mon Aug 10 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33-1
- Package upstream T3 Code 0.0.33 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32-1
- Package upstream T3 Code 0.0.32 binary release
* Sat Aug 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.31-1
- Package upstream T3 Code 0.0.31 binary release
