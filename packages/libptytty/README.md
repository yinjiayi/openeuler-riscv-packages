<!-- SPDX-License-Identifier: Apache-2.0 -->
# libptytty 2.0

Portable C/C++ pseudo-terminal and optional session-database handling, from
the official stable release at <https://dist.schmorp.de/libptytty/>. The fixed
archive is libptytty-2.0.tar.gz, SHA-256
8033ed3aadf28759660d4f11f2d7b030acf2a6890cb0f7926fb0cfa6739d31f7.
The current official directory lists 2.0; its detached signify Ed25519
signature was independently verified over those exact bytes with the key
and policy retrieved via HTTPS from dist.schmorp.de. This is not a claim
of a separate OpenPGP trust-chain verification. CI rechecks the pinned source
SHA-256; no source archive or foreign distribution recipe is committed.

Discovery lineage is frozen snapshot
discovery-20260808T165000Z-9a89920c269462cd: Arch extra 2.0-6, Debian 2.0-1,
Fedora 2.0-14.fc44, openSUSE 2.0-2.15 and Ubuntu 2.0-1build1. The recipe is
independently written from the official CMake and API sources, not executed
distribution packaging. This standalone component is not the rxvt terminal.

## Rights and source preservation

The library's original C++ implementations explicitly grant GPL-2.0-or-later;
the complete upstream GPL2 text is in COPYING. Embedded src/ecb.h grants
BSD-2-Clause OR GPL-2.0-or-later; this package retains the full dual notice
and elects its BSD branch. Files without separate headers remain in the
upstream GPL distribution context, not a newly invented per-file license.
src/estl.h preserves its statement that the MICO-derived original was
completely rewritten. All historical author lines, including the multiple
authors in logging.C, remain intact. All 19 original archive members are
copied verbatim with .notice suffixes before generation; a 19-entry SHA-256
manifest is verified during %check and installed smoke. The added API
driver carries its complete MIT grant, installed as PACKAGING-COPYING and
with the corresponding driver source. RPM and SRPM together retain source
and build instructions; binary-only publication is not an acceptance claim.

## Original defaults and added functional cases

Plain CMake retains shared-library ON, UTMP/WTMP/LASTLOG ON, the C API,
helper/reentrancy defaults, GNU libsupc++ detection and the actual TTY-group
runtime configure probe. No feature/probe is disabled or preseeded. The
original c-sample is built in default ALL. Upstream defines no CTest/check
target and has zero original runtime cases. The sample is not a runtime
test: it invokes optional login/database writes and a login shell, so it is
not installed or executed as a supposedly harmless smoke test.

Six additional strict cases exercise nonroot initialization/empty object,
allocated PTY descriptors, raw master-to-slave bytes, raw slave-to-master
bytes, Linux UTF8 input flag on/off and idempotent slave close/object teardown.
Assertions remain enabled after distribution flags. Five-second poll bounds
only prevent hangs; no native latency/performance assertion is made. No
login, shell, controlling-terminal, privilege-dropping or forced-helper call
is used. This needs working unprivileged target devpts. Its results do not
validate kernel/privileged/session-security correctness, nor all library
features. An unavailable PTY is a real target/infrastructure failure, not a
reason to remove cases or turn off defaults.

Installed smoke replays that exact driver. Because the installation harness runs as root,
smoke uses util-linux setpriv to execute the driver with numeric UID/GID
65534 and cleared supplemental groups; an already nonroot caller runs it
directly. The driver still rejects root or mismatched real/effective IDs.
This is test-harness setup, not a validation of library privilege handling.
It checks post-strip binary/source and original-notice hashes, and preserves full loader binding trace plus
SHA-256 even on driver failure. Eight exact normal-symbol bindings from the
absolute installed driver must target the same file as installed
/usr/lib64/libptytty.so.0; same-file comparison permits legitimate loader
aliases such as /lib64/lp64d, without accepting another library.

The full official target metadata audit covers build/runtime/command/header
and C++ compiler/supc++ provider closure, identity and owned paths. It is
static official-base evidence, not a claim of complete supplemental metadata
acceptance or an actual dependency solver result. The recipe requires no
undeclared fetch; the actual CI bridge may be network-enabled with checksum
verification, so this is not an offline-isolation attestation.

Only trusted repository tooling and source-verify-only run locally. No local
upstream compiler/build/test, RPM or QEMU was run. Real exact-head target CI,
installed products, all namespace evidence and physical RPM/SRPM review remain
required before merge/publication. No RISC-V-specific patch is asserted.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
