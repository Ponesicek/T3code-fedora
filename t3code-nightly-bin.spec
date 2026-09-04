%global upstream_version 0.0.39-nightly.20260904.1275
%global upstream_tag v%{upstream_version}
%global source0_sha256 70046a6844d86ff94af084471a49e09ac16c982364a566f662bd6b8c254e986e
%global source1_sha256 935d8f2af0c703f9c39517ee57cc4930b19d02d533be930b63f0e82f93614b43

Name:           t3code-nightly-bin
Version:        0.0.39~nightly.20260904.1275
Release:        1%{?dist}
Summary:        Nightly GUI for coding agents (upstream binary package)

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
Conflicts:      t3code-bin

# Keep the prebuilt, upstream-tested Electron payload intact.
%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_prefix}/lib/%{name}/.*$
%global __provides_exclude_from ^%{_prefix}/lib/%{name}/.*$

%description
T3 Code is a desktop control surface for coding agents. This package verifies
and repackages the x86_64 AppImage published with the latest upstream nightly
release. It does not download or execute code during installation.


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

appdir='/usr/lib/t3code-nightly-bin'
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
Name=T3 Code (Nightly)
Comment=Nightly GUI for coding agents
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
* Fri Sep 04 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260904.1275-1
- Package upstream T3 Code 0.0.39-nightly.20260904.1275 binary release
* Thu Sep 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260903.1272-1
- Package upstream T3 Code 0.0.39-nightly.20260903.1272 binary release
* Thu Sep 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260903.1270-1
- Package upstream T3 Code 0.0.39-nightly.20260903.1270 binary release
* Thu Sep 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260903.1268-1
- Package upstream T3 Code 0.0.39-nightly.20260903.1268 binary release
* Thu Sep 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260903.1262-1
- Package upstream T3 Code 0.0.39-nightly.20260903.1262 binary release
* Wed Sep 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260902.1260-1
- Package upstream T3 Code 0.0.39-nightly.20260902.1260 binary release
* Wed Sep 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260902.1257-1
- Package upstream T3 Code 0.0.39-nightly.20260902.1257 binary release
* Wed Sep 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.39~nightly.20260902.1253-1
- Package upstream T3 Code 0.0.39-nightly.20260902.1253 binary release
* Tue Sep 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260901.1248-1
- Package upstream T3 Code 0.0.38-nightly.20260901.1248 binary release
* Tue Sep 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260901.1246-1
- Package upstream T3 Code 0.0.38-nightly.20260901.1246 binary release
* Tue Sep 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260901.1245-1
- Package upstream T3 Code 0.0.38-nightly.20260901.1245 binary release
* Tue Sep 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260901.1243-1
- Package upstream T3 Code 0.0.38-nightly.20260901.1243 binary release
* Mon Aug 31 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260831.1241-1
- Package upstream T3 Code 0.0.38-nightly.20260831.1241 binary release
* Mon Aug 31 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260831.1236-1
- Package upstream T3 Code 0.0.38-nightly.20260831.1236 binary release
* Mon Aug 31 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.38~nightly.20260831.1235-1
- Package upstream T3 Code 0.0.38-nightly.20260831.1235 binary release
* Sun Aug 30 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.37~nightly.20260830.1227-1
- Package upstream T3 Code 0.0.37-nightly.20260830.1227 binary release
* Sat Aug 29 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.37~nightly.20260829.1223-1
- Package upstream T3 Code 0.0.37-nightly.20260829.1223 binary release
* Sat Aug 29 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.37~nightly.20260829.1219-1
- Package upstream T3 Code 0.0.37-nightly.20260829.1219 binary release
* Fri Aug 28 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.36~nightly.20260828.1211-1
- Package upstream T3 Code 0.0.36-nightly.20260828.1211 binary release
* Fri Aug 28 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.36~nightly.20260828.1209-1
- Package upstream T3 Code 0.0.36-nightly.20260828.1209 binary release
* Thu Aug 27 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.36~nightly.20260827.1207-1
- Package upstream T3 Code 0.0.36-nightly.20260827.1207 binary release
* Thu Aug 27 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.36~nightly.20260827.1205-1
- Package upstream T3 Code 0.0.36-nightly.20260827.1205 binary release
* Wed Aug 26 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.35~nightly.20260826.1195-1
- Package upstream T3 Code 0.0.35-nightly.20260826.1195 binary release
* Wed Aug 26 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.35~nightly.20260826.1194-1
- Package upstream T3 Code 0.0.35-nightly.20260826.1194 binary release
* Wed Aug 26 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260826.1189-1
- Package upstream T3 Code 0.0.34-nightly.20260826.1189 binary release
* Tue Aug 25 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260825.1185-1
- Package upstream T3 Code 0.0.34-nightly.20260825.1185 binary release
* Tue Aug 25 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260825.1184-1
- Package upstream T3 Code 0.0.34-nightly.20260825.1184 binary release
* Tue Aug 25 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260825.1182-1
- Package upstream T3 Code 0.0.34-nightly.20260825.1182 binary release
* Tue Aug 25 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260825.1180-1
- Package upstream T3 Code 0.0.34-nightly.20260825.1180 binary release
* Mon Aug 24 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260824.1176-1
- Package upstream T3 Code 0.0.34-nightly.20260824.1176 binary release
* Mon Aug 24 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260824.1174-1
- Package upstream T3 Code 0.0.34-nightly.20260824.1174 binary release
* Mon Aug 24 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260824.1172-1
- Package upstream T3 Code 0.0.34-nightly.20260824.1172 binary release
* Sun Aug 23 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260823.1170-1
- Package upstream T3 Code 0.0.34-nightly.20260823.1170 binary release
* Sun Aug 23 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260823.1168-1
- Package upstream T3 Code 0.0.34-nightly.20260823.1168 binary release
* Sun Aug 23 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260823.1166-1
- Package upstream T3 Code 0.0.34-nightly.20260823.1166 binary release
* Sun Aug 23 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260823.1164-1
- Package upstream T3 Code 0.0.34-nightly.20260823.1164 binary release
* Sat Aug 22 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260822.1160-1
- Package upstream T3 Code 0.0.34-nightly.20260822.1160 binary release
* Sat Aug 22 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260822.1159-1
- Package upstream T3 Code 0.0.34-nightly.20260822.1159 binary release
* Sat Aug 22 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260822.1157-1
- Package upstream T3 Code 0.0.34-nightly.20260822.1157 binary release
* Sat Aug 22 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260822.1155-1
- Package upstream T3 Code 0.0.34-nightly.20260822.1155 binary release
* Fri Aug 21 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260821.1153-1
- Package upstream T3 Code 0.0.34-nightly.20260821.1153 binary release
* Fri Aug 21 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260821.1151-1
- Package upstream T3 Code 0.0.34-nightly.20260821.1151 binary release
* Fri Aug 21 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260821.1149-1
- Package upstream T3 Code 0.0.34-nightly.20260821.1149 binary release
* Fri Aug 21 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260821.1147-1
- Package upstream T3 Code 0.0.34-nightly.20260821.1147 binary release
* Thu Aug 20 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260820.1142-1
- Package upstream T3 Code 0.0.34-nightly.20260820.1142 binary release
* Thu Aug 20 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260820.1141-1
- Package upstream T3 Code 0.0.34-nightly.20260820.1141 binary release
* Wed Aug 19 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260819.1133-1
- Package upstream T3 Code 0.0.34-nightly.20260819.1133 binary release
* Wed Aug 19 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260819.1132-1
- Package upstream T3 Code 0.0.34-nightly.20260819.1132 binary release
* Wed Aug 19 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260819.1129-1
- Package upstream T3 Code 0.0.34-nightly.20260819.1129 binary release
* Tue Aug 18 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260818.1127-1
- Package upstream T3 Code 0.0.34-nightly.20260818.1127 binary release
* Tue Aug 18 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260818.1124-1
- Package upstream T3 Code 0.0.34-nightly.20260818.1124 binary release
* Tue Aug 18 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260817.1120-1
- Package upstream T3 Code 0.0.34-nightly.20260817.1120 binary release
* Mon Aug 17 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260817.1119-1
- Package upstream T3 Code 0.0.34-nightly.20260817.1119 binary release
* Mon Aug 17 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260817.1116-1
- Package upstream T3 Code 0.0.34-nightly.20260817.1116 binary release
* Mon Aug 17 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260817.1113-1
- Package upstream T3 Code 0.0.34-nightly.20260817.1113 binary release
* Sun Aug 16 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260816.1110-1
- Package upstream T3 Code 0.0.34-nightly.20260816.1110 binary release
* Sun Aug 16 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260816.1109-1
- Package upstream T3 Code 0.0.34-nightly.20260816.1109 binary release
* Sun Aug 16 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260816.1106-1
- Package upstream T3 Code 0.0.34-nightly.20260816.1106 binary release
* Sun Aug 16 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260816.1105-1
- Package upstream T3 Code 0.0.34-nightly.20260816.1105 binary release
* Sat Aug 15 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260815.1102-1
- Package upstream T3 Code 0.0.34-nightly.20260815.1102 binary release
* Sat Aug 15 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260815.1101-1
- Package upstream T3 Code 0.0.34-nightly.20260815.1101 binary release
* Sat Aug 15 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260815.1098-1
- Package upstream T3 Code 0.0.34-nightly.20260815.1098 binary release
* Sat Aug 15 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260815.1097-1
- Package upstream T3 Code 0.0.34-nightly.20260815.1097 binary release
* Fri Aug 14 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260814.1095-1
- Package upstream T3 Code 0.0.34-nightly.20260814.1095 binary release
* Fri Aug 14 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260814.1093-1
- Package upstream T3 Code 0.0.34-nightly.20260814.1093 binary release
* Fri Aug 14 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260814.1090-1
- Package upstream T3 Code 0.0.34-nightly.20260814.1090 binary release
* Fri Aug 14 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260814.1089-1
- Package upstream T3 Code 0.0.34-nightly.20260814.1089 binary release
* Thu Aug 13 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260813.1087-1
- Package upstream T3 Code 0.0.34-nightly.20260813.1087 binary release
* Thu Aug 13 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260813.1085-1
- Package upstream T3 Code 0.0.34-nightly.20260813.1085 binary release
* Thu Aug 13 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260813.1082-1
- Package upstream T3 Code 0.0.34-nightly.20260813.1082 binary release
* Thu Aug 13 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260813.1081-1
- Package upstream T3 Code 0.0.34-nightly.20260813.1081 binary release
* Wed Aug 12 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260812.1076-1
- Package upstream T3 Code 0.0.34-nightly.20260812.1076 binary release
* Wed Aug 12 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260812.1072-1
- Package upstream T3 Code 0.0.34-nightly.20260812.1072 binary release
* Tue Aug 11 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260811.1069-1
- Package upstream T3 Code 0.0.34-nightly.20260811.1069 binary release
* Tue Aug 11 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260811.1067-1
- Package upstream T3 Code 0.0.34-nightly.20260811.1067 binary release
* Tue Aug 11 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260811.1064-1
- Package upstream T3 Code 0.0.34-nightly.20260811.1064 binary release
* Tue Aug 11 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260811.1063-1
- Package upstream T3 Code 0.0.34-nightly.20260811.1063 binary release
* Mon Aug 10 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260810.1061-1
- Package upstream T3 Code 0.0.34-nightly.20260810.1061 binary release
* Mon Aug 10 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.34~nightly.20260810.1059-1
- Package upstream T3 Code 0.0.34-nightly.20260810.1059 binary release
* Mon Aug 10 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260810.1056-1
- Package upstream T3 Code 0.0.33-nightly.20260810.1056 binary release
* Mon Aug 10 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260810.1054-1
- Package upstream T3 Code 0.0.33-nightly.20260810.1054 binary release
* Sun Aug 09 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260809.1045-1
- Package upstream T3 Code 0.0.33-nightly.20260809.1045 binary release
* Sun Aug 09 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260809.1043-1
- Package upstream T3 Code 0.0.33-nightly.20260809.1043 binary release
* Sun Aug 09 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260809.1041-1
- Package upstream T3 Code 0.0.33-nightly.20260809.1041 binary release
* Sun Aug 09 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260809.1039-1
- Package upstream T3 Code 0.0.33-nightly.20260809.1039 binary release
* Sat Aug 08 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260808.1035-1
- Package upstream T3 Code 0.0.33-nightly.20260808.1035 binary release
* Sat Aug 08 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260808.1033-1
- Package upstream T3 Code 0.0.33-nightly.20260808.1033 binary release
* Sat Aug 08 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260808.1031-1
- Package upstream T3 Code 0.0.33-nightly.20260808.1031 binary release
* Sat Aug 08 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260808.1029-1
- Package upstream T3 Code 0.0.33-nightly.20260808.1029 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260807.1026-1
- Package upstream T3 Code 0.0.33-nightly.20260807.1026 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.33~nightly.20260807.1025-1
- Package upstream T3 Code 0.0.33-nightly.20260807.1025 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260807.1022-1
- Package upstream T3 Code 0.0.32-nightly.20260807.1022 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260807.1019-1
- Package upstream T3 Code 0.0.32-nightly.20260807.1019 binary release
* Fri Aug 07 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260806.1018-1
- Package upstream T3 Code 0.0.32-nightly.20260806.1018 binary release
* Thu Aug 06 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260806.1015-1
- Package upstream T3 Code 0.0.32-nightly.20260806.1015 binary release
* Thu Aug 06 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260806.1012-1
- Package upstream T3 Code 0.0.32-nightly.20260806.1012 binary release
* Thu Aug 06 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260805.1009-1
- Package upstream T3 Code 0.0.32-nightly.20260805.1009 binary release
* Wed Aug 05 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260805.1006-1
- Package upstream T3 Code 0.0.32-nightly.20260805.1006 binary release
* Wed Aug 05 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260805.1002-1
- Package upstream T3 Code 0.0.32-nightly.20260805.1002 binary release
* Tue Aug 04 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260804.999-1
- Package upstream T3 Code 0.0.32-nightly.20260804.999 binary release
* Tue Aug 04 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260804.997-1
- Package upstream T3 Code 0.0.32-nightly.20260804.997 binary release
* Tue Aug 04 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260804.993-1
- Package upstream T3 Code 0.0.32-nightly.20260804.993 binary release
* Mon Aug 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260803.986-1
- Package upstream T3 Code 0.0.32-nightly.20260803.986 binary release
* Mon Aug 03 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260803.985-1
- Package upstream T3 Code 0.0.32-nightly.20260803.985 binary release
* Sun Aug 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260802.980-1
- Package upstream T3 Code 0.0.32-nightly.20260802.980 binary release
* Sun Aug 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260802.979-1
- Package upstream T3 Code 0.0.32-nightly.20260802.979 binary release
* Sun Aug 02 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260801.976-1
- Package upstream T3 Code 0.0.32-nightly.20260801.976 binary release
* Sat Aug 01 2026 Ponesicek <ponesicek@users.noreply.github.com> - 0.0.32~nightly.20260801.974-1
- Package upstream T3 Code 0.0.32-nightly.20260801.974 binary release
