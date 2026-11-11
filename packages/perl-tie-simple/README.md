<!-- SPDX-License-Identifier: Apache-2.0 -->
# Tie::Simple 1.04

Tie::Simple connects Perl variables to callback implementations. This package
installs the original pure-Perl modules and their generated manuals.

The fixed official CPAN release SHA-256 is
`29e9e2133951046c78f205f1b3e8df62c90e114f0e08fa06b817766a0f808b12`.
The authorized stable MetaCPAN release and PAUSE CHECKSUMS agree. Debian stable
`libtie-simple-perl` 1.04-4 provides discovery lineage, not source bytes.
The recipe fetches nothing during build, which does not assert physical CI
network isolation. No source archive is committed.

The original LICENSE retains Qubling Software LLC's same-Perl terms. Exact
Dist-Zilla 5.042 template rendering identifies four generated files; the
additive NOTICE.Dist-Zilla retains the generator's attribution and the same
dual grant. The license terms in the two source archives match except for
their copyright holder names. Original source and tests are unmodified.

The original `make test` selects six files. In the host preflight it ran 31
assertions; the two original author-only files self-skipped through their
unchanged upstream guard. No downstream filters or skips are introduced.
The installed smoke checks the version and observable tied-scalar FETCH and
STORE. Host tests and staged installation are not target RPM/SRPM evidence.
