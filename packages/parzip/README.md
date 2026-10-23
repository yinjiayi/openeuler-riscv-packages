<!-- SPDX-License-Identifier: Apache-2.0 -->
# parzip

This directory packages upstream `https://github.com/jpakkane/parzip` version `1.4.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official stable release archive is
`https://github.com/jpakkane/parzip/releases/download/1.4.0/parzip-1.4.0.tar.xz`,
SHA-256 `99cd404e42f6ecfa0e94c0c2d33710e648bd23d1fede7de7232f3e792b2ad8f1`.
All 57 regular source files match the official signed tag `1.4.0` commit
`8fa591e3ac8e2fcce0791b5494913f3bd7cde6a2`. Intake independently verified the
detached archive signature with the publisher's GitHub GPG public key,
fingerprint `19E2D6D9B46D8DAA6288F877C24E631BABB1FE70`. The six-file recipe
records that signature as advisory: CI must verify the pinned SHA-256; it does
not claim to perform a second signature verification without committed keys.
Frozen discovery component `github.com-jpakkane-parzip` retains Fedora
`1.4.0-9.fc44` and openSUSE `1.4.0-2.8` lineage from
`discovery-20260808T165000Z-9a89920c269462cd`; no distribution recipe was run.

Root COPYING and source headers grant GPL-3.0-or-later. Mark Adler's zpipe.c
example attribution in `src/decompress.cpp` explicitly dedicates that portion
to the public domain, as does Mathias Panzenboeck's `src/portable_endian.h`.
`LicenseRef-parzip-public-domain` denotes these explicit dedications, not a
guessed BSD/MIT/Apache version from the optional fallback wording. Every original
file is copied before build into a checksum-bound installed notice collection,
including both full notices and the ten unchanged synthetic ZIP fixtures.

Meson builds its complete original default target, including fuzz and the
GTK3 demonstration discovered through declared `gtk3-devel`. Upstream explicitly
does not install that immature GUI; only its default CLI/man-page install is
used. System zlib/liblzma resolve through the target repository and
`--wrap-mode=nofallback` prevents fallback downloads. No feature, source or test
is removed and `b_ndebug` is not changed. No RISC-V patch is introduced.

`%check` runs all three original Meson test entries unfiltered: four strict
bytequeue C++ cases plus ten extraction and eight creation Python unittest cases.
The installed smoke repeats the same original C++ test executable and unchanged
Python scripts/fixtures against `/usr/bin/parzip` and `/usr/bin/parunzip`, not
build-tree executables, and verifies the installed source/test manifests.
These are functional user-space checks, not syscall, timing or throughput
evidence. Potential unaligned ZIP64/Unix-extra reads are a static target risk;
the original cases must pass in real target CI, not be waived or labeled passed
from source review.

Fresh official full primary/filelists static admission has no package identity
or owned-path collision and no missing declared dependency provider. This is not
a DNF SAT transaction, supplemental repository acceptance, or RISC-V build proof.
Local onboarding runs only trusted repository tooling and checksum-only source
verification, never upstream QA, RPM or QEMU. Exact-head target build, original
tests, installed replay, physical products and full merge gates remain pending.
