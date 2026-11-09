# Lingua::EN::NameCase 1.21

This compatibility utility heuristically capitalizes personal names. Its
Western-prefix exceptions and Roman-numeral handling are not identity validation
or a universal statement of anyone's preferred capitalization.

## Source and supply

The fixed official CPAN archive is
`https://cpan.metacpan.org/authors/id/N/NH/NHORNE/Lingua-EN-NameCase-1.21.tar.gz`,
SHA-256 `d8ef2b0236aa4c9d0d3d17d13c770792a1b10c81e7a115c1e9e22ffd3a93962f`.
Debian stable `liblingua-en-namecase-perl` 1.21-2 supplies distribution lineage.
The current official and supplemental openEuler indexes and all open PR titles
and paths were checked for the canonical name, aliases and Perl module path.
All declared build/runtime dependencies are supplied by the target indexes.
The CPAN CHECKSUMS index is declared signature-advisory; a signed index is not
a detached signature over the source archive. SHA-256 remains mandatory.

## License scope and patch

The distribution's own code has its explicit Artistic License 2.0 grant.
Changes 1.03 (1999-05-05) explicitly records copying Kim Ryan's NameParse
Mc/Mac solution and comments. The official historical NameParse 0.04 archive
retains the matching implementation and twelve exception substitutions, with
Kim Ryan's 1999 copyright and explicit Perl Artistic License grant:
`https://backpan.perl.org/authors/id/K/KI/KIMRYAN/Lingua-EN-NameParse-0.04.tar.gz`,
SHA-256 `0e36022d8e31679ba1d1396fd8df9a6af5c468d5d4c47f5f5077d198edaedecb`.
Its source is historical corroboration of the named borrowed implementation,
not a claim that the unavailable original 0.03 archive was retrieved.

The package expression is `Artistic-2.0 AND Artistic-1.0-Perl`: borrowed material
is not represented as relicensed to Artistic2. Patch0 adds the exact historical
notice/grant, complete ten-section Perl Artistic1 text from
`https://dev.perl.org/licenses/artistic.html`, and complete Artistic2 text from
`https://perlfoundation.org/artistic-license-20.html`. The original module gets
a dated comment-only notice identifying the historical adaptation; no executable
statement or original test is changed. Source and this additive patch accompany
the public packaging repository and SRPM. License wording is unchanged; HTML
structure, line wrapping and trailing horizontal whitespace are normalized.
This is generic notice restoration, not a RISC-V behavior fix. Remove it when
upstream includes equivalent complete notices and terms.

## Tests and evidence boundary

The recipe runs upstream's entire `make test` unchanged. The original suite has
15 test files and 52 assertions in the observed host run; ten files retain their
upstream AUTHOR_TESTING condition and optional `pod-cm.t` retains its check for
Test::Pod::Spelling::CommonMistakes. No downstream test exclusion or author-mode
override is added. Host tests and the API smoke are preflight, not RISC-V RPM
build/install proof. Exact-head CI and physical RPM/SRPM remain required.

The recipe does not download build dependencies or source at build time and
the manifest declares network_during_build=false; this is not a claim that the
current CI physically isolates networking. Installed smoke exercises scalar,
list and in-place APIs, Mac exceptions, and Roman numerals.
