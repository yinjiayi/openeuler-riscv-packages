<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-hash-safekeys

This directory packages [Hash::SafeKeys 0.04](https://metacpan.org/dist/Hash-SafeKeys)
for openEuler 24.03 LTS SP3 on RISC-V/RVA23. It retains Debian stable
lineage and the fixed source SHA-256 checked against signed PAUSE CHECKSUMS.

The original README and module retain the upstream GNU GPL or Artistic
grant and credits. The package installs the architecture-specific Perl
extension and keeps the standard RPM compiler and debuginfo policy.

The full default test suite runs unchanged, including its original
author-only manifest self-skip. Installed smoke exercises the XS module
and checks that reading and copying a hash preserve iterator state.
