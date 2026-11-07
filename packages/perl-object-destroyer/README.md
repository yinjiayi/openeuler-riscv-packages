# Object::Destroyer 2.02

Canonical package `perl-object-destroyer`, RPM `perl-Object-Destroyer`, targets
openEuler 24.03 LTS SP3 / riscv64 RVA23. This is architecture-independent Perl;
host tests are not target RPM/build/install or native RISC-V acceptance.

## Source and lineage

Official fixed source:
`https://cpan.metacpan.org/authors/id/S/SI/SIMBABQUE/Object-Destroyer-2.02.tar.gz`
SHA-256: `dc19d516d56e89873d1f74d2a029be8b143ccd3d408a7c1c2feeda9e09157d8a`.
Both the official MetaCPAN release record and exact publisher CHECKSUMS entry
match. Its 2024-11 SHA-512 checksum-index signature mathematically verifies
under the official PAUSE primary `2E66557AB97C19C791AF8E20328DA867450F89EC`;
the signing subkey has expired. This is advisory index-signature evidence,
not a current detached archive signature; the archive SHA-256 is mandatory.
Discovery lineage is Debian stable trixie `libobject-destroyer-perl` 2.02-2.
Complete canonical/PR title and file aliases plus official/supplemental
Perl namespace providers were screened before acquisition and submission.

## License and generated helper notices

Upstream LICENSE and module POD explicitly grant the original authors' code
under the same terms as Perl. Distinct generated helpers were independently
audited; that grant is not assumed to cover their authors. The package-local
`0001-retain-generated-helper-notices.patch` adds only copyright/license
comments and `LICENSE.generated`, retaining the full Apache-2.0 and Artistic-2.0
texts. It does not change executable statements, assertions, or test selection.
The compound license covers these source-archive components, not a claim that
the installed Object::Destroyer module is relicensed.

Exact official CPAN helper archives and SHA-256 values:

- Dist-Zilla 6.025: `07798e270e5d904d1071e2b421309b732d0be7d682f4d9487945e815012726cc`; Ricardo SIGNES, same-Perl, MakeMaker and PodSyntaxTests.
- Dist-Zilla-Plugin-Test-ReportPrereqs 0.028: `2aa38c5e8498fa6d930c16d6d32d5b57edf776e33fac6a94ea2be4c242cf1be3`; David Golden 2012, Apache-2.0. Expanding its seven documented substitutions reproduces the original default test byte-for-byte.
- Dist-Zilla-Plugin-CheckChangesHasContent 0.011: `ab970b50349f87975ac7e3d5f0297f8d67e4f6fe09564778f27f42eca27ea154`; David Golden 2017, Apache-2.0, non-default release test.
- Dist-Zilla-Plugin-Test-Version 1.09: `7240508731bc1bf6dfad7701ec65450a18ef9245a521ab26ebd6acb39a9ebe17`; Caleb Cushing 2016, Artistic-2.0, non-default author test.
- Dist-Zilla-Plugin-MojibakeTests 0.8: `f1fff547ea24a8f7a483406a72ed6c4058d746d9dae963725502ddba025ab380`; Stanislaw Pusep 2014, same-Perl.
- Dist-Zilla-Plugin-Test-EOL 0.19: `a2b959c7a02ccc32edd43ee58609875613efd53cbcbbd60399e17f15467a4338`; Florian Ragwitz 2010, same-Perl.
- Dist-Zilla-Plugin-Test-MinimumVersion 2.000010: `b8b71f4b64b689f4b647a3a87d6aaaae45a68892d35e36baa976f605736370fb`; Mike Doherty 2010, same-Perl.

Each helper archive was retrieved at its official fixed CPAN URL and matched
the exact official MetaCPAN release SHA-256. Current publisher indexes no
longer list Dist-Zilla 6.025 and MinimumVersion 2.000010; no index-signature
claim is made for those auxiliary license inputs. Original downloaded bytes
are retained in evidence. Added license text only normalizes horizontal
line-end whitespace; the original template authors, grants and full terms
remain intact. No upstream write was made. Remove this generic packaging-only
patch when a stable release supplies equivalent complete notices; it is not
a RISC-V source fix.

## Recipe and tests

Use existing target MakeMaker, Test::More, Carp, PathTools, Scalar::Util and
CPAN::Meta providers. The recipe has no dependency downloader and declares
`network_during_build: false`; this states its network requirement, not proof
that the current CI physically isolates networking. Original `make test`
selects all `t/*.t`: six files and 99 assertions passed unchanged on host
Perl 5.34.1. The non-default `xt/author` and `xt/release` tests remain present
and are not relabeled as default checks. No missing default dependency was
converted to a skip. `%check` runs that original default target.

Installed smoke checks exact version, callback cleanup, dismissal, method
forwarding, explicit cleanup method and invalid constructor rejection. Target
CI must still establish build, original tests, installation and installed
smoke, with physical RPM/SRPM acceptance before any explicit merge. No local
RPM/QEMU/container build, automatic merge or native-RISC-V claim is made.
