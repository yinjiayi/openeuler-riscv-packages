# Math::Symbolic for openEuler RVA23

The frozen Ubuntu `libmath-symbolic-perl` 0.613-1 inventory key maps to
official stable CPAN Math-Symbolic 0.613. Its archive SHA-256
`d735febf9464fb9e0b1a5a803ba835db7ac71454340e9bc1af6d1fc86e8b4003`
matches the SMUELLER publisher `CHECKSUMS`. The official openEuler 24.03 LTS
SP3 riscv64 RVA23 primary has no `perl-Math-Symbolic` or
`perl(Math::Symbolic)` provider; it provides Parse::RecDescent, Memoize,
Data::Dumper, and Test::More for the declared default dependency closure.

Upstream README and `Math::Symbolic` POD grant redistribution under Perl 5
terms, represented by `GPL-1.0-or-later OR Artistic-1.0-Perl`. The bundled
standalone Parse::Yapp-derived parser is attributed to Francois Desarmenien.
The upstream Parser POD reproduces his GPL-or-Artistic grant and required
notice, and the generated Yapp driver retains its separate notice. No source,
test or fixture was modified.

The unchanged upstream `make test` runs all 23 default t/ files. A clean local
run passed 436 assertions with zero skips. `%check` preserves that command.
Installed smoke checks RPM/module ownership and version, the default parser,
expression evaluation and malformed input, plus the bundled Yapp parser.
Only exact-head hosted PR CI can establish target RPM/SRPM and installed-smoke
results; it does not establish public repository publication.
