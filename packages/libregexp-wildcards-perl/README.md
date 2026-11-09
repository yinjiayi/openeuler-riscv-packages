<!-- SPDX-License-Identifier: Apache-2.0 -->
# libregexp-wildcards-perl

`Regexp::Wildcards` converts wildcard patterns into Perl regular expressions.
This noarch package uses the official [CPAN release](https://metacpan.org/dist/Regexp-Wildcards)
1.05 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23, with
[Debian stable](https://packages.debian.org/stable/libregexp-wildcards-perl)
as discovery lineage. `sources.yaml` pins the archive by SHA-256; the digest
matches the PAUSE-signed author-directory `CHECKSUMS`. The original README,
which contains the same-Perl license notice, is installed without changes.
No source patch is needed.

The build runs offline and `%check` runs the unchanged upstream `make test`.
Installed smoke verifies the module version and checks that a converted
wildcard matches the expected filename but rejects the wrong extension.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
