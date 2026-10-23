<!-- SPDX-License-Identifier: Apache-2.0 -->
# libident 0.32

This contains the RFC1413 Ident client library, default shared/static libraries,
public header, manual page and an additional packaging API smoke driver. It does
not install or enable an Ident server. Ident replies are remote assertions, not
cryptographic authentication; no security assurance or modern protocol
recommendation is made by this onboarding.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Official source and discovery

The maintainer's [official release index](https://www.remlab.net/files/libident/)
advertises stable0.32 alongside0.30/0.31. The fixed official HTTPS archive is
`libident-0.32.tar.bz2`, SHA-256
`a88a24adc377322008aaf7bf7078e6d409f5327e9515ce0d755345dd249dce22`.
All32 regular archive members were inspected inertly: one `libident-0.32` root,
no absolute/traversing names, links, special files or duplicate names. No
checksum/signature is advertised in that inspected official index; these bytes
were independently hashed, not signature-verified.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` contains precise
`remlab.net-files-libident` lineage: Debian stable/main0.32-4 and Ubuntu
resolute/universe0.32-5build1. These are source/version lineage, not official
source checksums or executable recipes. The snapshot's unresolved license hold
is resolved by the actual source's explicit COPYING grant, not by treating an
unknown distro license as permission. The separate stale AUR row is not used.

## License and complete notices

`LicenseRef-libident` means exactly the source COPYING grant: unlimited permission
to copy/redistribute with or without modification, provided authoring information
is not misrepresented. COPYING also retains Peter Eriksson's original public
domain dedication. This does not mean every bundled file is public domain.
COPYING and AUTHORS are preserved verbatim, including original encoding/names.

Generated Makefile/configure/INSTALL and portions of aclocal/sockaddr macros have
FSF unlimited-permission notices (FSFULLR). Other bundled GNU build macros retain
GPL-2.0-or-later; several helper scripts expressly permit distribution under the
containing program's terms. `admin/install-sh` has the X Consortium MIT grant.
The combined license declaration conservatively retains GPL-2.0-or-later, FSFULLR
and MIT rather than discarding notices based on exceptions. Before autoreconf,
the SPEC copies every original member into `license-notices`, preserving all
attribution/exceptions before generated-file replacement. Those source-only
notice copies are not executed. This does not claim build macros are linked
into the client library or convert its permissive license to GPL.

The first exact-head target build exposed a packaging defect despite passing CI:
target configure macros recursively replaced the notice copies named config.guess
and config.sub and hardened ltmain.sh. Only those three inert copies now have
temporary `.original` suffixes during regeneration/configure, restored after
installation and before RPM's later license-copy phase. Active build helpers and
target hardening remain unchanged. A pre-regeneration SHA256SUMS covers the 32
original members plus auxiliary GPL2 text; both check and installed smoke verify
it. Fresh repaired-head target CI and all 32 installed original-byte comparisons
are still required; this recipe correction does not claim they have passed.

Auxiliary Source1 `gpl-2.0.txt` is the verbatim GPLv2 license, not a GCC software
component/dependency. Its immutable official gcc-mirror release14.3.0 commit
`c9cd41fba9ebd288c4f101e4b99da934bcb96a11` COPYING Git blob was checked against
separately fetched raw bytes; SHA-256
`231f7edcc7352d7734a96eef0b8030f77982678c516876fcb81e25b32d68564c`.
The existing schema's `upstream-release` source kind is used for this pinned
auxiliary upstream license document. It is installed as COPYING.GPL2 together
with COPYING, AUTHORS and complete original notices. No GCC code/recipe is used.
The new API driver includes its full ISC notice and is copied to license-notices
before compilation; original packaging files remain Apache-2.0.

## Recipe and original checks

Original Autotools defaults remain: shared/static enabled; debug and optional
inetd/manual tester programs disabled. `autoreconf -fi` refreshes generated
helpers using declared target Autotools so config.sub recognizes riscv64.
No upstream source/parser/test/compiler error is patched or hidden; no RISC-V
patch exists. Removed libtool `.la` installation metadata is not an API/feature;
public header, static library and ABI linker symlinks remain.

The recipe requires no undeclared fetch after sources are materialized. Actual
CI uses a network-enabled bridge; `network_during_build=false` is a recipe
requirement, not proof of network isolation.
BuildRequires are autoconf, automake, bash, binutils, coreutils, gcc, glibc-devel,
grep, libtool, make and sed. Explicit runtime requirements are bash/coreutils/grep;
ELF dependencies are generated normally. The full fresh official-base
primary/filelists join (18,503 records/2,207,942 paths) resolves a static
204-package closure/209 versioned bounds including actual tool paths/C headers,
with no missing provider or official identity/path conflict. This is not a DNF
SAT transaction, target build or supplemental-repository namespace acceptance.

Original Makefile.am declares no TESTS/check_PROGRAMS. `make check` is still run;
no nonzero upstream automated test count is invented. Optional manual network
testers remain at their original disabled default, not a deleted automated suite.
Additional `%check` and installed smoke execute the same six-case driver: USERID
with/without charset, ERROR, malformed/unknown reply, exact query formatting.
The driver uses unprivileged AF_UNIX socketpairs, no remote daemon, port113,
privileged socket, timer tolerance, hardware or performance measurement. It checks
version0.32 and actual APIs with assertions enabled despite RPM flags. Installed
smoke checks post-brp helper checksums and loader bindings for id_parse/id_query/
ident_free to libident.so.0. The helper still asserts `id_version == "0.32"` by
string comparison; no directional loader binding is required for this data
symbol because ELF COPY relocations can reverse its binding direction. Smoke
does not validate real server/network identity or native timing.

## Acceptance boundary

Local work is inert source/rights/provider review, metadata/shell and trusted
repository tests, golden evaluation and checksum-only source verification.
No local upstream source QA, RPM/QEMU build or target execution occurs. RISC-V
status stays `unknown` until exact-head CI genuinely compiles the target, runs
unchanged check/additional driver, installs and executes committed smoke.
Physical RPM/SRPM, complete enabled-repository namespace and current main/head/
full required CI are separate gates before explicit serial squash; no auto-merge.
