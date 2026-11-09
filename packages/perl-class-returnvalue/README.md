# Class::ReturnValue 0.55

Pure-Perl context-sensitive success/error objects, lists and stack traces.
The noarch payload targets openEuler 24.03 LTS SP3 riscv64/RVA23. No architecture
patch is needed; host source tests are not target RPM build or install evidence.

## Source and lineage

Fixed official archive:
https://cpan.metacpan.org/authors/id/J/JE/JESSE/Class-ReturnValue-0.55.tar.gz
SHA-256 `ed3836885d78f734ccd7a98550ec422a616df7c31310c1b7b1f6459f5fb0e4bd`
(14,339 bytes). Physical archive, MetaCPAN metadata and PAUSE CHECKSUMS agree.
The historical 2021 SHA-1 index signature is mathematically valid under officially
anchored primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, with an expired signing
subkey. This is advisory index-only evidence, not a detached archive or current
strong signature. Full archive SHA-256 is mandatory. Debian stable
libclass-returnvalue-perl 0.55-4 supplies retained discovery lineage; no external
recipe was executed. Current managed/open-PR aliases and target RPM/module/file
providers were checked for canonical duplication.

## Licensing and notice repair

Jesse Vincent's original 2002, 2003, 2005, 2007 copyright and same-Perl grant in
lib/Class/ReturnValue.pm are preserved and installed. Eight bundled Module::Install
0.67 helper bodies match exact official source after removing only POD, #line
directives and blank lines. Fixed auxiliary archive:
https://backpan.perl.org/authors/id/A/AD/ADAMK/Module-Install-0.67.tar.gz
SHA-256 `6c6f2d159871d4025b2cfb9828658711af1f8bd71414596f451e3f7da8861304`.
The patch adds BUNDLED-HELPER-NOTICES containing the original Brian Ingerson,
Audrey Tang and Adam Kennedy notices/grants, and MODULE-INSTALL-LICENSE with the
original full Perl license texts. Only trailing horizontal whitespace in the
added license copy is normalized; all terms are unchanged. The auxiliary archive
is not bundled. No executable code, original member or default test is changed.
The generic notice repair is not submitted upstream; remove when upstream carries
the complete notices and license. Actual %patch applies it with zero fuzz.

## Dependencies and tests

Retain both upstream runtime prerequisites: Test::More (perl-Test-Simple) and
Devel::StackTrace. Target providers also supply EUMM and all core helper modules.
The recipe uses perl -I. Makefile.PL to select the unchanged bundled loader on
modern Perl. Host %INC evidence binds that loader; upstream removes extension
entries from %INC, so it is not represented as a complete extension load trace.
Makefile.PL does not invoke auto_install; the recipe downloads no dependencies.
network_during_build=false is a manifest requirement, not physical CI isolation.

Original default make test remains in %check: one original test file, 32 assertions,
no skips. All 15 original members are verified unchanged after the notice-only
patch. Host Perl 5.34.1 uses isolated hash-verified Devel::StackTrace 2.04; no global
installation. GNU patch zero-fuzz, host tests/smoke, source-only and repository
gates do not establish target success. Exact-head target build/default-tests,
installed smoke and physical RPM/SRPM acceptance remain required. Smoke covers
version, list context, false error context, fields and actual stack traces.
