# Class::Default 1.51

This pure-Perl base class supports class-level default instances without changing
normal instance method semantics. Target: openEuler 24.03 LTS SP3 riscv64/RVA23;
the RPM payload is architecture-independent. No RISC-V-specific change is needed.

## Provenance and dependencies

The fixed official CPAN archive is
https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Class-Default-1.51.tar.gz,
SHA-256 `adfb4eb7a05fe637b8934601176c15d33e5c4b4ca628f8a19babf6a1c5e3d3ed`.
MetaCPAN release metadata and the exact PAUSE CHECKSUMS entry agree. The index's
2021 signature validates mathematically against the officially anchored PAUSE
primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, but uses historical SHA-1 and
a now-expired signing subkey: advisory index evidence, not a required detached
archive signature or current strong signature. Full archive SHA-256 is mandatory.
Debian stable trixie `libclass-default-perl` 1.51-5 provides discovery lineage;
no external packaging recipe was executed or copied.

Adam Kennedy explicitly grants Perl's terms in the module; LICENSE is retained.
The official target supplies Perl, Carp, PathTools, ExtUtils::MakeMaker,
Test::More via perl-Test-Simple, make and perl-generators. Complete official and
supplemental provider/namespace indexes and all open PR identities were screened.
No target module or file collision was found. Makefile.PL has no auto_install.
The recipe does not download build dependencies. Manifest network_during_build
false describes its requirements; this is not proof of physical CI isolation.

## Bundled helper notice patch

`0001-preserve-helper-notices.patch` restores the original individual copyright
and license notices for eight POD-stripped Module::Install 0.68 helpers. All eight
code bodies match the fixed official Module-Install-0.68.tar.gz after only POD,
line-directive and blank-line removal. Auxiliary archive SHA-256 is
`f6aa0c315cbc9456f642db3de8d2315d658f0a59d46aa0946737fee09d2e293c`.
Its full LICENSE is already byte-identical to this release's LICENSE. Attribution
for Brian Ingerson, Audrey Tang and Adam Kennedy is retained in the added
BUNDLED-HELPER-NOTICES, shipped with LICENSE. No helper or test code changes.
This is a generic packaging notice repair, not a RISC-V port or upstream submission.
It applies to 1.51; remove when upstream includes the complete bundled notices.
SPEC applies it with the standard RPM patch macro and zero fuzz.

## Validation boundary

The entire original `make test` remains in %check: 22 functional assertions and
two original AUTOMATED_TESTING-gated author checks. In a default installation the
author files skip by upstream design; no new skip or environment override is added.
All original source/test members are hash-checked unchanged before/after the
notice-only patch and host tests. Host Perl checks and source-only verification
do not establish target RPM build or installation. CI must build and install
the exact head and run the installed-module smoke, which checks persistence,
instance isolation, subclass isolation and class identity. Native hardware and
performance claims are outside this package's acceptance.
