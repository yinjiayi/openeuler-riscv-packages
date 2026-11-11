<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsort-fields-perl

This directory packages upstream `https://metacpan.org/release/BRIANDFOY/Sort-Fields-1.003` version `1.003` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The CPAN archive is SHA-256 pinned and checked against signed PAUSE
checksums. The release's package-specific LICENSE explicitly grants
Artistic-2.0, while older MakeMaker metadata uses the generic `perl`
label. The original release, full LICENSE and Joseph N. Hall's
attribution are preserved.

The RPM runs the unchanged upstream `make test` harness, which selects
`t/test.t`. Upstream's optional Test::Manifest would select the same file;
it is not required or supplied in this target. The installed smoke check
also exercises stable numerical ordering with tied fields.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
