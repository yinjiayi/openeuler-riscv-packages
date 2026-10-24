<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxdiff

This directory packages upstream `https://github.com/spotrh/libxdiff` version `1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official stable tag `1.0` resolves to commit `9c6289c5a088bf24f18f0b7bf8acaaf643aa411d`.
The immutable archive SHA256 is `667751e2e11971765a421d8d20e038ee2d4122d784ccf8da479cf6f578252159`;
all 39 archive members match their exact upstream Git blobs. No detached
signature was advertised in the inspected tag/release metadata.
Frozen Fedora `1.0-30.fc44` discovery lineage is retained; no distro recipe ran.

This is the spotrh Git/libgit2-derived fork, not old libxdiff 0.23 API compatibility.
The official repository's `libgit2` declares `bundled(libxdiff)`, but full joined
primary/filelists has no standalone `libxdiff.so.1`, `pkgconfig(libxdiff)` or
`/usr/include/xdiff` supplier. This package neither replaces libgit2 nor declares
its capabilities; it supplies the standalone library/interface independently.
All 18,503 official packages and 2,207,942 file paths were inspected against a
fresh root. This static admission is not a solver run, supplemental acceptance,
or target build result; full supplemental namespace remains a later merge gate.

Core C/header notices are LGPL-2.1-or-later. `xhistogram.c` carries the complete
Eclipse Distribution License 1.0, a BSD-3-Clause-style grant including its own
copyright and non-endorsement notice. Generated Autotools/Libtool helpers have
their own FSFULLR/MIT/GPL2-or-later/GPL3-or-later and distribution-exception
notices. All 39 original members are copied byte-for-byte to `license-notices`
with a `.notice` suffix before regeneration, alongside full GPL2/GPL3 texts;
that suffix prevents recursive target configure macros from rewriting inert
notice copies. Their 41-entry SHA256 list is checked in build and installed
smoke. The original ISC-licensed packaging API driver is also included there.

No patch is introduced. Shared/static and algorithm defaults are retained.
Target-supplied Autotools regenerate current configuration helpers for riscv64.
`README.md` is copied to the Automake-expected `README` documentation name only.
Original `make check` remains unfiltered: its `check-am: all-am` target contains
zero upstream automated cases, not an implied upstream test-suite success.
The added six-case API driver checks equal input, minimal/patience/histogram
diff output, whitespace-ignore behavior, and a conflict-free three-way merge.
Long lines at non-eight-byte line offsets exercise the default little-endian
fast-hash path; actual riscv64 CI must validate it, no feature is disabled.
It is replayed after normal installation with four actual shared-library
symbol bindings, public headers/static library/pkg-config metadata presence,
notice checksums and post-install-strip driver checksum verification.

The recipe requires no undeclared fetch after source materialization. The
actual CI bridge is network-enabled and checks cached source checksums; this
is not an offline-isolation claim. Local verification only runs trusted recipe
tooling and source verification, never upstream QA, RPM builds, ELF or QEMU.
Exact-head hosted build/check/install, physical RPM/SRPM and complete namespace
acceptance remain required. No timing, performance, kernel or native-hardware
claim is made; current RISC-V status remains `unknown`.
