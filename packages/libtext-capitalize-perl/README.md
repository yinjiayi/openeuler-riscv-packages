<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-capitalize-perl

The frozen inventory's exact `libtext-capitalize-perl` key maps to official
[Text-Capitalize 1.5](https://metacpan.org/dist/Text-Capitalize). The CPAN
HTTPS archive and its official `CHECKSUMS` entry both have SHA-256
`e01bf82325415538e02b4acf4a22d08e0afd63864a56c7d9c84b53367f37ab38`.
Every archive entry is under one top-level tree, with no traversal path,
link or special file. The included README and module POD explicitly grant
redistribution and modification under Perl's GPL-or-Artistic terms. This
release-level check resolves the frozen inventory's old `unverified-upstream`
decision; it does not assume that old marker was a license waiver.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-Capitalize` nor a `perl(Text::Capitalize)` provider.
It provides Perl Env 1.04, Module::Build, Data::Dumper, FindBin and
Test::More for the release's declared build/test dependencies. This snapshot
check does not guarantee future repository contents.

`%check` retains all nine default upstream `t` files, including locale and
random-case cases. Local Perl 5.34.1 passed all nine files/608 assertions
without a conditional skip; another locale or Perl runtime may differ, so
exact-head QEMU CI must prove the target outcome. Installed-RPM smoke checks
the module provider and a deterministic title transformation. PR artifacts
alone do not establish public RPM repository publication.
