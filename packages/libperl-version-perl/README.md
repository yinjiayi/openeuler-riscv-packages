<!-- SPDX-License-Identifier: Apache-2.0 -->
# libperl-version-perl

`Perl::Version` parses and compares Perl version strings. This package also
ships `perl-reversion`, the upstream utility for inspecting and updating
version strings in a Perl source tree. It does not replace Perl's `version`
module or its RPM.

The package uses the official [CPAN release](https://metacpan.org/dist/Perl-Version)
1.019 and records [Debian stable](https://packages.debian.org/stable/libperl-version-perl)
as package-discovery lineage. `sources.yaml` pins the archive digest, which
matches the PAUSE-signed author-directory `CHECKSUMS` manifest. The unchanged
upstream `LICENSE` explicitly specifies Artistic-2.0 and is installed as the
license file. No source patch or network access during the build is needed.

`%check` runs upstream `make test` without changing its tests or skip
conditions. Both upstream POD checks are supplied with their optional test
dependencies. The release has no `MANIFEST.SKIP`, so the original manifest
test handles that condition itself. Installed smoke checks verify the module
version, parsing and comparison, and the installed utility's help command.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
