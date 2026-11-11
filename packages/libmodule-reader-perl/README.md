<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodule-reader-perl

This directory packages [Module::Reader 0.003003](https://metacpan.org/release/HAARG/Module-Reader-0.003003)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The module reads Perl source
using include-path search and, when supplied by its caller, trusted Perl hooks.
Do not use untrusted paths or hooks with this API.

The fixed source SHA-256 is `2d5a0adb772517754fbfec0180d6a51039bb0cd3bd3316a59eaa32c05ddde284`.
The publisher's PAUSE CHECKSUMS and authorized MetaCPAN release agree.
The tracked sources and tests match upstream tag commit
`89c86b115592c28dd116f13ce2e70144a29f0b2d`. Graham Knop's original README and
module retain the grant under the same terms as Perl itself; the release
metadata declares `perl_5`. The RPM ships the original README and both
complete Perl license texts. Makefile.PL uses the present release META.yml,
so the checkout-only Distar helper and its network clone are not run.

The recipe runs all three unmodified upstream default test files under
MakeMaker. The source tests cover disk files, symlinks, file permissions
when run unprivileged, and explicit in-memory include hooks. The separate
installed smoke reads the installed module through both public APIs and
compares the bytes. The installed smoke also checks real INC, AUTOLOAD,
an overridden can, a named overload, and preservation of hook errors.
No upstream test files are removed or modified.

Perl 5.38 changed the missing-method diagnostic for unsupported object
hooks. The original test compares it to Perl's own require diagnostic;
it failed for Regexp and a class without INC. Patch 0001 adapts Petr
Písař's [CPAN RT #148979](https://rt.cpan.org/Ticket/Display.html?id=148979)
fix carried by [Debian #1042849](https://bugs.debian.org/1042849). It does
not call a user-overridden can or bypass real INC/AUTOLOAD dispatch. INCDIR
and string-overloaded search hooks remain unsupported by this release;
the patch does not add those features. Remove it when upstream ships a
compatible fix that passes the original suite.
