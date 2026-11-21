<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-abortable

This directory packages upstream `https://metacpan.org/dist/Test-Abortable` version `0.003` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

- Canonical lineage: Debian `libtest-abortable-perl` 0.003-2 and Fedora 44 GA `perl-Test-Abortable` 0.003-9.fc44. The source is the signed PAUSE archive and is verified by SHA-256 before the offline build.
- The notice-only patch adds the original attribution and full Apache-2.0 terms for generated helpers from Dist::Zilla 6.029, Test::ReportPrereqs 0.028 and CheckChangesHasContent 0.011, and credits the same-Perl `version` 0.9909 regex. It does not modify original files, tests or runtime code.
- `make test TEST_VERBOSE=1` runs the full original default harness. It includes its upstream conditional `t/failures.t` skip when the optional `failures` module is absent; no recipe skip is added.
- The install smoke checks that an installed block returns its result and an ordinary exception still propagates.
