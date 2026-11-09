<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-useallmodules

This directory packages upstream `https://metacpan.org/dist/Test-UseAllModules` version `0.17` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive matches the official MetaCPAN release and author
CHECKSUMS. Both the original README and module POD retain Kenichi Ishigaki's
copyright and the same-terms-as-Perl grant. The original project Makefile.PL
uses the installed ExtUtils::MakeMaker and bundles no external templates.

The recipe runs the entire original default `make test`. Two original
fixtures intentionally self-skip with an absent manifest or no modules,
and the upstream POD checks retain their `TEST_POD` opt-in. The installed
smoke test checks that the packaged module can find and load a module
listed in a temporary MANIFEST.
