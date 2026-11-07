# Class::Data::Accessor 0.04004

Creates inheritable class accessors with independently overridable subclass and
hash-object values. Target openEuler24.03 LTS SP3 riscv64/RVA23; noarch Perl payload.

This is a legacy compatibility package for existing consumers. Upstream's module
POD explicitly marks the API deprecated and recommends Class::Accessor::Grouped
or Moose instead. It is not recommended here for new applications. Debian stable
still supplies this version; the manifest's active maintenance status describes
this downstream recipe, not active upstream development or a new API endorsement.

## Source and supply

Official archive https://cpan.metacpan.org/authors/id/C/CL/CLACO/Class-Data-Accessor-0.04004.tar.gz
SHA-256 `c122d6e2df6136ce9bea1e6d2b776cb9e69e00085ece995301814c7af3a8e814`
matches MetaCPAN and the exact PAUSE CHECKSUMS entry. Its 2021 signed index has
mathematical VALIDSIG under official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`, but historical SHA-1 and an expired
subkey make it advisory index evidence, not a detached archive signature.
Mandatory full archive SHA-256 verification is retained.
Discovery lineage: Debian stable trixie libclass-data-accessor-perl0.04004-4;
no distro recipe was executed. Current complete PR/canonical/provider namespace
checks found no collision. Target supplies all SPEC dependencies, including
Test::More via perl-Test-Simple and pod2text via perl-podlators.

## Licensing and generic notice patch

The module names Matt S Trout, Christopher H Laco and the acknowledged upstream
contributors and explicitly grants use, redistribution and modification under
Perl's terms. All original notices remain in the module/POD and README.
Eleven bundled ModuleInstall0.77/AutoInstall helper code bodies exactly match
the official fixed auxiliary archive after only POD, line-directive and blank
line removal. Auxiliary SHA-256:
`b115b096e4aeb6639044ce13561686f69bbae08e8bd4f41e70b6605d4c38e5e3`.
Fresh official MetaCPAN historical metadata binds those bytes; current CPAN index
no longer lists0.77, so no auxiliary signed-index verification is claimed.
The notice-only patch preserves the original individual grants/attributions and
complete LICENSE in BUNDLED-HELPER-NOTICES. Only horizontal trailing whitespace
of inserted license text is normalized for git whitespace policy; original
official bytes and normalization comparison are retained as evidence.
No executable code or tests change. This generic packaging patch is not RISC-V
specific or submitted upstream; remove when upstream includes complete notices.
It is declared in series and applied by standard `%patch -P 0 -p1` with zero fuzz.

## Original tests and evidence boundaries

The complete original make test remains in %check:20 functional assertions and
seven unchanged TEST_AUTHOR-gated author test files. No author gate is overridden.
PERL_AUTOINSTALL=--skipdeps only prevents dependency installation/download; it
does not disable tests. The explicit `perl -I.` configure invocation loads the
bundled inc/ helpers rather than relying on dot in @INC or an unrelated installed
Module::Install. A host has such a global helper, so its default configure success
alone is not target evidence; the exact explicit-inc invocation was also tested
with PERL5LIB/PERL5OPT/PERL_USE_UNSAFE_INC removed. Upstream Makefile.PL invokes pod2text to generate
README; the observed host output was byte-identical to the original README.
The build requires no network; manifest network=false is not physical CI isolation
evidence. Original and patched host suites preserve all original source/test
bytes; installed smoke checks inheritance, class/instance override isolation and
invalid instance accessor construction. Source-only/host validation is not target
RPM build/install evidence; exact-head CI and physical RPM/SRPM acceptance remain
required. No native-hardware or performance claim is made.
