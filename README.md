# T3 Code binary RPMs for COPR

This repository publishes two unofficial Fedora packages:

- `t3code-bin`: latest non-prerelease T3 Code desktop release
- `t3code-nightly-bin`: latest `v*-nightly.*` desktop release

Both packages repackage the x86_64 AppImage published by
[`pingdotgg/t3code`](https://github.com/pingdotgg/t3code/releases). Upstream
does not currently publish a Linux aarch64 AppImage, so the specs deliberately
use `ExclusiveArch: x86_64`.

## Safety model

- The release tag and asset name must match strict expected patterns.
- The workflow reads the SHA-256 digest recorded by GitHub for the release
  asset, writes it into the spec, and verifies the downloaded bytes twice:
  before creating the SRPM and again inside the isolated COPR build.
- A checksum change for an already packaged tag stops the workflow for manual
  review instead of accepting a replaced asset.
- Installation performs no network access and runs no downloaded scripts.
- The launcher does not add Electron's unsafe `--no-sandbox` flag.
- The workflow's checkout action is pinned to a full commit SHA.

This proves that the RPM contains the exact binary published in the selected
upstream GitHub release. It does not independently reproduce or audit the
upstream Electron build.

## Install

For stable releases:

```bash
sudo dnf copr enable ponesicek/t3code-bin
sudo dnf install t3code-bin
```

For nightly releases:

```bash
sudo dnf copr enable ponesicek/t3code-nightly-bin
sudo dnf install t3code-nightly-bin
```

The packages conflict intentionally: both own `/usr/bin/t3code`, the desktop
entry, icons, and the `t3code:` URL handlers. Switching channels is explicit:

```bash
sudo dnf swap t3code-bin t3code-nightly-bin
```

## Updates

The [Update from upstream](https://github.com/Ponesicek/T3code-fedora/actions/workflows/update.yml)
workflow checks both release channels every six hours. A new upstream version
is checksum-pinned in its spec, built in COPR, and committed only after the
COPR build succeeds.

- [Stable COPR project](https://copr.fedorainfracloud.org/coprs/ponesicek/t3code-bin/)
- [Nightly COPR project](https://copr.fedorainfracloud.org/coprs/ponesicek/t3code-nightly-bin/)
