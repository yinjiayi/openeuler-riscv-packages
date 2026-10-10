# App::Control 1.07

This package proposes the official AWRIGLEY stable release for openEuler
24.03 LTS SP3, riscv64, RVA23, using the repository's immutable locked CI image.
There is no target build, installed-RPM, native-RISC-V or publication success
claim before this exact proposal has actually passed hosted CI and product audit.

## Source and discovery evidence

The authorized/latest/released MetaCPAN API identifies App-Control 1.07 at
`https://cpan.metacpan.org/authors/id/A/AW/AWRIGLEY/App-Control-1.07.tar.gz`.
The original 5,835-byte archive SHA-256 is
`9ece528a449d57241053ee91d103486e189e0ae2323646d29ccd767e77626604`,
equal to both API and publisher CHECKSUMS. All 11 ordinary archive members,
nine regular files, original modes and complete MANIFEST are preserved without
patching or repacking. `sample/test.pl` remains executable; no signature is
provided or claimed cryptographically verified.

The immutable discovery snapshot is
`discovery-20260808T165000Z-9a89920c269462cd`. Its canonical component
`metacpan.org-release-app-control` has genuine Debian stable/main
`libapp-control-perl` 1.07-2, fetched 2026-08-08T16:50:00Z. The separate exact
inventory key `libapp-control-perl` is Ubuntu resolute/universe 1.07-2, not that
Debian row. These are source-discovery lineage, not upstream checksum or grant
proof. Full checksum-bound official target primary metadata has no
`perl-App-Control` or `perl(App::Control)` supplier; it supplies the reviewed
direct prerequisites. Metadata does not prove a successful DNF transaction.

The updater uses the official MetaCPAN JSON version/download_url projection,
with `release_regex: null`; it does not apply a guessed HTML-directory regex.

## Original rights and full notices

The original Control.pm POD and README explicitly grant copyright (c) 2001
Ave Wrigley redistribution and modification under the same terms as Perl.
The generated META license is unknown, not a replacement for that source grant.
The unchanged archive does not bundle full GPL/Artistic text. The original
official Perl v5.38.0 annotated tag resolves to commit
`76298ae68aa7796f0ffc05095b127d23f4b2de8f`; its byte-exact `Copying` and `Artistic`
are pinned separately in sources.yaml and installed with the original README.
They preserve full GPL version 1 and the ten-clause Perl Artistic variant,
including disclaimers, for `GPL-1.0-or-later OR Artistic-1.0-Perl` accounting.
They are release-origin license notices, not an executable dependency, proof of
Perl 5.38 code ancestry, a relicense or a verified tag signature. Source0 and all
original copyright notices remain unchanged. Changes is retained as documentation.
This is bounded notice accounting, not a general legal-certainty claim.

## Complete default tests and process containment

The original `make test` runs `test.pl`, with its original plan of two assertions:
one module-load assertion and one aggregation of constructor, start/status/stop,
restart, HUP, PID-file and ignore-file behavior. The actual helper forks/executes
and sleeps until signalled. There is no skip or TODO branch; the complete original
test and helper remain, not a load-only substitute or invented comparison suite.
The first hosted build demonstrated that legacy MakeMaker runs `test.pl`
directly, not through Test::Harness. Its two actual assertions passed, but its
caught-error path can print `not ok 2` and still return zero. Packaging therefore
captures that same unchanged default run and uses TAP::Parser to require one
two-test plan, both numbered assertions actually successful, and no skip, TODO,
bailout or parse error. It does not execute the suite a second time or manufacture
an upstream test. The parser has a separate finite deadline; its failure is fatal.

Target `%check` requires the fixed ordinary UID 10001 and a fresh private build
directory without old `pids/test.pid` or `ignore.tmp`, inside the disposable CI
container's PID namespace. GNU coreutils `timeout --kill-after=10s 180s` bounds
the complete unchanged `make test` process group, including the original helper;
`--foreground` is not used. A timeout remains failure, never success. Existing CI
container teardown supplies the final namespace boundary; no host process is
signalled by packaging. Original start/stop wait loops have no internal deadline,
and an error can leave a helper alive, so this containment is essential. No upstream
sleep, signal, test plan, loop, expected result or feature is changed.

Ordinary nonprivileged fork/exec/same-UID signals and PID-file handling alone do
not establish privileged-kernel/hardware/native-only validation. A future hosted
QEMU result would remain limited to the observed ordinary process behavior, not
native performance, general daemon reliability, process security or production
service validation. No such runtime test has been executed locally.

## Installed smoke boundary

The installed smoke verifies exact RPM/module version and capability, original
module/README/full-license bytes, then private constructor/file and invalid-input
behavior with two fail-closed positive assertions. It never executes its private
executable fixture and does not start, stop, restart or signal a real child.
Lifecycle coverage belongs to the retained full upstream default suite, not this
constructor-only smoke. No public RPM/SRPM address is inferred from a PR artifact.
