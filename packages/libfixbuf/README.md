<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfixbuf 2.5.4

This directory packages upstream `https://tools.netsa.cert.org/fixbuf2/` version `2.5.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The IPFIX library is distinct from fixbuf-tools, YAF and pyfixbuf. Official
current pages identify 2.x as stable and 3.x as pre-release; stable 2.5.4 is
dated 2026-03-12. Published archive SHA-256:
106b8e1e560928a4dc91d8264326bd2463767570d77417535964f450de1f972e.
Frozen lineage is openSUSE Tumbleweed 2.5.4-1.4 observed 2026-08-08; no distro
recipe was executed or copied.

## Rights

LICENSE.txt supplies LGPL3 terms and CMU's distribution statement. HPE's
fbexporter contribution retains its attribution. IANA IPFIX registry data in
src/infomodel/ipfix.xml and generated .i has a separate CC0-1.0 dedication:
https://www.iana.org/help/licensing-terms is the joint IANA/IETF statement
dated 2021-11-10. This covers technical Protocol Registry data, not linked RFC
publications; bundled XML consists of structured registry records, not an
entire RFC. The policy and CC0 legal text are checksum-pinned extra sources.
Other retained rights include X11 install-sh (including name-use restriction),
FSF permissive macros, GNU configuration/libtool exceptions and bundled
Doxygen JavaScript by jQuery, jQuery UI, Ariel Flesler, PowerTip, Touch Punch
and SmartMenus (MIT branch where dual licensing permits).

All 119 original ordinary archive members are copied byte-for-byte with inert
.notice suffixes before configuration can replace active helpers. Four extra
licensing documents give 123 checksummed members; the manifest excludes itself.
Both %check and installed smoke verify every checksum. The composite license
does not relabel all components as LGPL. The added API driver has a full ISC
notice and installed corresponding source.

## Original defaults and checks

Plain %configure preserves shared/static libraries, warning/debug policy,
abort-on-default-sizespec and enabled maintainer mode. SCTP, OpenSSL and Spread
remain upstream opt-ins, neither enabled nor disabled by this recipe. No cached
configuration result is forced. The alignment probe remains for real target
CI, not local execution. Libtool version-info 10:2:1 gives libfixbuf.so.9.1.2.
Generated configure/Makefiles and model .i inputs in this archive are newer
than their source inputs; Perl generates model C/headers. Doxygen generation
is an explicit manual/dist target, not default all/check. Source timestamps
and tests are unchanged. Unfiltered make check is retained, but four original
Makefiles define zero upstream runtime cases: success alone is not a suite.

Six added asserted API cases cover model lookup, template layout, session/domain,
IPFIX headers, byte order and in-memory export/collection round-trip. They use
no sockets, privileges or timing threshold. -UNDEBUG retains assertions.
The buffer exporter overwrites its caller's buffer on every emit; the driver
therefore explicitly emits and retains the Template Message before the Data
Message. It asserts the template's header/domain, Set ID 2, Template ID 257,
two IPv4 fields (IDs 8/12, each four bytes), and both message lengths. The
collector receives the two complete messages in order and learns its external
template from the wire; no external collector template is preinstalled. The
original data header, network byte order and exact round-trip value assertions
remain strict. Unbuffered diagnostic output preserves earlier case results if
a later assertion fails.
Installed smoke verifies post-strip driver/source hashes and all six cases;
after clearing loader overrides it checks four exact function bindings to the
installed library, and logs the full raw loader trace plus its SHA256 before
cleanup (also retaining the real driver status and trace on failure). The
driver is invoked by its absolute installed path. Each exact `normal symbol`
record must identify that installed driver and the same physical file as
`/usr/lib64/libfixbuf.so.9.1.2`, using Bash file identity (`-ef`). Absolute
loader aliases, including the observed `/lib64/lp64d/libfixbuf.so.9`, satisfy
the check only if they identify that same installed file. Relative paths,
different callers or files, similarly named symbols and contradictory target
records do not satisfy the check; no library-path allowlist replaces identity.

## Scope and limitations

The fixed target is the locked openEuler 24.03 LTS SP3 riscv64/RVA23 image.
GCC/binutils, glib2-devel, Perl, pkg-config, make and actual shell/file utilities
are declared. RPM generates ELF requirements; bash/coreutils/grep support smoke.
Fresh official primary/filelists joined all 18,503 packages and 2,207,942 paths:
no missing provider or standalone name/provides/path collision. This is static
official-base evidence, not a DNF solver or acceptance of supplemental namespace.
The recipe requires no undeclared fetch after materialization, not network
isolation of the network-enabled CI bridge. Local gates execute trusted tooling
and source verification only, never upstream QA, RPM, ELF or QEMU.
Exact-head CI must still prove build/install, API outcomes, preserved notices
and physical RPM/SRPM checksums. Source-only gates do not qualify merge/release.
