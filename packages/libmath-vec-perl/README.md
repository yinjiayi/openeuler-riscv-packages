# Math::Vec for openEuler RVA23

This package pins the official CPAN Math-Vec 1.01 archive to SHA-256
`1de393ef44b5dd7d9312b84b81e267ac2911068fa7cd88d2df4d97b197faffaf`,
matching publisher `E/EW/EWILHELM/CHECKSUMS`. Frozen Ubuntu discovery records
`libmath-vec-perl` 1.01-5. The official openEuler 24.03 LTS SP3 riscv64 RVA23
primary metadata has neither `perl-Math-Vec` nor `perl(Math::Vec)`; it does
supply `perl(Module::Build)` and `perl(Test::More)`.

The sole module POD attributes Eric Wilhelm and Wayne M. Syvinski and grants
a choice of GNU GPL or Artistic License, linking the historical Perl Artistic
license. The GPL version is not specified, so the RPM claims only the Artistic
option (`Artistic-1.0-Perl`), and the module is installed as the license
notice. The other bundled build, documentation, and test files have no
contrary notice. No upstream source or test file is modified.

The Module::Build `%check` executes all three unchanged default t/ files.
Clean local execution passed 27 assertions with zero skips. The installed
smoke checks RPM and module providers, version, vector length, dot product,
and cross product. Target QEMU/riscv64 behavior and physical RPM/SRPM bytes
require exact-head hosted PR CI; PR CI does not establish publication.
