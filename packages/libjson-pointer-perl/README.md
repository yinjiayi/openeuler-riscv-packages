<!-- SPDX-License-Identifier: Apache-2.0 -->
# libjson-pointer-perl

This directory packages upstream `https://metacpan.org/dist/JSON-Pointer` version `0.07` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The release archive matches the author-directory PAUSE SHA-256 manifest and Debian stable's original archive byte for byte. The package preserves all 17 files in the upstream default recursive Module::Build suite. Release-author tests retain the upstream opt-in behavior. The install smoke exercises escaped pointer tokens and add/remove without mutating the original document.

The archive retains Toru Yamaguchi's full Perl dual-license grant. The RPM/SRPM additionally preserve the complete rights texts and attribution for the Minilla v1.0.0-generated Build.PL and the adapted Mojolicious v4.0 test; the untouched adapted test remains available in the source archive under Artistic-2.0. See `SOURCE-DONOR-NOTICE` in the built package.
