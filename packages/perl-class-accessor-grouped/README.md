# Class::Accessor::Grouped 0.10014

Grouped object/class accessors, packaged noarch for openEuler 24.03 LTS SP3
riscv64/RVA23. Default compiler-capable behavior is retained; no PUREPERL_ONLY,
no source-feature workaround, and no default tests removed.

## Source and licenses

Official source: https://cpan.metacpan.org/authors/id/H/HA/HAARG/Class-Accessor-Grouped-0.10014.tar.gz
SHA-256 `35d5b03efc09f67f3a3155c9624126c3e162c8e3ca98ff826db358533a44c4bb`,
28,703 bytes, freshly matched to official release metadata and PAUSE CHECKSUMS.
The historical publisher index signature has an expired signing subkey under
official primary `2E66557AB97C19C791AF8E20328DA867450F89EC`. Its verification is
advisory index evidence, not current-valid or detached archive authentication;
archive SHA-256 remains mandatory. Debian stable source lineage is retained
from the discovery snapshot, without executing a distribution recipe.

Original README/module Matt S. Trout copyright and same-Perl grant remain.
Bundled ExtUtils::HasCompiler0.021 retains its own complete Leon Timmermans2014
copyright and same-Perl grant; the original file is installed as license
documentation. Makefile.PL's parse_args wrapper says "copied from EUMM" but
calls the existing EUMM API rather than embedding the parser implementation.
A notice-only addition retains original EUMM AUTHORS/LICENSE text from official
7.34 (SHA-256 `95f1eb44de480d00b28d031b574ec868f7aeeee199eb5abe5666f6bcbbf68480`).
That fixed source contains the analogous PERL_MM_OPT/ARGV calling pattern and
matches the release's stated EUMM generation version. This is not an assertion
of the earliest copying version or byte-identical copied parser code. No
auxiliary archive is added to the SRPM. All37original members remain unchanged;
the only new upstream-tree file is BUILD-HELPER-LICENSE.

## Dependencies and tests

Keep Module::Runtime/Scalar::Util/Carp and the default compiler-triggered
Class::XSAccessor/Sub::Name requirements. Explicit gcc/perl-devel preserve the
original capability probe. Target BR also retains Devel::Hide and Package::Stash
for original optional tests. Text::ParseWords supports the unchanged argument
wrapper. Perl5.006 is translated to dotted RPM5.6. Recipe logic does not download
dependencies; network=false is not a physical network-isolation claim.

The unchanged default make test selects eleven t/*.t files. On host Perl5.34.1
it passed4730assertions with one natural original pure-Perl-path test skip due
to absent host Devel::Hide in the presence of Sub::Name. The target explicitly
provides Devel::Hide and must establish its actual count. The host's original
compiler capability probe reported missing Perl CORE EXTERN.h and naturally
took its no-compiler path; these host results do not validate the target's
compiler-capable configuration, which remains enabled with gcc/perl-devel.
The original seven
xt author tests remain separate/non-default. GNU patch --fuzz=0 and unchanged
original-source hashes verify the notice-only addition. Smoke covers zero-valued
and updated accessors plus read-only accessors.

Host/source-only/repository tests are not target RPM build/install acceptance.
Exact-head CI must validate default tests, actual installation/smoke and physical
RPM/SRPM. No local RPM/QEMU build, native-hardware or publication success is
claimed; auto-merge remains off.
