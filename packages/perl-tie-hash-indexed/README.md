<!-- SPDX-License-Identifier: Apache-2.0 -->
# Tie::Hash::Indexed 0.08

Insertion-ordered Perl hashes implemented in XS, packaged from the unchanged
[official release](https://cpan.metacpan.org/authors/id/M/MH/MHX/Tie-Hash-Indexed-0.08.tar.gz).
SHA-256: `37bc62815f5a848ac77912b9bf4788a9f272884e83a52e2093dab4a83a4a7b10`
(71,749 bytes). The exact archive entry in the publisher's CHECKSUMS matches.
Its SHA-512 index signature verifies mathematically against the official PAUSE
primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, but the historical signing
subkey is expired. This is advisory historical index evidence, not a current
strong signature or a detached archive signature. Archive SHA-256 is mandatory.

## Source, license and target dependencies

The original README, module, XS, typemap, build script and test headers explicitly
license Marcus Holland-Moritz's work under the same terms as Perl. Bundled
`ppport.h` 3.52 explicitly retains the Perl grant and original notices for Marcus
Holland-Moritz, Paul Marquess and Kenneth Albanowski. README and the unchanged
complete ppport header are installed as license material; no new upstream grant
is invented. Debian's `+ds1` lineage regenerates ppport; this package instead
retains and audits the original official source without importing Debian code.

Discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` retains Debian
stable and Arch lineage. Only upstream release/source and actual license grants
resolve its earlier unknown-source/license classification; distro recipes were
not executed. Normalized module/RPM names and paths were screened against all
open PRs, managed packages and complete official/supplemental provider indexes.

The locked openEuler target supplies GCC, make, Perl 5.38, perl-devel,
ExtUtils::MakeMaker, Test::Harness, Test::Pod, Storable and perl-generators.
Perl supplies the legacy Test module. Test::Pod and Storable are explicit build
dependencies so the original optional POD and serialization checks execute.
The XS library is architecture-dependent and installs to perl_vendorarch.

## Tests and RISC-V status

The original default `make test` target is retained without file exclusions,
feature switches or patches. All seven original test files (293 assertions,
including POD, Storable, Unicode and magic behavior) pass in an isolated macOS
Perl 5.34 source build. The installed smoke checks version, insertion order,
value replacement and deletion. Host/source-only validation is not evidence of
an openEuler/RISC-V RPM build, installation or performance.

No RISC-V-specific change is currently justified. Approved CI must build, run
the complete original tests, produce real RPM/SRPM artifacts and install/smoke
the RPM before acceptance. No local RPM/QEMU build was performed; Auto-merge is
disabled. `patches/series` is intentionally empty. External source licenses
remain upstream's; Apache-2.0 covers only original packaging material.
