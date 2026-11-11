<!-- SPDX-License-Identifier: Apache-2.0 -->
# libzt

Libzt 0.3.1 is the official stable C testing-library release from
https://github.com/zyga/libzt, tagged at
`cdf916c53544154fc2f4ed94b5055d48bb44d421`. Use the published
`libzt_0.3.1.tar.gz` asset, not the Git tag archive: the published distribution
contains the original bundled ZMK 0.3.6 and generated configure script.
All 46 common source files match the tagged Git blobs; bundled build files
and the release `.version` are retained. SHA-256 is mandatory for both inputs.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd` retains Debian
stable `0.3.1-4` and Ubuntu Resolute `0.3.1-4build2` metadata lineage. Its
unknown-license hold is resolved by the complete original LGPLv3-only LICENSE
and per-file notices, including bundled ZMK. No distro recipe was executed.
The full official GNU GPLv3 text accompanies, and does not replace, LGPLv3.
Original packaging and the downstream fixture are Apache-2.0; upstream remains
LGPL-3.0-only.

The published detached signature was verified locally using the official
maintainer GitHub-account key, fingerprint
`B76CED9B45CAF1557D271A6A2894E93A28C67B47`. The account's older key copy produced
an expiration warning. Retrieving the refreshed, self-signed key for that exact
fingerprint from `keys.openpgp.org` resolved it: GnuPG returned zero, GOODSIG and
VALIDSIG without expiration or revocation errors. This is cryptographic
signature evidence, not personal identity attestation. CI's supported source
policy remains mandatory SHA-256 with advisory signature metadata. No token or
key from chat is used, and no upstream writes are made.

The recipe retains the complete default shared/static library, public header,
manuals, installed self-test and original `make check`, with assertions enabled.
The original self-test source is untouched. The success marker is mandatory,
so a cross-compilation skip cannot pass. Separately, a downstream consumer
exercises six claims against staged and installed shared/static libraries;
an installed negative control requires a false claim to return exactly one.
These consumer checks are not counted as upstream cases.

All direct build dependencies are present in the official openEuler 24.03 LTS
SP3 RVA23 repository. Full official/supplemental primary and filelists joins
found no libzt namespace or installed-path collision. There is no external test
framework, runtime source fetch, benchmark or privileged/hardware requirement.
The exact locked riscv64 target build/install/smoke is pending remote CI; local
review and repository tooling tests are not RPM or native-RISC-V success.
