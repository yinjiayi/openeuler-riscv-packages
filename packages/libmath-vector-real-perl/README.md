# Math::Vector::Real for openEuler RVA23

This package pins official CPAN Math-Vector-Real 0.18 to SHA-256
`b24d1907e60619300db24af21c6ee95327c51d9f75c5a0c3921d6ed64e3e54fa`,
matching publisher `S/SA/SALVA/CHECKSUMS`. Frozen Ubuntu discovery records
`libmath-vector-real-perl` 0.18-3. Official openEuler 24.03 LTS SP3 riscv64
RVA23 primary metadata has neither `perl-Math-Vector-Real` nor the main and
test-helper Perl module providers. It supplies MakeMaker, Test::More and
Test::Builder::Module.

The README and primary module POD attribute Salvador Fandiño and grant this
library the same terms as Perl 5.10.0 or any later Perl 5. The second
installed file, Math::Vector::Real::Test, is a bundled helper within that
library; other source, examples and tests have no contrary notice. The RPM
uses the repository's Perl-terms SPDX expression and installs README as its
license notice. No upstream source, optional-backend selection or test is
changed.

`%check` runs the only original default test file, which upstream explicitly
places on its pure-Perl backend using `t/dont_use_xs`. Clean local execution
passed all 29 assertions with zero skips. Installed smoke checks both RPM
module providers and vector norm, dot and cross products. Exact-head hosted
CI must establish target RPM/QEMU behavior and physical RPM/SRPM bytes; it
does not establish public repository publication.
