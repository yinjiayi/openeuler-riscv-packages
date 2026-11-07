<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Accessor::Named 0.009

Development aid that gives generated Class::Accessor and Class::Accessor::Fast
accessors distinct profiler names. Target: openEuler 24.03 LTS SP3 riscv64/RVA23.

## Fixed source and license

Official [CPAN archive](https://cpan.metacpan.org/authors/id/J/JE/JESSE/Class-Accessor-Named-0.009.tar.gz)
SHA-256 `44f8b0e66d71276a79f6efa3e5ed4ad1f6cc7d5b9e41cb8747fcb72b04beef01`
matches both MetaCPAN and PAUSE CHECKSUMS. The archive name, module VERSION and
author's Changes say 0.009; META.yml still says 0.008. The 0.009 change is an
installer update. All 20 original historical signed member digests agree.
The embedded 2010 DSA/SHA-1 signature is cryptographically good under the
published key fingerprint `AB4A62CF1A1A119A046239D6122F5DF7108E4046`, whose
UID matches the author but is not trust-certified here. This is advisory only;
the official archive SHA-256 is mandatory. Debian/Ubuntu catalog evidence is
discovery lineage, not an executable recipe.

Best Practical Solutions' original same-Perl notice is retained. The eleven
bundled Module::Install executable bodies match the fixed upstream 0.91
release after removing POD, generated line directives and blank lines.
The notice-only patch adds upstream distribution and per-module authors/grants
plus complete supplied license text, preserving all original archive members
and tests. Added copies normalize trailing horizontal whitespace only; no
license wording or clauses are changed. No donor source is bundled.

## Build and tests

Target package providers supply dependencies before configuration. Upstream
Module::AutoInstall recognizes `PERL_AUTOINSTALL=--skipdeps`; this suppresses
installer dependency fetching, not the original checks. Upstream Makefile.PL
and default `make test` remain unchanged. The two optional original POD tests
retain their skip rules and their dependencies are declared for target CI.
The smoke test verifies actual profiler names, getter and setter semantics
for both accessor generators. Local source checks do not prove target
build, installation or physical RPM/SRPM acceptance.
