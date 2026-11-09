<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-tempdir-tiny

This directory packages upstream `https://metacpan.org/dist/Test-TempDir-Tiny` version `0.018` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Source: CPAN's official release, matched to the signed PAUSE SHA-256 and Fedora 44 GA lineage. The Apache-licensed distribution carries a generated Dist::Zilla MakeMaker wrapper and prerequisite diagnostic test; the pinned donor archives provide their original notices, including the embedded version::LAX code grant. Donor code is not executed or installed.

The build runs the three original default tests and both nested fixtures unchanged. Capture::Tiny is explicitly supplied for the default capture path. The installed smoke verifies entering and restoring the caller directory, writing a sentinel to the actual returned directory, and separating named test directories.
