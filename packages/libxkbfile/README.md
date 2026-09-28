<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxkbfile

This package tracks X.Org's official stable `libxkbfile` 1.2.0 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org release announcement](https://lists.x.org/archives/xorg-announce/2026-January/003662.html)
publishes SHA-256 `7f71884e5faf56fb0e823f3848599cf9b5a9afce51c90982baeb64f635233ebf`,
which matches the independently downloaded release tarball. The initial PR CI
could not reach `xorg.freedesktop.org`: four HTTPS attempts timed out before
`rpmbuild` started. For this release, `sources.yaml` instead pins the official
[X.Org GitLab release commit](https://gitlab.freedesktop.org/xorg/lib/libxkbfile/-/commit/42e5dedd7fd3c7c73f3870a8751893c03c1afc69)
archive at SHA-256 `45aaffea04615ce5b338ec7a068241a98c3d8938f5b7b8176c0f32d81901e453`.
The extracted GitLab and published release source trees compare identically;
the archive containers and their SHA-256 values differ. CI rechecks the pinned
GitLab archive hash before building. The archive has one top-level source
directory, no symlinks or special files, and its license is declared as MIT by
upstream Meson and included as `COPYING`. The build still uses upstream Meson
and requires no new Autotools dependencies. CI reachability of the alternate
host remains to be confirmed by the rerun.

The release contains no upstream test directory or Meson-registered tests.
`%check` retains the upstream Meson test target without claiming a passing
upstream suite. The installed-RPM smoke test compiles and runs against the
installed `xkbfile.pc`, `libxkbfile.so.1`, and public `XkbRF_Create`/
`XkbRF_Free` APIs. It requires no X server or display.

The frozen inventory's exact `libxkbfile` discovery key maps to this package
ID. Its Debian and Ubuntu versions are lineage evidence, not the source of
packaging code. Build and installed-smoke CI results must be read at the exact
PR head; neither a green build nor a CI artifact proves public RPM publication.
