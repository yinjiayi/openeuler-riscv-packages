<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdatetime-format-mysql-perl

This directory packages upstream `https://metacpan.org/dist/DateTime-Format-MySQL` version `0.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The source is the authorized CPAN archive pinned in `sources.yaml` and
matched against the publisher CHECKSUMS and MetaCPAN release metadata.
The original same-Perl `LICENSE` is installed unchanged. Debian stable
`0.08-1` establishes package identity; no Debian recipe is executed or
copied.

The noarch recipe uses upstream Module::Build and retains its complete
default suite (three files, 97 assertions). DateTime and
DateTime::Format::Builder (minimum 0.60) come from the official target
repository; the provider also supplies Builder's Strptime dependency.
The installed smoke test round-trips a leap-day timestamp without needing
a MySQL server. Local staged checks do not replace target CI.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
