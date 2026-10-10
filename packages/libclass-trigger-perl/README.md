<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Trigger 0.15

Frozen Debian `libclass-trigger-perl` 0.15-2 lineage maps to the official
stable CPAN release. The 17,705-byte MIYAGAWA archive SHA-256
`b7a878d44dea67d64df2ca18020d9d868a95596debd16f1a264874209332b07f`
matches the publisher's `CHECKSUMS` file.

The top-level `LICENSE` grants same-as-Perl rights for “This software.”
The installed module and README grant the same rights for “This library.”
Attribution is imprecise: the generated LICENSE labels Tony Bowden's
original idea as copyright, while the module and README identify Tatsuhiko
Miyagawa as the code author and Jesse Vincent as a contributor. None gives
a contrary license notice. The distribution-wide and module grants are
the redistribution basis, not the generated copyright label alone; no
vendored code is present. The RPM expression records the GPL-1-or-later
or Artistic-1 choice.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has
no `perl-Class-Trigger` name or `perl(Class::Trigger)` provider. It supplies
IO::Scalar 2.113, IO::WrapTie 2.113, Test::Pod 1.52 and all other required
build/test providers. The unchanged default suite normally runs ten
functional files/51 assertions and self-skips its author POD test. With
`AUTHOR_TESTING=1`, all eleven original files/52 assertions pass locally
without skips; `%check` requires that same scope on the target. CI must
also prove physical RPM/SRPM products and installed callback smoke. No
local RPM/QEMU build or publication occurred.
