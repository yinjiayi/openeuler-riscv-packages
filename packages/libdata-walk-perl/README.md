# Data::Walk

Data::Walk traverses Perl data structures with callback hooks. This introduces
official upstream 2.01 from frozen Ubuntu `libdata-walk-perl` 2.01-2 lineage.
Pinned target primary SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has neither `perl-Data-Walk` nor `perl(Data::Walk)`; this is missing coverage,
not a target-owned version uplift. Official Scalar::Util 1.63 satisfies >=1.38;
all BuildRequires, including mandatory Harness, are available there.

## Source identity and rights accounting

Original [CPAN Source0](https://cpan.metacpan.org/authors/id/G/GU/GUIDO/Data-Walk-2.01.tar.gz)
is 20,397 bytes, SHA-256
`88461561839fcbfebe1121cebee9bade20e609a12f8c7cb386eac22c8c54334a`,
matching author CHECKSUMS and stable MetaCPAN API. All 26 safe members, including
22 complete regular files, were reviewed independently before upload.

Guido Flohr's original code, build scripts and all eight default tests explicitly
grant GNU Library GPL version 2 or later (`LGPL-2.0-or-later`); the bundled
COPYING.LESSER is verbatim LGPL 2.1, an allowed later version. The module admits
adapted File::Find documentation. Its concrete options/preprocess/postprocess/
wanted-function POD retains the separate Perl `GPL-1.0-or-later OR
Artistic-1.0-Perl` grant, not a purported LGPL relicensing. The RPM aggregate
accounts for both grants.

A dated documentation-only patch adds a prominent scope/copyright/disclaimer
notice inside Walk.pm and PERL-POD-ORIGIN, without changing executable bytes,
tests or Source0. Perl 5.8.7 commit
`3eef4faaf8d7fa185749184afd7dc737b8039f42` provides a contemporaneous
File::Find 1.09 comparison reference, not proof of the exact copied ancestor.
Byte-exact original README, Artistic and Copying are checksum-pinned Source1-3
notice supplements from the official Perl repository. The source schema has no
notice kind; `upstream-release` identifies fixed release-origin notice files,
not another software build or test dependency.

The inherited prose route uses Artistic section 3(a): modifications and their
preferred source are freely available in the package PR/patch and SRPM.
Section 4(b) is addressed by the same machine-readable corresponding sources
accompanying the RPM; no non-standard executable or Perl interpreter is shipped.
Original terms, copyright, no-warranty text and the full mapping are installed
as license materials. This is bounded packaging notice accounting, not a claim
of legal certainty or verified historical ancestry.

Original SIGNATURE remains unchanged in Source0. Its 22 historical SHA1 rows
have one matching file, nine existing-file mismatches and twelve missing old
TC/TS paths; PGP identity is unverified. It is obsolete/unverified, not a
current signature verification success or a failure silently waived.
`signature: null` makes no detached-signature claim. Official HTTPS author
CHECKSUMS/API SHA-256 independently identify the exact archive.

## Tests and evidence boundary

All eight unchanged default tests retain their 266 planned assertions and
self-contained fixtures. Preserve make test plus mandatory full Test::Harness
evaluation. Some upstream expressions are non-asserting/no-ops; default-suite
presence is not complete semantic coverage. No skip, test or feature is removed.
Installed smoke checks callback traversal, depth ordering, cyclic references,
blessing preservation and byte-exact original license materials.

Local work is metadata/unit/Golden/Dashboard and source/patch verify-only,
not an upstream, RPM or QEMU build. Exact-head hosted target CI plus physical
source/RPM/SRPM/schema checks are mandatory. No native or protected-main
publication claim; CI artifacts are not public repository RPM/SRPM links.
