<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-text-shellwords

This directory packages upstream `https://metacpan.org/dist/Text-Shellwords` version `1.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

- Stable signed CPAN 1.08, corroborated by the exact-source Fedora 44 GA package 1.08-52.fc44. The original same-Perl grant is extracted verbatim from the module; MetaCPAN's machine-readable license is unknown.
- The original notice refers to a warranty disclaimer that is not present in the signed release. The notice is retained verbatim and no missing text is fabricated.
- This is a legacy compatibility namespace; upstream recommends Text::ParseWords for new code. The original MakeMaker test directly executes `test.pl` (six TAP assertions), unchanged.
- The installed smoke tests quotes, escaped spaces and a literal pipe token without executing commands.
