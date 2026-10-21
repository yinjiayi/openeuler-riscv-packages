<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdisplay-info

This directory packages libdisplay-info 0.4.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is the official release asset attached
to upstream's current stable `0.4.0` release (tag commit
`c67a3e9bedb05ab61c7443704a1a107e76254595`). Its locally verified SHA-256
matches upstream's independently published `.sha256sum` asset and is pinned
in `sources.yaml`. The XZ archive has one source root and no unsafe paths,
special files, or escaping links.

Frozen discovery snapshot `discovery-20260813T080000Z-b34-libdisplay-info`
records Arch `0.3.0-1`, Debian stable `0.2.0-2`, Fedora 44
`0.3.0-1.fc44`, openSUSE Tumbleweed `0.3.0-2.5`, and Ubuntu Resolute
`0.3.0-1`. These frozen distribution versions establish maintained
cross-distribution lineage; the source bytes come only from upstream's newer
official stable release. No distribution recipe was read or executed.

The target repository snapshot contains diffutils `3.10-2.oe2403sp3`, GCC
`14.3.1-10.oe2403sp3`, hwdata `0.372-3.oe2403sp3`, Meson
`1.3.1-1.oe2403sp3`, Ninja `1.11.1-1.oe2403sp3`, patch
`2.7.6-22.oe2403sp3`, Python `3.11.6-20.oe2403sp3`, and pkgconf
`1.9.5-2.oe2403sp3`. It contains no libdisplay-info package, CLI, matching
Provides, or `libdisplay-info.so.4` ABI. The built library declares SONAME
`libdisplay-info.so.4`, while its installed implementation file is
`libdisplay-info.so.0.4.0`.

`%check` runs every test registered by the official source: decode and print
golden comparisons for all 34 registered entries, 68/68 passed with zero
skips. The duplicated `cta-timings` registration is preserved exactly as
upstream defines it. The optional `gen-test-data` maintenance target uses an
external reference decoder but is not a registered test; wrap downloads stay
disabled and no test is removed. The installed smoke links through
`libdisplay-info.pc`, checks the public CTA VIC lookup and round-trip ABI, and
executes the installed decoder's defined empty-input error path.

The installed implementation and packaging metadata are MIT. The official
source archive also contains CC-BY-4.0 EDID fixtures used only by `%check` and
not installed in a binary RPM; `sources.yaml` records both redistribution
licenses. Apache-2.0 covers only this repository's original packaging metadata
and scripts.
