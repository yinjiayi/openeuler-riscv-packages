<!-- SPDX-License-Identifier: Apache-2.0 -->
# libset-crontab-perl

`Set::Crontab` expands crontab-style integer lists in Perl. It supports
numeric ranges, steps and exclusions, and exposes membership checks.

This noarch package uses the exact [CPAN release](https://metacpan.org/dist/Set-Crontab)
1.03, with [Debian stable](https://packages.debian.org/stable/libset-crontab-perl)
as discovery lineage. `sources.yaml` records the SHA-256 from official
MetaCPAN metadata and the CPAN author directory. The original same-Perl grant
in `README` is installed as license documentation; the module notice is intact.

The upstream `test.pl` emits TAP (a numbered stream of test results with an
expected count). It runs twelve assertions but declares eleven, and its
direct MakeMaker invocation can exit successfully despite the mismatch.
The package's only patch corrects the declared count. It does not remove or
change any assertion. `%check` runs upstream `make test` and uses `prove` to
fail on a mismatched count or assertion failure. Remove the patch when a
future release has a valid TAP plan for its unchanged test coverage.

The build is offline. Installed smoke checks verify the version, expansion,
and positive and negative membership on the installed module.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
