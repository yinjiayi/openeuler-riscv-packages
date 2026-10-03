<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::OverloadInfo 0.008

Frozen Ubuntu `resolute/universe` `libdevel-overloadinfo-perl` 0.008-1 maps
to the official stable ILMARI CPAN release. The fixed HTTPS source is 16,801
bytes, SHA-256 `91347d3a0b9a269180a3ea0e0d43f12c55dec3ddb974642f0e19093f907543d4`,
matching the publisher's `CHECKSUMS`.

The top-level `LICENSE` and `README` grant same-as-Perl for Dagfinn Ilmari
Mannsåker's software, repeated in the only installed PM. The bundled
configure-only `inc/ExtUtils/HasCompiler.pm` names Leon Timmermans and
independently grants the same terms. Its redistribution does not rely solely
on Dagfinn's generated notice; no contrary file grant was found.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Devel-OverloadInfo` name or `perl(Devel::OverloadInfo)` provider. It
supplies MRO::Compat 0.15, Package::Stash 0.40, Sub::Util 1.63, Test::Fatal
0.014, gcc and perl-devel. BuildRequires retains upstream's default compiler
capability probe; this package itself installs no XS. A hard runtime
Sub::Util dependency and target checks ensure the modern branch executes.

All four original default files remain unchanged. Locally the two functional
files passed 22 assertions; the two author-only POD files self-skipped by
upstream design. Target `%check` requires precisely that count and skip scope
and asserts the Sub::Util branch. Installed smoke separately exercises actual
overload discovery and declaring-class inspection. Target exact-head CI must
prove physical RPM/SRPM and DNF-installed behavior. No local RPM/QEMU build
or publication occurred.
