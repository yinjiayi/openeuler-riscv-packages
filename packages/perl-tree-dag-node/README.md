# Tree::DAG_Node 1.39

Pure-Perl nodes, tree traversal/manipulation and textual rendering. The noarch
payload targets openEuler 24.03 LTS SP3 riscv64/RVA23; no RISC-V-specific code
change is needed. Target build and installation are not established by host tests.

## Source and lineage

Official fixed source:
https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-DAG_Node-1.39.tgz
SHA-256 `2d3aa0d85a0c2c391d940ff928bc44f48538be50f9bf7415fbc4899e808bb93f`
(69,290 bytes). Physical bytes match current MetaCPAN metadata and PAUSE CHECKSUMS.
The current SHA-512 CHECKSUMS signature verifies under officially anchored primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`; this is publisher-index evidence, not
a detached archive signature. Full archive SHA-256 remains mandatory.
Arch extra perl-tree-dag-node 1.39-1 supplies retained discovery lineage. No
external packaging recipe was executed. Managed packages, all open PR aliases and
target RPM/module/file providers were screened for this canonical upstream.

## License and notice-only patch

The original LICENSE contains GPL-1.0-or-later or Artistic-1.0-Perl, with Sean M.
Burke and David Hand's notices. The module acknowledges adapting its renderer from
Stevan Little's Forest::Tree::Writer::ASCIIWithBranches. The fixed official earlier
Forest 0.09 archive (2010-09-27) is:
https://cpan.metacpan.org/authors/id/S/ST/STEVAN/Forest-0.09.tar.gz
SHA-256 `85fa217adfbf858f162b301f64c173b9d377728cec626ab9146b313ee1353728`.
Its named module explicitly carries Stevan Little's author credit, Copyright
2008-2010 Infinity Interactive, Inc. and redistribution/modification under Perl's
terms. The original renderer matches Forest 0.10; actual traversal, branch-state,
sibling and indentation expressions correspond to the acknowledged adaptation,
introduced in Tree-DAG_Node 1.07 (2012). No claim of whole target-function identity.
The sole patch adds FOREST-NOTICE with those original notices and exact provenance;
all 32 original archive members, including code and default tests, stay unchanged.
LICENSE and FOREST-NOTICE are installed together. The auxiliary Forest archive is
not bundled. This generic notice repair is not submitted upstream; remove it when
upstream retains these notices. The actual RPM patch macro uses zero fuzz.

## Dependencies and validation

Retain all original declared prerequisites, including ExtUtils::MakeMaker >=7.70,
File::Slurper >=0.014 and Getopt::Long >=2.57. The target provides these exact or
sufficient versions, plus Data::Dumper, File::Spec/PathTools, File::Temp and
Test::More. No install-time dependency download is requested by the recipe.
Upstream's Perl decimal minimum 5.020004 means Perl 5.20.4; the SPEC spells it
as RPM's dotted version 5.20.4. RPM compares numeric version segments as integers,
not Perl decimal notation. Target perl is 4:5.38.0-10.oe2403sp3; host comparison
checks the version segments only, with target dependency resolution left to CI.
The manifest sets network_during_build=false; this is a recipe requirement, not
proof of physical CI network isolation. Source fetching is independently hashed.

The unchanged default make test remains in %check: six original test files,
29 assertions, with no added skips. Optional xt/author tests remain upstream's
original separate selection. Host Perl 5.34.1 uses isolated, SHA-verified official
ExtUtils::MakeMaker 7.70, Getopt::Long 2.57 and File::Slurper 0.014 libraries;
none is installed globally or bundled in the RPM. Original and patched host suites,
GNU patch --fuzz=0, source-only validation and installed-smoke logic are local
checks only. Exact-head target CI and physical RPM/SRPM verification remain required.
Smoke covers version, parent/daughter links, adapted rendering and unlinking.
