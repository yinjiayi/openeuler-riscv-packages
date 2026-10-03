# Data::Section::Simple

Data::Section::Simple 0.07 extracts named text sections from Perl DATA handles.
Its official CPAN 11,479-byte archive matches the author CHECKSUMS SHA-256.
The frozen `libdata-section-simple-perl` Ubuntu lineage is 0.07-4; openSUSE's
0.70.0 packaging number is not claimed as an upstream release.

Bundled LICENSE, README and the module POD grant Perl GPL/Artistic terms.
Static inspection covered every source, helper and test file and found no
conflicting file-specific restriction. The archive contains 22 ordinary entries
under one root. The verified official target primary metadata SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has neither the RPM name nor module provider and supplies the test dependencies.

`%check` runs all five default files with `RELEASE_TESTING=1`, including upstream
release POD validation. Installed smoke reads two sections through functional
and object interfaces and checks missing names. Source verify-only and local
metadata gates are separate from locked openEuler SP3 riscv64 RVA23 CI. No
local RPM/QEMU build or public publication is claimed.
