# Math::Expression::Evaluator for openEuler RVA23

The frozen Fedora `perl-Math-Expression-Evaluator` 0.3.2-39.fc44 inventory
key maps to official stable CPAN Math-Expression-Evaluator v0.3.2. Its archive
SHA-256 `21b03869abd963be14c1acd1df824a22ba3a1f8e2a3fd8bd6fe1e6997472886a`
matches the MORITZ publisher `CHECKSUMS`. The official openEuler 24.03 LTS SP3
riscv64 RVA23 primary has no `perl-Math-Expression-Evaluator` or
`perl(Math::Expression::Evaluator)` provider. It supplies Math::Trig,
Data::Dumper, Test::More, Test::Pod and Test::Pod::Coverage for the declared
runtime and test dependency closure.

Upstream module POD grants redistribution under Perl 5 terms, represented
by `GPL-1.0-or-later OR Artistic-1.0-Perl`. `Parser.pm` attributes its
borrowed floating-point regex to Damian Conway and Abigail from
Regexp::Common. The official Regexp::Common source independently grants
Artistic 1/2, BSD and MIT terms; no source, regex, test or fixture was changed.

The unchanged upstream `make test` via its shipped Makefile.PL runs all 19
default t/ files; a clean local run passed 337 assertions with zero skips,
including POD coverage. `%check` preserves that path and requires the POD
dependencies, so those tests must execute on target. Installed smoke checks
RPM/module ownership, version, evaluation, optimization, compiled output and
malformed input. Only exact-head hosted PR CI can establish target RPM/SRPM
and installed-smoke results; it does not establish public repository
publication.
