<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-text-xsv

This directory packages upstream `https://metacpan.org/dist/Text-xSV` version `0.21` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The upstream module states it is redistributable under the same terms as Perl.
The original `make test` runs the release's `test.pl`; it is also run unchanged
under `prove` so its TAP failures cause the build to fail. The archived PAUSE
CHECKSUMS records the pinned SHA-256, but its historical signing key is expired;
that signature is not presented as current authentication.
