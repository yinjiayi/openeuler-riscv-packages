# Class::Handle 1.07

Objects wrap Perl class introspection, inheritance and loading. The payload is
pure Perl/noarch; the declared target is openEuler 24.03 LTS SP3 riscv64/RVA23.
No RISC-V-specific patch is needed; the upstream API remains unchanged.

## Source and discovery

Fixed official source:
https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Class-Handle-1.07.tar.gz
SHA-256: `000320fcc2c9732f0a53b02d3e7cea460ea69de9dc8fced1a24502be27228035`
(26,657 bytes). Physical bytes, current MetaCPAN metadata and exact PAUSE
CHECKSUMS entry agree. Archive SHA-256 is mandatory. The publisher index's
historical SHA-1 signature is mathematically valid against officially anchored
primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, with an expired signing
subkey: advisory index evidence, not a detached archive or current strong signature.
Ubuntu resolute/universe `libclass-handle-perl` 1.07-5 supplies discovery lineage;
no third-party packaging recipe was executed or copied. Complete current managed,
all-open-PR and target provider names/modules/files were screened without collision.

## Licensing and helper patch

Adam Kennedy's 2002-2006 module notice explicitly grants Perl's terms; the
original full LICENSE is retained. All eight bundled Module::Install 0.68 helper
bodies match the exact official release after removing only POD, #line directives
and blank lines. Auxiliary source:
https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Module-Install-0.68.tar.gz
SHA-256 `f6aa0c315cbc9456f642db3de8d2315d658f0a59d46aa0946737fee09d2e293c`.
Its full LICENSE is byte-identical to the package's LICENSE. The notice-only
patch restores original Brian Ingerson, Audrey Tang and Adam Kennedy copyright
and grants in BUNDLED-HELPER-NOTICES, shipped with LICENSE. No executable helper
or original test changes. This generic packaging repair applies to 1.07 and has
not been submitted upstream; remove when upstream retains the complete notices.
The actual RPM patch macro applies it with zero fuzz; GNU patch was also tested.

## Dependencies and tests

Target providers include Class::ISA 0.36 (minimum 0.31), Class::Inspector 1.36
(minimum 1.12), PathTools, ExtUtils::MakeMaker and Test::More via perl-Test-Simple.
The recipe explicitly uses `perl -I. Makefile.PL` so bundled Module::Install is
loaded on modern Perl; host configure retained `%INC` evidence of those paths.
Makefile.PL has no auto_install invocation. The recipe downloads no dependencies;
manifest network_during_build=false records that requirement, not physical CI
network isolation. Source retrieval is separately SHA-256 verified.

The unmodified default `make test` remains in %check: four original test files,
38 functional assertions and two original AUTOMATED_TESTING-gated author skips
in a normal installation. No new skip or testing override is added. All 19
original archive files are hash-checked unchanged after the notice patch and
host suite. Host Perl 5.34.1 uses isolated official Class::ISA 0.36 and
Class::Inspector 1.36 libraries, never a global installation. Host tests and
source-only verification do not establish target RPM build, install or smoke
success; exact-head CI and physical RPM/SRPM acceptance remain required.
The installed smoke checks version, class introspection, function calls, invalid
names and installed dependency paths. No native hardware/performance claim.
