# Carp::Assert 0.22

Pure-Perl executable assertions for openEuler 24.03 LTS SP3 riscv64/RVA23.

## Source and licensing

Fixed official source: https://cpan.metacpan.org/authors/id/Y/YV/YVES/Carp-Assert-0.22.tar.gz
SHA-256 `807ea97c6bed76ac2e4969efba7dae48fefeb9f28797f112671b3ac8a49355f7`,
11,343 bytes, matched to fresh official release metadata and PAUSE CHECKSUMS.
The current publisher index signature verifies under official primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`; this authenticates the index,
not a detached archive signature. Archive SHA-256 remains mandatory and
signature policy advisory. Discovery lineage is retained without executing
external distribution packaging.

Original Michael G Schwern 2001-2007 copyright and same-Perl terms remain in
lib/Carp/Assert.pm. Supplied t/embedded-Carp-Assert.t regenerates exactly from
its own POD and official Pod-Tests 1.20, except interpreter shebang. A notice-only
addition preserves the original pod2test author/copyright sections and complete
distribution LICENSE (only trailing horizontal whitespace normalized in the
added copy). Fixed helper SHA-256 is
`99b43f83acb2fb9f30e74a52ff5bddedc8d8296a204587d116f438789cc6bc5f`.
Both Schwern and Adam Kennedy notices remain; no generated-output waiver or
earliest-version claim. No helper archive is shipped. All eleven original
source members and three default test files remain byte-identical.

## Recipe and validation

Original Makefile.PL and make test retained; no assertion modes or tests
disabled. Default tests cover enabled, disabled and embedded POD examples.
Host Perl 5.34.1 passed all three files / 44 assertions with zero skips before
and after the notice-only patch. Optional upstream Pod::Tests regeneration and
PERL_TEST_ALL author behavior are unchanged; no generator dependency is forced.
Required core Perl, Carp/Exporter, EUMM and Test::More providers are present.
Perl5.006 is represented as RPM5.6; no recipe build-time dependency downloads.
Manifest network=false is not physical network-isolation evidence.

GNU patch fuzz=0, original-member hashes, actual CI patch policy, source-only
verification and repository gates are retained. Smoke checks equality,
inequality, enabled failure and disabled assertions. Host/source-only evidence
does not prove target RPM build/install; exact-head CI and physical RPM/SRPM
acceptance remain required. No local RPM/QEMU build; auto-merge off.
