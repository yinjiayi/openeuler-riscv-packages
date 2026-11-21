<!-- SPDX-License-Identifier: Apache-2.0 -->
# libterm-size-perl-perl

This directory packages upstream `https://metacpan.org/dist/Term-Size-Perl` version `0.031` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The authorized official CPAN source SHA-256 is
`ae9a6746cb1b305ddc8f8d8ca46878552b9c1123628971e13a275183822f209e`.
It matches the signed publisher checksum at signing time.
Debian stable 0.031-2 establishes naming lineage only.
The full original LICENSE retains both Perl license texts and the author notice.

The original build probes the target terminal ioctl ABI. It generates
`Params.pm`, whose ABI constants stay unchanged; only its volatile
creation-date comment is normalized. The generated parameter manual
retains its upstream MakeMaker filename `Term::Size::Params.3pm`.

The default upstream tests run unchanged. The same original terminal
test is also run against a real pseudo-terminal, where all 17 assertions
can run rather than taking the original non-terminal skips. Installed
smoke verifies both known character and pixel sizes via an unprivileged
pseudo-terminal. These tests do not require physical terminal hardware.
