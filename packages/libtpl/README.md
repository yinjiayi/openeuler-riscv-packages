<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtpl 1.6.1

The official stable `v1.6.1` tag resolves to
`5ac54fe7beab67cbfb6f95552c15a68204a014bd`. The fixed codeload archive is
190,019 bytes, SHA-256
`36d50402f9bcba5de9441e8133abf126ab1327e4b64e3a11ba7f0479bb9b95f4`.
All 399 regular members were checked against that official Git tree's blob
identities and sizes. There are no release assets or detached signature assets.
The real frozen discovery lineage is Debian stable/main `libtpl` 1.6.1-1.1;
no distribution recipe code was executed or reused.

The root LICENSE is BSD-1-Clause (one source-retention condition), notwithstanding
legacy documentation's generic “BSD revised” wording. README explicitly applies
it to this software. Five AsciiDoc HTML pages additionally embed Mihai Bazon's
TOC script under the unversioned GNU GPL, with GPL modifications attributed to
Troy Hanson and Stuart Rackham. We elect GPL-2.0-or-later for that script and
include complete GPL2 text from a fixed official GCC mirror commit. All 399
original members, including documents, optional bindings, Windows helpers and
binary fixtures, are copied byte-for-byte to inert `.notice` files before
autoreconf/configure. Those 399 files plus GPL2 have a 400-entry checksum
manifest, verified in `%check` and installed smoke. The added API driver has a
complete ISC grant in its installed source; no original notice is replaced.

The Git archive lacks generated configure/helpers, so target `autoreconf -fiv`
generates them. Default configure options preserve both shared and static
libraries. Original internal version strings (`AC_INIT` 1.4, TPL_VERSION 1.6)
are retained, not rewritten to manufacture a runtime version result. The actual
libtool version-info 0:0:0 gives the `libtpl.so.0.0.0`/`.so.0` ABI. No optional
thread/other suite or Windows mmap implementation is silently enabled on Linux.

`%check` keeps the unfiltered automake check target (zero upstream runtime
cases) and additionally runs the README's unchanged Linux `tests/Makefile`
default via serial `make -C tests -j1`: 125 programs compile, but the unchanged
Perl runner executes/answer-compares 124 programs because test125 has no `.ans`.
The runner reports output mismatches and exits with their count; it does not
separately assert child exit status. That limitation is not presented as 125
strict runtime successes. Original test26's sleep/select merely fragments a
pipe; no elapsed-time or native scheduling guarantee is claimed.

Six additional strict API cases cover a signed integer, narrow signed/unsigned
integers, double, fixed array, binary data including NUL, and ordered dynamic
array exhaustion. Assertions are enabled after RPM optimization flags. They
use `size_t` for memory-image sizes and release caller-owned images/buffers.
Build-tree replay links the built library; installed replay binds post-strip
helper/source checksums and six actual function bindings to the installed
`libtpl.so.0.0.0`. The absolute installed driver is used; exact normal-symbol
records require the caller and target to be the same physical files as that
driver and installed library (`-ef`), including valid loader hwcap aliases.
Loader overrides are cleared, raw traces and hashes printed
even when the helper fails. No performance or native-hardware claim is made.

Full fresh official primary/filelists metadata were joined for static provider,
transitive capability/command/header and owned-path checks. Generic template
`.tpl` paths and the ProFTPD-private `hanson-tpl.h` are not a standalone libtpl
ABI or an owned-path collision. This is not DNF solver equivalence or acceptance
of supplemental repository metadata. The recipe requires no undeclared fetch;
the actual trusted CI bridge remains network-enabled with pinned cache checksums.
Local validation is tooling/source-verification only: no upstream program,
compiler, target ELF, RPM build, or QEMU execution was performed. Actual target
build, original-suite, API and install results must come from exact-head CI.
