# Tree::Binary 1.09

Binary trees, search trees and traversal visitors, packaged as noarch for
openEuler 24.03 LTS SP3 riscv64/RVA23. No source patch or architecture workaround.

## Source and license

Fixed official source:
https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-Binary-1.09.tgz
SHA-256 `976e5e325b812d87a8210a79ea4d97a1f462a67d002b753f8667edf03fc797fc`
(40,283 bytes), matching the physical archive, official metadata and PAUSE
CHECKSUMS. Current SHA-512 publisher-index signature verified under primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. Index evidence is not a detached
archive signature; full archive SHA-256 is mandatory. AUR perl-tree-binary 1.09-1
provides discovery lineage only; no PKGBUILD or external recipe was executed.
Canonical aliases, managed packages, full current open-PR scope and complete
target RPM/module/file namespace were checked before submission.

Original LICENSE explicitly grants GPL-1.0-or-later or Artistic terms; README
declares the same terms as Perl 5.10.0. Original Infinity Interactive copyright,
Stevan Little authorship, Ron Savage maintenance and Karl Kaestner test notice
are retained. The main module describes reuse from Tree::Simple by its same
original author. No external generated build helper is bundled. All 38 original
members and original notices remain byte-identical. Original LICENSE/README
are installed. The source's old README installation examples do not alter the
independently verified 1.09 archive/module version.

## Dependencies and tests

Retain Scalar::Util/constant and every declared original test prerequisite,
including Test::Exception, Test::More, Test::Pod and Test::Pod::Coverage.
The target also supplies Test::Memory::Cycle 1.06, explicitly required to enable
the unchanged optional leak test. Upstream Perl 5.006000 is mapped to dotted RPM
minimum 5.6. The recipe downloads no dependencies; manifest networking=false
does not claim physical network isolation.

Unchanged default make test remains in %check. Host Perl 5.34.1 ran 14 files and
489 assertions, with the original leak test naturally skipped because that
optional host module was absent. It was not disabled or removed. Four immutable,
officially hash-verified Pod coverage/parser helper sources were used only on
private host PERL5LIB; no global installs or bundled dependencies. Target CI,
with the supplied memory-test dependency, must establish its actual test count.
The two original xt author tests retain their separate non-default selection.

Host smoke checks version, in-order traversal including zero, depth and detach.
Host/source-only/repository gates are not target build or installation evidence.
Exact-head target CI and physical RPM/SRPM acceptance remain separate; no native
RISC-V hardware or publication success is claimed.
