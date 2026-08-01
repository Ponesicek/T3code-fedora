# T3 Code binary RPMs for COPR

This directory is a ready-to-copy standalone packaging repository for two
unofficial packages:

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

## Set up the repositories

1. Copy the contents of this directory into a new GitHub repository. Preserve
   `.github/workflows/update.yml` and make both scripts executable.
2. Create COPR projects named `ponesicek/t3code-bin` and
   `ponesicek/t3code-nightly-bin`. Enable the Fedora x86_64 chroots you want;
   no external repositories or custom build options are required.
3. From the [COPR API page](https://copr.fedorainfracloud.org/api/), copy the
   complete configuration into a GitHub Actions secret named `COPR_CONFIG`.
4. If the project names differ, set repository variables
   `COPR_STABLE_PROJECT` and `COPR_NIGHTLY_PROJECT`.
5. Run **Update from upstream** once with **rebuild** enabled. Afterwards it
   checks both channels every six hours and submits only changed releases.

The default install commands are:

```bash
sudo dnf copr enable ponesicek/t3code-bin
sudo dnf install t3code-bin
```

or:

```bash
sudo dnf copr enable ponesicek/t3code-nightly-bin
sudo dnf install t3code-nightly-bin
```

The packages conflict intentionally: both own `/usr/bin/t3code`, the desktop
entry, icons, and the `t3code:` URL handlers. Switching channels is explicit:

```bash
sudo dnf swap t3code-bin t3code-nightly-bin
```
