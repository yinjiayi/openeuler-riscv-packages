# Data::Validate 0.09

This small traditional Perl module collects numeric and string validation
helpers. Successful results may be zero or an empty string: callers must check
definedness rather than boolean truth. The predicates are not context-specific
shell, SQL or HTML sanitizers and this package does not make that security claim.

## Fixed source and lineage

Official source:
`https://cpan.metacpan.org/authors/id/S/SO/SONNEN/Data-Validate-0.09.tar.gz`.
SHA-256: `ff55c4a993af203482748806d5210189f4f32e1c939fa13d82ad32cbc379c7eb`.
Debian stable `libdata-validate-perl` 0.09-4 is retained catalog lineage.
The separate Data::Validate::IP and Data::Validate::Type distributions are not
aliases for this component; their open PR paths were reviewed independently.
Target indexes are checked for this exact module, RPM and installed path.
Math::BigInt's upstream minimum 1.77 is explicit in the SPEC.

The official CPAN CHECKSUMS index is declared signature-advisory; it is not a
detached signature over the archive. Its 2021 signature mathematically verifies
against the officially anchored PAUSE certificate, but uses SHA-1 and an expired
historical signing subkey: this is not a current strong signature claim.
Mandatory source SHA-256 and official HTTPS provenance are unchanged.

## Original notices

Validate.pm and README explicitly retain Richard Sonnen's 2004 copyright and
grant redistribution/modification under the same terms as Perl itself.
Bundled `t/ExtUtils/TBone.pm` version 1.124 refers to COPYING, which this archive
omits. Its bytes exactly match both lib and t copies of the official release:
`https://cpan.metacpan.org/authors/id/E/ER/ERYQ/ExtUtils-TBone-1.124.tar.gz`,
SHA-256 `adb4d72b09e93cff7f400160957684d27b78b4c7b836aec894887ddb1eebd752`.
That release's original COPYING explicitly preserves Eryq's 1996 and ZeeGee
Software Inc.'s 1999 copyright, Perl terms, and warranty disclaimer.

Patch0 restores that original notice and complete GNU GPL1/Perl Artistic1
texts from `https://www.gnu.org/licenses/old-licenses/gpl-1.0.txt` and
`https://dev.perl.org/licenses/artistic.html`. Only HTML structure/newlines and
horizontal trailing whitespace are normalized, not the license wording. All
21 original files remain byte-identical; no upstream executable statement or
default test is changed. This generic notice fix is not RISC-V-specific and
should be removed once upstream includes equivalent complete notices.

## Tests and limits

The recipe runs the entire original `make test`: observed host preflight
13 files, 106 assertions, zero skips, before and after the additive patch.
The bundled helper writes only the source-tree testout logs. No downstream
filter, test suppression, timing waiver or network-only override is added.
The installed smoke exercises the actual AutoLoader-backed functions, so the
recipe includes both Data/Validate.pm and the auto/Data/Validate files.

Host preflight and source-only verification are not target-build evidence.
Exact-head CI must still build/test the real RISC-V RPM and install it for smoke;
physical RPM/SRPM and current-main checks are required before explicit merge.
The recipe downloads nothing during build and declares network_during_build=false;
this is not an assertion of CI network isolation. Sources and private evidence
are not committed.
