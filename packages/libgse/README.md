<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgse 1.2.1

Canonical component `github.com-cnes-libgse` comes from retained AUR discovery
`libgse 1.2.1-1`, snapshot `discovery-20260808T165000Z-9a89920c269462cd`.
That stale discovery row is provenance only: official CNES tag `1.2.1`
freshly resolved to `8d7fe35d2cc0a669af89ca039f506e787a6ebaa6`, and
all523 archive files matched that commit's Git blobs. No distribution recipe
was executed. Source SHA256 is
`cdf4158f0952501d80e8eaec1a5c39ed7862e997ae40f104b1caeb82a0a4c58b`.
No upstream signature was supplied; official Git identity and SHA256 are
identity checks, not a fabricated signature.

The original library grant is LGPL3-or-later. CRC code retains the Regents
of the University of California's four-clause notice, identified as
[BSD-4-Clause-UC](https://spdx.org/licenses/BSD-4-Clause-UC.html).
Berkeley's [official amendment](https://ipira.berkeley.edu/sites/default/files/amendment_of_4-clause_bsd_software_license.pdf)
retroactively deletes its advertising clause for software officially licensed
by Berkeley. This is limited to the Regents' grant: it does not purport to
relicense TAS modifications, whose copyright and project LGPL grant remain.
The RPM preserves original `COPYING.BSD`, `COPYING.LESSER` and full official
GNU GPL3 text; no license notice or source header is rewritten.

The release tag is1.2.1 but unmodified `configure.ac`/`gse.pc` report1.2.0.
The actual pkg-config module is `gse`, not upstream README's `libgse` example.
Consumers include `<gse/encap.h>` etc.; the original public test uses bare
header names, so its compiler invocation explicitly adds `/usr/include/gse`.
No version patch or fake pkg-config claim is introduced. The shared library
and all app subdirectories are built with upstream defaults. Static libraries
are disabled by upstream default, not silently enabled. Only Libtool `.la`
metadata is removed from staging; no API/header/source or warning is disabled.

`make -j1 check VERBOSE=1` retains all32 original registered shell scripts:
3 common,18 encapsulation/FIFO/refragmentation,10 deencapsulation and1 end-to-end.
All19 original check programs are built. Some original wrappers retry failures
with verbose output; they remain byte-for-byte, not described as fail-first.
A separate downstream replay compiles unmodified original public-API
`test_encap_deencap.c` with installed public headers and shared library at
O0/O2. Its original maximum-PDU PCAP is checksum-checked; exact original
argument0 and additional fragment sizes1400/4096 are run directly once each,
requiring byte-equal recovered payloads and successful library status paths.
All6 executions fail on their first nonzero result. This runs against staging
and after RPM install; it is not counted as additional upstream tests.
Link resolution, SONAME dependency, no RPATH/RUNPATH and RPM ownership are
checked. A pass is not a full protocol certification or native hardware result.

`distcheck` is not an upstream default/CI requirement; the official tag's
`EXTRA_DIST` names absent `debian/` files. No distcheck pass is claimed and
the original default `check` target is not reduced. These offline tests need
no network, TUN device, privileged tunnel execution or performance benchmark.

Complete official18503/supplemental1244 primary/filelists inventories found
no canonical RPM, `pkgconfig(gse)`, SONAME or public-header collision. Target
build/installed-test dependencies include gcc/autotools/libtool/libpcap-devel/
pkgconf. Actual DNF resolution and target build/install remain CI gates, not
inferred from the static dependency review.

The target is locked openEuler24.03-LTSSP3/riscv64/RVA23 under QEMU-user9.2.
No source patch, local upstream/RPM/QEMU execution, Auto-merge or publication
is included. Exact-head target CI and real RPM/SRPM payload acceptance must
complete before an explicit squash. Packaging scripts/docs are Apache-2.0;
upstream sources and notices retain their original licenses.
