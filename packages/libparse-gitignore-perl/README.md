<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-parse-gitignore

This directory packages upstream `https://metacpan.org/dist/Parse-Gitignore` version `1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN release is verified against MetaCPAN, signed PAUSE checksums and Fedora 44 GA lineage. The package ships the original module and separate POD, and copies the POD's original copyright and license grant byte-for-byte as its license file.

The recipe retains both upstream default tests and their original fixtures. The installed smoke uses a controlled ignore file and verifies that a matching cache file is ignored while an ordinary file is not.
