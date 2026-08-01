#!/usr/bin/bash
set -euo pipefail

usage() {
  echo "usage: $0 <stable|nightly> <spec-file>" >&2
  exit 2
}

[[ $# -eq 2 ]] || usage
channel=$1
spec=$2
[[ $channel == stable || $channel == nightly ]] || usage
[[ -f $spec ]] || { echo "Spec file not found: $spec" >&2; exit 1; }

repo=pingdotgg/t3code
headers=(
  --header 'Accept: application/vnd.github+json'
  --header 'X-GitHub-Api-Version: 2022-11-28'
)
if [[ -n ${GH_TOKEN-} ]]; then
  headers+=(--header "Authorization: Bearer $GH_TOKEN")
fi

if [[ $channel == stable ]]; then
  release=$(curl --fail --silent --show-error --location "${headers[@]}" \
    "https://api.github.com/repos/$repo/releases/latest")
else
  releases=$(curl --fail --silent --show-error --location "${headers[@]}" \
    "https://api.github.com/repos/$repo/releases?per_page=50")
  release=$(jq --compact-output '
    [.[] | select(.draft == false and .prerelease == true)
      | select(.tag_name | test("^v[0-9]+\\.[0-9]+\\.[0-9]+-nightly\\.[0-9]{8}\\.[0-9]+$"))]
    | sort_by(.published_at) | last
  ' <<<"$releases")
  [[ $release != null ]] || { echo 'No upstream nightly release found' >&2; exit 1; }
fi

tag=$(jq --raw-output '.tag_name' <<<"$release")
upstream_version=${tag#v}
if [[ $channel == stable ]]; then
  [[ $tag =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
    echo "Unexpected stable release tag: $tag" >&2
    exit 1
  }
  rpm_version=$upstream_version
else
  [[ $tag =~ ^v([0-9]+\.[0-9]+\.[0-9]+)-nightly\.([0-9]{8})\.([0-9]+)$ ]] || {
    echo "Unexpected nightly release tag: $tag" >&2
    exit 1
  }
  rpm_version="${BASH_REMATCH[1]}~nightly.${BASH_REMATCH[2]}.${BASH_REMATCH[3]}"
fi

asset_name="T3-Code-$upstream_version-x86_64.AppImage"
asset=$(jq --compact-output --arg name "$asset_name" \
  '[.assets[] | select(.name == $name)] | if length == 1 then .[0] else null end' \
  <<<"$release")
[[ $asset != null ]] || { echo "Release does not have exactly one $asset_name asset" >&2; exit 1; }

digest=$(jq --raw-output '.digest' <<<"$asset")
[[ $digest =~ ^sha256:([0-9a-f]{64})$ ]] || {
  echo "Upstream did not publish a SHA-256 digest for $asset_name" >&2
  exit 1
}
source0_sha256=${BASH_REMATCH[1]}

license_file=$(mktemp)
trap 'rm -f "$license_file"' EXIT
curl --fail --silent --show-error --location --retry 3 \
  --output "$license_file" \
  "https://raw.githubusercontent.com/$repo/$tag/LICENSE"
source1_sha256=$(sha256sum "$license_file" | awk '{print $1}')

read_macro() {
  awk -v macro="$1" '$1 == "%global" && $2 == macro { print $3; exit }' "$spec"
}

current_version=$(read_macro upstream_version)
current_source0=$(read_macro source0_sha256)
current_source1=$(read_macro source1_sha256)

# A changed asset under an unchanged immutable release tag is suspicious. Stop
# for review instead of silently trusting a replacement upload.
if [[ $current_version == "$upstream_version" && \
      ( $current_source0 != "$source0_sha256" || $current_source1 != "$source1_sha256" ) ]]; then
  echo "Checksums changed for already-packaged tag $tag; refusing automatic update" >&2
  exit 1
fi

changed=false
if [[ $current_version != "$upstream_version" ]]; then
  changed=true
  sed -i -E "s/^%global upstream_version .*/%global upstream_version $upstream_version/" "$spec"
  sed -i -E "s/^%global source0_sha256 .*/%global source0_sha256 $source0_sha256/" "$spec"
  sed -i -E "s/^%global source1_sha256 .*/%global source1_sha256 $source1_sha256/" "$spec"
  sed -i -E "s/^Version:[[:space:]]+.*/Version:        $rpm_version/" "$spec"

  release_date=$(LC_ALL=C date '+%a %b %d %Y')
  sed -i "/^%changelog/a * $release_date Ponesicek <ponesicek@users.noreply.github.com> - $rpm_version-1\\
- Package upstream T3 Code $upstream_version binary release" "$spec"
fi

echo "$channel: $tag ($source0_sha256), changed=$changed"
if [[ -n ${GITHUB_OUTPUT-} ]]; then
  echo "changed=$changed" >>"$GITHUB_OUTPUT"
  echo "tag=$tag" >>"$GITHUB_OUTPUT"
  echo "upstream_version=$upstream_version" >>"$GITHUB_OUTPUT"
  echo "rpm_version=$rpm_version" >>"$GITHUB_OUTPUT"
fi
