<!-- SPDX-License-Identifier: Apache-2.0 -->
# libregexp-grammars-perl

This directory packages upstream `https://metacpan.org/dist/Regexp-Grammars` version `1.058` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The module is distributed under the same terms as Perl, and both license
texts and the upstream author notice are retained. The source archive also
contains an unchanged demo dictionary. Its 50,002 rows match the leading
rows of GNU miscfiles 1.4.2 `web2` byte for byte. The recipe retains that
release's GNU and Berkeley notices and GPL-2.0 text; the demo and dictionary
are not installed by the binary RPM. The source license declaration includes
the GNU terms for that separate material; it does not relicense the module.

All original default tests remain enabled. The installed smoke separately
checks a grammar's structured capture and rejection of invalid input.
