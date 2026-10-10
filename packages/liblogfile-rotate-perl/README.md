# Logfile::Rotate 1.04

This package imports the frozen Ubuntu `liblogfile-rotate-perl` 1.04-7 lineage
using the author's original CPAN release, not a distribution repack. Source0
is 11,932 bytes with SHA-256
`810f8b7ccd8657d3b1ef53cd47582547845cebb58202b05539b3408638cada3e`.
The official author [CHECKSUMS](https://cpan.metacpan.org/authors/id/P/PA/PAULG/CHECKSUMS)
and [release API](https://fastapi.metacpan.org/v1/release/Logfile-Rotate)
agree on the complete archive size and digest. No detached signature was
verified (`signature: null`); the API's unknown license is not a grant.

## Version and scope

An archive version names the author's published distribution; an embedded
module version is the module's own `$VERSION` used by Perl providers. Here
the official archive/API and RPM are **1.04**, while unchanged `Rotate.pm`
contains `$Revision: 1.5`, calculating module **1.05**. Explicit
`perl(Logfile::Rotate)` Provides and installed smoke use that actual 1.05.
This is disclosed upstream inconsistency, not a version uplift or source fix.

The first target CI built and installed the RPM but failed the strict provider
assertion: target perl-generators 1.10-11 lexically extracts `$Revision` as 1.5,
ignoring the module's zero-padding expression. Release 2 filters only that exact
automatic capability and declares the unchanged runtime version 1.05 explicitly.
All other automatic Requires/Provides, source bytes, and complete tests remain.
The [RPM dependency-generator documentation](https://rpm.org/docs/4.20.x/manual/dependency_generators.html)
defines the generated-string filter used here. This corrects package metadata,
not upstream code; the new exact-head CI must still establish the runtime value
and full installed behavior. The first failed run is not product acceptance.

Actual main764 package paths/RPM/module aliases, all OPEN PR paths, and the
checksum-bound official openEuler RVA23 primary lack this component/provider.
The inventory alone is not a target-absence or rights decision.
Source0 is not repacked; all seventeen original archive files/modes, credits
and the ASCII-codepoint fixture are preserved in the pinned archive/SRPM.
Release 3 applies only the diagnostic test observer described below: all
runtime source and original test statements/loops/assertions remain unchanged.
No version rewriting, feature removal or test-expectation repair is performed.

## Diagnostic-only Persist observation

Release 2's exact-head CI `a979a5e19b40ffd7e1bc94467ab205b0ced26546`,
run 37165275731, passed the first original 9-file/115-assertion `make test`
but failed the second complete strict Harness on t/06persist.t assertions
14, 21 and 28 (mtime). This is an actual full-test failure, not accepted CI.
The original rotation shifts history, copies the active file to `.1`, restores
that copy's metadata and then truncates the active file. The test chooses
historical `.1`, `.2` and `.3` in successive iterations, comparing the same
earliest archived content generation with each active post-truncation file;
the next fixture copy changes active content between those comparisons.
The original Persist POD explicitly promises ownership/permissions and FIFO
history, not equality of every historical mtime with the current active file.
This source-order/oracle discrepancy is static evidence, not a proven cause
of the observed failure or justification for changing runtime/test semantics.

Numbered patch `0001-observe-persist-file-metadata.patch` adds test-only
STDERR diagnostics, not a fix. A labelled active generation means the ordinal
fixture-copy operation within one persist-mode branch, not a proven content
identity or historical timestamp contract. Diagnostics record phase,
persist mode, iteration, active generation and the selected archive path;
before/after the initial/next fixture copy and each rotation they observe
fixture, active file and slots `.1`/`.2`/`.3`, reporting device, inode, size,
mode, UID/GID, atime/mtime or accurate absent/stat-error status. Original
oracle stat arrays are also reported with their observed field differences
without replacing any assertion. Every original test statement, plan,
loop and all 115 assertions remain intact; runtime Rotate.pm and other
original files are unchanged. Original smoke/provider correction is intact.

Observers localise Perl errno/eval/child-status variables and emit no TAP;
they do not write fixtures, change timestamps, sleep, freeze time, skip or
retry tests. Added stat/STDERR activity has execution-time overhead, so this
is an observer run, not an internal syscall trace, zero-perturbation result
or deterministic reenactment; pre/post snapshots cannot capture the internal
utime/truncation instant. A chance passing diagnostic CI does not establish
a repair. Full unchanged default/strict tests must still fail normally when
their conditions fail; current-head metadata is the diagnostic acceptance
target, not package-success acceptance. The modified test prominently dates
and explains the downstream diagnostic change. Observer additions/patch use
GPL-1.0-or-later OR Artistic-1.0-Perl under the original complete Perl terms;
this is not relicensing of upstream source. Remove the observer only
after captured evidence and a separately reviewed solution close the issue.

## Rights and full terms

Original module/README/HTML notices identify Paul Gampe's 1997–99 copyright,
grant redistribution/modification under Perl's terms and retain the full
disclaimer. The code's `GPL-1.0-or-later OR Artistic-1.0-Perl` expression names
the original alternatives; it is not a new grant or legal-certainty claim.
The archive has no complete license-term files, so three byte-exact official
Perl 5.8.7 README/Artistic/Copying documents from immutable official commit
`3eef4faaf8d7fa185749184afd7dc737b8039f42` supplement the original notices.
They document Perl terms, not a claim that this Logfile code descended from
that interpreter release, nor a software build/test dependency. Their schema
`upstream-release` kind means release-origin notice documents. Original
README/HTML, contribution Changes and all three complete supplements are
installed as `%license` and hash-checked; original source grants remain intact.

## Tests, dependencies and identity

The original nine default `t/*.t` suites plan 115 TAP assertions. Their bare
helper processes can print legacy `not ok` without failing exit status;
original MakeMaker `make test` already parses this through Harness and is
retained. A second explicit Test::Harness over all nine files requires exactly
9 files, 115 planned/passed assertions, no skips/TODO/bonus or failed records,
and fails on any missing statistics. Before either run,
fail-closed checks require ordinary UID, target Config gzip, the executable
RPM-owned `/usr/bin/gzip`, Compress::Zlib and Harness. Target Perl RPM
5.38.0-10.oe2403sp3's checksum-verified `Config_heavy.pl` explicitly contains
`gzip='gzip'`; no Config override is used. Target supplies File::Copy 2.41
(required >=2.02), Config, Fcntl, IO::File, Carp, MakeMaker, Zlib 2.206,
Harness, gzip, File::Temp, coreutils and util-linux's `/usr/bin/setpriv`.

Compression tests' original conditional skips remain unchanged, but installed
dependencies/prechecks ensure their premises are present; complete no-skip
115-assertion success must be verified from actual current-head CI, not assumed.
The default compression test uses the library when installed; it does not
prove external gzip merely because Config has gzip.

Upstream warns against external gzip as root. `build.user: unprivileged`
runs default tests on private files as the fixed ordinary build identity.
The fresh installed-smoke image need not contain that username: declared
util-linux `setpriv` drops root to numeric UID/GID 10001 with supplementary
groups cleared and no-new-privileges before Perl creates a mode0700 private
File::Temp directory. No account creation or persistent-host changes occur.
Smoke records and checks real/effective UID/GID and all supplementary groups,
requires the exact numerical identity and cleared groups after root drop,
rejects all root groups, and is bounded by coreutils timeout120s. It checks explicit absolute external
gzip and library compression by decompressed bytes, no compression, retention,
callbacks, relocation, rejected arguments and propagated callback failures,
plus all six installed original notice/term digests. It does not execute the
POD syslog/kill examples. The suite's Signal test is an ordinary callback,
not a daemon signal; private-file flock/Persist are not cross-process/native
locking, permission-security, privileged-system or performance validation.

No local upstream tests, source builds, RPM or QEMU execution is performed.
Only metadata/unit/golden/dashboard and source verification run locally;
target CI must establish exact-head build/install evidence. PR success does
not imply protected-main/native RISC-V validation or published RPM/SRPM URLs.
