<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-csv-xs-perl

This is a deliberate newer-version supplier, not a package-missing claim.
The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains `perl-Text-CSV_XS` 1.48 for riscv64. The target's Text::CSV 2.04
wrapper requires XS at least 1.53 to select the XS backend. That mismatch
is the verified dependency cause of failed PR #2296; a successful build of
this separate supplier alone will not repair or publish #2296.

The frozen inventory records 1.61, while official stable CPAN is now 1.64.
The pinned 287,904-B `Text-CSV_XS-1.64.tgz` SHA-256
`65c5662d4fe8ef3039a1b32f641634d0aae6ab10eabbb24f740c75332f2caf30`
matches publisher `CHECKSUMS`. Its archive contains one safe root and only
regular files/directories. README and module POD grant redistribution under
the same terms as Perl; the RPM declares the corresponding GPL or Artistic
dual-license expression.

The SPEC keeps all 35 default upstream `t/*.t` files in `%check`, including
the memory-regression test, and installs the XS module plus its examples as
documentation. An additional build-time integration assertion requires the
official target Text::CSV 2.04 wrapper and verifies that its default preference
selects the newly built XS 1.64 backend and correctly parses a quoted record.
Text::CSV is a test dependency only. Its installed-RPM smoke verifies the module
provider,
version, quoted CSV parse and serialization. This is functional QEMU-user
coverage, not a native RISC-V, memory-performance or security claim.

Exact-head target CI must demonstrate this RPM upgrades the official 1.48
package, retains full tests, and passes installed smoke. #2296 additionally
needs the newer supplier publicly resolvable and then its own full PP/XS
test and installed-smoke run. PR artifacts do not provide public RPM/SRPM
repository links.
