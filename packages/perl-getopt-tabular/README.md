# Getopt::Tabular 0.3

This traditional Perl module describes command-line options in tables with
types, argument counts and destinations. It includes generated help and
extensible type handlers. The package does not execute arbitrary user-supplied
option tables as a sandbox; callbacks and eval handlers are application code.

## Source, identity and license

Official fixed source:
`https://cpan.metacpan.org/authors/id/G/GW/GWARD/Getopt-Tabular-0.3.tar.gz`.
SHA-256: `9bdf067633b5913127820f4e8035edc53d08372faace56ba6bfa00c968a25377`.
Debian stable `libgetopt-tabular-perl` 0.3-4 supplies retained lineage.
The archive and module VERSION identify 0.3; the upstream README heading still
says 0.2. That historical text is preserved, not used to override source identity.

Tabular.pm explicitly grants this package under the same terms as Perl itself
and retains Greg Ward copyright 1995-98. README/POD retain the earlier 1995-97
notice. The demo describes its same-author origin. Tk_ParseArgv is described as
loose inspiration, not a bundled third-party implementation. All eight original
files are preserved byte-for-byte; no source patch is needed.

Official CPAN CHECKSUMS is signature-advisory, not a detached archive signature.
Its 2021 PAUSE-anchored signature mathematically verifies, but uses SHA-1 and an
expired historical signing subkey. This is not current strong-signature proof;
mandatory archive SHA-256 and official HTTPS provenance remain independent.

## Original tests and validation boundary

The SPEC runs the entire original `make test`, whose test.pl emits nine TAP
checks. The historical MakeMaker recipe invokes test.pl directly, so it then
additionally runs that same complete unmodified file through Test::Harness to
make TAP failure fatal. No test is omitted, rewritten, or replaced. Host
preflight observed all nine checks passing, and a synthetic not-ok fixture
confirmed that the added harness exits nonzero on failure.

The installed smoke checks typed values, boolean flags, leftovers and preservation
of the input argument array. Host tests and source-only checks are not target RPM
or installed-smoke acceptance. Exact-head CI must provide those later, with
physical RPM/SRPM and current-main checks before any explicit merge.
The recipe needs no build networking and declares network_during_build=false;
this is not a claim of CI network isolation. Source archives stay outside Git.
