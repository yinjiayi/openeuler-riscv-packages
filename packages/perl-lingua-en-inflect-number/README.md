<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-lingua-en-inflect-number

Packages [Lingua::EN::Inflect::Number 1.12](https://metacpan.org/dist/Lingua-EN-Inflect-Number)
for openEuler 24.03 LTS SP3 `riscv64`/RVA23 as a noarch Perl module.
It identifies singular, plural and ambiguous noun forms and provides
`to_S`/`to_PL` conversion alongside exports from `Lingua::EN::Inflect`.

Upstream explicitly warns that the implementation relies on undocumented
behavior of `Lingua::EN::Inflect`, is reliable only for nouns, and may require
rework after dependency changes. This is not a general English grammar engine
or a claim of correctness for arbitrary words and parts of speech.

## Source, license and lineage

The fixed official CPAN archive is
`https://cpan.metacpan.org/authors/id/N/NE/NEILB/Lingua-EN-Inflect-Number-1.12.tar.gz`,
SHA-256 `66fb33838512746f5c597e80264fea66643f7f26570ec2f9205b6135ad67acbf`.
Its digest matches official release metadata and the exact PAUSE checksum-index
entry. The current SHA-512 index signature was verified using signing subkey
`4584D789E682F9F53B392F1837D079412CC9032E` bound to the PAUSE primary fingerprint
`2E66557AB97C19C791AF8E20328DA867450F89EC`, anchored by CPAN's official PAUSE page.
Historical expired certificate subkeys are not the current signer. The index
signature is advisory, not a detached archive signature; SHA-256 is mandatory.

`LICENSE`, `README` and the module POD explicitly grant Simon Cozens's software
under the same terms as Perl 5. Complete GPL-1.0-or-later and Artistic-1.0-Perl
texts remain in the unchanged upstream license file. The standard Dist::Zilla
5.032 MakeMaker output retains its provenance; no bundled installer library or
generated auxiliary test template is present. No source patch is applied.
Debian stable's `liblingua-en-inflect-number-perl` 1.12-3 supplies distribution
lineage; its packaging was not executed or copied.

## Dependencies and validation

The target repositories supply make, Perl, ExtUtils::MakeMaker, Test::More,
perl-generators, Exporter and `perl-Lingua-EN-Inflect` 1.905. The exact module
namespace and RPM/file names were checked against current managed packages,
all open PRs and official/supplemental providers before intake.

The recipe retains `make test`, including the unchanged `t/basic.t`: one file,
21 assertions, with no test deletion, filtering or ignored exit status. Original
tests cover imported functions, singular/plural/ambiguous forms, and conversion
of goat, brewery, beer and sheep. Installed smoke checks version, conversion,
idempotence, ambiguity and an upstream re-export; it does not replace the suite.

Host-language preflight ran the original 21 assertions on macOS Perl 5.34.1 using
a private, fixed official Lingua::EN::Inflect 1.905 source dependency through
`PERL5LIB`, without global installation or source/test changes. That verifies
host behavior only, not an RPM installation, RISC-V execution or target build.
The approved exact-head CI must provide the target RPM/SRPM, original tests and
installation/smoke evidence before acceptance. No local RPM/QEMU build was run.

`network_during_build: false` means this recipe requires no network during its
build/tests; CI may separately retrieve the pinned source and verify its SHA-256.
This metadata does not claim physical network isolation of CI execution.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
