<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxml-filter-buffertext-perl

This noarch package provides [XML::Filter::BufferText](https://metacpan.org/dist/XML-Filter-BufferText)
1.01 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The authorized CPAN
archive is pinned in `sources.yaml`; [Debian stable](https://packages.debian.org/stable/libxml-filter-buffertext-perl)
establishes naming lineage. The original BufferText.pm includes Robin Berjon's
same-Perl grant and is installed unchanged as license evidence.

The package runs the original default `make test` unchanged. Installed smoke
checks that two adjacent SAX character chunks are coalesced into one event.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
