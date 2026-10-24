# Call::Context

Call::Context 0.05 checks Perl function calling context. This package follows
the `libcall-context-perl` frozen inventory entry; the Fedora and Debian
MetaCPAN aliases identify the same distribution.

The official CPAN archive SHA-256 matches its author's CHECKSUMS. Its bundled
LICENSE grants MIT redistribution, and static archive inspection found 16
ordinary file/directory entries under one root. The official target primary
metadata with SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
contains neither the RPM name nor `perl(Call::Context)`.

`%check` runs all three default upstream test files (13 assertions) unchanged.
The installed smoke checks list results, scalar-context exceptions and void
context. Source verification is performed separately from target CI. CI builds
on locked openEuler 24.03 LTS SP3 riscv64 RVA23 with network access and verifies
the fixed source digest. No local RPM/QEMU build or public publication is
inferred from metadata validation.
