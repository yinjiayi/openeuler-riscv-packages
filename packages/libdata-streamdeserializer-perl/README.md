<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdata-streamdeserializer-perl

The frozen inventory's exact `libdata-streamdeserializer-perl` key maps to
official stable CPAN Data::StreamDeserializer 0.06. The 150,827-byte release
tarball's SHA-256 `22f43e0d88d4f612bddff8db87e767f5b6dd16714f18d394f2e2b41d3a8195f4`
matches the publisher's `CHECKSUMS`. The archive has one root and only regular
files and directories, without traversal, links or special files.

The archive's generic `META.yml` license is `unknown`, but both README and
module POD explicitly grant redistribution under the terms of Perl 5.10.1 or
later. The RPM declares `GPL-1.0-or-later OR Artistic-1.0-Perl`. The official
openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Data-StreamDeserializer` nor a
`perl(Data::StreamDeserializer)` provider and supplies the listed build/test
dependencies. This snapshot does not guarantee future repository contents.

The unchanged upstream test suite has seven default files and 69 assertions;
it passed on local macOS Perl 5.34 using an absolute `PERL5LIB`/`prove` path.
One upstream memory-checker assertion is explicitly skipped except on three
named author hosts; the memory-leak assertion itself passed. Plain `make test`
on this Mac failed before tests could run because hardened system Perl rejects
relative dynamic-library paths; no source or test was patched to bypass this.
Installed-module smoke checks version, generated package provider and a parsed
two-element array. Target riscv64 RPM build, original `%check` and installed
smoke remain for CI to verify; PR artifacts alone do not prove public repository
publication or native RISC-V hardware behavior.
