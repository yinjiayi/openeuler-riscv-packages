<!-- SPDX-License-Identifier: Apache-2.0 -->
# libosip2

GNU oSIP 5.3.2 is packaged for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Its [official source archive](https://ftp.gnu.org/gnu/osip/)
is pinned by SHA-256. The frozen AUR discovery record is stale (5.3.1), so it
is used only as lineage, not as version or packaging authority. No AUR build
recipe was read or executed. Upstream headers and COPYING identify the source
license as LGPL-2.1-or-later.

The build retains pthread support and enables upstream tests. `%check` runs
the complete registered SIP fixture suite and rejects nonzero failure counts
even though the upstream shell driver returns success on failed fixtures.
Installed-RPM smoke links to both the parser and transaction libraries and
checks a URI round trip and core initialization. QEMU user-mode functional
tests do not establish timing or native-hardware performance.

Apache-2.0 covers original packaging metadata, scripts, and this document;
the upstream source retains its own LGPL terms.
