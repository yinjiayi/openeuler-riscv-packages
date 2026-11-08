<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-number-range

This directory packages upstream `https://metacpan.org/dist/Number-Range` version `0.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Provenance and license

The fixed official CPAN archive is `Number-Range-0.12.tar.gz`, SHA-256
`433e821ac44ab6164c7e92b60ff7afa60a279bc550134c82ceb70b3ef4ee2925`.
Its original README and module POD name Larry Shatzer Jr. and explicitly grant
redistribution under the same terms as Perl. The README is retained as the RPM
license document; all original notices remain in the source RPM. The seven-file
source contains no bundled build-helper implementation. The metadata site's
unknown license classification is not used as the license grant.

The source hash is mandatory. CPAN's signed CHECKSUMS entry matches the exact
archive hash and size. Its signature was checked against the official PAUSE
primary-key anchor `2E66557AB97C19C791AF8E20328DA867450F89EC`; the historical
expired-key result is advisory, not a currently valid strong signature or a
detached signature over this archive. The policy is recorded in sources.yaml.

The discovery catalog records Debian stable `libnumber-range-perl` 0.12-2.
This is naming/provenance evidence, not proof of openEuler build success.
The complete open-PR title/current-and-previous-file inventory, managed package
IDs, and official/supplemental RPM names, provides and file namespaces were
screened for aliases before acquisition. Target providers include Perl 5.38,
MakeMaker 7.70, Test::Harness 3.48, Test::More 1.302198, Carp and Exporter.

## Patch and retained tests

Upstream documents scalar multi-value `inrange` as true only when every supplied
value is in range. Version 0.12 returns after the first successful value, so
`inrange(10, 9999)` can incorrectly succeed. The package-local patch moves that
success return after the loop and preserves the original empty-input false
empty string and list-context results. This is a general upstream correctness
fix, not a RISC-V-specific claim. Remove it when an authenticated upstream
release supplies the correction and passes the retained regression.

The official archive is unchanged. Before applying the patch, `%prep` changes
only CRLF line endings in the text module `lib/Number/Range.pm` to LF: the
upstream CRLF form prevents a strict LF patch from matching. A byte comparison
verified this exact line-ending transformation with no other pre-patch changes.
The real `%patch` command uses `_default_patch_fuzz 0`.

The original 40 assertions and their test file are unchanged. A separate
33-assertion regression covers mixed true/false order, small and large ranges,
single values, list results and empty input. With the regression added to the
unmodified source, 6 of its 33 assertions fail; after the patch the complete
default `make test` passes all 73 assertions in two files. `%check` retains that
complete default target without test exclusions. The installed smoke test
checks the public API, including the corrected all-of behavior.

These are source-level host checks, not target RPM build or installation
evidence. RISC-V build/install acceptance remains the responsibility of the
exact-head CI. The manifest disallows build-time downloads and the recipe does
not fetch dependencies; this does not assert physical network isolation.
