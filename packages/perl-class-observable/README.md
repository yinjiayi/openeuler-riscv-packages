# Class::Observable 2.004

This pure-Perl module implements observer registration and event notification
for objects and classes. Payload is noarch; target validation remains openEuler
24.03 LTS SP3 riscv64/RVA23. No RISC-V-specific change or patch is introduced.

## Source, provenance and license

Fixed official source:
https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Class-Observable-2.004.tar.gz
SHA-256 `6df32e9fe5f008891fc4efa4e4f45eaa1404d30220459c8fc8a501f0a7cf2e69`
(19,475 bytes), verified against physical bytes, current MetaCPAN metadata and
the exact publisher CHECKSUMS entry. SHA-256 is mandatory. The 2024-11-20 SHA-512
index signature validates mathematically against officially anchored PAUSE
primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, but its signing subkey is
expired: advisory index evidence, not a current strong or detached archive
signature. Fedora Everything-source `perl-Class-Observable` 2.004-8.fc44 supplies
discovery lineage; no external packaging recipe was executed or copied.

Original LICENSE explicitly grants Perl 5 terms for Aristotle Pagaltzis's
software (2021) and Chris Winters's documentation (2002-2004), including the full
GPL-1.0-or-later/Artistic terms. All original notices remain in source and LICENSE
is installed. The two inc/ helpers and Makefile.PL match exact upstream Git tag
v2.004, commit `d02d8a37223e19831bfaa9d04ff1adb7ac641b4e`. Official per-path
history identifies the helpers as Aristotle's project release tooling:
WriteMakefile.pl introduction `80b8a4a43fa8e58347460cb8c7976b0dfad217aa`,
boilerplate.pl lineage back to `ba85752ed76ccf4be9e6d04fe3ee5fa3c2bbb9e1`.
This supports original-code provenance; the actual permission is the fixed
archive LICENSE, not the Git author field or a presumed generator exemption.
No separate borrowed implementation or missing third-party grant was identified.

## Dependencies and original tests

Target supplies Class::ISA 0.36 (minimum 0.32), Scalar::Util via
perl-Scalar-List-Utils 1.63 (minimum 1.14), ExtUtils::MakeMaker 7.70,
Test::More and Perl threads. Complete current managed/all-open-PR identities and
official/supplemental provider names/modules/paths were screened without collision.
The fixed archive already contains META.yml, so WriteMakefile.pl does not add
its release-generation boilerplate target. Software::LicenseUtils and
Pod::Readme::Brief are release-authoring tools, not normal build dependencies.
The recipe performs no dependency downloads; network_during_build=false is the
manifest requirement, not a claim of physical CI network isolation.

The original default `make test` is preserved without selection or skip changes:
seven files and 90 assertions passed on host Perl 5.34.1, including original
thread checks. Their upstream runtime-conditional behavior remains unchanged.
All 19 original archive files remain unchanged after host configure/build/tests.
Host checks use an isolated official Class::ISA 0.36 library, not a global install.
Host tests and source-only verification are not target build/install evidence.
Exact-head CI must build RPM/SRPM, run the same suite and installed-module smoke;
physical artifact verification remains a separate acceptance step. The smoke
checks registration, notification, copying and deletion. No native or performance
claim is made.
