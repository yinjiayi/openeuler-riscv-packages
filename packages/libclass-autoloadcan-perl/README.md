# Class::AutoloadCAN

Class::AutoloadCAN cooperates between dynamic method dispatch, `can` and Perl
inheritance. This package introduces official upstream 0.03 from the frozen
inventory's Ubuntu `libclass-autoloadcan-perl` 0.03-4 lineage; the distro revision
is not an upstream version.

The official target primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`) contains
neither `perl-Class-AutoloadCAN` nor `perl(Class::AutoloadCAN)`. This is missing
target coverage, not a version uplift. The upstream MakeMaker build requires no
non-core runtime modules; the official target supplies the toolchain packages.

## Source and redistribution evidence

The [official CPAN archive](https://cpan.metacpan.org/authors/id/T/TI/TILLY/Class-AutoloadCAN-0.03.tar.gz)
is 6,276 bytes with SHA-256
`e7eac7beeafbc8b983816e412bd3cf922986d315b0cfc44a4afa1ca0a8441a58`.
This matches the [author CHECKSUMS](https://cpan.metacpan.org/authors/id/T/TI/TILLY/CHECKSUMS)
and the [MetaCPAN stable release](https://metacpan.org/release/TILLY/Class-AutoloadCAN-0.03).
The archive is kept unmodified, without repacking or source patches.

All eleven archive entries (eight regular files and three directories) were
inspected. `lib/Class/AutoloadCAN.pm` explicitly identifies Ben Tilly's 2005
copyright and grants copying, modification and distribution on the same terms
as Perl. `Build.PL` and `META.yml` consistently declare Perl licensing.
`Makefile.PL` is the 248-byte upstream-generated traditional MakeMaker stub,
not a vendored Module::Build implementation. The complete module, `test.pl`,
README, Changes, MANIFEST, Build.PL, Makefile.PL and META.yml contain no observed
competing file-specific restriction, third-party fixture or bundled helper.
The SPEC installs the original module with `%license`, preserving its actual
copyright/grant; no substitute license notice is invented.

## Validation boundary

`%check` retains the complete sole default upstream `test.pl`: twenty assertions
cover load, normal methods, inherited dynamic callbacks, `can`, missing-method
errors, changing import and overridden `can`. There is no optional dependency,
skip or TODO branch. The upstream traditional Makefile.PL is used as intended,
with no source/test change. The legacy `test.pl` failure branch only prints
`not ok`, without making the Perl process exit nonzero. Therefore release 2
preserves the original `make test` and additionally requires `Test::Harness`
evaluation of the unchanged complete test.pl with its built `blib` paths.
Official target `perl-Test-Harness` 2:3.48-1.oe2403sp3 is an explicit BuildRequires.
Installed smoke separately checks inherited dynamic
dispatch, the returned `can` callback and missing-method failure.

Historical [CI 37145223071](https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/37145223071)
at `52e4ec1a2a42da0ee7ae361c1a297ba867dd4b35` printed twenty `ok` assertions
and installed smoke passed, but that run did not enforce TAP failure. Its
products are release 1 and do not validate release 2's mandatory Harness gate.
Fresh exact-current-head target CI and release 2 product-byte audit are required;
historical green is not current-head clearance.

Local checks verify source identity, static metadata and repository tests only;
no local RPM, QEMU or upstream build is performed. Target test/install/product
results must be tied to the exact PR head by CI. A PR build is not protected-main
publication, and this package has no public RPM/SRPM links until publication is
independently verified. Native RISC-V validation is not claimed.
