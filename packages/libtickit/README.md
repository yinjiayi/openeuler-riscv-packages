<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtickit

libtickit is a C library for constructing interactive terminal interfaces, not a
terminal emulator or a standalone command. This package targets openEuler 24.03
LTS SP3, `riscv64`/RVA23.

## Source and provenance

The official stable release index is
<https://www.leonerd.org.uk/code/libtickit/>. The fixed source is
<https://www.leonerd.org.uk/code/libtickit/libtickit-0.4.6.tar.gz>, 168188 bytes,
SHA-256 `4af827ba3aeaf591f4364c20d6e31c608e46fa6ada9ef7389ed5fba597f797b8`.
The source index advertised 0.4.6 as its latest stable release when reviewed; no
detached signature or upstream checksum link was advertised. The calculated
digest pins the observed release bytes; it is not a signature-verification claim.
The HTTPS GitHub mirror identifies upstream but is not the build input.

Discovery lineage is fresh AUR metadata for `libtickit` 0.4.6-1, observed
2026-10-20T16:47:40Z, retained as
`intake148-libtickit-20261020T164740Z`. The 235 archive members were inspected
as inert data. No external distribution recipe was executed or copied. Canonical
main and open-PR identity checks are admission checks, not target build evidence.

## Default behavior and package split

The recipe uses upstream's original `make` and `make install`, with RPM compiler
and linker flags and conventional `/usr` and `/usr/lib64` paths. The mandatory
libtermkey dependency and preferred unibilium backend (at least 1.1.0) are kept;
upstream's fallback logic is unchanged. No feature-selection patch is applied.

The runtime owns the versioned shared library (SONAME `libtickit.so.3`). The
development package owns all four public headers, `tickit.pc`, the unversioned
shared-library linker name, `libtickit.a`, and all 245 real/alias API manual
paths from the default install. The only default-install filtering removes the
exact `/usr/lib64/libtickit.la` libtool metadata file. This is packaging metadata,
not a removed static library or disabled API. Optional example programs are not
upstream's default build/install target; their source remains unchanged.

## Tests and acceptance boundary

`%check` runs the original full `make test` TAP suite: all 44 original numbered
C test sources, with no added skip, ignored failure, or test-source patch.
Upstream conditionally skips screen terminal output when required terminfo
capabilities cannot be loaded, and the linux builder case when that terminal
entry is unavailable. These conditions remain upstream's own code; actual skips
must be read from the target CI log, not assumed here. Signal, process, timer,
and event-loop tests remain enabled. Any actual emulator or native-only failure
requires classification from its log, not disabling that test.

The committed installed-package smoke test verifies the package version/arch,
file integrity, SONAME provide, pkg-config paths, public headers, static archive,
manual inventory, and the two original license-file hashes. It compiles and runs
new small shared and static consumers against installed files, exercising pens,
rectangles, UTF-8 width, reference-counted strings, mock-terminal rendering, and
root-window geometry. The static link explicitly names termkey and unibilium,
because the upstream `tickit.pc` does not declare static dependency flags.
This complements, rather than replaces, the original TAP suite. It does not
claim live-terminal, native hardware, timing/performance, or exhaustive API
coverage. Source/metadata and shell-syntax checks are not an RPM build or RISC-V
installation success. Target build, original TAP execution, installation/smoke,
and physical RPM/SRPM verification remain required CI acceptance gates.

## Licenses and patches

The upstream `LICENSE` is MIT, copyright Paul Evans 2012–2020. `CREDITS` retains
the Bruce Mitchener attribution for the original window implementation.
`src/unicode.h` contains the complete Markus Kuhn 2007 wcwidth permission and
warranty disclaimer plus the upstream modification record. `LicenseRef-wcwidth`
names that exact embedded notice; it does not assert equivalence to another
SPDX-listed license. Both unchanged files are installed with `%license` in both
runtime and development packages and retained in the source RPM.

There are no downstream patches; `patches/series` is intentionally empty.
Original packaging metadata, scripts, and documentation are Apache-2.0. External
source retains its original licenses; the repository license does not relicense
it. RISC-V validation remains `unknown` until real target CI results are checked.
