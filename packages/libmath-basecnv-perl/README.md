# Math::BaseCnv for openEuler RVA23

This package pins official CPAN Math-BaseCnv 1.14 at SHA-256
`c93566a0e9bbc9aab5998243ff8129d2389ed98cf2414bec88f5e5a57af4e7ee`,
matching publisher `P/PI/PIP/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-basecnv-perl` 1.14-3; its original archive MD5
`ca915c08437332daef7f5548f53b55d5` equals the official CPAN archive's
MD5. Official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata has
neither `perl-Math-BaseCnv` nor `perl(Math::BaseCnv)` and supplies the
runtime providers for Carp, Math::BigInt, Memoize, and the test dependencies.

Upstream `BaseCnv.pm` POD expressly grants GPL version 3 or later; the
included `LICENSE` is GPLv3, and Makefile.PL/META.json agree. Debian's
source copyright attributes the original distribution to Pip Stuart under
GPL-3. No included file has a conflicting notice. The source's
`t/02base.t` credits Ken Williams' Math::BaseCalc test cases as an
inspiration, but contains Math::BaseCnv-specific conversion calls and no
bundled Math::BaseCalc code.

The RPM retains the upstream `cnv` command. `%check` runs all three original
`t/*.t` files, including POD and POD coverage, with target BuildRequires
enabling both optional POD tests. The local source run passed 32 assertions
but skipped POD coverage because that optional module was absent; target
CI must establish actual target execution without a skip. Installed smoke
checks RPM/module/command ownership and numeric conversion through both
the module and command. PR artifacts do not establish public publication.
