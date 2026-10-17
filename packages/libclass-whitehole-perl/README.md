# Class::WhiteHole

Class::WhiteHole is a base class that blocks accidental inheritance of AUTOLOAD
methods. This introduces official upstream 0.04 from the frozen inventory's
Ubuntu `libclass-whitehole-perl` 0.04-9 lineage. Official target primary SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a` supplies
neither `perl-Class-WhiteHole` nor `perl(Class::WhiteHole)`; this is missing
target coverage, not a version uplift. All declared BuildRequires, including
`perl-Test-Harness` 2:3.48-1.oe2403sp3, are available in that official repository.

## Source and rights

The [official archive](https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/Class-WhiteHole-0.04.tar.gz)
is 3,279 bytes, SHA-256
`5ff0c93dee6e3497424eea0eda75de4a19532802a796b0358b262ec0372c6aea`.
This matches [author CHECKSUMS](https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/CHECKSUMS)
and [MetaCPAN's stable release](https://metacpan.org/release/MSCHWERN/Class-WhiteHole-0.04).
The original source archive is retained without repack or patches.

All ten safe archive entries, including six complete regular files, were
reviewed. The module explicitly grants redistribution/modification under Perl
terms with Michael G Schwern's 2000 copyright. Its short Perl 5.6 diagnostic
format retains the original attribution. Makefile.PL's Arena Networks template
header carries no competing ownership or license notice; the review does not
claim independent verification of that template's historical author. Changes,
MANIFEST, META.yml and the self-contained test contain no observed competing
notice or external fixture. Independent second review preceded source upload.
The SPEC installs the original module grant as `%license`, without inventing a
replacement license document.

## Tests and evidence boundary

The complete default `t/WhiteHole.t` is unchanged: all six assertions and its
line57 error-message fixture remain. Preserve upstream `make test`, and also
require explicit Test::Harness evaluation of the complete file. Legacy `ok()`
prints failing TAP without exiting nonzero itself; mandatory Harness prevents
such failures from being accepted. No assertion, skip policy or feature is
removed. Installed smoke checks static methods, `can`, inherited AUTOLOAD
rejection and harmless DESTROY, with every failure exiting nonzero.

Local work is source verify-only and repository static/unit/Golden/Dashboard
checking, not an RPM/QEMU or upstream build. Target tests, smoke and physical
RPM/SRPM hashes must come from exact-head CI. No native RISC-V validation or
protected-main publication is claimed, and CI artifacts are not public RPM/SRPM
repository links.
