<!-- SPDX-License-Identifier: Apache-2.0 -->
# duf

This directory packages the upstream `https://github.com/muesli/duf` release
`0.9.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI downloads the
official tag archive over HTTPS and verifies the SHA-256 recorded in
`sources.yaml` before the network-enabled target build.

duf is a pure Go command-line utility for displaying disk usage and free space
across mounted filesystems. The RPM installs the `duf` executable and its
manual page. `%check` runs the upstream Go tests, then checks the version
reported by the built binary; the installed smoke test additionally exercises
JSON output against the root filesystem. Interactive terminal rendering is
not treated as a deterministic package-build test.

The release archive is pinned to SHA-256
`1334d8c1a7957d0aceebe651e3af9e1c1e0c6f298f1feb39643dd0bd8ad1e955`, as
reviewed in `catalog/upstream-releases.yaml`. No distribution recipe or AUR
content is executed during discovery or build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
