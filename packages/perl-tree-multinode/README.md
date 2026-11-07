# Tree::MultiNode 2.02

Pure-Perl hierarchical trees with nodes and independent navigation handles.
The noarch package targets openEuler 24.03 LTS SP3 riscv64/RVA23. No code patch
or architecture-specific workaround is needed.

## Source and licensing

Fixed official source:
https://cpan.metacpan.org/authors/id/T/TO/TODDR/Tree-MultiNode-2.02.tar.gz
SHA-256 `97686467d87522b80ad516e570e8850faa3cb7da555d8de66690cf918b44d4a7`
(25,344 bytes). Physical archive, current MetaCPAN metadata and PAUSE CHECKSUMS
agree. The current SHA-512 publisher-index signature verifies under official
primary `2E66557AB97C19C791AF8E20328DA867450F89EC`. Index evidence is not a detached
archive signature; mandatory archive SHA-256 is retained in sources.yaml.
Debian stable libtree-multinode-perl 1.0.14-0.2 supplies discovery lineage;
2.02 is independently verified from upstream, not inferred from that older
distribution version. No external recipe executed. Complete current managed,
all-open-PR aliases and target RPM/module/file providers were screened.

Original LICENSE explicitly grants GPL-1.0-or-later or the Artistic license
that accompanies Perl. Original module/README author credits for Kyle R. Burton,
Daniel X. Pape, Eric Joanis and Todd Rinaldo are preserved. The three project
modules and hand-written EUMM configuration contain no bundled external build
helper. All 33 original source members remain byte-identical; no patch is added.
Original LICENSE and README are shipped; no invented copyright attribution.

## Dependencies and tests

Scalar::Util is supplied by target perl-Scalar-List-Utils 1.63; EUMM 7.70 and
Test::More 1.302198 are provided. Upstream Perl decimal minimum 5.008 is represented
as dotted RPM version 5.8. The recipe does not download dependencies.
network_during_build=false is a manifest requirement, not proof of physical
CI network isolation. Source acquisition is separately checksum-verified.

The unchanged default make test is retained in %check: 17 original test files,
183 assertions and zero skips. The two xt author tests retain their upstream
separate, non-default selection. Host Perl 5.34.1 ran the complete default suite
without globally installing dependencies or changing source/tests. Installed-smoke
logic checks version, child values including zero, removal, remaining keys and
false node keys. Source-only checks and host tests do not establish target build,
installation or physical product success. Exact-head target CI and independent
RPM/SRPM acceptance remain required; there is no native-hardware claim.
