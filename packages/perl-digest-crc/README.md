# Digest::CRC 0.24

Digest::CRC calculates cyclic redundancy checks through Perl functional and
incremental APIs. CRC detects accidental data corruption and is not a
cryptographic integrity check.

The CPAN release `Digest-CRC-0.24.tar.gz` is fixed by SHA-256
`ba022a05b1adbec73712c46f233d8489fe13a1b9fc40a1fcceed9b52f90defc1`
in both official release metadata and the author's PAUSE CHECKSUMS entry.
Debian stable `libdigest-crc-perl` 0.24-1 supplies discovery lineage, not
archive bytes. No upstream archive is committed. The recipe downloads
nothing during build; this does not assert physical CI network isolation.

The original distribution declares public domain. Ross Williams's named
CRC reference explicitly dedicates its reference C code to the public domain;
this does not cover his prose, which is not bundled. The upstream Changes
identifies h2xs 1.19; the historical Perl 5.005_03 release carries the matching
template fragments and gives the Artistic alternative. An additive notice
patch retains those separately scoped terms and the full Artistic text;
every original member, including `README` (a test input), is unchanged.

`make test` runs all 32 original default checks. The additional upstream
`WITH_CRC64=1` run exercises the same test file with 34 assertions, and an
explicit XS check fails if the module silently falls back to Perl. The
installed-package smoke checks real XS, standard CRC vectors, zero-padded
hex output using string comparison, and incremental input. Host evidence
does not substitute for locked openEuler target build/install or RPM/SRPM.
