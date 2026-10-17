<!-- SPDX-License-Identifier: Apache-2.0 -->
# libac

This directory packages upstream `https://github.com/ac000/libac` version `2.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official tag `v2.0.0` is pinned to commit `061bdbb82ffa76fdf91e78920ca142d2b8a40211`.
The archive SHA-256 is `26806adfddd294d7d5cba67bf452cd880c4209bf2bfce03bee30b36d07d560d6`;
all 45 source files were matched to the immutable official Git tree. No patch is applied.

The root default `make` builds the shared library and the original `src/test`
example. Upstream `make test` only compiles that example, which unconditionally
returns success and has no assertions. Its 15 print-oriented groups are not an
upstream semantic pass count. Manual execution also touches `/tmp/services` and
`/tmp/libac` and performs external DNS; this offline recipe does not invoke it or
alter its source, original targets, warning flags or default features.

Separately labelled downstream checks use the installed public header and
`libac.so.2`: queue FIFO/empty behavior, circular-buffer capacity/wrap/reset,
string splitting/edit distance and JSON escaping/value/length. The runner fails
at the first failed check and is compiled at O0 and O2 both in `%check` against
the staged library and after RPM installation. It verifies fixture checksums,
SONAME linkage, absence of RPATH/RUNPATH and exact loaded-library resolution.
These are limited API/ABI checks, not exhaustive coverage, native-hardware
validation or performance evidence. No static or pkg-config API is invented.

Primary source SPDX `LGPL-2.1` and the README's version-2.1 grant are treated as
LGPL-2.1-only. The glibc-derived common files separately carry LGPL-2.1-or-later,
and `random_r.c` additionally carries the three surviving Berkeley conditions
(numbered 1, 2, 4; no advertising clause). The FreeBSD-only `tdestroy.c` is Apache-2.0.
The source union is recorded conservatively; it does not relicense primary code
or imply that FreeBSD implementations are compiled on Linux. Complete original
LGPL, official GPL2/Apache2 texts and source notice files accompany the RPM.

Full official and supplemental target primary/file inventories were checked for
names, SONAMEs, header/file collisions and required providers. `crypt.h` is from
`libxcrypt-devel`; `/etc/services` belongs to `setup`, not `iana-etc`. The latter
is not needed by the offline consumer and is not an invented dependency. Actual
target DNF resolution, riscv64 build, installed tests and physical RPM/SRPM
acceptance remain CI gates; local source verification is not a build result.

First-head Package CI 38816587539 failed before compilation: unconstrained
`libxcrypt-devel` selected supplemental 4.5.2-1, which cannot satisfy the fixed
SP3 `glibc-devel` static-provider closure. The official 4.4.36-3.oe2403sp3 devel
package already supplies `libxcrypt-static` in that image. BuildRequires and
the installed devel consumer requirements therefore pin that compatible EVR.
Inventory/provider presence alone was not proof of DNF solver compatibility.
Remove or revise this target-specific pin only after a complete compatible
libxcrypt static/devel provider set and the locked image are jointly validated.
This dependency repair does not alter upstream source, flags or test targets;
replacement exact-head CI must establish build/install success independently.
