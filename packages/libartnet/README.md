# libartnet 1.2.0

Canonical component: `atlesn/libartnet`, official tag `v1.2.0`, fixed commit
`416a83e92d150e8e0295a9aabd7ad1fb1c1689bc`. The official source archive SHA-256 is
`440cd4118cb08f0d8051586f1583b06e45cf414fe90987049eda6d79f83c7cbf`.
All 42 source files were matched to the fixed Git tree. Discovery lineage is
`aur:libartnet` 1.2.0-1 in snapshot
`discovery-20260808T165000Z-9a89920c269462cd`; its historical stale-AUR rejection
is retained, not used as current official-release authority. No AUR code ran.

The source copyright grants LGPL-2.1-or-later; original full COPYING and source
notices are retained. The recipe and separate downstream fixtures are original
Apache-2.0 packaging work. The small upstream-context patch is LGPL-2.1-or-later.
No distribution recipe or upstream write is used.

Default autotools shared and static library features and original warning flags
(including `-Werror`) are preserved. `autoreconf -fi`, the normal configure/build
and unmodified `make check` target are run. Upstream registers no original tests;
an empty check target is not reported as upstream semantic coverage.

One generic patch declares the IPv6 configure probe's `main` and `exit` correctly
for modern C without forcing its runtime result. It also corrects pkg-config's
include root: installed headers are `artnet/*.h` and refer to `<artnet/common.h>`.
Remove it when an official stable release fixes both contracts. It does not
change network/protocol implementation or work around QEMU/RISC-V behavior.

The downstream **offline ABI/argument contract** is a separately labelled public
header and shared-library consumer: 30 fail-first checks for exported constants,
socket-option values and existing NULL-node/list argument guards, built at O0
and O2 against both staged and installed products. It verifies fixture SHA-256,
pkg-config version/include/library paths, SONAME, exact loaded library and absence
of embedded RPATH/RUNPATH. It creates no network node, opens no socket, and claims
no packet exchange, DMX interoperability, hardware, timing or native coverage.

Target: locked openEuler 24.03 LTS SP3, riscv64/RVA23 QEMU user-mode image. Complete
official/supplemental provider/file inventories were reviewed for dependency and
namespace compatibility; provider presence is not a successful DNF transaction.
Build/install execute without network after dependency/source preparation. The
default static archive is retained; only libtool `.la` metadata is removed.
Local schema/golden/source/tooling checks do not establish target build/install
or physical-product acceptance. Target CI and physical acceptance remain pending
at submission; no local RPM/QEMU/upstream execution, auto-merge or release claim.
