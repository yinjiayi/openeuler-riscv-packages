<!-- SPDX-License-Identifier: Apache-2.0 -->
# Text::Context

This directory packages upstream `https://metacpan.org/dist/Text-Context` version `3.7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed official CPAN release is SHA-256 pinned and was corroborated against signed PAUSE CHECKSUMS and the byte-identical Debian source archive. The original README and module grant GPL v2 or later; the complete GPL v2 license text is included from a fixed SPDX revision.

The recipe preserves the original default MakeMaker suite, including POD tests, and installs both modules and their manuals. The installed smoke checks a highlighted context snippet and HTML escaping. Optional caller-supplied formatting tags should be trusted application constants. No source patch is needed.
