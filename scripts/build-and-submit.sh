#!/usr/bin/bash
set -euo pipefail

if [[ $# -ne 2 || ! -f $1 ]]; then
  echo "usage: $0 <spec-file> <copr-owner/project>" >&2
  exit 2
fi

spec=$1
project=$2
read_macro() {
  awk -v macro="$1" '$1 == "%global" && $2 == macro { print $3; exit }' "$spec"
}

upstream_version=$(read_macro upstream_version)
source0_sha256=$(read_macro source0_sha256)
source1_sha256=$(read_macro source1_sha256)
tag="v$upstream_version"
artifact="T3-Code-$upstream_version-x86_64.AppImage"

topdir=$(mktemp -d)
trap 'rm -rf "$topdir"' EXIT
mkdir -p "$topdir"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

curl --fail --show-error --location --retry 3 \
  --output "$topdir/SOURCES/$artifact" \
  "https://github.com/pingdotgg/t3code/releases/download/$tag/$artifact"
curl --fail --silent --show-error --location --retry 3 \
  --output "$topdir/SOURCES/LICENSE" \
  "https://raw.githubusercontent.com/pingdotgg/t3code/$tag/LICENSE"

echo "$source0_sha256  $topdir/SOURCES/$artifact" | sha256sum --check --strict -
echo "$source1_sha256  $topdir/SOURCES/LICENSE" | sha256sum --check --strict -

rpmbuild -bs --target x86_64 --define "_topdir $topdir" "$spec"
srpm=$(find "$topdir/SRPMS" -maxdepth 1 -name '*.src.rpm' -print -quit)
[[ -n $srpm ]] || { echo 'rpmbuild did not produce an SRPM' >&2; exit 1; }

# COPR builds every enabled x86_64 chroot in the project. The command waits and
# fails the workflow unless every configured build succeeds.
copr build "$project" "$srpm"
