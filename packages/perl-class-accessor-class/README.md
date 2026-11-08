# Class::Accessor::Class 0.504

Pure-Perl shared class-variable accessors; noarch payload targeting openEuler
24.03 LTS SP3 riscv64/RVA23. No architecture workaround is introduced.

## Fixed source and lineage

Official archive:
https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Class-Accessor-Class-0.504.tar.gz
SHA-256 `491bf5e95f82595f72e6c9557b2338d6ae23a12c85de62c082a5805103131dca`
(17,328 bytes). Physical archive, official metadata and PAUSE CHECKSUMS agree.
The current SHA-512 publisher-index signature verifies under official primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`; this is index-only evidence, not a
detached archive signature. Mandatory archive SHA-256 remains in sources.yaml.
Debian stable libclass-accessor-class-perl 0.504-1 supplies retained discovery
lineage; no external recipe executed. Canonical aliases, every open PR's
current/previous files and titles, managed packages and target module/RPM/file
providers were screened before acquisition and again before submission.

## Original license and generated helpers

Ricardo SIGNES's original 2004 same-Perl grant and complete GPL/Artistic LICENSE
remain unchanged. The exact official generator releases were independently
hashed and their outputs compared with original source:

- Dist-Zilla 6.020: SHA-256
  `3a17054f58f873c2dd60e1d2f88e97043e30dfd215cab10e1c0fbfb0fb0a93a6`;
  MakeMaker/Readme/PodSyntaxTests rendered outputs match exactly, with original
  2021 Ricardo SIGNES same-Perl notice preserved.
- Dist-Zilla-Plugin-Test-ReportPrereqs 0.028: SHA-256
  `2aa38c5e8498fa6d930c16d6d32d5b57edf776e33fac6a94ea2be4c242cf1be3`;
  exact test template, original 2012 David Golden Apache-2.0 notice.
- Dist-Zilla-Plugin-CheckChangesHasContent 0.011: SHA-256
  `ab970b50349f87975ac7e3d5f0297f8d67e4f6fe09564778f27f42eca27ea154`;
  exact release-test template, original 2017 David Golden Apache-2.0 notice
  and original author/contributor credits.
- version 0.9909: SHA-256
  `6998f2eea7985e11cbb8e6fd2a404980c3b187c0bd484c88e2af91e80bedf3fe`;
  the ReportPrereqs regex explicitly marked from $version::LAX equals this
  release's expanded grammar, ignoring only qr option wrappers and /x whitespace.
  Original 2004-2010 John Peacock same-Perl grant and regex credits are retained.

The patch only adds GENERATED-HELPER-NOTICES and the complete original Apache
license copy. Trailing horizontal whitespace in the added license copy is
normalized; license terms are unchanged. All 16 original members, executable
code and tests are byte-identical. Auxiliary archives are not bundled. This
generic notice repair is not submitted upstream; remove when upstream includes
complete notices. SPEC applies the real patch with zero fuzz. Metadata includes
Apache-2.0 for these source helpers rather than claiming their output is exempt.

## Dependencies and validation boundary

Original prerequisites are retained: Class::Accessor >=0.16, EUMM >=6.78,
Test::More >=0.96 and core File::Spec/parent/strict/warnings. Target File::Spec
3.88 is explicitly supplied by perl-PathTools and parent 0.241 by perl-parent;
Class::Accessor 0.51, EUMM 7.70 and Test::More 1.302198 satisfy upstream minima.
Perl minimum 5.012
is represented as RPM dotted version 5.12. Recipe and upstream Makefile.PL
download no dependencies; network_during_build=false is a requirement, not a
claim of physical CI network isolation.

Unchanged default make test remains in %check: four original files and 94
assertions, zero skips. The two xt tests remain their original separate
non-default author/release tests. Host Perl 5.34.1 and already-installed
Class::Accessor 0.51 were used without global installs. Notice-patched source,
GNU zero-fuzz application, source-only gates and repository tests do not prove
target RPM build or installation. Installed smoke checks version and data shared
between class/two objects, including zero. Exact-head CI and independent physical
RPM/SRPM acceptance remain required; no native-hardware success is claimed.
