# Math::Calc::Units for openEuler RVA23

The frozen Debian and Ubuntu `libmath-calc-units-perl` 1.07-2.1 inventory
keys map to the official SFINK CPAN Math-Calc-Units 1.07 archive. Its SHA-256
`61e3cfdb27bb3bee27beb97124dd930760e1039edc1eb7816c2f5627765f8f8f`
matches the publisher `CHECKSUMS`. Official openEuler 24.03 LTS SP3 riscv64
RVA23 primary lacks `perl-Math-Calc-Units` and `perl(Math::Calc::Units)`;
its core Perl, Time::Local, MakeMaker and Test::Pod providers cover the declared
runtime and test dependencies.

The archive `LICENSE` grants Steve A. Fink's code under GPL version 2 or the
Artistic license, represented as `GPL-2.0-only OR Artistic-1.0-Perl`. The
bundled standalone Parse::Yapp 1.04 driver in `Units/Grammar.pm` preserves
Francois Desarmenien's copyright notice. His original official Parse::Yapp
1.04 module (SHA-256
`1b1158fde9ef8719999aecf1ea7c8ceda3084fbfcdab89e2582527a0862feb03`)
directly grants GPL or Artistic distribution and requires retaining this
notice. No upstream source, test or fixture was changed.

The unchanged upstream `make test` runs both default t/ files: a clean local
run passed 79 assertions with zero skips, including the POD test. `%check`
retains this path and BuildRequires Test::Pod so the test runs on target.
Installed smoke checks RPM/module and CLI ownership, version, unit equality,
conversion and the `ucalc` command. Only exact-head hosted PR CI can establish
target RPM/SRPM and installed-smoke results; it does not establish public
repository publication.
