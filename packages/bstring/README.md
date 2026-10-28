<!-- SPDX-License-Identifier: Apache-2.0 -->
# Bstring 1.1.1 shared C SDK

Fixed official stable source: msteinert/bstring tagv1.1.1,
commit3ad93de7fda8b23901d78fefb2afcbc17ba5312a, tree91fec60a4f2fc627e1caf5869da9a9d2a37d7799.
The149111-byte source archive SHA256 is
449ca08cd2d7e5385792132ef680f6378faeaa7fdfc457e5ba1a0d875890eb73.
All53 regular Git files and executable classes match; no source patch or submodule.
The stale Fedora1.0.3 catalog row is retained as lineage, not source checksum evidence.

Root ordinary published-component review chooses the upstream BSD3 offer and
retains full COPYING, GPLv2 alternative, all original notices and comparative
documentation/attributions. Twelve code/header/test/fuzz files have explicit
BSD3-or-GPLv2 grants. No personal external-origin warranty, separately obtained
CERT/Robert Seacord permission or imported external implementation is claimed.
Owned packaging/QA is Apache2 with its complete legal text retained separately.

The actual annotated tag reconstructs to bbb1a3295b327cf6f103e4626bf5778ab74cd40b
and independently verifies with current linked official rdmark signing key
FCDCD52FC94EE535D92B42A159052F44A337E0E9, without a keyserver/default keyring
or expiry waiver. GitHub's bad_email remains recorded: tagger/profile
daniel@mindani.net differs from the key's verified markstedt@gmail.com;
the actual release and commit link to that same account. No email equality,
unsigned-commit signature, detached archive signature or legal-rights proof
is inferred from cryptographic verification.

Preserve native shared-only production library, default UTF8 and four public
root headers. Existing upstream tests are opt-in, not default-enabled: enable
all3 original Check suites as upstream Linux CI, preserving all83 registered
cases and their failure exit codes. Leave VALGRIND_OPTS and Check-selection
overrides absent; do not reduce core000's original bounded matrix. The README
upstream Testing command mistakenly enables docs; the actual Meson/CI contract
is authoritative. Default-off docs/fuzz/old-API/bgets options remain unchanged.

Additive target-only consumers cover C99/C11 times installed/relocated prefix:
four shared multi-translation-unit programs, each with six semantic groups,
all4 exact header traces, exact pkg-config owner/version/directories, ELF64
RISC-V, SONAME1, link-map and actual PID-tagged candidate loader-init proof.
Three negative controls cover missing header, undefined symbol and absent PC
prefix. Native default has no static library, CMake package or CLI: none is
invented. Relocation copies only exact SDK-owned files, never wholesale /usr.

This fork shares ancestry/API with websnarf/bstrlib, but its root headers,
libbstring.so.1 and bstring.pc differ from the managed legacy subdirectory
headers and libbstrlib/libbstrwrap/libbsafe archives. Fresh full canonical and
provider namespace/dependency projections are separate from actual target DNF,
link, build/install and physical-RPM acceptance. Real exact-head CI must satisfy
those gates. No local compiler, source/owned functional QA, RPM or QEMU run,
performance result, target success or publication success is claimed.
