<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhtml-linkextractor-perl

`HTML::LinkExtractor` extracts links and related attributes from HTML in Perl.
This noarch package uses the official
[CPAN release](https://metacpan.org/dist/HTML-LinkExtractor) 0.13 for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The exact SHA-256 is pinned in
`sources.yaml`; [Debian stable](https://packages.debian.org/stable/libhtml-linkextractor-perl)
provides discovery lineage and spells the version `0.130`. The original
module and `LICENSE` retain their CRLF line endings. No patch is needed.

The build runs offline. `%check` runs original `make test` and uses `prove`
to enforce the test's original TAP plan, its declared assertion count.
Installed smoke verifies the module version and extracts a known link target
and visible text from an in-memory HTML fixture without a network request.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
