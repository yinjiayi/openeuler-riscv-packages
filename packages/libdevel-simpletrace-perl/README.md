<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::SimpleTrace 0.08

The frozen Ubuntu `resolute/universe` `libdevel-simpletrace-perl` 0.08-4 row
maps to the official stable SAPER CPAN tar. Its 17,826-byte HTTPS archive has
SHA-256 `d318a85bb29ee3c770e6b888585692a6f1a0173faf001be995e97481212536bf`,
matching the publisher's `CHECKSUMS`.

The archive's top-level `LICENSE` expressly licenses the program under the
same terms as Perl and includes the Artistic 1.0 and GPL version 2 texts. `README`
and the only installed module repeat that grant; no file has a contrary
notice. The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary
has no `perl-Devel-SimpleTrace` name or `perl(Devel::SimpleTrace)` provider.
It supplies Module::Build 0.4234, Data::Dumper 2.183, Test 1.31, Test::More
1.302198, Test::Distribution 2.00 and its hard providers, Test::Pod 1.52,
Test::Pod::Coverage 1.10 and Test::Portability::Files 0.10.

All ten original default `t/` files are unchanged. On the local macOS host,
seven files ran 17 assertions and passed; three distribution/coverage/
portability files self-skipped because their optional test modules are absent
locally. Those providers are hard target BuildRequires, and target `%check`
requires all ten files to run with no skips. Installed smoke separately
checks that the hooks are active and a thrown exception includes nested caller
frames. No local RPM/QEMU build or publication occurred; target exact-head CI
must prove physical RPM/SRPM and DNF-installed behavior.
