<!-- SPDX-License-Identifier: Apache-2.0 -->
# dos2unix

This directory packages dos2unix `7.5.7`, which the official project page
marks stable, for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The exact
officially linked SourceForge archive is independently SHA-256 pinned and
passed single-root, path, link, and special-entry safety inspection.

The frozen snapshot records Arch `7.5.6-1`, Debian `7.5.2-1`, Fedora 44 GA
`7.5.3-3.fc44`, openSUSE Tumbleweed `7.5.6-1.3`, and Ubuntu GA `7.5.4-1`; it
contains no canonical stable AUR row. No AUR recipe or distribution spec was
read or executed. The complete upstream Perl suite remains a hard gate and
installed smoke verifies the exact bytes of both conversion directions. Exact
run `33137638190` attempt 2 passed the complete upstream build and Perl suite,
then exposed the stale 7.5.6 installed-version assertion; release `2`
synchronizes that assertion without changing the conversion checks.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
